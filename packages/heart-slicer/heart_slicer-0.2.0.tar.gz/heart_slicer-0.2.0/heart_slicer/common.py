"""
Commonly usable functions for the heart_slicer package.
"""

import os
import logging
from PIL import Image
import yaml

use_relative_paths = False

# Configure the logger
logging.basicConfig(level=logging.INFO)
# format='%(asctime)s - %(name) - %(levelname) - %(message)')
logger = logging.getLogger(__name__)
# Add a file handler
fh = logging.FileHandler("logger.log")
logger.addHandler(fh)


# TODO: move use filehandles instead of opening the file in various methods
# Import the config file
def load_config(file_path):
    """Load config file."""
    logger.info(f"Loading config file: {file_path}...")

    with open(file_path, "r") as config_file:
        config = yaml.safe_load(config_file)
        if use_relative_paths is True:
            logger.info("..using relative paths in folder settings")
            config["settings"]["folder_input"] = os.path.realpath(
                config["settings"]["folder_input"]
            )
            config["settings"]["folder_output"] = os.path.realpath(
                config["settings"]["folder_output"]
            )
    logger.info("..checking config")
    return config


CONFIG_FILE = "config.yml"
config_path = os.path.join(os.path.dirname(__file__), "..", CONFIG_FILE)
config = load_config(config_path)

logconfig = config["logging"]

# check loglevel
loglevels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
if logconfig["level"] not in loglevels:
    msg = (
        f"Not a valid logging level: {logconfig['level']}\n"
        + f"\t\toptions are: {loglevels}"
    )
    logger.error(msg)
    raise ValueError(msg)
# set loglevel
logger.setLevel(logconfig["level"])

# check loaded config
missing_settings = []
for key in config["settings"].keys():
    if config["settings"][key] is None:
        missing_settings.append(key)
if missing_settings != []:
    for setting in missing_settings:
        msg = f"missing value for setting: {setting}"
        logger.error(msg)
    raise ValueError(f"missing settings: {missing_settings}")
logger.info("..values for all settings provided")

# lead settings to locals
settings = config["settings"]
colors = config["colors"]


# check if folders exist
provided_folders = [
    "folder_input",
    "folder_output",
    "diagram_outputfolder",
]
for fld in provided_folders:
    if os.path.isdir(settings[fld]) is False:
        msg = (
            "Invalid value for "
            + f"'{fld}'\n\t {settings[fld]}\n\t\tis not an existing folder."
            + "\nPlease create the folder or provide a valid path in the config file."
        )
        logger.error(msg)
        raise ValueError(msg)
logger.info("..folders exists")

logger.info("..Config checked and seems OK :)")


def logging_decorator(fn):
    """Basic logging decorator"""

    def func(*args, **kwargs):
        logger.debug(f"{fn.__name__}({args}, {kwargs})")
        return fn(*args, **kwargs)

    return func


##### FOR SC2 IMAGES #####
# image resolution: 40.316 pix/mm
# pixel side length = 0.024804mm
# pixel area = 0.0006152 mm2

# import time
# t1 = time.time()


@logging_decorator
def sign(x):
    """
    return the signum of x.
    edge cases not well defined
    """
    if x < 0:
        return -1
    return 1


def image_width(im):
    """
    Return the width of the image
    """
    return im.size[0]


def image_height(im):
    """
    Return the height of the image
    """
    return im.size[1]


@logging_decorator
def secs_to_str(s):
    """return string MM:SS for a given number of seconds."""
    return f"{s // 60:0>2.0f}:{s % 60:0>2.0f}"


@logging_decorator
def create_folder(folder):
    """
    Check if the folder exists. If it doesn't create the folder."""
    # check if folder exists
    if os.path.exists(folder):
        logger.info(
            "..Folder already exists: "
            + f".\{os.path.relpath(folder, os.path.dirname(__file__))}"
        )
    else:
        # create directory
        os.mkdir(folder)
        logger.info(
            f"Created folder: .\{os.path.relpath(folder, os.path.dirname(__file__))}."
        )


@logging_decorator
def pngs_in_fld(fld):
    """
    Find all .png files in the given folder.
    Args:
        fld (str): The path to the folder to search for .png files.

    Returns:
        list: A list of filenames (str) of all .png files in the given folder.

    Logs:
        Logs the list of all files in the folder.
        Logs a message if no .png files are found.
        Logs the list of found .png files.
    """
    logger.info(os.listdir(fld))
    images_to_proces = []
    for file in os.listdir(fld):
        # check if it's a file
        filepath = os.path.join(fld, file)
        if os.path.isfile(filepath) is False:
            continue
        # check if it's a .png
        if os.path.splitext(file)[1] != ".png":
            continue
        # add to images to proces
        images_to_proces.append(file)
        if len(images_to_proces) == 0:
            logger.info(f"Found no images to in folder {fld}")
    # show result
    logger.info(f"Searched folder: {fld} \n\tfound the following files:")
    for png in images_to_proces:
        logger.info(f"\n=t{png}")

    return images_to_proces


@logging_decorator
def params_from_filename(file: str, type: str) -> list:
    """Extract parameters from a filename based on the specified type.
    The filename should follow the naming convention:
        for a slice:
            heartName_sliceNr_section_resolution_abblationState_none_segmentType_SegmentNr.png
        for a segment:
            heartName_sliceNr_section_resolution_abblationState_none.png

    params:
        file (str): The full path or name of the file.
        type (str): The type of parameters to extract. Can be either "segment" or "slice".
    Returns:
        list: A dictionary containing the extracted parameters.
    Raises:
        ValueError: If the filename does not adhere to the expected format.
    Example:
    >>> params_from_filename("heartA_01_section1_256x256_ablation1_none_segmentA_01.png", "segment")
    {
        'heart': 'heartA',
        'slice_nr': '01',
        'section': 'section1',
        'abblation_state': 'ablation1',
        'resolution': '256x256',
        'segment_nr': '01',
        'segment_type': 'segmentA'
    >>> params_from_filename("heartA_01_section1_256x256_ablation1_none.png", "slice")
    {
        'heart': 'heartA',
        'slice_nr': '01',
        'section': 'section1',
        'abblation_state': 'ablation1',
        'resolution': '256x256'
    """
    # remove leading folders if they exist
    filename = str(os.path.split(file)[1])
    # check if the filename has the correct number of underscores
    nr_underscores = os.path.splitext(filename)[0].count("_")
    try:
        if type == "segment":
            if nr_underscores != 7:
                raise ValueError(
                    f"not a supported file name format. Expected 7 underscores got {nr_underscores}"
                )
            (
                heart,
                slice_nr,
                section,
                resolution,
                abblation_state,
                _,
                segment_type,
                segment_nr,
            ) = os.path.splitext(filename)[0].split("_")[:8]
            out = {
                "heart": heart,
                "slice_nr": slice_nr,
                "section": section,
                "abblation_state": abblation_state,
                "resolution": resolution,
                "segment_nr": segment_nr,
                "segment_type": segment_type,
            }
        if type == "slice":
            if nr_underscores != 5:
                raise ValueError(
                    f"not a supported file name format. Expected 5 underscores got {nr_underscores}"
                )
            (heart, slice_nr, section, resolution, abblation_state, _) = (
                os.path.splitext(filename)[0].split("_")[:6]
            )
            out = {
                "heart": heart,
                "slice_nr": slice_nr,
                "section": section,
                "abblation_state": abblation_state,
                "resolution": resolution,
            }
        return out
    except ValueError as e:
        # raise InputError('not a supported file name format.')  # run calculation
        logger.info(
            f"Not a valid file name: {filename}\n"
            + "images should adhere to the following naming convention:\n\t"
            + "heartName_sliceNr_section_resolution_abblationState_none_"
            + "segmentType_SegmentNr.png"
        )
        # skip this file
        raise ValueError from e


@logging_decorator
def generate_filename_segment(
    file_params: dict, segmentation_type: str, segment_name: str
) -> str:
    """
    Generate the filename for the segment based on segment name
    and parameters from image file name.

    Parameters:
        file_params (dict): The parameters extracted from the image file name.
        segmentation_type (str): The type of segmentation.
        segment_name (str): The name of the segment.
    Returns:
        str: The generated filename

    """
    out = (
        "_".join(
            [
                file_params["heart"],
                file_params["slice_nr"],
                file_params["section"],
                file_params["resolution"],
                file_params["abblation_state"],
                "out",
                segmentation_type,
                segment_name,
            ]
        )
        + ".png"
    )
    return out


@logging_decorator
def save_image(
    im: Image, save_folder: str, filename: str, overwrite_existing: bool
) -> bool:
    """
    Saves an image to the specified folder with the given filename.

    Parameters:
        im (Image): The image to be saved.
        save_folder (str): The folder where the image will be saved.
        filename (str): The name of the file to save the image as.
        overwrite_existing (bool): If False, the function will not overwrite an existing file with the same name.

    Returns:
        bool: True if the image was saved successfully, False if the file already exists and overwrite_existing is False.
    """
    # skip file if a file with the same filename exists
    if (
        overwrite_existing is False
        and os.path.isfile(os.path.join(save_folder, filename)) is True
    ):
        # skip segment
        logger.info(
            f".skipping file: {filename}"
            + "\nalready exists in folder .\\"
            + f"{os.path.relpath(save_folder, os.path.dirname(__file__))}."
        )
        return False
    # otherwise save

    im.save(os.path.join(save_folder, filename))
    logger.info(
        f"Saved file {filename}\n\tas: "
        + f"{filename}\n\tin folder: .\\"
        + f"{os.path.relpath(save_folder, os.path.dirname(__file__))}."
    )
    return True
