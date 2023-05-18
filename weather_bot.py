import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


bot = Bot(token='token')
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def greeting_message(message):
    msg = f'Приветствую Вас, {message.from_user.first_name}. Я могу подсказать какая сейчас погода на улице. Для этого выберите интересующий Вас город:'
    kb = [
        [
            types.KeyboardButton(text="Тверь"),
            types.KeyboardButton(text="Кимры")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='или введите название вручную'
    )

    await message.answer(msg, reply_markup=keyboard)

@dp.message_handler(content_types='text')
async def send_weather(message: types.Message):
    city = message.text
    weather = get_weather(city)
    await message.answer(weather)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=your_id&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f'Погода в городе {city}: {weather_description}, температура: {temperature}°C'



executor.start_polling(dp, skip_updates=True)