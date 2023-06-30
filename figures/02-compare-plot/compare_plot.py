"""
Compare first and second trial of Perses benchmark.
Intended to be used for data extracted from https://github.com/kntkb/protein-ligand-benchmark-custom.
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


def _plot_absolute_custom(input_prefix, targets, forcefield, figure_extension):
    """ Plot predicted binding absolute free energy difference among two different trials.
    """
    # https://github.com/OpenFreeEnergy/cinnabar/blob/0.3.0/cinnabar/plotting.py#L414
    labels = []
    for i, target in enumerate(targets):
        # First trial
        path = os.path.join(input_prefix, target, forcefield, "states12")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]     
        fe = wrangle.FEMap(cinnabar_file)
        exp_data = np.asarray([node[1]["exp_DG"] for node in fe.graph.nodes(data=True)])
        _x_data = np.asarray([node[1]["calc_DG"] for node in fe.graph.nodes(data=True)])
        _xerr = np.asarray([node[1]["calc_dDG"] for node in fe.graph.nodes(data=True)])
        shift = exp_data.mean()
        _x_data = _x_data - np.mean(_x_data) + shift
        del path, cinnabar_file, fe, exp_data

        # Second trial
        path = os.path.join(input_prefix, target, forcefield, "states12-2")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]     
        fe = wrangle.FEMap(cinnabar_file)
        exp_data = np.asarray([node[1]["exp_DG"] for node in fe.graph.nodes(data=True)])
        _y_data = np.asarray([node[1]["calc_DG"] for node in fe.graph.nodes(data=True)])
        _yerr = np.asarray([node[1]["calc_dDG"] for node in fe.graph.nodes(data=True)])
        shift = exp_data.mean()
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
        xlabel='Calculated(1)',
        ylabel='Calculated(2)',
        #statistics=["RMSE", "MUE", "R2", "rho"],
        statistics=["RMSE", "MUE"],
        quantity=rf"$\Delta$ G",
        target_name=f'No. of ligands',
        title=f'Absolute binding energies - All',
        figsize=5,
        dpi=dpi,
        color=colors,
        filename=f'./plot_absolute_{forcefield}_custom.{figure_extension}',
        xy_lim=[-13.9, -0.5],
        xy_tick_frequency=2,
    )


def _plot_relative_custom(input_prefix, targets, forcefield, figure_extension):
    """ Plot predicted relative binding free energy difference among two different trials.
    """
    # https://github.com/OpenFreeEnergy/cinnabar/blob/0.3.0/cinnabar/plotting.py#L282
    for i, target in enumerate(targets):

        # First trial
        path = os.path.join(input_prefix, target, forcefield, "states12")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]     
        fe = wrangle.FEMap(cinnabar_file)
        _x_data = [x[2]["calc_DDG"] for x in fe.graph.edges(data=True)]
        _xerr = np.asarray([x[2]["calc_dDDG"] for x in fe.graph.edges(data=True)])
        del path, cinnabar_file, fe

        # Second trial
        path = os.path.join(input_prefix, target, forcefield, "states12-2")
        cinnabar_file = glob.glob(path + "/cinnabar*.csv")[0]     
        fe = wrangle.FEMap(cinnabar_file)
        _y_data = [x[2]["calc_DDG"] for x in fe.graph.edges(data=True)]
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
        xlabel='Calculated(1)',
        ylabel='Calculated(2)',
        statistics=["RMSE", "MUE", "R2", "rho"],
        target_name=f'No. of ligands',
        title=f'Relative binding energies - All',
        figsize=5,
        dpi=dpi,
        color=colors,
        filename=f'./plot_relative_{forcefield}_custom.{figure_extension}',
        xy_lim=[-5.1, 5.1],
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

    # Calculate abosolute values for individual target sytem and merge them together 
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


