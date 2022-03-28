import asyncio
import random
import urllib
import datetime
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


TOKEN = "5288298713:AAFW6cXZ2YmVb3sP6xfyzgNBjLqt8XIA7NY"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def s(message: types.Message):
    await message.answer(f"Привет! Отправь мне файлы с расширением .knd или .knvis")
'''    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="добавить винил")
    keyboard.add(button_1)
    button_2 = "добавить тюнинг"
    keyboard.add(button_2)
    await message.answer("Выберите кнопку", reply_markup=keyboard)'''

@dp.message_handler(commands=['help'])
async def h(message: types.Message):
    await message.answer(f"Привет! Отправь мне файлы с расширением .knd или .knvis")

'''@dp.message_handler(lambda message: message.text == "добавить винил")
async def av(message: types.Message):
    await message.answer(f'Выпало {random.randint(1, 6)}')'''


'''@dp.message_handler(lambda message: message.text == "добавить тюнинг")
async def at(message: types.Message):
    #await message.answer(f"Отправьте сообщение, с котором должно быть:\nname: название тюнинга\ndesc: описание\nфайл с расширением .knd\nкартинка-превью(необязательно)\nОтправляйте текст и файлы в таком порядке, как написано в этом сообщении!")
    await message.answer('Отправьте файл с разширением .knd')'''
@dp.message_handler(content_types=['document'])
async def tun(message: types.Message):
    # добавить описание и кнопки с моделямим машины
    while True:
        try:
            document_id = message.document.file_id
            file_info = await bot.get_file(document_id)
            fi = file_info.file_path
            name = message.document.file_name
            print(name)
            if name[-4::] == ".knd":
                from data import db_session
                db_session.global_init("db/database.db")
                db_sess = db_session.create_session()
                from data.tuns import Tuns
                # urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}', f'./{name}')
                vins = Tuns(user="CarX.bot", name=name,
                            description="Файл добавлен через бота, описание отсутствует",
                            car_type="CarX.bot", created_date=datetime.date.today())
                db_sess.add(vins)
                db_sess.commit()
                dbg = db_sess.query(Tuns).all()
                for i in dbg:
                    if i == vins:
                        try:
                            urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
                                                       f'./static/img/tunes/knd/{i.id}.knd')
                            # form.file.data.save(f'static/img/tunes/knd/{i.id}.knd')
                            # form.img_f.data.save(f'static/img/tunes/imgs/{i.id}.jpg')
                            break
                        except AttributeError:
                            pass
                await message.answer('Тюнинг успешно сохранён')
                break
            elif ".knvis" == name[-6::]:
                print("QQ")
                from data import db_session
                db_session.global_init("db/database.db")
                db_sess = db_session.create_session()
                from data.vins import Vinils
                # urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}', f'./{name}')
                vins = Vinils(user="CarX.bot", name=name,
                              description="Файл добавлен через бота, описание отсутствует",
                              car_type="CarX.bot", created_date=datetime.date.today())
                db_sess.add(vins)
                db_sess.commit()
                dbg = db_sess.query(Vinils).all()
                for i in dbg:
                    if i == vins:
                        try:
                            urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
                                                       f'./static/img/vins/knvis/{i.id}.knvis')
                            print("Q")
                            from PIL import Image
                            image = Image.open('bot.jpg')
                            #urllib.request.urlretrieve(f'{image}',
                                                       #f'./static/img/vins/imgs/{i.id}.jpg')
                            image.save(f'static/img/vins/imgs/{i.id}.jpg')
                            # form.file.data.save(f'static/img/tunes/knd/{i.id}.knd')
                            # form.img_f.data.save(f'static/img/tunes/imgs/{i.id}.jpg')
                            break
                        except Exception as e:
                            print(f'error {e}')
                from subprocess import call
                call('git init', shell = True)
                call('git add .', shell = True)
                call('git commit -a "commiting..."', shell = True)
                call('git push origin master', shell = True)
                await message.answer('Винил успешно сохранён')
                break
        except Exception as e:
            print(e)
            await message.answer(f'Произошла ошибка\n{e}')





@dp.message_handler(commands=['exit'])
async def ex(message: types.Message):
    await message.answer(f"Действие отменено")


'''@dp.message_handler(content_types=['document'])
async def tun(message: types.Message, f=False):
    #добавить описание и кнопки с моделямим машины
    while True:
        if f:
            try:
                document_id = message.document.file_id
                file_info = await bot.get_file(document_id)
                fi = file_info.file_path
                name = message.document.file_name
                ct = "хачи-roku"
                print(name)
                if name[-4::] == ".knd":
                    from data import db_session
                    db_session.global_init("db/database.db")
                    db_sess = db_session.create_session()
                    from data.tuns import Tuns
                    #urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}', f'./{name}')
                    vins = Tuns(user="CarX.bot", name=name, description="Файл добавлен через бота, описание отсутствует",
                                car_type=ct, created_date=datetime.date.today())
                    db_sess.add(vins)
                    db_sess.commit()
                    dbg = db_sess.query(Tuns).all()
                    for i in dbg:
                        if i == vins:
                            try:
                                urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}', f'./static/img/tunes/knd/{i.id}.knd')
                                #form.file.data.save(f'static/img/tunes/knd/{i.id}.knd')
                                #form.img_f.data.save(f'static/img/tunes/imgs/{i.id}.jpg')
                                break
                            except AttributeError:
                                pass
                    await message.answer('Файл успешно сохранён')
                break
            except Exception as e:
                print(e)
                await message.answer(f'Произошла ошибка\n{e}')'''

@dp.message_handler(commands=['work'])
async def w(message: types.Message):
    await message.answer(f"Спасибо за оценку, ждём вас на сайте!")



@dp.message_handler()
async def main(message: types.Message):
    await message.answer(f'Я получил сообщение {message["text"]}, у меня нет такой команды(\n Чтобы получить список команд, напишите /help')


executor.start_polling(dp, skip_updates=True)
