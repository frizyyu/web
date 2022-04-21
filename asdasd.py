import urllib
import asyncio

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
import re

TOKEN = "5288298713:AAFW6cXZ2YmVb3sP6xfyzgNBjLqt8XIA7NY"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
CLEANR = re.compile('<.*?>')

@dp.message_handler(commands=['start'])
async def s(message: types.Message):
    await message.answer(f"Привет!\nОтправь мне команду /sv цифра, и я отправлю винил с сайта\nОтправь команду /st цифра и отправлю тюнинг с сайта")

@dp.message_handler(commands=['help'])
async def h(message: types.Message):
    await message.answer(f"Привет!\nОтправь мне команду /sv цифра, и я отправлю винил с сайта\nОтправь команду /st цифра и отправлю тюнинг с сайта")

@dp.message_handler(commands=['sv'])
async def sv(message: types.Message):
    import requests
    res = requests.get(f'https://webforumcarx.herokuapp.com/vinils/{message["text"].split()[-1]}')
    file_num = str(res.text)[
               str(res.text).find('<p><a href="/static/img/vins/knvis/') + 35:str(res.text).find('.knvis"')]
    if 'Ничего не найдено :(' in res.text:
        await message.answer(f"Похоже, на форуме нет винила с таким номером")
    else:
        urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/vins/knvis/{file_num}.knvis',
                                   f'./static/img/vins/knvis/{file_num}.knvis')
        try:
            urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/vins/imgs/{file_num}.jpg',
                                     f'./static/img/vins/imgs/{file_num}.jpg')
            no_img = False
        except AttributeError:
            no_img = True
        model = str(res.text)[str(res.text).find('Винил для модели'):str(res.text).rfind('    </div>')].split('<p><align="left"; height=0>')
        name = str(res.text)[str(res.text).find('<div  class="h">') + 39::]
        name = name[:name.find("    </div>")]
        desc = str(res.text)[str(res.text).find('<div  class="desc">') + 26::]
        desc = desc[:desc.find("     </div>")]
        name = re.sub(CLEANR, '', name)
        desc = re.sub(CLEANR, '', desc)
        msg = f"Название: {name}\nОписание: {desc}\n"
        for el in model:
            msg += el.strip() + "\n"
        await message.answer(f"По вашему запросу нашлась такая публикация на сайте")
        await message.answer(msg)
        if no_img:
            await message.answer(f"Изображения нет :(")
        else:
            await bot.send_photo(message["from"]["id"],
                                    open(f'./static/img/vins/imgs/{file_num}.jpg', 'rb'))
        await bot.send_document(message["from"]["id"], open(f'./static/img/vins/knvis/{file_num}.knvis', 'rb'))
        await message.answer(f'Страница на сайте\nhttps://webforumcarx.herokuapp.com/vinils/{message["text"].split()[-1]}')


@dp.message_handler(commands=['st'])
async def st(message: types.Message):
    import requests
    res = requests.get(f'https://webforumcarx.herokuapp.com/tuning/{message["text"].split()[-1]}')
    file_num = str(res.text)[str(res.text).find('<p><a href="/static/img/tunes/knd/') + 34:str(res.text).find('.knd"')]
    if 'Ничего не найдено :(' in res.text:
        await message.answer(f"Похоже, на форуме нет тюнинга с таким номером")
    else:
        urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/tunes/knd/{file_num}.knd',
                                   f'./static/img/tunes/knd/{file_num}.knd')
        try:
            urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/tunes/imgs/{file_num}.jpg',
                                     f'./static/img/tunes/imgs/{file_num}.jpg')
            no_img = False
        except Exception:
            no_img = True
        model = str(res.text)[str(res.text).find('Тюнинг для модели'):str(res.text).rfind('    </div>')].split('<p><align="left"; height=0>')
        name = str(res.text)[str(res.text).find('<h2 align="center";>') + 20::]
        name = name[:name.find("</h2>")]
        desc = str(res.text)[str(res.text).find('<div  class="desc">') + 26::]
        desc = desc[:desc.find("     </div>")]
        name = re.sub(CLEANR, '', name)
        desc = re.sub(CLEANR, '', desc)
        msg = f"Название: {name}\nОписание: {desc}\n"
        for el in model:
            msg += el.strip() + "\n"
        await message.answer(f"По вашему запросу нашлась такая публикация на сайте")
        await message.answer(msg)
        if no_img:
            await message.answer(f"Изображения нет :(")
        else:
            print("Q")
            await bot.send_photo(message["from"]["id"],
                                    open(f'./static/img/tunes/imgs/{file_num}.jpg', 'rb'))
        await bot.send_document(message["from"]["id"], open(f'./static/img/tunes/knd/{file_num}.knd', 'rb'))
        await message.answer(f'Страница на сайте\nhttps://webforumcarx.herokuapp.com/tuning/{message["text"].split()[-1]}')


@dp.message_handler()
async def main(message: types.Message):
    await message.answer(f'Я получил сообщение {message["text"]}, у меня нет такой команды(\n Чтобы получить список команд, напишите /help')


async def hh(time):
    import requests
    while True:
        await asyncio.sleep(time)
        res = requests.get(f'https://webforumcarx.herokuapp.com/')
        print("working site")


loop = asyncio.get_event_loop()
loop.create_task(hh(1200))
executor.start_polling(dp, skip_updates=True)
