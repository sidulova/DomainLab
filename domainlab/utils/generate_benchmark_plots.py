'''
generate the benchmark plots by calling the gen_bencmark_plots(...) function
'''
import os
from ast import literal_eval   # literal_eval can safe evaluate python expression
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns
import numpy as np

matplotlib.use('Agg')

COLNAME_ALGO = "algo"
COLNAME_PARAM = "params"


def gen_benchmark_plots(agg_results: str, output_dir: str):
    '''
    generate the benchmark plots from a csv file containing the aggregated restults.
    The csv file must have the columns:
    [param_index, task, algo, epos, te_d, seed, params, ...]
    all columns after seed are intrepreted as objectives of the results, they can e.g.
    be acc, precision, recall, specificity, f1, auroc.

    agg_results: path to the csv file
    output_dir: path to a folder which shall contain the results
    '''
    raw_df = pd.read_csv(agg_results, index_col=False,
                         converters={COLNAME_PARAM: literal_eval},
                         # literal_eval can safe evaluate python expression
                         skipinitialspace=True)
    raw_df[COLNAME_PARAM] = round_vals_in_dict(raw_df[COLNAME_PARAM])
    # crop param_index and task from the dataframe
    dataframe = raw_df.iloc[:, 2:]  # @FIXME: hard coded
    # generating plot
    gen_plots(dataframe, output_dir)


def round_vals_in_dict(df_column_in):
    '''
    replaces the dictionary by a string containing only the significant digits of the hyperparams
    df_column_in: columns of the dataframe containing the dictionary of hyperparams
    '''
    df_column = df_column_in.copy()
    df_column_out = df_column_in.copy()
    for i in range(df_column.shape[0]):
        string = ''
        for num, val in enumerate(list(df_column[i].values())):
            key = list(df_column[i].keys())[num]
            val = np.format_float_scientific(val, precision=1, unique=False, trim='0')
            string += str(key) + ': ' + str(val) + ', '
        df_column_out[i] = string[:-2]
    return df_column_out


def gen_plots(dataframe: pd.DataFrame, output_dir: str):
    '''
    dataframe: dataframe with columns
    [' algo', ' epos', ' te_d', ' seed', ' params', ' acc', ' precision', ... ]
    '''
    os.makedirs(output_dir, exist_ok=True)
    # scatterplot matrices
    scatterplot_matrix(dataframe, file=output_dir + '/sp_matrix_reg.png',
                       reg=True, distinguish_param_setups=False)
    scatterplot_matrix(dataframe, file=output_dir + '/sp_matrix.png',
                       reg=False, distinguish_param_setups=False)
    scatterplot_matrix(dataframe, file=output_dir + '/sp_matrix_dist_reg.png',
                       reg=True, distinguish_param_setups=True)
    scatterplot_matrix(dataframe, file=output_dir + '/sp_matrix_dist.png',
                       reg=False, distinguish_param_setups=True)

    # radar plots
    radar_plot(dataframe, file=output_dir + '/radar_dist.png', distinguish_hyperparam=True)
    radar_plot(dataframe, file=output_dir + '/radar.png', distinguish_hyperparam=False)

    # scatter plots for parirs of objectives
    os.makedirs(output_dir + '/scatterpl', exist_ok=True)
    obj = dataframe.columns[5:]
    for i, obj_i in enumerate(obj):
        for j in range(i+1, len(obj)):
            try:
                scatterplot(dataframe, [obj_i, obj[j]],
                            file=output_dir + '/scatterpl/' + obj_i + '_' + obj[j] + '.png')
            except IndexError:
                print(f'WARNING: disabling kde because cov matrix is singular for objectives '
                      f'{obj_i} & {obj[j]}')
                scatterplot(dataframe, [obj_i, obj[j]],
                            file=output_dir + '/scatterpl/' + obj_i + '_' + obj[j] + '.png',
                            kde=False)

    # create plots for the different algortihms
    for algorithm in dataframe[COLNAME_ALGO].unique():
        os.makedirs(output_dir + '/' + str(algorithm), exist_ok=True)
        dataframe_algo = dataframe[dataframe[COLNAME_ALGO] == algorithm]

        # scatterplot matrices
        scatterplot_matrix(dataframe_algo,
                           file=output_dir + '/' + str(algorithm) + '/sp_matrix_reg.png',
                           reg=True, distinguish_param_setups=False)
        scatterplot_matrix(dataframe_algo,
                           file=output_dir + '/' + str(algorithm) + '/sp_matrix.png',
                           reg=False, distinguish_param_setups=False)
        scatterplot_matrix(dataframe_algo,
                           file=output_dir + '/' + str(algorithm) + '/sp_matrix_dist_reg.png',
                           reg=True, distinguish_param_setups=True)
        scatterplot_matrix(dataframe_algo,
                           file=output_dir + '/' + str(algorithm) + '/sp_matrix_dist.png',
                           reg=False, distinguish_param_setups=True)

        # radar plots
        radar_plot(dataframe_algo, file=output_dir + '/' + str(algorithm) + '/radar_dist.png',
                   distinguish_hyperparam=True)
        radar_plot(dataframe_algo, file=output_dir + '/' + str(algorithm) + '/radar.png',
                   distinguish_hyperparam=False)

        # scatter plots for parirs of objectives
        os.makedirs(output_dir + '/' + str(algorithm) + '/scatterpl', exist_ok=True)
        obj = dataframe_algo.columns[5:]
        for i, obj_i in enumerate(obj):
            for j in range(i + 1, len(obj)):
                try:
                    scatterplot(dataframe_algo, [obj_i, obj[j]],
                                file=output_dir + '/' + str(algorithm) +
                                '/scatterpl/' + obj_i + '_' + obj[j] + '.png',
                                distinguish_hyperparam=True)
                except IndexError:
                    print(f'WARNING: disabling kde because cov matrix is singular for objectives '
                          f'{obj_i} & {obj[j]}')
                    scatterplot(dataframe_algo, [obj_i, obj[j]],
                                file=output_dir + '/' + str(algorithm) +
                                '/scatterpl/' + obj_i + '_' + obj[j] + '.png',
                                kde=False,
                                distinguish_hyperparam=True)


def scatterplot_matrix(dataframe_in, file=None, reg=True, distinguish_param_setups=True):
    '''
    dataframe: dataframe containing the data with columns
        [algo, epos, te_d, seed, params, obj1, ..., obj2]
    file: filename to save the plots (if None, the plot will not be saved)
    reg: if True a regression line will be plotted over the data
    distinguish_param_setups: if True the plot will not only distinguish between models,
        but also between the parameter setups
    '''
    dataframe = dataframe_in.copy()
    index = list(range(5, dataframe.shape[1]))
    if distinguish_param_setups:
        dataframe_ = dataframe.iloc[:, index]
        dataframe_.insert(0, 'label',
                          dataframe[COLNAME_ALGO].astype(str) + ', ' +
                          dataframe[COLNAME_PARAM].astype(str))
    else:
        index_ = list(range(5, dataframe.shape[1]))
        index_.insert(0, 0)
        dataframe_ = dataframe.iloc[:, index_]

    if reg:
        if not distinguish_param_setups:
            g_p = sns.pairplot(data=dataframe_, hue=COLNAME_ALGO, corner=True, kind='reg')
        else:
            g_p = sns.pairplot(data=dataframe_, hue='label', corner=True, kind='reg')
    else:
        if not distinguish_param_setups:
            g_p = sns.pairplot(data=dataframe_, hue=COLNAME_ALGO, corner=True)
        else:
            g_p = sns.pairplot(data=dataframe_, hue='label', corner=True)

    for i in range(len(index)):
        for j in range(len(index)):
            if i >= j:
                g_p.axes[i, j].set_xlim((-0.1, 1.1))
                for k in range(j):
                    g_p.axes[j, k].set_ylim((-0.1, 1.1))

    g_p.fig.set_size_inches(12.5, 12)
    sns.move_legend(g_p, loc='upper right', bbox_to_anchor=(1., 1.), ncol=1)
    plt.tight_layout()

    if file is not None:
        plt.savefig(file, dpi=300)


def scatterplot(dataframe_in, obj, file=None, kde=True, distinguish_hyperparam=False):
    '''
    dataframe: dataframe containing the data with columns
        [algo, epos, te_d, seed, params, obj1, ..., obj2]
    obj1 & obj2: name of the objectives which shall be plotted against each other
    file: filename to save the plots (if None, the plot will not be saved)
    kde: if True the distribution of the points will be estimated and plotted as kde plot
    distinguish_param_setups: if True the plot will not only distinguish between models,
        but also between the parameter setups
    '''
    obj1, obj2 = obj

    dataframe = dataframe_in.copy()
    dataframe[COLNAME_PARAM] = dataframe[COLNAME_PARAM].astype(str)

    if distinguish_hyperparam:
        if kde:
            g_p = sns.jointplot(data=dataframe, x=obj1, y=obj2, hue=COLNAME_PARAM,
                                xlim=(-0.1, 1.1), ylim=(-0.1, 1.1), kind='kde',
                                zorder=0, levels=8, alpha=0.35, warn_singular=False)
            gg_p = sns.scatterplot(data=dataframe, x=obj1, y=obj2, hue=COLNAME_PARAM,
                                   ax=g_p.ax_joint)
        else:
            g_p = sns.jointplot(data=dataframe, x=obj1, y=obj2, hue=COLNAME_PARAM,
                                xlim=(-0.1, 1.1), ylim=(-0.1, 1.1))
            gg_p = g_p.ax_joint
    else:
        if kde:
            g_p = sns.jointplot(data=dataframe, x=obj1, y=obj2, hue=COLNAME_ALGO,
                                xlim=(-0.1, 1.1), ylim=(-0.1, 1.1), kind='kde',
                                zorder=0, levels=8, alpha=0.35, warn_singular=False)
            gg_p = sns.scatterplot(data=dataframe, x=obj1, y=obj2, hue=COLNAME_ALGO,
                                   style=COLNAME_PARAM,
                                   ax=g_p.ax_joint)
        else:
            g_p = sns.jointplot(data=dataframe, x=obj1, y=obj2, hue=COLNAME_ALGO,
                                xlim=(-0.1, 1.1), ylim=(-0.1, 1.1))
            gg_p = sns.scatterplot(data=dataframe, x=obj1, y=obj2, style=COLNAME_PARAM,
                                   ax=g_p.ax_joint)

    gg_p.set_aspect('equal')
    gg_p.legend(fontsize=6, loc='best')

    if file is not None:
        plt.savefig(file, dpi=300)


def max_0_x(x_arg):
    '''
    max(0, x_arg)
    '''
    return max(0, x_arg)


def radar_plot(dataframe_in, file=None, distinguish_hyperparam=True):
    '''
    dataframe_in: dataframe containing the data with columns
        [algo, epos, te_d, seed, params, obj1, ..., obj2]
    file: filename to save the plots (if None, the plot will not be saved)
    distinguish_param_setups: if True the plot will not only distinguish between models,
        but also between the parameter setups
    '''
    dataframe = dataframe_in.copy()
    if distinguish_hyperparam:
        dataframe.insert(0, 'label',
                         dataframe[COLNAME_ALGO].astype(str) + ', ' +
                         dataframe[COLNAME_PARAM].astype(str))
    else:
        dataframe.insert(0, 'label', dataframe[COLNAME_ALGO])
    index = list(range(6, dataframe.shape[1]))
    num_lines = len(dataframe['label'].unique())
    _, axis = plt.subplots(figsize=(9, 9 + (0.28 * num_lines)), subplot_kw=dict(polar=True))
    num = 0

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = list(np.linspace(0, 2 * np.pi, len(dataframe.columns[index]), endpoint=False))
    for algo_name in dataframe['label'].unique():
        mean = dataframe.loc[dataframe['label'] == algo_name].iloc[:, index].mean().to_list()
        std = dataframe.loc[dataframe['label'] == algo_name].iloc[:, index].std().to_list()

        angles_ = angles
        # The plot is a circle, so we need to "complete the loop"
        # and append the start value to the end.
        mean = np.array(mean + mean[:1])
        std = np.array(std + std[:1])
        angles_ = np.array(angles_ + angles_[:1])

        # Draw the outline of the data.
        axis.plot(angles_, mean,
                  color=list(plt.rcParams["axes.prop_cycle"])[num]['color'],
                  linewidth=2, label=algo_name)

        # Fill it in.
        axis.fill_between(angles_, list(map(max_0_x, mean - std)),
                          y2=mean + std,
                          color=list(plt.rcParams["axes.prop_cycle"])[num]['color'],
                          alpha=0.1)
        num += 1
        num = num % len(list(plt.rcParams["axes.prop_cycle"]))

    # Fix axis to go in the right order and start at 12 o'clock.
    axis.set_theta_offset(np.pi / 2)
    axis.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    axis.set_thetagrids(np.degrees(angles), dataframe.columns[index])

    axis.set_ylim((0, 1))

    plt.legend(loc='lower right', bbox_to_anchor=(1., 1.035),
               ncol=1, fontsize=10)

    if file is not None:
        plt.savefig(file, dpi=300)