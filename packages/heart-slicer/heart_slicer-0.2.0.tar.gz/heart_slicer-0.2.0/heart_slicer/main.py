"""
Main file for the heart_slicer package.
"""
# TODO: fix example path error

from __future__ import annotations
import os

# import cProfile
# import pstats
# from pstats import SortKey
# import numpy as np
# package
# import common
# import slicer
# import slice_analyser
from . import common, slice_analyser, slicer

# for testing performance
common.settings["profile"] = False


def run_heart() -> None:
    """Run the heart script with configuration from config.yml"""
    common.logger.info("RUNNING HEART.PY AS MAIN.")
    # profile performance
    # if common.settings['profile'] is True:
    #     pr = cProfile.Profile()
    #     pr.enable()

    all_modes = [
        "all",
        "-A",
        "cutter",
        "-X",
        "counter_SC2",
        "-SC2",
        "example",
        "counter",
    ]

    common.logger.info(f"Selected mode: {common.settings['mode']}")

    if common.settings["mode"] not in all_modes:
        common.logger.info(
            f"unknown mode {common.settings['mode']}, choose from {all_modes}"
        )
        raise NotImplementedError(
            f"unknown mode {common.settings['mode']},"
            + f" supported modes are: {all_modes}"
        )
    
    if common.settings["mode"] == "example":
        common.logger.info(
            "running in EXAMPLE mode. Process all slices for example image"
        )
        # overwrite output folder to test
        # TODO fix ".." not correct for all systems
        common.settings["folder_output"] = os.path.join(
            os.path.dirname(__file__), "..", "example", "output"
        )
        common.settings["folder_input"] = os.path.join(
            os.path.dirname(__file__), "..", "example", "input"
        )
        # cutter
        common.logger.info(
            slicer.process_heart_images_in_directory(
                directory_in=common.settings["folder_input"],  # contains 3 test files
                directory_out=common.settings["folder_output"],
                move_file=common.settings["move_slice_file"],
                overwrite_existing=True,
                segmentation_types=["CAG", "AHA", "MINI"],
            )
        )
        # counter
        slice_analyser.counter_sc2(
            directory=common.settings["folder_output"],
            outputfilename=common.settings["output_file"],
            analyze_models=["CAG"],
            file_per_folder=common.settings["outputfile_per_folder"],
        )
        common.logger.info(f"\n{30 * '-'}\nFinished example\n{30 * '-'}")

    if common.settings["mode"] in ["all", "-A", "cutter", "-X"]:
        _ = slicer.process_heart_images_in_directory(
            directory_in=common.settings["folder_input"],
            directory_out=common.settings["folder_output"],
            move_file=common.settings["move_slice_file"],
            overwrite_existing=common.settings["overwrite_existing"],
            segmentation_types=["AHA", "CAG", "MINI"],
        )

    if common.settings["mode"] in ["counter", "counter_SC2", "-SC2", "all", "-A"]:
        slice_analyser.counter_sc2(
            directory=common.settings["folder_output"],
            outputfilename=common.settings["output_file"],
            analyze_models=["AHA", "CAG", "MINI"],
            file_per_folder=common.settings["outputfile_per_folder"],
        )

    common.logger.info("------- END OF HEART SCRIPT ---------")
