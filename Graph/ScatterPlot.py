import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

colors = ['black', 'red', 'blue', 'orange', 'purple', 'gray']


# def draw_scatterplot(x1, y1, y1_label='y1', X_axis='X Axis', Y_axis='Y Axis', x2=None, y2=None, y2_label='y2',
#                      secondary_axis=False, Y2_axis='Y2 Axis'):
#     fig, ax = plt.subplots()
#
#     ax.scatter(x1, y1, label=y1_label, color=colors[0])
#
#     ax.set_xlabel(X_axis)
#     ax.set_ylabel(Y_axis)
#
#     if y2 is not None:
#         if secondary_axis:
#             ax2 = ax.twinx()
#             ax2.set_ylabel(Y2_axis)
#         else:
#             ax2 = ax
#
#         ax2.scatter(x2, y2, label=y2_label, color=colors[1])
#
#     # plt.legend()
#
#     plt.show()


def struct_ampm_scatterplot(X_axis, Y_axis):
    gs = GridSpec(2, 2)
    fig = plt.figure(figsize=(16, 8))
    plt.subplots_adjust(wspace=0.2, hspace=0.5)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlabel(X_axis)
    ax1.set_ylabel(Y_axis)
    ax1.set_title('am')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlabel(X_axis)
    ax2.set_ylabel(Y_axis)
    ax2.set_title('pm')

    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_xlabel(X_axis)
    ax3.set_ylabel(Y_axis)
    ax3.set_title('daily')

    return plt, ax1, ax2, ax3


def draw_ampm_scatterplot(X_axis, Y_axis, data1, data2, draw_regression=False):
    plt, ax1, ax2, ax3 = struct_ampm_scatterplot(X_axis, Y_axis)

    ax1.scatter('x', 'y', data=data1, color='lightgray', s=8)
    ax1.scatter('filtered_x', 'filtered_y', data=data1, color='red', s=8)
    if draw_regression:
        ax1.plot('x_values', 'y_predict', '--', data=data1, color="darkgreen")
        ax1.text(min(data1['filtered_x']), max(data1['filtered_y']), data1['equation'], fontsize=6)

    ax2.scatter('x', 'y', data=data2, color='lightgray', s=8)
    ax2.scatter('filtered_x', 'filtered_y', data=data2, color='red', s=8)
    if draw_regression:
        ax2.plot('x_values', 'y_predict', '--', data=data2, color="darkgreen")
        ax2.text(min(data2['filtered_x']), max(data2['filtered_y']), data2['equation'], fontsize=6)

    ax3.scatter('x', 'y', data=data1, color='lightgray', s=8)
    ax3.scatter('x', 'y', data=data2, color='lightgray', s=8)
    ax3.scatter('filtered_x', 'filtered_y', data=data1, color='red', s=8)
    ax3.scatter('filtered_x', 'filtered_y', data=data2, color='blue', s=8)

    if draw_regression:
        ax3.plot('x_values', 'y_predict', '--', data=data1, color="darkgreen")
        ax3.plot('x_values', 'y_predict', '--', data=data2, color="dodgerblue")

    # plt.ylim(0, None)
    plt.show()


# def draw_ampm_regression_scatterplot(data1, data2, X_axis='X_axis', Y_axis='Y_axis'):
#     fig = plt.figure(figsize=(16, 8))
#
#     plt.scatter('x', 'y', data=data1, color='lightgray', s=8)
#     plt.scatter('x', 'y', data=data2, color='lightgray', s=8)
#     plt.scatter('filtered_x', 'filtered_y', data=data1, color='red', s=8)
#     plt.scatter('filtered_x', 'filtered_y', data=data2, color='blue', s=8)
#     plt.plot('x_values', 'y_predict', '--', data=data1, color="darkgreen")
#     plt.plot('x_values', 'y_predict', '--', data=data2, color="dodgerblue")
#
#     plt.xlabel(X_axis)
#     plt.ylabel(Y_axis)
#
#     plt.show()

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
    ax1.scatter('real_datetime', 'real_y', data=data1, color='lightgray', s=8)
    ax1.scatter('real_datetime', 'predict_y', data=data1, color='red', s=8)

    ax2.scatter('real_datetime', 'real_y', data=data2, color='lightgray', s=8)
    ax2.scatter('real_datetime', 'predict_y', data=data2, color='red', s=8)

    ax3.scatter('real_datetime', 'real_y', data=data1, color='lightgray', s=8)
    ax3.scatter('real_datetime', 'real_y', data=data2, color='lightgray', s=8)
    ax3.scatter('real_datetime', 'predict_y', data=data1, color='red', s=8)
    ax3.scatter('real_datetime', 'predict_y', data=data2, color='blue', s=8)

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

    ax1.scatter('x', 'y', data=data1, color='lightgray', s=8)
    ax1.scatter('filtered_x', 'filtered_y', data=data1, color='red', s=8)
    if draw_regression:
        ax1.plot('x_values', 'y_predict', '--', data=data1, color="darkgreen")
        ax1.text(min(data1['filtered_x']), max(data1['filtered_y']), data1['equation'], fontsize=6)

    ax2.scatter('x', 'y', data=data2, color='lightgray', s=8)
    ax2.scatter('filtered_x', 'filtered_y', data=data2, color='red', s=8)
    if draw_regression:
        ax2.plot('x_values', 'y_predict', '--', data=data2, color="darkgreen")
        ax2.text(min(data2['filtered_x']), max(data2['filtered_y']), data2['equation'], fontsize=6)

    ax3.scatter('x', 'y', data=data3, color='lightgray', s=8)
    ax3.scatter('filtered_x', 'filtered_y', data=data3, color='red', s=8)
    if draw_regression:
        ax3.plot('x_values', 'y_predict', '--', data=data3, color="darkgreen")
        ax3.text(min(data3['filtered_x']), max(data3['filtered_y']), data3['equation'], fontsize=6)

    ax4.scatter('x', 'y', data=data1, color='lightgray', s=8)
    ax4.scatter('x', 'y', data=data2, color='lightgray', s=8)
    ax4.scatter('x', 'y', data=data3, color='lightgray', s=8)
    ax4.scatter('filtered_x', 'filtered_y', data=data1, color='red', s=8)
    ax4.scatter('filtered_x', 'filtered_y', data=data2, color='blue', s=8)
    ax4.scatter('filtered_x', 'filtered_y', data=data3, color='green', s=8)

    if draw_regression:
        ax4.plot('x_values', 'y_predict', '--', data=data1, color="darkred")
        ax4.plot('x_values', 'y_predict', '--', data=data2, color="dodgerblue")
        ax4.plot('x_values', 'y_predict', '--', data=data3, color="darkgreen")

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
