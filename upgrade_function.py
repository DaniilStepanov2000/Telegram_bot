import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os


def plot_darker():
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = (first_array * first_array) // 255
    plt.plot(first_array, second_array, '-')
    path = os.path.join(os.getcwd(), 'plot_darker.jpg')
    plt.savefig(path)
    plt.clf()
    return path


def plot_lighter():
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = np.sqrt(first_array * 255)
    plt.plot(first_array, second_array, '-')
    plt.axis([-2, 255, -2, 255])
    path = os.path.join(os.getcwd(), 'plot_lighter.jpg')
    plt.savefig(path)
    plt.clf()
    return path


def plot_negative():
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = first_array * (-1) + 255
    plt.plot(first_array, second_array, '-')
    plt.axis([-2, 255, -2, 255])
    path = os.path.join(os.getcwd(), 'plot_negative.jpg')
    plt.savefig(path)
    plt.clf()
    return path


def plot_sigmoid():
    first_array = np.linspace(0, 255, num=100, endpoint=True)
    second_array = 255 / (1 + np.exp(-(first_array - 128)))
    plt.plot(first_array, second_array, '-')
    path = os.path.join(os.getcwd(), 'plot_sigmoid.jpg')
    plt.savefig(path)
    plt.clf()
    return path


def plot_function(message: str) -> str:
    if message == 'darker':
        return plot_darker()
    if message == 'lighter':
        return plot_lighter()
    if message == 'negative':
        return plot_negative()
    if message == 'sigmoid':
        return plot_sigmoid()


def darker(image: Image.Image) -> str:
    array = np.asarray(image)
    array = np.uint16(array)
    step_one = array * array
    step_two = step_one // 255
    np.putmask(step_two, step_two > 255, 255)
    new_image = Image.fromarray(np.uint8(step_two))
    path = r'C:\Users\dan-s\PycharmProjects\bot\lighter.jpg'
    new_image.save(path)
    return path


def negative(image: Image.Image) -> str:
    array = np.asarray(image)
    array = np.uint16(array)
    step_two = array * (-1) + 255
    np.putmask(step_two, step_two > 255, 255)
    new_image = Image.fromarray(np.uint8(step_two))
    path = r'C:\Users\dan-s\PycharmProjects\bot\liner.jpg'
    new_image.save(path)
    return path


def sigmoid(image: Image.Image) -> str:
    array = np.asarray(image)
    array = np.int64(array)
    step_one = 255 / (1 + np.exp(-(array - 128)))
    np.putmask(step_one, step_one > 255, 255)
    new_image = Image.fromarray(np.uint8(step_one))
    path = r'C:\Users\dan-s\PycharmProjects\bot\sigmoid.jpg'
    new_image.save(path)
    return path


def lighter(image: Image.Image) -> str:
    array = np.asarray(image)
    array = np.uint16(array)
    first_step = array * 255
    second_step = np.sqrt(first_step)
    np.putmask(second_step, second_step > 255, 255)
    new_image = Image.fromarray(np.uint8(second_step))
    path = r'C:\Users\dan-s\PycharmProjects\bot\sigmoid.jpg'
    new_image.save(path)
    return path


def operations(message: str) -> str:
    image = Image.open(r'C:\Users\dan-s\PycharmProjects\bot\laba2_base_photo.jpg')
    if message == 'darker':
        return darker(image)
    if message == 'negative':
        return negative(image)
    if message == 'sigmoid':
        return sigmoid(image)
    if message == 'lighter':
        return lighter(image)
