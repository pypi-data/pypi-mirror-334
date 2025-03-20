"""
Create a diagram based on the slice_analyser results.
"""

import os
import copy  # needed to copy colormap to prevent error
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import patches, lines

# import matplotlib.lines as lines
from .common import logger, settings

# Settings
FIGSIZE_X = 6
FIGSIZE_Y = 6
ROWS = 1
COLS = 1
WINDOW_TITLE = "test titel"
DEFAULT_CMAP = "hsv"
DEFAULT_HATCH = "/"
ERROR_VALUE = -1
ERROR_COLOR = (1, 1, 1)
ERROR_HATCH = "oo"


def get_cmap_by_valuetype(value_type, norm_range=None):
    """Return cmap based on value type.

    Parameters
    ----------
    value_type : str
            Value type to base colormap on.
    norm_range : list, length 2
            minimum (norm_range[0]) and maximum (norm_range[1]) values of the colormap

    Output
    ------
    Colormap
            default value is 'hsv'
    norm : matplotlib.colors.Normalize function
            normalizes values to between v_min and v_max to the colormap.
    """
    # set colormap
    match value_type:
        # set default colormap based on data type
        # For fibrosis_perc: RdYlGn_r
        case "fibrosis_perc_NABL" | "fibrosis_perc_WABL":
            chosen_cmap = "RdYlGn_r"
            # fix the scale to 0-100 for percentages
            norm_range = [0, 100]
        # for fibrosis mm2:YlOrRd
        case "red_pixels_NABL" | "red_pixels_WABL":
            chosen_cmap = "YlOrRd"
        # for VM mm2: Wistia
        case "yellow_pixels_NABL" | "yellow_pixels_WABL":
            chosen_cmap = "plasma"
        # for tissue mm2: Spectral
        case "tissue_pixels_NABL" | "tissue_pixels_WABL":
            chosen_cmap = "Spectral"
        # for border mm: viridis
        case "edge_counter_NABL" | "edge_counter_WABL":
            chosen_cmap = "gnuplot"
        # for border over mm2:
        case "edge_score_NABL" | "edge_score_WABL":
            chosen_cmap = "viridis"
            # fix the scale to 0-10
            norm_range = [0, 1]
        case _:
            # otherwise use default
            chosen_cmap = DEFAULT_CMAP

    # set colormap, copy to prevent error from matplotlib
    cmap = copy.copy(mpl.cm.get_cmap(chosen_cmap))
    # set bad value for colormap
    cmap.set_bad(color="w")

    # normalize colormap
    if norm_range is not None:
        # default to normalize min, max
        ##values = [line['value'] for line in data]
        norm = mpl.colors.Normalize(vmin=norm_range[0], vmax=norm_range[1])

    return cmap, norm


def cag_border_plot(fig, ax, data, value_type, cmap=None, hatchtype=None, norm=None):
    """
    CAG border plot for segments surrounding a VT related site.

    Parameters
    ----------
    fig : figure object
    ax : axes
    data : dict
            Dict with indices: 'vt', 'cw', 'ccw', 'sup', 'inf'.
            Each entry has the values:
                    value : int or float
                            value of the segment
                    border : int or float
                            border thickness
                    hatch : True or False
                            show hatch
                    'vt':{'value':1, 'border':10, 'hatch':True},
    value_type : str
            Type of value being plotted, requered to set correct cmap
    border : list of floats with border thickness, optional
            A list with the segments to highlight
    cmap : ColorMap or None, optional
            Optional argument to set the desired colormap
    hatchtype : str
            hatchtype for the plot (see matplotlib.patch.hatch)

    Returns
    -------
    matplotlib plot object
    """

    # scale border
    border_scale = 20 / 100
    # calculate min and max values
    # min_val = min([k["value"] for k in data.values() if k["value"] != ERROR_VALUE])
    # max_val = max([k["value"] for k in data.values()])

    # set colormap	cmap, norm = get_cmap_by_valuetype(value_type, norm_range=[min_val, max_val])

    # add legend color bar
    # ..create axis for the colorbar
    fig.subplots_adjust(bottom=0.15)  # make space for colorbar
    bar_width = 0.8
    bar_height = 0.03
    bar_from_bottom = 0.08

    # ..set size [x, y, width, height]
    ax_bar = fig.add_axes([(1 - bar_width) / 2, bar_from_bottom, bar_width, bar_height])
    plt.colorbar(
        mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
        cax=ax_bar,
        orientation="horizontal",
        label=value_type,
    )

    for el in ["vt", "cw", "ccw", "sup", "inf"]:
        match el:
            case "vt":
                xy = (1, 1)
                xline = [1, 1, 2, 2, 1]
                yline = [1, 2, 2, 1, 1]
            case "ccw":
                xy = (0, 1)
                xline = [1, 0, 0, 1]
                yline = [1, 1, 2, 2]
            case "cw":
                xy = (2, 1)
                xline = [2, 3, 3, 2]
                yline = [1, 1, 2, 2]
            case "sup":
                xy = (1, 2)
                xline = [1, 1, 2, 2]
                yline = [2, 3, 3, 2]
            case "inf":
                xy = (1, 0)
                xline = [1, 1, 2, 2]
                yline = [1, 0, 0, 1]
            case _:
                xy = (-10, -10)

        # check if needs to be hashed
        if data[el]["hatch"] is True:
            hatch = hatchtype
        else:
            hatch = None

        # set color

        if data[el]["value"] == ERROR_VALUE:
            color = ERROR_COLOR
            hatch = ERROR_HATCH
        else:
            color = cmap(norm(data[el]["value"]))

        # Create a Rectangle patch and line
        rect = patches.Rectangle(
            xy, 1, 1, linewidth=1, edgecolor=(0, 0, 0), facecolor=color, hatch=hatch
        )
        line = lines.Line2D(
            xline, yline, linewidth=data[el]["border"] * border_scale, color=(0, 0, 0)
        )

        # Add the patch and line to the Axes
        ax.add_patch(rect)
        ax.add_line(line)
    return fig, ax


def create_border_plot(data, value_type, title):
    """
    Create the border plot with required data.

    Parameters:
            data : dict
                    --see CAG_border_plot help--
    Output:
            matplotlib.plt
                    resulting plot
    """

    # Make figure with axes in desired dimensions
    fig, ax = plt.subplots(figsize=(FIGSIZE_X, FIGSIZE_Y), nrows=ROWS, ncols=COLS)

    # setup axis
    plt.xlim([-0.1, 3.1])
    plt.ylim([-0.1, 3.1])
    plt.axis("off")  # don't show them
    ax.set_title(title)

    cag_border_plot(fig, ax, data, value_type, hatchtype=DEFAULT_HATCH)

    return plt


def cag_bullseye_plot(
    plot_type,
    fig,
    ax,
    data,
    value_type,
    border=None,
    cmap=None,
    norm=None,
    label=None,
    norm_border=None,
    title=None,
):
    """
    CAG bullseye representation for the left ventricle.

    Parameters
    ----------
    plot_type : type of plot: CAG, AHA or MINI
    fig : figure object
    ax : axes
    data : list of int and float
            The intensity values for each of the 16 segments (named 'A' to 'P')
    value_type : str
            Type of value being plotted, requered to set correct cmap
    border : list of floats with border thickness, optional
            A list with the segments to highlight
    cmap : ColorMap or None, optional
            Optional argument to set the desired colormap
    norm : [min, max] or None, optional
            Optional argument to normalize data into the [0.0, 1.0] range
    norm_border : [min (float), max (float)] or None, optional
            Optional min, max range to normalize border thickness
            Default: user min, max from border data

    Notes
    -----
    .....
    """
    border_thickness_min = 0.1  # Minimal thickness of the border
    border_thickness_max = 5  # maximum thickness of the border
    border_colour = "k"
    # theta_zero_location = "N"  # set the location of theta0 (N, NW, ...)

    # set colormap
    # see: https://matplotlib.org/3.1.1/tutorials/colors/
    # 		colorbar_only.html#sphx-glr-tutorials-colors-colorbar-only-py

    # TODO: check if this is the same as used in slicer.py
    # correct segment indicator based on plot_type and offset
    # label keys from outside to inside and counter clockwise
    # ..offset in degrees counter clockwise
    if plot_type == "CAG":
        keys = [
            ["A", "B", "C", "D", "E", "F"],
            ["G", "H", "I", "J", "K", "L"],
            ["M", "N", "O", "P"],
            ["Q"],
        ]
        offset = [0, 0, 0, 0]
    elif plot_type == "AHA":
        keys = [
            ["1", "2", "3", "4", "5", "6"],
            ["7", "8", "9", "10", "11", "12"],
            ["13", "14", "15", "16"],
            ["17"],
        ]
        offset = [-30, -30, -45, 0]
    elif plot_type == "MINI":
        keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
            ["13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"],
            ["25", "26", "27", "28", "29", "30", "31", "32"],
            ["33"],
        ]
        offset = [0, 0, 0, 0]
    else:
        raise ValueError(
            f"{plot_type} is not a supported plot type." + "choose from: 'AHA', 'CAG"
        )

    cmap = get_cmap_by_valuetype(value_type, norm_range=[min(data), max(data)])

    # add legend color bar
    # ..create axis for the colorbar
    fig.subplots_adjust(bottom=0.15)  # make space for colorbar
    bar_width = 0.8
    bar_height = 0.03
    bar_from_bottom = 0.08
    # ..set size [x, y, width, height]
    ax_bar = fig.add_axes([(1 - bar_width) / 2, bar_from_bottom, bar_width, bar_height])
    plt.colorbar(
        mpl.cm.ScalarMappable(cmap=cmap, norm=norm),
        cax=ax_bar,
        orientation="horizontal",
        label=value_type,
    )

    # pre process data
    # sort the data on slice, segment
    data = sorted(
        data, key=lambda point: str(point["slice"]).zfill(2) + point["segment"]
    )
    # determine number of slices
    nr_slices = data[-1]["slice"] - data[0]["slice"] + 1

    # normalize the border
    if norm_border is None:
        # use min, max by default
        borders = [line["border"] for line in data]
        bmin = min(borders)
        bmax = max(borders)
    elif all(isinstance(n, float) for n in norm_border) and len(norm_border) == 2:
        bmin = norm_border[0]
        bmax = norm_border[1]
    else:
        raise ValueError(
            f"norm_border not list of two floats (provided: {norm_border})"
        )

    def norm_borders_func(x):
        return border_thickness_min + ((x - bmin) / (bmax - bmin)) * (
            border_thickness_max - border_thickness_min
        )

    # prep data
    plot_data = []  # actual values to plot
    plot_border = []  # list of border to plot, same dimensions as 'plot_data'
    plot_label = []  # store the labels to plot
    plot_offset = []  # store the offset (degrees)
    last_slice = data[0]["slice"] - 1  # to keep track of the last used slice
    # ..loop data
    for segment in data:
        # ..check if new slice
        if segment["slice"] != last_slice:
            # fill in gaps of missing slices if there are any.
            while segment["slice"] > last_slice + 1:
                plot_data.append([np.NaN])
                plot_border.append([0])
                plot_label.append([None])
                plot_offset.append(0)
                last_slice += 1
            # ..create correct number of segments for slice based on segment letter
            # can do this more flexible (but...this works)

            def prep_segment(key_to_find):
                # prepare correct number of fields or return error
                for keys_slice in keys:
                    if key_to_find in keys_slice:
                        plot_data.append([np.NaN] * len(keys_slice))
                        plot_border.append([None] * len(keys_slice))
                        plot_label.append([None] * len(keys_slice))
                        plot_offset.append(offset[keys.index(keys_slice)])
                        return
                # if not found, raise error
                raise ValueError(
                    f"segment '{key_to_find}' not supported in plot type: {plot_type}"
                )

            prep_segment(segment["segment"])

            last_slice = segment["slice"]

        # ..add data to correct position in data, fill np.NaN for all non numeric values
        def index_segment(v, ks):
            try:
                ind = ks.index(v)
            except ValueError:
                ind = -1
            return ind

        index = max([index_segment(segment["segment"], ks) for ks in keys])

        # check if it is a number
        if type(segment["value"]) in [float, int]:
            plot_data[-1][index] = segment["value"]
        # add normalized border
        plot_border[-1][index] = norm_borders_func(segment["border"])
        # ..add labels
        # TODO: use actual label
        if label == "value":
            plot_label[-1][index] = segment["value"]
        elif label == "label":
            plot_label[-1][index] = segment["label"]
        elif label == "segment":
            plot_label[-1][index] = segment["segment"]

    # some graph settings
    inner_circle_diameter = 0.15  # size of the inner circle
    outer_circle_diameter = 1.0  # outer size of the circle
    segment_height = (outer_circle_diameter - inner_circle_diameter) / nr_slices

    # loop the slices
    for i in enumerate(plot_data):
        # for i in range(len(plot_data)):
        # based on: https://matplotlib.org/gallery/pie_and_polar_charts/
        # 		nested_pie.html#sphx-glr-gallery-pie-and-polar-charts-nested-pie-py
        # draw line plot_data
        nsc = len(plot_data[i])  # number of segments in the circle
        width = 2 * np.pi / nsc
        bottom = inner_circle_diameter + i * segment_height

        # calculate correct x-values including offset
        x = list(np.arange(0, 2 * np.pi, width) + plot_offset[i] * np.pi / 180)

        # draw bar graph
        ax.bar(
            x=x,
            width=width,
            bottom=bottom,
            height=segment_height,
            color=[
                cmap(norm(value)) for value in plot_data[i]
            ],  # TODO: check if corect
            edgecolor=border_colour,
            linewidth=plot_border[i],
            align="edge",
        )
        # add annotation
        if label is not None:
            for j in range(len(plot_data[i])):
                ax.annotate(
                    plot_label[i][j],
                    xy=(x[j] + width / 2, bottom + segment_height / 2),  # (theta, r)
                    xycoords="data",
                    textcoords="data",
                    horizontalalignment="center",
                    verticalalignment="center",
                    color="k",
                )

    # don't show tick labels
    ax.set_theta_zero_location("N")
    ax.grid(False)
    ax.set_ylim([0, outer_circle_diameter])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_title(title)


def create_bullseye_plot(df, heart, plot_type, value_type):
    """
    Create a bullseye plot with data in df.
    """
    # prep data

    # create filters
    filter_heart = df["HEART"] == heart
    filter_cag = df["AHA_CAG_MINI"] == plot_type

    # temp store the data
    data_slice = list(df[filter_cag & filter_heart]["SLICE"])
    data_segment = list(df[filter_cag & filter_heart]["segment"])
    data_border = list(df[filter_cag & filter_heart]["ABL_loss_perc"])
    data_value = list(df[filter_cag & filter_heart][value_type])

    # scale to maximum in category
    max_value_type = df[filter_heart][value_type].max()
    min_value_type = df[filter_heart][value_type].min()

    # merge into list of dicts (to be fair, looking back maybe not most convenient option)
    data = []
    for i in range(len(data_slice)):
        data.append(
            {
                "slice": data_slice[i],
                "segment": data_segment[i],
                "value": data_value[i],
                "border": data_border[i],
                "label": None,
            }
        )

    # create plot
    # Make figure with axes in desired dimensions
    fig, ax = plt.subplots(
        figsize=(FIGSIZE_X, FIGSIZE_Y),
        nrows=ROWS,
        ncols=COLS,
        subplot_kw=dict(projection="polar"),
    )
    # fig.canvas.set_window_title(f"{heart} - {value_type} ({plot_type})")

    # run bullseye plot
    cag_bullseye_plot(
        plot_type,
        fig,
        ax,
        data,
        value_type=value_type,
        norm=[min_value_type, max_value_type],
        label=None,
        norm_border=[0.0, 100.0],
        cmap=None,
        title=f"Heart {heart} ({plot_type})",
    )

    # show plot
    if settings["diagram_show"]:
        plt.show()

    if settings["save_diagram_to_file"]:
        savefile = os.path.join(
            settings["diagram_outputfolder"], f"{heart}_{value_type}_{plot_type}.png"
        )
        plt.savefig(savefile)

    # close figure
    plt.close(fig)


if __name__ == "__main__":
    logger.info('Running "heart.diagram.py as MAIN"')

    settings["diagram_inputfile"] = "testfile.csv"
    Base_path = os.getcwd()  # assume everything is in the folder of the python file.
    settings["diagram_outputfolder"] = "output_CAG_diagram"
    settings["save_diagram_to_file"] = True

    def data_csv_line_to_data(csv_line):
        """transform to dict for plotting.

        format of the input line:
        data_csv_line = 'filename,value_type,vt_value,vt_border,vt_hatch,ccw_value,
                                        ccw_border,ccw_hatch,cw_value,cw_border,cw_hatch,sup_value,
                                        sup_border,sup_hatch,inf_value,inf_border,inf_hatch'
        """
        data_csv = csv_line.strip().split(",")
        filename = data_csv[0]
        value_type = data_csv[1]
        data = {}  # empty dict for output
        index = 2

        for part in ["vt", "ccw", "cw", "sup", "inf"]:
            data[part] = {}  # empty dict
            for para in ["value", "border", "hatch"]:
                try:
                    if para == "hatch":
                        val = bool(int(data_csv[index]))
                    else:
                        val = float(data_csv[index])
                except ValueError:
                    val = ERROR_VALUE

                data[part][para] = val
                index += 1

        return filename, value_type, data

    # open file and loop through lines
    with open(os.path.join(Base_path, settings["diagram_inputfile"]), "r") as f:
        for line in f.readlines():
            # read contents of line
            try:
                filename, value_type, data = data_csv_line_to_data(line)
                logger.info(filename, value_type)
                """
				data = {'vt':{'value':3.2, 'border':1, 'hatch':True},\
							'ccw':{'value':1, 'border':3, 'hatch':False},\
							'cw':{'value':2, 'border':2, 'hatch':False},\
							'sup':{'value':3, 'border':4, 'hatch':True},\
							'inf':{'value':4, 'border':1, 'hatch':True},}	
				"""
                title = f"{filename} ({value_type})"

                plt = create_border_plot(data, value_type, title)

                # show plot
                if settings["diagram_show"]:
                    plt.show()

                if settings["save_diagram_to_file"] is True:
                    savefile = os.path.join(Base_path, f"{filename}_{value_type}.png")
                    plt.savefig(savefile)

                # close figure
                plt.close()

            except ValueError as e:
                logger.info(f"Couldn't proces line {line}\nError:{e}")

    if False:
        # import the data
        logger.info(f"importing: {settings['diagram_inputfile']}")
        # read data from file using pandas dataframe
        df = pd.read_csv(settings["diagram_inputfile"], delimiter=";", decimal=",")
        # list of all the hearts in the file
        # df['HEART'] = df['HEART'].apply(lambda x: x.upper())  # convert to upper case
        hearts = list(df["HEART"].unique())
        logger.info(f"Hearts found ({len(hearts)}): {hearts}")
        plot_types = list(df["AHA_CAG_MINI"].unique())

        # value types - columns not used for other data
        value_types = np.setdiff1d(
            list(df.keys()),
            ["HEART", "SLICE", "AHA_CAG_MINI", "ABL_State", "segment", "ABL_loss_perc"],
        )

        # if saving to file, check if output folder exists, if not create it
        folder = os.path.join(
            os.path.split(settings["diagram_inputfile"])[0],
            settings["diagram_outputfolder"],
        )
        if settings["save_diagram_to_file"] is True and not os.path.exists(folder):
            # create folder
            os.makedirs(folder)
            logger.info(f"created output folder: {folder}")

        # loop data in dataframe
        total_plots = len(hearts) * len(value_types) * len(plot_types)
        plot_nr = 0
        for heart in hearts:
            for value_type in value_types:
                for plot_type in plot_types:
                    plot_nr += 1
                    logger.info(
                        f"running: {heart} - {value_type} ({plot_type}-plot) ({plot_nr}/{total_plots})"
                    )
                    create_bullseye_plot(df, heart, plot_type, value_type)

    logger.info("End of heart.diagram.py")
