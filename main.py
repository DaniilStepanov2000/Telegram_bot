import logging
import pathlib

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


from operations import get_way, get_max_sized_photo


class First(StatesGroup):
    lab_one_step_one = State()
    lab_one_step_two = State()
    lab_one_step_three = State()
    lab_one_step_four = State()


class Second(StatesGroup):
    lab_second_step_one = State()
    lab_second_step_two = State()
    lab_second_step_three = State()


API_TOKEN = '1459813755:AAEIBDuZzJ6K0Ju2EAM77kbwdEfAHxR090g'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())  # сообщения от бота


@dp.message_handler(commands=['start', 'help'], state=None)
async def main_send_welcome(message: types.Message):
    await message.answer("Choose one of the commands: /first_lab or /second_lab")


@dp.message_handler(commands=['second_lab'], state=None)
async def second_send_welcome(message: types.Message):
    await message.answer("Enter the picture:")
    await Second.lab_second_step_one.set()


@dp.message_handler(content_types='photo', state=Second.lab_second_step_one)
async def second_send_welcome(message: types.Message, state: FSMContext):
    photo = get_max_sized_photo(message.photo)
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    photo_name = 'laba2_base_photo.jpg'
    path_in_computer = r'C:\Users\dan-s\PycharmProjects\bot\laba2_base_photo.jpg'
    await state.update_data(base_image=path_in_computer)
    await bot.download_file(file_path, path_in_computer)

    paths = create_histogram(path_in_computer)

    string_message = message.as_json()
    norm_message = json.loads(string_message)

    chat_id = norm_message["chat"]["id"]

    media = create_media(paths)

    await message.answer_media_group(media=media)

    key_board = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton('darker')
    second_button = KeyboardButton('negative')
    third_button = KeyboardButton('sigmoid')
    four_button = KeyboardButton('lighter')
    key_board.row(first_button, second_button, third_button, four_button)

    await message.answer('Choose on of the operations:', reply_markup=key_board)
    await Second.lab_second_step_two.set()


@dp.message_handler(content_types='text', state=Second.lab_second_step_two)
async def update_photos(message: types.Message, state: FSMContext):
    path = operations(message.text)
    open_photo = open(path, 'rb')

    string_message = message.as_json()
    norm_message = json.loads(string_message)

    chat_id = norm_message["chat"]["id"]
    plot_path = plot_function(message.text)

    await message.reply('Ok', reply_markup=ReplyKeyboardRemove())

    open_plot_photo = open(plot_path, 'rb')
    await bot.send_photo(chat_id, open_plot_photo, caption=f'{message.text} function')

    await bot.send_photo(chat_id, open_photo)

    paths = create_histogram(path)

    media = create_media(paths)
    await message.answer_media_group(media=media)

    await message.answer("Let's make some interpolation, enter the coordinates in range from 0 to 255:")
    await Second.lab_second_step_three.set()


@dp.message_handler(content_types='text', state=Second.lab_second_step_three)
async def make_interpolation(message: types.Message, state: FSMContext):
    result = await state.get_data()
    image_path = result["base_image"]
    path_points, path_plot, inter_path = begin_draw_plots(message.text, image_path)
    message_string = message.as_json()
    norm_message = json.loads(message_string)
    chat_id = norm_message["chat"]["id"]
    file_points = open(path_points, 'rb')
    file_plot = open(path_plot, 'rb')
    file_inter_pict = open(inter_path, 'rb')

    await bot.send_photo(chat_id, file_points, caption='Your points')
    await bot.send_photo(chat_id, file_plot, caption='Your interpolation')
    await bot.send_photo(chat_id, file_inter_pict, caption='Your interpolate image')

    paths = create_histogram(inter_path)
    media = create_media(paths)
    await message.answer_media_group(media=media)

    await state.finish()
    await message.answer("Enter /start to begin again")


@dp.message_handler(commands=['first_lab'], state=None)
async def first_send_welcome(message: types.Message):
    await message.answer("Enter the first picture:\n")

    # Задаем новое состояние, то есть теперь, когда пользователь будет
    # отвечать на вопрос мы будем считать это как ответ на этот вопрос



@dp.message_handler(content_types='photo', state=First.lab_one_step_one)
async def answer_q1(message: types.Message, state: FSMContext):
    # answer_1 = message.text
    # получение json() ввиде строки
    # получение json, что бы обращаться по индексу к ниму
    # получение photo_id, фото, которое отправиль пользователь
    photo = get_max_sized_photo(message.photo)
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    first_name = "first_picture.jpg"
    path_in_computer = r'C:\Users\dan-s\PycharmProjects\bot\first_picture.jpg'

    print(file)
    print(file_path)
    # сохранение картинки по пути
    await bot.download_file(file_path, path_in_computer)

    # сохраняю ответ, полученный от пользователя
    await state.update_data(first_name=first_name)

    await message.answer("Enter the second picture:\n")

    # объявляю новое состояние
    await First.lab_one_step_two.set()


@dp.message_handler(content_types='photo', state=First.lab_one_step_two)
async def answer_q2(message: types.Message, state: FSMContext):
    # получение json, что бы обращаться по индексу к ниму
    # получение photo_id, фото, которое отправиль пользователь
    photo = get_max_sized_photo(message.photo)
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    second_name = "second_picture.jpg"
    path_in_computer = r'C:\Users\dan-s\PycharmProjects\bot\second_picture.jpg'

    print(file)
    print(file_path)
    # сохранение картинки по пути
    await bot.download_file(file_path, path_in_computer)

    await state.update_data(second_name=second_name)

    new_key_board = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text="RGB")
    second_button = KeyboardButton(text="R")
    third_button = KeyboardButton(text="G")
    four_button = KeyboardButton(text="B")
    five_button = KeyboardButton(text="RG")
    six_button = KeyboardButton(text="RB")
    seven_button = KeyboardButton(text="GB")

    new_key_board.row(first_button)
    new_key_board.row(second_button, third_button, four_button)
    new_key_board.row(five_button, six_button, seven_button)

    await message.answer(text="Choose the channel to work:", reply_markup=new_key_board)

    await First.lab_one_step_three.set()


@dp.message_handler(content_types='text', state=First.lab_one_step_three)
async def new_command(message: types.Message, state: FSMContext):
    await state.update_data(channel_name=message.text)
    await message.reply(text="Ok", reply_markup=ReplyKeyboardRemove())

    key_board = ReplyKeyboardMarkup(resize_keyboard=True)

    first_button = KeyboardButton(text="SUM")
    second_button = KeyboardButton(text="AVER")
    third_button = KeyboardButton(text="MAX")
    four_button = KeyboardButton(text="MIN")
    five_button = KeyboardButton(text="CIRCLE MASK")
    six_button = KeyboardButton(text="SQUARE MASK")
    seven_button = KeyboardButton(text="RECTANGLE MASK")

    key_board.row(first_button, second_button)
    key_board.row(third_button, four_button)
    key_board.row(five_button, six_button, seven_button)

    await message.answer(text="Choose:", reply_markup=key_board)

    await First.lab_one_step_four.set()


@dp.message_handler(content_types='text', state=First.lab_one_step_four)
async def command(message: types.Message, state: FSMContext):
    result = await state.get_data()
    rgb_message = result['channel_name']

    path = get_way(message.text, rgb_message)  # возвращает путь, куда сохранилась картинка
    string_message = message.as_json()
    norm_message = json.loads(string_message)

    chat_id = norm_message["chat"]["id"]

    file = open(path, 'rb')

    await bot.send_photo(chat_id, file)

    await message.answer(f"It is {message.text}, enter /start to begin again", reply_markup=ReplyKeyboardRemove())
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
