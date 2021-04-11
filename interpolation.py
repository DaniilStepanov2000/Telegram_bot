import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from PIL import Image


def get_inter_image(image_path: str, inter_func: interp1d) -> str:
    image = Image.open(image_path)
    array = np.uint16(np.asarray(image))
    temp = inter_func(array)
    np.putmask(temp, temp > 255, 255)
    new_image = Image.fromarray(np.uint8(temp))
    path = r'C:\Users\dan-s\PycharmProjects\bot\f_inter.jpg'
    new_image.save(r'C:\Users\dan-s\PycharmProjects\bot\f_inter.jpg')
    return path


def get_interpolation(x_list: list, y_list: list) -> (str, str):
    x = np.asarray(x_list)
    y = np.asarray(y_list)
    f = interp1d(x, y)
    # plt.plot(x, y, 'o', x, f(x), '-')
    plt.plot(x, y, 'o')
    plt.axis([-2, 257, -2, 257])
    path_points = r'C:\Users\dan-s\PycharmProjects\bot\points.jpg'
    plt.savefig(path_points)
    path_plot = r'C:\Users\dan-s\PycharmProjects\bot\plot.jpg'
    plt.plot(x, y, 'o', x, f(x), '-')
    plt.savefig(path_plot)
    plt.clf()
    return path_points, path_plot, f


def separate_coordinates(test_list: list) -> (list, list):
    new_coordinates = list(map(int, test_list))
    test_x_coordinates = []
    test_y_coordinates = []
    for i in range(len(new_coordinates)):
        if i % 2 == 0:
            test_x_coordinates.append(new_coordinates[i])
        else:
            test_y_coordinates.append(new_coordinates[i])
    return test_x_coordinates, test_y_coordinates


def convert_string(string: str) -> list:
    list_string = list(string.split(" "))
    return list_string


def begin_draw_plots(string: str, image_path: str) -> (str, str, str):
    list_string = convert_string(string)
    x_cor, y_cor = separate_coordinates(list_string)
    points_path, plot_path, inter_f = get_interpolation(x_cor, y_cor)
    inter_path_picture = get_inter_image(image_path, inter_f)

    return points_path, plot_path, inter_path_picture
