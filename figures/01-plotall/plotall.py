"""
Plot relative and absolute binding free energy results from multiple targets into a single plot.
Intended to be used for systems extracted from https://github.com/kntkb/protein-ligand-benchmark-custom.
"""
import os, sys
import numpy as np
import glob
import click
from cinnabar import plotting, wrangle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.set_loglevel("critical")
mycolor_dict = mcolors.TABLEAU_COLORS
#{ 'tab:blue': '#1f77b4',
#  'tab:orange': '#ff7f0e',
#  'tab:green': '#2ca02c',
#  'tab:red': '#d62728',
#  'tab:purple': '#9467bd',
#  'tab:brown': '#8c564b',
#  'tab:pink': '#e377c2',
#  'tab:gray': '#7f7f7f',
#  'tab:olive': '#bcbd22',
#  'tab:cyan': '#17becf'}


def load_csv(input_prefix, targets, forcefield):
    """ Load cinnabar csv file from multiple targets and merge them together.
    """
    # Load data
    mydict = {"Experimental": [], "Calculated": []}
    dict_exp = {}
    dict_calc = {}
    for target in targets:
        #print(target)
        dict_exp[target] = []
        dict_calc[target] = []
        # get csv
        path = os.path.join(input_prefix, target, forcefield, "states12")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]
        # load and loop through cinnabar result for each target
        f = open(cinnabar_file, "r")
        is_exp = True
        is_calc = False
        for l in f.readlines():
            l = l.strip('\n')
            # check if it is an experimental block or calculated block
            if l.startswith("# Calculated block"):
                is_exp = False
                is_calc = True
            # store data
            if l.startswith("lig_"):
                l = l.replace("lig_", f"{target}_lig_")
                if is_exp == True and is_calc == False:
                    dict_exp[target].append(l)
                elif is_exp == False and is_calc == True:
                    dict_calc[target].append(l)
        f.close()

    # Store data
    mydict["Experimental"] = dict_exp
    mydict["Calculated"] = dict_calc

    # Export
    csv_path = f'./cinnabar_{forcefield}.csv'
    wf = open(csv_path, "w")
    # Header
    block_name = "Experimental"
    wf.write("# Experimental block\n")
    wf.write("# Ligand, expt_DG, expt_dDG\n")
    for target_name, values in mydict[block_name].items():
        for value in values: 
            wf.write(f"{value}\n")
    # Header
    block_name = "Calculated"
    wf.write("# Calculated block\n")
    wf.write("# Ligand1(OLD),Ligand2(NEW), calc_DDG, calc_dDDG(MBAR), calc_dDDG(additional)\n")
    for target_name, values in mydict[block_name].items():
        for value in values: 
            wf.write(f"{value}\n")
    wf.close()

    return csv_path


def _plot_absolute_custom(input_prefix, targets, forcefield, figure_extension):
    """ Plot absolute binding free energy calculation for multiple targets.
    """
    # https://github.com/OpenFreeEnergy/cinnabar/blob/0.3.0/cinnabar/plotting.py#L414
    labels = []
    for i, target in enumerate(targets):
        path = os.path.join(input_prefix, target, forcefield, "states12")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]
        fe = wrangle.FEMap(cinnabar_file)
        _x_data = np.asarray([node[1]["exp_DG"] for node in fe.graph.nodes(data=True)])
        _y_data = np.asarray([node[1]["calc_DG"] for node in fe.graph.nodes(data=True)])
        _xerr = np.asarray([node[1]["exp_dDG"] for node in fe.graph.nodes(data=True)])
        _yerr = np.asarray([node[1]["calc_dDG"] for node in fe.graph.nodes(data=True)])

        shift = _x_data.mean()
        _x_data = _x_data - np.mean(_x_data) + shift
        _y_data = _y_data - np.mean(_y_data) + shift

        if i == 0:
            x_data = _x_data
            y_data = _y_data
            xerr = _xerr
            yerr = _yerr
            colors = [list(mycolor_dict.values())[i] for _ in range(len(_x_data))]
            labels += target
        else:
            x_data = np.concatenate((x_data, _x_data), axis=-1)
            y_data = np.concatenate((y_data, _y_data), axis=-1)
            xerr = np.concatenate((xerr, _xerr), axis=-1)
            yerr = np.concatenate((yerr, _yerr), axis=-1)
            colors += [list(mycolor_dict.values())[i] for _ in range(len(_x_data))]
            labels += target

    if figure_extension == "png":
        dpi=600
    else:
        dpi=2400

    from cinnabar.plotting import _master_plot
    _master_plot(
        x_data,
        y_data,
        xerr=xerr,
        yerr=yerr,
        #statistics=["RMSE", "MUE", "R2", "rho"],
        statistics=["RMSE", "MUE"],
        quantity=rf"$\Delta$ G",
        target_name=f'No. of ligands',
        title=f'Absolute binding energies - All',
        figsize=5,
        dpi=dpi,
        color=colors,
        filename=f'./plot_absolute_{forcefield}_custom.{figure_extension}',
        xy_lim=[-14.8, -0.8],
        xy_tick_frequency = 2
    )


def _plot_relative_custom(input_prefix, targets, forcefield, figure_extension):
    """ Plot relative binding free energy calculation for multiple targets.
    """
    # https://github.com/OpenFreeEnergy/cinnabar/blob/0.3.0/cinnabar/plotting.py#L282
    for i, target in enumerate(targets):
        path = os.path.join(input_prefix, target, forcefield, "states12")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]
        fe = wrangle.FEMap(cinnabar_file)
        _x_data = [x[2]["exp_DDG"] for x in fe.graph.edges(data=True)]
        _y_data = [x[2]["calc_DDG"] for x in fe.graph.edges(data=True)]
        _xerr = np.asarray([x[2]["exp_dDDG"] for x in fe.graph.edges(data=True)])
        _yerr = np.asarray([x[2]["calc_dDDG"] for x in fe.graph.edges(data=True)])

        if i == 0:
            x_data = _x_data
            y_data = _y_data
            xerr = _xerr
            yerr = _yerr
            colors = [list(mycolor_dict.values())[i] for _ in range(len(_x_data))]
        else:
            x_data = np.concatenate((x_data, _x_data), axis=-1)
            y_data = np.concatenate((y_data, _y_data), axis=-1)
            xerr = np.concatenate((xerr, _xerr), axis=-1)
            yerr = np.concatenate((yerr, _yerr), axis=-1)
            colors += [list(mycolor_dict.values())[i] for _ in range(len(_x_data))]

    if figure_extension == "png":
        dpi=600
    else:
        dpi=2400

    from cinnabar.plotting import _master_plot
    _master_plot(
        x_data,
        y_data,
        xerr=xerr,
        yerr=yerr,
        statistics=["RMSE", "MUE", "R2", "rho"],
        target_name=f'No. of ligands',
        title=f'Relative binding energies - All',
        figsize=5,
        dpi=dpi,
        color=colors,
        filename=f'./plot_relative_{forcefield}_custom.{figure_extension}',
        xy_lim=[-4.9, 4.9],
        xy_tick_frequency=1
    )


def _plot_dummy_legend(targets, figure_extension):
    """ Create dummy legend figure.
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    for i, target in enumerate(targets):
        ax.scatter(x=[], y =[], s=100, label=target, c=list(mycolor_dict.values())[i])
    ax.legend(loc="upper right", fontsize=20)
    plt.tight_layout()
    if figure_extension == "png":
        dpi=300
    else:
        dpi=2400
    plt.savefig(f"legend.{figure_extension}", dpi=dpi)


def run(kwargs):
    """
    """
    input_prefix = kwargs["input_prefix"]
    targets = kwargs["targets"]
    forcefield = kwargs["forcefield"]
    targets = [ str(_) for _ in targets.split() ]
    
    # Calculate abosolute and relative results for individual target sytem and merge them together 
    figure_extension = "png"
    _plot_absolute_custom(input_prefix, targets, forcefield, figure_extension)
    _plot_relative_custom(input_prefix, targets, forcefield, figure_extension)
    _plot_dummy_legend(targets, figure_extension)

    figure_extension = "svg"
    _plot_absolute_custom(input_prefix, targets, forcefield, figure_extension)
    _plot_relative_custom(input_prefix, targets, forcefield, figure_extension)
    _plot_dummy_legend(targets, figure_extension)


@click.command()
@click.option("--input_prefix", default="..",  help='path to each target system where cinnabar csv files are stored')
@click.option("--targets",      required=True, help='string of target name')
@click.option("--forcefield",  required=True, help='name of the forcefield')
def cli(**kwargs):
    print(kwargs)
    run(kwargs)



if __name__ == "__main__":
    cli()


