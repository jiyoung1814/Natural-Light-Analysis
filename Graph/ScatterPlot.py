import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

colors = ['black', 'red', 'blue', 'orange', 'purple', 'gray']


def struct_ampm_scatterplot(X_axis, Y_axis):
    if Y_axis.isdigit():
        Y_axis = 'Spectral Irradiance[W/m^2]'
    if X_axis == 'elevation':
        X_axis = X_axis + "[°]"
    gs = GridSpec(2, 2)
    fig = plt.figure(figsize=(16, 8))
    plt.subplots_adjust(wspace=0.2, hspace=0.5)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlabel(X_axis)
    ax1.set_ylabel(Y_axis)
    plt.title("AM")

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlabel(X_axis)
    ax2.set_ylabel(Y_axis)
    plt.title("PM")

    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_xlabel(X_axis)
    ax3.set_ylabel(Y_axis)

    return plt, ax1, ax2, ax3


def draw_ampm_scatterplot(X_axis, Y_axis, data1, data2, draw_regression=False):
    plt, ax1, ax2, ax3 = struct_ampm_scatterplot(X_axis, Y_axis)

    x_color = 'lightgray'
    y_color = 'gray'
    plot_color = 'black'
    plot_label = '-' # Solid: '-', Dashed: '--', Dotted: ':', Dash-dot: '-.'

    ax1.scatter(f'{X_axis}', f'{Y_axis}', data=data1, color=x_color, s=8, label = 'all')
    ax1.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data1, color=y_color, s=8, label = 'filtered')
    if draw_regression:
        ax1.plot(f'regression_{X_axis}', f'regression_{Y_axis}', plot_label, data=data1, color=plot_color, label = 'regression', linewidth=3)
        # ax1.text(min(data1['filtered_x']), max(data1['filtered_y']), data1['equation'], fontsize=6)
    ax1.legend()
    ax1.set_ylim(0, None)

    ax2.scatter(f'{X_axis}', f'{Y_axis}', data=data2, color=x_color, s=8, label = 'all')
    ax2.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data2, color=y_color, s=8, label = 'filtered')
    if draw_regression:
        ax2.plot(f'regression_{X_axis}', f'regression_{Y_axis}', plot_label, data=data2, color=plot_color, label = 'regression', linewidth=3)
        # ax2.text(min(data2['filtered_x']), max(data2['filtered_y']), data2['equation'], fontsize=6)
    ax2.legend()
    ax2.set_ylim(0, None)
    #
    ax3.scatter(f'{X_axis}', f'{Y_axis}', data=data1, color=x_color, s=8)
    ax3.scatter(f'{X_axis}', f'{Y_axis}', data=data2, color=x_color, s=8)
    ax3.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data1, color=y_color, s=8)
    ax3.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data2, color=y_color, s=8)

    if draw_regression:
        ax3.plot(f'regression_{X_axis}', f'regression_{Y_axis}', plot_label, data=data1, color='red')
        ax3.plot(f'regression_{X_axis}', f'regression_{Y_axis}', plot_label, data=data2, color='blue')
    ax3.set_ylim(0, None)
    # plt.legend()
    plt.show()


def draw_ampm_predict_scatter(X_axis, Y_axis, data1, data2):
    # plt, ax1, ax2, ax3 = struct_ampm_scatterplot(X_axis, Y_axis)
    # ax1.scatter('real_x', 'real_y', data=data1, color='lightgray', s=8)
    # ax1.scatter('real_x', 'predict_y', data=data1, color='red', s=8)
    #
    # ax2.scatter('real_x', 'real_y', data=data2, color='lightgray', s=8)
    # ax2.scatter('real_x', 'predict_y', data=data2, color='red', s=8)
    #
    # ax3.scatter('real_x', 'real_y', data=data1, color='lightgray', s=8)
    # ax3.scatter('real_x', 'real_y', data=data2, color='lightgray', s=8)
    # ax3.scatter('real_x', 'predict_y', data=data1, color='red', s=8)
    # ax3.scatter('real_x', 'predict_y', data=data2, color='blue', s=8)

    plt, ax1, ax2, ax3 = struct_ampm_scatterplot(X_axis, Y_axis)
    ax1.scatter('real_datetime', f'real_{Y_axis}', data=data1, color='lightgray', s=8)
    ax1.scatter('real_datetime', f'predict_{Y_axis}', data=data1, color='red', s=8)

    ax2.scatter('real_datetime', f'real_{Y_axis}', data=data2, color='lightgray', s=8)
    ax2.scatter('real_datetime', f'predict_{Y_axis}', data=data2, color='red', s=8)

    ax3.scatter('real_datetime', f'real_{Y_axis}', data=data1, color='lightgray', s=8)
    ax3.scatter('real_datetime', f'real_{Y_axis}', data=data2, color='lightgray', s=8)
    ax3.scatter('real_datetime', f'predict_{Y_axis}', data=data1, color='red', s=8)
    ax3.scatter('real_datetime', f'predict_{Y_axis}', data=data2, color='blue', s=8)

    plt.show()

def struct_am_noon_pm_scatterplot(X_axis, Y_axis):
    gs = GridSpec(2, 3)
    fig = plt.figure(figsize=(16, 8))
    plt.subplots_adjust(wspace=0.2, hspace=0.5)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlabel(X_axis)
    ax1.set_ylabel(Y_axis)
    ax1.set_title('am')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlabel(X_axis)
    ax2.set_ylabel(Y_axis)
    ax2.set_title('noon')

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_xlabel(X_axis)
    ax3.set_ylabel(Y_axis)
    ax3.set_title('noon')

    ax4 = fig.add_subplot(gs[1, :])
    ax4.set_xlabel(X_axis)
    ax4.set_ylabel(Y_axis)
    ax4.set_title('daily')

    return plt, ax1, ax2, ax3, ax4

def draw_am_noon_pm_scatterplot(X_axis, Y_axis, data1, data2, data3, draw_regression=False):
    plt, ax1, ax2, ax3, ax4= struct_am_noon_pm_scatterplot(X_axis, Y_axis)

    ax1.scatter(X_axis, Y_axis, data=data1, color='lightgray', s=8)
    ax1.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data1, color='red', s=8)
    if draw_regression:
        ax1.plot(f'regression_{X_axis}', f'regression_{Y_axis}', '--', data=data1, color="darkgreen")
        # ax1.text(min(data1['filtered_x']), max(data1['filtered_y']), data1['equation'], fontsize=6)

    ax2.scatter(X_axis, Y_axis, data=data2, color='lightgray', s=8)
    ax2.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data2, color='red', s=8)
    if draw_regression:
        ax2.plot(f'regression_{X_axis}', f'regression_{Y_axis}', '--', data=data2, color="darkgreen")
        # ax2.text(min(data2['filtered_x']), max(data2['filtered_y']), data2['equation'], fontsize=6)

    ax3.scatter(X_axis, Y_axis, data=data3, color='lightgray', s=8)
    ax3.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data3, color='red', s=8)
    if draw_regression:
        ax3.plot(f'regression_{X_axis}', f'regression_{Y_axis}', '--', data=data3, color="darkgreen")
        # ax3.text(min(data3['filtered_x']), max(data3['filtered_y']), data3['equation'], fontsize=6)

    ax4.scatter(X_axis, Y_axis, data=data1, color='lightgray', s=8)
    ax4.scatter(X_axis, Y_axis, data=data2, color='lightgray', s=8)
    ax4.scatter(X_axis, Y_axis, data=data3, color='lightgray', s=8)
    ax4.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data1, color='red', s=8)
    ax4.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data2, color='blue', s=8)
    ax4.scatter(f'filtered_{X_axis}', f'filtered_{Y_axis}', data=data3, color='green', s=8)

    if draw_regression:
        ax4.plot(f'regression_{X_axis}', f'regression_{Y_axis}', '--', data=data1, color="darkred")
        ax4.plot(f'regression_{X_axis}', f'regression_{Y_axis}', '--', data=data2, color="dodgerblue")
        ax4.plot(f'regression_{X_axis}', f'regression_{Y_axis}', '--', data=data3, color="darkgreen")

    # plt.ylim(0, None)
    plt.show()

def draw_am_noon_pm_predict_scatter(X_axis, Y_axis, data1, data2, data3):
    plt, ax1, ax2, ax3, ax4 = struct_am_noon_pm_scatterplot(X_axis, Y_axis)
    ax1.scatter('real_datetime', 'real_y', data=data1, color='lightgray', s=8)
    ax1.scatter('real_datetime', 'predict_y', data=data1, color='red', s=8)

    ax2.scatter('real_datetime', 'real_y', data=data2, color='lightgray', s=8)
    ax2.scatter('real_datetime', 'predict_y', data=data2, color='red', s=8)

    ax3.scatter('real_datetime', 'real_y', data=data3, color='lightgray', s=8)
    ax3.scatter('real_datetime', 'predict_y', data=data3, color='red', s=8)

    ax4.scatter('real_datetime', 'real_y', data=data1, color='lightgray', s=8)
    ax4.scatter('real_datetime', 'real_y', data=data2, color='lightgray', s=8)
    ax4.scatter('real_datetime', 'real_y', data=data3, color='lightgray', s=8)
    ax4.scatter('real_datetime', 'predict_y', data=data1, color='red', s=8)
    ax4.scatter('real_datetime', 'predict_y', data=data2, color='blue', s=8)
    ax4.scatter('real_datetime', 'predict_y', data=data3, color='green', s=8)

    plt.show()


def struct_satellite_scatterplot(X_axis, Y_axis):
    '''

    :param X_axis: str
    :param Y_axis: list[str, str...]
    :return: ax list[ax, ax, ax]
    '''

    if X_axis == 'elevation':
        X_axis = X_axis + "[°]"
    gs = GridSpec(2, int(len(Y_axis)/2))
    fig = plt.figure(figsize=(16, 9))
    plt.subplots_adjust(wspace=0.4, hspace=0.5)

    ax = []
    for i in range(len(Y_axis)):
        if i < len(Y_axis)/2:
            ax.append(fig.add_subplot(gs[0, int(i % (len(Y_axis)/2))]))
        else:
            ax.append(fig.add_subplot(gs[1, int(i % (len(Y_axis) / 2))]))

        ax[i].set_xlabel(X_axis)

        if Y_axis[i] in ['gkb01_kc','gkb02_kc','gkb03_kc','gkb04_kc','gkb05_kc','gkb06_kc']:
            ax[i].set_ylabel(Y_axis[i]+"Radiance[W/m2srμm]")
        elif Y_axis[i] in ['gkb07_kc','gkb08_kc','gkb09_kc','gkb10_kc','gkb11_kc','gkb12_kc','gkb13_kc','gkb14_kc','gkb15_kc','gkb16_kc']:
            ax[i].set_ylabel(Y_axis[i] + "Radiance[mW/m^2/sr/cm^-1]")
        elif Y_axis[i] == 'lux':
            ax[i].set_ylabel("Illuminance[lux]")

    return plt, ax

def draw_satellite_scatterplot(X_axis, Y_axis, data):
    '''
    :param X_axis: str (ex elevation)
    :param Y_axis: list[filter_y, filter_y, filter_y,]
    :param data: dict{ percentage: [{DayData dic}, {}..]}
    :return:
    '''
    plt, ax = struct_satellite_scatterplot(X_axis, Y_axis)
    colors = ['red', 'coral', 'orange', 'gold', 'yellow', 'lightgreen', 'green', 'skyblue', 'blue', 'purple']

    for i, y_axis in enumerate(Y_axis):
        for p, d in data.items():
            ax[i].scatter([x[X_axis] for x in d], [y[y_axis] for y in d], label = f'{p}~{p+10}%', color = colors[int(p/10)])
        ax[i].legend()
        # ax[i].set_ylim(0, None)

    plt.show()


