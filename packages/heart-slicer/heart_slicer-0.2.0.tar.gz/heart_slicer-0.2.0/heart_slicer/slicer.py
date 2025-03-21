"""
Functions related to cutting a slice into multiple segments.
"""

from __future__ import annotations
import math
import os
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# import .common as common
from . import common
from .common import logger, settings


@common.logging_decorator
def _cut_polygon_from_image(im: Image, polygon: list, trim: bool = None) -> Image:
    """
    Cut a polygon out of an image and return the result.

    im          Image
    polygon     polygon to cut
    trim        trim the image?
                Default uses settings['trim_image']
                if trimmed the border is set to settings['border']

    polygon can by any polygon as defined in ImageDraw.
    works only for RGB images.
    """
    # create a mask (255=show, 0=hide)
    mask = Image.new("1", (im.width, im.height), color=0)
    # ceate draw objkect on mask
    draw = ImageDraw.Draw(mask)
    draw.polygon(polygon, fill=1)

    # apply the mask
    # copy existing image
    cut_image = Image.new("RGB", im.size, color=(255, 255, 255))
    cut_image.paste(im, box=None, mask=mask)

    if trim is None:
        trim = settings["trim_image"]
    if trim:
        bounding_box = _find_bounding_box(cut_image)
        # crop to size and add border
        cut_image = crop_image(
            im=cut_image, bbox=bounding_box, border=settings["border"]
        )

    return cut_image


@common.logging_decorator
def _boundingbox(im: Image, background: set) -> list:
    """
    Newest method to find the bounding box of the image
    using the build in bbox function of the Image module

    environment variable (not preferred)
        im: Image
            the image to find the bounding box of
        background: rgb()
            the background color
            defoult is white (255, 255, 255)
    returns bounding box set:
        "Bounding box coordinates [x_min, y_min, x_max, y_max]
    """
    im_array = np.array(im)
    im_array[np.all(im_array == background, axis=2), :] = 0
    bbox = Image.fromarray(im_array).getbbox()
    if bbox is None:
        # no bbox found with empty image
        bbox = [0, 0, 1, 1]
    return list(bbox)


@common.logging_decorator
def _find_bounding_box(im, background=(255, 255, 255), method: callable = _boundingbox):
    """
    Trim white off image and then add a white border of given bordersize.
        im: Image
            the image to find the bounding box of
        background: rgb()
            the background color
            defoult is white (255, 255, 255)
        bbox_method: callable
            the function to use when processing the image
            options currently are:
            - boundingbox_newest (default)
            - boundingbox_new
            - boundingbox_old
    """

    [x_min, y_min, x_max, y_max] = method(im, background=background)
    return [x_min, y_min, x_max, y_max]


@common.logging_decorator
def crop_image(im, bbox, border=0):
    """Crop the image to the given bounding box and optionally add a white border.
    parameters:
        im      Image to crop
        bbox    coordinates of the bounding box defined by two points
                [x0, y0, x1, y1]
        border  additional blank space around the selected crop area in [px]
                default = 0
    returns:
        canvas  a convas with the cropped image.
    """

    width = bbox[2] - bbox[0] + 2 * border
    height = bbox[3] - bbox[1] + 2 * border
    # cretae new image canvas
    canvas = Image.new("RGB", (width, height), (255, 255, 255))
    # crop from original image
    canvas.paste(im.crop(bbox), box=(border, border))
    # canvas.show()
    return canvas


def _get_image_center(im: Image) -> list:
    """
    Get the coordinates in pixels of the center of the image.
    returns:
        (px_x, px_y) of center
    """
    # assume the center of the image is the center of the heart
    return (round(im.width / 2), round(im.height / 2))


def _get_corner_angles(im: Image, offset: float = -math.pi / 2):
    """
    create a list of the angles from the CENTER of the image to
    four corners.
    parameters:
        im      Image to process
        offset  offset in rad of the first cut.
                used to have the angles in the right order.
    returns:
        sorted list with the anggles to the corners
    """

    corners = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    corner_angles = []
    for a, o in corners:
        angle = math.atan((o * im.height / 2) / (a * im.width / 2))
        if o < 0:
            # in pi-2pi range
            angle += math.pi
        if angle < offset:
            angle += 2 * math.pi
        corner_angles.append(angle)
    corner_angles = sorted(corner_angles)
    return corner_angles


@common.logging_decorator
def _create_slice_polygon(
    p_center: tuple,
    p0: tuple,
    angle: float,
    radius: int,
    im_size: tuple,
    corner_angles: list,
) -> list:
    """
    Returns a polygon of the desired slice based on the
    provided points, angle and image size
    parameters:
        p_center        (x, y) of starting point
        p0              (x, y) of zero'th point
        angle_p1        angle of point 1 in [rad]
        radius          maximum radius of image (center -> corner)
        im_size         (width, height)
        corner_angles   angles of the corner in [rad]
    returns:
        polygon:    [xc, yc, x0, y0, xe, ye, x1, y1]
                    where xe, ye is an additional point required
                    when passing a corner of the image
    """
    # calculate x and y around origin
    xt = math.cos(angle) * radius
    yt = math.sin(angle) * radius
    # see where it's outside the bounding box (edge of picture)
    # this is always the case because radius is the maximum radius

    if abs(xt) >= im_size[0] / 2:
        # crosses left or right side, scale y value
        yt = yt * (im_size[0] / 2) / abs(xt)
        # set x value to maximum
        xt = common.sign(xt) * im_size[0] / 2
    elif abs(yt) >= im_size[1] / 2:
        # crosses top or bottom,  scale x value
        xt = xt * (im_size[1] / 2) / abs(yt)
        # set y value to maximum
        yt = common.sign(yt) * im_size[1] / 2
    else:
        raise NotImplementedError("something went wrong here :(")
    # set relative to center
    x1 = p_center[0] + xt
    y1 = p_center[1] + yt

    # check if the angle passes a corner
    if len(corner_angles) > 0 and angle > corner_angles[0]:
        # add extra point in corner
        corner_angle = corner_angles.pop(0)  # pop first value
        xe = p_center[0] + math.cos(corner_angle) * radius
        ye = p_center[1] + math.sin(corner_angle) * radius
    else:
        # map point onto existing point
        xe, ye = [x1, y1]

    polygon = [p_center[0], p_center[1], p0[0], p0[1], xe, ye, x1, y1]
    return polygon


@common.logging_decorator
def create_folders_heart_slice(
    directory: str, heart: str, slice_nr: str, segmentation_type: str
) -> dict:
    """Creates a folder structure for heart slices within a given directory.

    This function checks if the specified directory exists. If it does not,
    it logs an error message and raises a ValueError. It then creates a folder
    for the heart within the directory, followed by a folder for the slice
    within the heart folder, and finally a folder for the segmentation type
    within the slice folder.

    Parameters:
        directory (str): The path to the base directory where the heart folder
                         should be created.
        heart (str): The name of the heart folder to be created.
        slice_nr (str): The name of the slice folder to be created within the
                        heart folder.
        segmentation_type (str): The name of the segmentation type folder to be
                                 created within the slice folder.

    Returns:
        dict: A dictionary containing the paths to the created folders with
              keys 'heart_folder', 'slice_folder', and 'segment_folder'.

    Raises:
        ValueError: If the specified directory does not exist."""

    # check that the provided directory exists
    if os.path.isdir(directory) is False:
        msg = (
            f"directory doesn't exist: {directory}\n"
            + "\t\tPleuase create this directory prior to running the script."
        )
        logger.error(msg)
        raise ValueError(msg)
    # create folder for heart, if it already exists raise error
    heart_folder = os.path.join(directory, heart)
    common.create_folder(heart_folder)
    # create folder for slice
    slice_folder = os.path.join(heart_folder, slice_nr)
    common.create_folder(slice_folder)
    # create folder segmentation_type
    segment_folder = os.path.join(slice_folder, segmentation_type)
    common.create_folder(segment_folder)
    return {
        "heart_folder": heart_folder,
        "slice_folder": slice_folder,
        "segment_folder": segment_folder,
    }


@common.logging_decorator
def images_for_segmentation_type(im: Image, segmentation_type: str, section: str):
    """
    Create segments from the image based on the provided segmentation type.
    Supported segmentation types:
        CAG, AHA, MINI

    Parameters:
        image               image to segment
        segmentation_type   name of the used segmentation
        section             name of the section the heart is from
        ## offset              angle of the starting cut (North direction)

    Yields:
        segment_image, segment_name
        each segment image for the provided segmentation_type.

    Assumes:
        center image is center of heart
    """
    segment_names, offset = segment_names_by_segmentation_type(
        segmentation_type=segmentation_type, section=section
    )

    # get relevant angles and points
    corner_angles = _get_corner_angles(im=im, offset=offset)
    nsegments = len(segment_names)
    point_center = _get_image_center(im=im)
    # maximal radius = center to corner
    radius = math.sqrt((im.width / 2) ** 2 + (im.height / 2) ** 2)

    # starting coordinates of the first cut
    # p0 = (x0, y0) = [im.width / 2 , 0]
    # set start point coordinates of first 'cut'
    p0 = (
        point_center[0] + math.cos(offset) * im.width / 2,
        point_center[1] + math.sin(offset) * im.height / 2,
    )

    # loop through segments
    for cur_segmentnr in range(1, nsegments + 1):
        logger.info(f"..creating segment: {segment_names[cur_segmentnr - 1]}")

        # get current angle (- to rotate clockwise)
        rad = offset + cur_segmentnr * 2 * math.pi / nsegments

        polygon_segment = _create_slice_polygon(
            p_center=point_center,
            p0=p0,
            angle=rad,
            radius=radius,
            im_size=(im.width, im.height),
            corner_angles=corner_angles,
        )

        # create segment
        im_segment = _cut_polygon_from_image(im, polygon_segment)

        # take last point as next point
        p0 = (polygon_segment[6], polygon_segment[7])  # p1
        # TODO: check
        logger.info(f"...created segment: {segment_names[cur_segmentnr - 1]}")

        yield im_segment, segment_names[cur_segmentnr - 1]


@common.logging_decorator
def segment_names_by_segmentation_type(segmentation_type, section):
    """
    Create segmented images of the given image_file according to segmentation type that is provided.
        Supported segmentation_types:
            CAG - Claire's segmentation
            AHA - American Heart Association
            MINI - Small sections that can be combined into either CAG or AHA segmentations
        Parameters:
            segmentation_type
                the segmentation_type to lookup
            section
                relevant section in within segmentation_type
        returns: dict
            segmentation_names
                names of the segments given the segmentation_type and section.
            offset
                offset for 0-line in radians .
    """

    match segmentation_type:
        case "TEST":
            # for testing
            logger.info("Requested test segmentation")
            segment_names = ["T", "E", "S", "T"]
            offset = -math.pi / 2
        case "MINI":
            # determine naming based on section and
            match section:
                case "B":
                    segment_names = [str(x) for x in range(12, 0, -1)]
                case "M":
                    segment_names = [str(x) for x in range(24, 12, -1)]
                case "A":
                    segment_names = [str(x) for x in range(32, 24, -1)]
                case _:
                    raise NotImplementedError(
                        f"unsupported section name '{section}' for segmentation MINI"
                        + ", should be 'B', 'M' or 'A'."
                    )
            offset = -math.pi / 2

        case "CAG":
            # determine naming based on section and
            match section:
                case "B":
                    segment_names = ["F", "E", "D", "C", "B", "A"]
                case "M":
                    segment_names = ["L", "K", "J", "I", "H", "G"]
                case "A":
                    segment_names = ["P", "O", "N", "M"]
                case _:
                    raise NotImplementedError(
                        f"unsupported section name '{section}' for segmentation CAG"
                        + ", should be 'B', 'M' or 'A'."
                    )
            offset = -math.pi / 2

        case "AHA":
            # determine naming based on section and
            match section:
                case "B":
                    segment_names = [str(x) for x in range(6, 0, -1)]
                    offset = -math.pi / 3
                case "M":
                    segment_names = [str(x) for x in range(12, 6, -1)]
                    offset = -math.pi / 3
                case "A":
                    segment_names = [str(x) for x in range(16, 12, -1)]
                    offset = -math.pi / 4
                case _:
                    raise NotImplementedError(
                        f"Unsupported section '{section}' for segmentation AHA"
                        + ", should be 'B', 'M' or 'A'."
                    )

        case _:
            raise NotImplementedError(
                f"Segmentation not supported: {segmentation_type}."
            )

    return segment_names, offset


def move_image_file(file, directory_from: str, directory_to: str) -> bool:
    """
    Move a file from one directory to another one
    """
    # TODO: directory from is redundant, path is in file
    # move image file to slice folder
    os.rename(
        os.path.join(directory_from, file),  # from
        os.path.join(directory_to, os.path.split(file)[1]),
    )  # to
    logger.info(
        f"Moved image file: {file}\n"
        + f"from folder: {os.path.relpath(directory_from, directory_to)}\n"
        + "  to folder: "
        + f"{os.path.relpath(directory_to, directory_from)}"
    )
    return True


def plot_image(im: Image, title: str):
    """
    Plot a PIL image using Matplotlib.

    Parameters:
        im (Image): The image to be plotted.
        title (str): The title of the plot.

    Returns:
        None
    """
    """Plot a PIL.image."""
    # Plot the image using Matplotlib
    plt.title(title)
    plt.imshow(im)
    plt.show()


@common.logging_decorator
def process_heart_images_in_directory(
    directory_in=None,
    directory_out=None,
    move_file=True,
    overwrite_existing=True,
    segmentation_types=None,
):
    """
    Proces heart slice images in folder with multiple segmentation types.
    Assumes filename is structured according to common.params_from_filename.
    Parameters
        directory_in
            directory of images to process
            if no directory is provided the directory of the file is used
        directory_out
            directory to store the processed files
        move_file
            True (default) move the image file to the folder that is created for that image.
            False: don't move image
        overwrite_existing
            True (default): overwrite an existing file
            False: skip file if it exists
        segmentation_types
            segmentation types to use.
            default= ['MINI', 'CAG', 'AHA']
    returns
    """

    # segmentation types to use
    if segmentation_types is None:
        segmentation_types = ["MINI", "CAG", "AHA"]

    # use directory of file if no directory is provided
    if directory_in is None:
        directory_in = os.path.dirname(__file__)
        logger.info(
            "No directory providid using directory of current file:\n"
            + f"{directory_in}"
        )
    common.logger.info(f"Processing directory:\n\t{directory_in}")

    # track process
    output = {}
    counters = {}
    # get list of images in folder
    images_to_proces = common.pngs_in_fld(directory_in)
    # add counters
    counters["images_total"] = len(images_to_proces)
    counters["segmentations"] = counters["images_total"] * len(segmentation_types)
    counters["image"] = 0
    counters["segmentation"] = 0

    for image_filename in images_to_proces:
        file = os.path.join(directory_in, image_filename)
        # get parameters from image file name.

        counters["segments"] = 0
        counters["errors"] = 0
        # open image
        with Image.open(file) as im:
            # im = common.load_image(file)
            # loop through segmentation types
            for segmentation_type in segmentation_types:
                # create folder
                heart_params = common.params_from_filename(file=file, type="slice")
                folders = create_folders_heart_slice(
                    directory=directory_out,
                    heart=heart_params["heart"],
                    slice_nr=heart_params["slice_nr"],
                    segmentation_type=segmentation_type,
                )
                # generate images
                segmentation_images = images_for_segmentation_type(
                    segmentation_type=segmentation_type,
                    im=im,
                    section=heart_params["section"],
                )  # returns generator

                # loop segments for segmentation_type
                for segment_im, segment_name in segmentation_images:
                    if settings["plot_image_cuts"] is True:
                        plot_image(
                            im=segment_im,
                            title=f"{heart_params['heart']} - {heart_params['slice_nr']} - "
                            + f"{segmentation_type} - {segment_name}",
                        )

                    segment_folder = os.path.join(
                        folders["slice_folder"], segmentation_type
                    )
                    # save the segment image if required
                    if settings["save_segment_image"]:
                        common.save_image(
                            im=segment_im,
                            save_folder=segment_folder,
                            filename=common.generate_filename_segment(
                                file_params=heart_params,
                                segmentation_type=segmentation_type,
                                segment_name=segment_name,
                            ),
                            overwrite_existing=overwrite_existing,
                        )
                    counters["segments"] += 1

        moved = False
        if move_file is True:  # and (counters['segments'] == len(segmentation_types)):
            # only move hen all segmentations are processed correctly
            moved = move_image_file(
                file=file,
                directory_from=directory_in,
                directory_to=folders["slice_folder"],
            )
        # errors currently not implemented
        # logger.info(f"{file} - correct:{counters['segments']}, errors:{counters['errors']}")
        output[file] = {
            "segments": counters["segments"],
            "errors": counters["errors"],
            "moved": moved,
        }

    return output
