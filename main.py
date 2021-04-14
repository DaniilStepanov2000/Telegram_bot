import logging
import pathlib

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from gradation_transformations.histogram_functions import create_histogram
from gradation_transformations.interpolation import begin_draw_plots
from gradation_transformations.media_group import create_media
from work_with_images.operations import process_operation, get_max_sized_photo
from gradation_transformations.upgrade_function import operations
from gradation_transformations.upgrade_function import plot_function
from config import Settings


class First(StatesGroup):
    work_with_images_one = State()
    work_with_images_two = State()
    work_with_images_three = State()
    work_with_images_four = State()


class Second(StatesGroup):
    gradation_transformations_one = State()
    gradation_transformations_two = State()
    gradation_transformations_three = State()


settings = Settings.from_json(pathlib.Path('./config.json'))
bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(format="%(asctime)s %(name)s[%(levelname)s]: %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)


@dp.message_handler(commands=['start', 'help'], state=None)
async def main_send_welcome(message: types.Message):
    """Process start and help command.

    Args:
        message: Message from telegram update.
    """
    await message.answer("Choose one of the commands: \n1. /work_with_images \n2. /gradation_transformations")


@dp.message_handler(commands=['gradation_transformations'], state=None)
async def second_send_welcome(message: types.Message):
    await message.answer("Enter the picture:")
    await Second.gradation_transformations_one.set()


@dp.message_handler(content_types='photo', state=Second.gradation_transformations_one)
async def second_send_welcome(message: types.Message, state: FSMContext):
    """"Read photo from telegram server and choose operations to do on photo.

    Args:
        message: Message from telegram update.
        state: State from Finite State Machine.
    """
    photo = get_max_sized_photo(message.photo)
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    photo_path = settings.project_static_path / f'{message.from_user.id}_2_lab_base_photo.jpg'

    await state.update_data(base_image=photo_path)
    await bot.download_file(file_path, photo_path)

    paths = create_histogram(str(photo_path), settings, message.from_user.id)

    media = create_media(paths)

    await message.answer_media_group(media=media)

    key_board = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton('darker')
    second_button = KeyboardButton('negative')
    third_button = KeyboardButton('sigmoid')
    four_button = KeyboardButton('lighter')
    key_board.row(first_button, second_button, third_button, four_button)

    await message.answer('Choose on of the operations:', reply_markup=key_board)
    await Second.gradation_transformations_two.set()


@dp.message_handler(content_types='text', state=Second.gradation_transformations_two)
async def update_photos(message: types.Message, state: FSMContext):
    """"Send upgraded photo, channel diagrams and set coordinates to do interpolation.

    Args:
        message: Message from telegram update.
        state: State from Finite State Machine.
    """
    result = await state.get_data()
    picture_path = result['base_image']
    path = operations(message.text, picture_path, message.from_user.id)
    if path is None:
        await message.answer('Error! Try again!')
        return

    plot_path = plot_function(message.text, message.from_user.id, picture_path.parent)
    if plot_path is None:
        await message.answer('Error! Try again!')
        return

    await message.reply('Ok', reply_markup=ReplyKeyboardRemove())

    chat_id = message.chat.id
    with plot_path.open('rb') as open_plot_photo:
        await bot.send_photo(chat_id, open_plot_photo, caption=f'{message.text} function')

    with path.open('rb') as open_photo:
        await bot.send_photo(chat_id, open_photo)

    paths = create_histogram(str(path), settings, message.from_user.id)
    media = create_media(paths)
    await message.answer_media_group(media=media)

    await message.answer("Let's make some interpolation, enter the coordinates in range from 0 to 255:")
    await Second.gradation_transformations_three.set()


@dp.message_handler(content_types='text', state=Second.gradation_transformations_three)
async def make_interpolation(message: types.Message, state: FSMContext):
    """"Draw and send plots, send histograms and image after interpolation.

    Args:
        message: Message from telegram update.
        state: State from Finite State Machine.
    """
    result = await state.get_data()
    image_path = result["base_image"]
    path_points, path_plot, inter_path = begin_draw_plots(message.text, image_path, message.from_user.id, settings)

    chat_id = message.chat.id

    with path_points.open('rb') as file_points, \
            path_plot.open('rb') as file_plot, \
            inter_path.open('rb') as file_inter_pict:
        await bot.send_photo(chat_id, file_points, caption='Your points')
        await bot.send_photo(chat_id, file_plot, caption='Your interpolation')
        await bot.send_photo(chat_id, file_inter_pict, caption='Your interpolate image')

    paths = create_histogram(inter_path, settings, message.from_user.id)
    media = create_media(paths)
    await message.answer_media_group(media=media)

    await state.finish()
    await message.answer("Enter /start to begin again")


@dp.message_handler(commands=['work_with_images'], state=None)
async def first_send_welcome(message: types.Message):
    """Process work_with_images command.

    Args:
        message: Message from telegram updates.
    """
    await message.answer("Enter the first picture:\n")
    await First.work_with_images_one.set()


@dp.message_handler(content_types='photo', state=First.work_with_images_one)
async def answer_q1(message: types.Message, state: FSMContext):
    """Save first picture path to computer.

    Args:
        message: Message from telegram updates.
        state: State from Finite State Machine.
    """
    photo = get_max_sized_photo(message.photo)
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    photo_path = settings.project_static_path / f'{message.from_user.id}_first_picture.jpg'
    await bot.download_file(file_path, photo_path)

    await state.update_data(first_name=photo_path)

    await message.answer("Enter the second picture:\n")

    await First.work_with_images_two.set()


@dp.message_handler(content_types='photo', state=First.work_with_images_two)
async def answer_q2(message: types.Message, state: FSMContext):
    """"Choose the channel to work.

    Args:
        message: Message from telegram updates.
        state: State from Finite State Machine.
    """
    photo = get_max_sized_photo(message.photo)
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    photo_path = settings.project_static_path / f'{message.from_user.id}_second_picture.jpg'

    await bot.download_file(file_path, photo_path)

    await state.update_data(second_name=photo_path)

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

    await First.work_with_images_three.set()


@dp.message_handler(content_types='text', state=First.work_with_images_three)
async def new_command(message: types.Message, state: FSMContext):
    """Choose operation to do with images.

    Args:
         message: Message from telegram updates.
         state: State from Finite State Machine.
    """
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

    await First.work_with_images_four.set()


@dp.message_handler(content_types='text', state=First.work_with_images_four)
async def command(message: types.Message, state: FSMContext):
    """Send result photo.
    Args:
         message: Message from telegram updates.
         state: State from Finite State Machine.
    """
    result = await state.get_data()
    rgb_message = result['channel_name']

    first_path = result['first_name']
    second_path = result['second_name']
    user_id = message.from_user.id

    path = process_operation(message.text, rgb_message, first_path, second_path, user_id)

    if path is None:
        await message.answer('Something is going wrong! Try again!')
        return

    with path.open('rb') as file:
        await bot.send_photo(message.chat.id, file)

    await message.answer(f"It is {message.text}, enter /start to begin again", reply_markup=ReplyKeyboardRemove())
    await state.finish()


if __name__ == '__main__':
    log.info('Bot has been started!')
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        log.exception(f'Exception occurred!')

    log.info('Bot has been stopped!')
