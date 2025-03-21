"""
Functions to analyze the slice or segment.
"""

from __future__ import annotations
import math
import os
from PIL import Image
from .common import (
    image_height,
    image_width,
    logger,
    logging_decorator,
    colors,
    settings,
    params_from_filename,
)
# import .common as common

PIXAREA = settings["pixarea"]
PIXLENGTH = settings["pixlength"]
DELIMITER = settings["delimiter"]


def image_get_pixel(im, x, y):
    """
    Return the pixel at coordinates x,y in the image.
    """
    return im.getpixel((x, y))


def pixel_red(pixel):
    """
    Return red value of pixel.
    """
    return pixel[0]


# not used
def pixel_green(pixel):
    """
    Return green value of pixel
    """
    return pixel[1]


# not usd
def pixel_blue(pixel):
    """
    Return blue value of pixel
    """
    return pixel[2]


def redchecker(pi):
    """
    Return if the given pixel is red (REDRED)
    """
    return pixel_red(pi) == colors["redred"]


def yellowchecker(pi):
    """
    Return if the given pixel is yellow (YELLOWRED)
    """
    return pixel_red(pi) == colors["yellowred"]


# not used
def whitechecker(pi):
    """
    Return if the pixel is white (WHITERED)
    """
    return pixel_red(pi) == colors["whitered"]


# not used
def blackchecker(pi):
    """
    Return if the pixel is black (BLACKRED)
    """
    return pixel_red(pi) == colors["blackred"]


@logging_decorator
def count_pixels_and_edges(im: Image):
    """count pixels and red borders in the image."""

    red_counter = 0
    yellow_counter = 0
    border_counter = 0

    ####### counting pixels & borders #########
    for y in range(1, image_height(im) - 1):
        for x in range(1, image_width(im) - 1):
            pix = image_get_pixel(im, x, y)
            if redchecker(pix) is True:
                red_counter += 1

                # For red pixels count the border
                pixa = image_get_pixel(im, x, y - 1)
                pixb = image_get_pixel(im, x + 1, y)
                pixc = image_get_pixel(im, x, y + 1)
                pixd = image_get_pixel(im, x - 1, y)
                if redchecker(pix) is True:
                    if redchecker(pixa) is False:
                        border_counter = border_counter + 1
                    if redchecker(pixb) is False:
                        border_counter = border_counter + 1
                    if redchecker(pixc) is False:
                        border_counter = border_counter + 1
                    if redchecker(pixd) is False:
                        border_counter = border_counter + 1

            elif yellowchecker(pix) is True:
                yellow_counter += 1

    return red_counter, yellow_counter, border_counter


@logging_decorator
def edge_count_min_value(pixels: int):
    """
    calculate the minimum possible value of outside edges given a number of pixels.
    This assumes the pixels are positioned as compact as possible, i.e. a filled square.
    """

    n = int(math.sqrt(pixels))  # return only the integer part aka round down
    edges_square = 4 * n

    rest = pixels - n**2
    edges_rest = 0
    if rest > 0:
        if rest <= n:
            edges_rest = 2
        elif rest <= 2 * n + 1:
            edges_rest = 4

    return edges_square + edges_rest


@logging_decorator
def analyse_image(filepath, outputfilepath, variables=None, open_mode="a+"):
    """
    Analyze the pixel color of an imagefile and write to an output file.
    you can define the variables you want to save in 'variables'.

    Parameters:
        filepath        name of the file containing the image
        outputfilepath  path of the file to write the output to
        variables       variables to write to file
        open_mode       mode to open the file with, default "a+"
                        note: when appending to the output file
                        the header will be added when it is missing
                        or when the existing header differs from
                        the current one.
    returns:
        None
    """
    if variables is None:
        # define variables to write to file if not provided
        variables = [
            "heart",
            "slice_nr",
            "section",
            "resolution",
            "abblation_state",
            "segment_type",
            "segment_nr",
            "red_pixels",
            "yellow_pixels",
            "tissue_pixels",
            "fibrosis_perc",
            "edge_counter",
            "edge_count_min",
            "edge_count_max",
            "edge_score",
            "pixarea",
            "tissue_mm2",
            "VM_mm2",
            "fibrosis_mm2",
            "pixlength",
            "border_mm",
        ]

    data_heart = params_from_filename(file=filepath, type="segment")
    # add pixarea and pixlength
    data_heart["pixarea"] = PIXAREA
    data_heart["pixlength"] = PIXLENGTH
    # get the pixels and edges
    with Image.open(filepath) as im:
        (
            data_heart["red_pixels"],
            data_heart["yellow_pixels"],
            data_heart["edge_counter"],
        ) = count_pixels_and_edges(im)

    # calculate values to export.
    data_heart["tissue_pixels"] = data_heart["red_pixels"] + data_heart["yellow_pixels"]
    try:
        data_heart["fibrosis_perc"] = (
            data_heart["red_pixels"] / data_heart["tissue_pixels"] * 100
        )
    except ZeroDivisionError:
        data_heart["fibrosis_perc"] = "Null"
    # edge values
    data_heart["edge_count_min"] = edge_count_min_value(data_heart["red_pixels"])
    # every red pixels has only yellow pixels as neighbor.
    data_heart["edge_count_max"] = 4 * data_heart["red_pixels"]
    try:
        data_heart["edge_score"] = (
            data_heart["edge_counter"] - data_heart["edge_count_min"]
        ) / (data_heart["edge_count_max"] - data_heart["edge_count_min"])
    except ZeroDivisionError:
        data_heart["edge_score"] = "Null"
    # Calculate areas
    data_heart["tissue_mm2"] = data_heart["tissue_pixels"] * PIXAREA
    data_heart["VM_mm2"] = data_heart["yellow_pixels"] * PIXAREA
    data_heart["fibrosis_mm2"] = data_heart["red_pixels"] * PIXAREA
    data_heart["border_mm"] = data_heart["edge_counter"] * PIXLENGTH

    header = DELIMITER.join(variables) + "\n"

    # todo split into separate function
    # write data to file.
    with open(outputfilepath, open_mode, encoding="utf-8") as fh:
        # check if header is already written...
        # move cursor to beginning of file
        fh.seek(0)
        if not fh.readline() == header:
            # ...if not add it.
            logger.info(
                f"...adding header to output file {os.path.split(outputfilepath)[1]}"
            )
            fh.write(header)
        # move cursor back to end of file
        fh.seek(0, 2)

        for variable in variables:
            try:
                fh.write(str(data_heart[variable]) + DELIMITER)
            except KeyError:
                fh.write("Null" + DELIMITER)

        fh.write("\n")


@logging_decorator
def counter_sc2(
    directory: str | None = None,
    outputfilename: str = "output.csv",
    file_per_folder=False,
    analyze_models=None,
):
    """
    Analyse all the segments in MINI folders that have not already been analyzed.
        directory           directory to analyze
                            if none is provided, the directory of the script is used.

        outputfilename      the name of the outputfile,
                            it will be saved to the current working directory

        file_per_folder     False: all data is saved to one file
                            True: data is saved to a file per folder

        analyze_models      The models to analyze, can be MINI, CAG, AHA
                            Note: the directories with the segments need to
                            be named MINI, CAG or AHA accordingly
                            default: ['MINI', 'CAG', 'AHA']
    """
    if directory is None:
        directory = os.path.dirname(__file__)

    if analyze_models is None:
        analyze_models = ["MINI", "CAG", "AHA"]

    file_per_folder = False
    # analyze_models = analyze_models

    outputfile = os.path.join(directory, outputfilename)
    # walk through the folders
    for dirpath, dirs, _ in os.walk(directory):
        for directory in dirs:
            if directory in analyze_models:
                # found a MINI directory
                logger.info(f"..found directory: ./{directory}")
                if file_per_folder:
                    outputfile = os.path.join(dirpath, outputfilename)
                    # check if there is an outputfilename file
                    if os.path.exists(outputfile):
                        # if so skip the folder
                        logger.info(
                            f"Skipped directory - {outputfile} already exists\n"
                        )
                        continue
                else:
                    # analyse the files in the folder
                    # TODO: use common.pngs_in_fld instead
                    for file in os.listdir(os.path.join(dirpath, directory)):
                        if os.path.splitext(file)[1] == ".png":
                            logger.info(f"..Analysing image: {file}.")
                            analyse_image(
                                filepath=os.path.join(dirpath, directory, file),
                                outputfilepath=outputfile,
                            )
