import datetime
import urllib

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor

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

@dp.message_handler(commands=['sv'])
async def sv(message: types.Message):
    import requests
    res = requests.get(f'https://webforumcarx.herokuapp.com/vinils/{message["text"].split()[-1]}')
    if 'Ничего не найдено :(' in res.text:
        await message.answer(f"Похоже, на форуме нет винила с таким номером")
    else:
        urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/vins/knvis/{message["text"].split()[-1]}.knvis',
                                   f'./static/img/vins/knvis/{message["text"].split()[-1]}.knvis')
        try:
            urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/vins/imgs/{message["text"].split()[-1]}.jpg',
                                     f'./static/img/vins/imgs/{message["text"].split()[-1]}.jpg')
            no_img = False
        except AttributeError:
            no_img = True
        model = str(res.text)[str(res.text).find('Винил для модели'):str(res.text).rfind('    </div>')].split('<p><align="left"; height=0>')
        name = str(res.text)[str(res.text).find('<div  class="h">') + 39::]
        name = name[:name.find("    </div>")]
        desc = str(res.text)[str(res.text).find('<div  class="desc">') + 26::]
        desc = desc[:desc.find("     </div>")]
        print(desc)
        msg = f"Название: {name}\nОписание: {desc}\n"
        for el in model:
            msg += el.strip() + "\n"
        await message.answer(f"По вашему запросу нашлась такая публикация на сайте")
        await message.answer(msg)
        if no_img:
            await message.answer(f"Изображения нет :(")
        else:
            await bot.send_photo(message["from"]["id"],
                                    open(f'./static/img/vins/imgs/{message["text"].split()[-1]}.jpg', 'rb'))
        await bot.send_document(message["from"]["id"], open(f'./static/img/vins/knvis/{message["text"].split()[-1]}.knvis', 'rb'))


@dp.message_handler(commands=['st'])
async def st(message: types.Message):
    import requests
    res = requests.get(f'https://webforumcarx.herokuapp.com/tuning/{message["text"].split()[-1]}')
    if 'Ничего не найдено :(' in res.text:
        await message.answer(f"Похоже, на форуме нет винила с таким номером")
    else:
        urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/tunes/knd/{message["text"].split()[-1]}.knd',
                                   f'./static/img/tunes/knd/{message["text"].split()[-1]}.knd')
        try:
            urllib.request.urlretrieve(f'https://webforumcarx.herokuapp.com/static/img/tunes/imgs/{message["text"].split()[-1]}.jpg',
                                     f'./static/img/tunes/imgs/{message["text"].split()[-1]}.jpg')
            no_img = False
        except Exception:
            no_img = True
        model = str(res.text)[str(res.text).find('Тюнинг для модели'):str(res.text).rfind('    </div>')].split('<p><align="left"; height=0>')
        name = str(res.text)[str(res.text).find('<h2 align="center";>') + 20::]
        name = name[:name.find("</h2>")]
        desc = str(res.text)[str(res.text).find('<div  class="desc">') + 26::]
        desc = desc[:desc.find("     </div>")]
        print(desc)
        msg = f"Название: {name}\nОписание: {desc}\n"
        for el in model:
            msg += el.strip() + "\n"
        await message.answer(f"По вашему запросу нашлась такая публикация на сайте")
        print(msg, "|||||||||||\n\n\n\n", res.text)
        await message.answer(msg)
        if no_img:
            await message.answer(f"Изображения нет :(")
        else:
            print("Q")
            await bot.send_photo(message["from"]["id"],
                                    open(f'./static/img/tunes/imgs/{message["text"].split()[-1]}.jpg', 'rb'))
        await bot.send_document(message["from"]["id"], open(f'./static/img/tunes/knd/{message["text"].split()[-1]}.knd', 'rb'))

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
                #path = '/n92322vg.beget.tech/public_html/FOLDER'
                '''ftp = ftplib.FTP("n92322vg.beget.tech")
                ftp.login("n92322vg", "NMcsXFjP")'''
                #загрузка на фтп сервер
                #берём файл с фтп и сохраняем в локалке и добавляем запись в бд(asd.py)
                #удаляем файл с фтп(asd.py)
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
                            '''ftp.cwd('/n92322vg.beget.tech/public_html/FOLDER/static/vins/knvis')
                            ftp.retrbinary("RETR " + f'{i.id}.knvis', open(f'./static/img/vins/knvis/{i.id}.knvis', 'wb').write)'''
                            print("Q")
                            from PIL import Image
                            image = Image.open('bot.jpg')
                            #urllib.request.urlretrieve(f'{image}',
                                                       #f'./static/img/vins/imgs/{i.id}.jpg')
                            image.save(f'static/img/vins/imgs/{i.id}.jpg')
                            # form.file.data.save(f'static/img/tunes/knd/{i.id}.knd')
                            # form.img_f.data.save(f'static/img/tunes/imgs/{i.id}.jpg')
                            break
                        except AttributeError:
                            pass
                #ftp.quit()
                await message.answer('Винил успешно сохранён')
                break
        except Exception as e:
            print(e)
            await message.answer(f'Произошла ошибка\n{e}')





'''@dp.message_handler(commands=['exit'])
async def ex(message: types.Message):
    await message.answer(f"Действие отменено")'''


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

'''@dp.message_handler(commands=['work'])
async def w(message: types.Message):
    await message.answer(f"Спасибо за оценку, ждём вас на сайте!")'''



@dp.message_handler()
async def main(message: types.Message):
    await message.answer(f'Я получил сообщение {message["text"]}, у меня нет такой команды(\n Чтобы получить список команд, напишите /help')


executor.start_polling(dp, skip_updates=True)