import asyncio
import logging
import os
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, FSInputFile
from aiogram.filters.command import Command
from config import token

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! {0}, отправьте номер телефона(ОБЯЗАТЕЛЬНО С '+') или ник телеграм с '@'".format(message.from_user.first_name))

@dp.message(F.text)
async def message_message(message: types.Message):
    print('--------------------------------------------------------------------------')
    print('Дата и время: ', message.date)
    print('Имя: {0}'.format(message.from_user.first_name))
    print('Username: {0}'.format(str(message.from_user.username)))
    print('Chat Id: {0}'.format(str(message.chat.id)))
    print('Сообщение: {0}'.format(message.text))
    if message.text[0] == '+':
        messagephone = message.text.lstrip('+')
        await message.answer(text="Начинаю искать в базе")
        try:
            messagephoneint = int(messagephone)
            await message.answer(text="Поиск в 1 базе данных")
            with open(r'C:\Python\EyeGod\db\{0}\{1}\{2}\{3}\{4}\{5}\00000-99999.json'.format(messagephone[0],
                messagephone[1],messagephone[2],messagephone[3],messagephone[4],messagephone[5]),'r', encoding="utf8") as f:
                JsonFileLoad = json.load(f)
                JsonFileLen = len(JsonFileLoad)
                KolvoZapros = 0
                NotPhon = 0
                while KolvoZapros < JsonFileLen:
                    if message.text == JsonFileLoad[KolvoZapros][0]:
                        await message.answer(text="Phone: "+JsonFileLoad[KolvoZapros][0]+"\n"+"Город: "+
                                             JsonFileLoad[KolvoZapros][1]+"\n"+"Улица: "+
                                             JsonFileLoad[KolvoZapros][2]+"\n"+"Дом: "+
                                             JsonFileLoad[KolvoZapros][3]+"\n"+"Фио: "+
                                             JsonFileLoad[KolvoZapros][9]+"\n"+"Почта: "+
                                             JsonFileLoad[KolvoZapros][8])
                        NotPhon = 1
                        KolvoZapros = KolvoZapros + 1
                    elif KolvoZapros == JsonFileLen:
                        break
                    else:
                        KolvoZapros = KolvoZapros + 1

                if NotPhon == 0:
                    await message.answer(text="Данных нет")
            await message.answer(text="Поиск в 2 базе данных")
            with open("БД Telegram [HACKER PHONE].txt", 'r', encoding="utf8") as file:
                lines = file.readlines()
            notuser = 0
            for line in lines:
                if messagephone in line:
                    notuser = 1
                    await message.answer(text="|Системный номер|name|fname|phone|uid|nik|wo|"+"\n"+line)
            if notuser == 0:
                await message.answer(text="Пользователь не найден")
        except Exception as e:
            await message.answer(text="Прислали не номер телефона.\n Ошибка: {0}".format(e))
    elif message.text[0] == '@':
        try:
            # userid = message.text
            messageNik = message.text.lstrip('@')
            await message.answer(text="Поиск в базе Тг")
            with open("БД Telegram [HACKER PHONE].txt", 'r', encoding="utf8") as file:
                    lines = file.readlines()
            notuser = 0
            for line in lines:
                if messageNik in line:
                    notuser = 1
                    await message.answer(text="|Системный номер|name|fname|phone|uid|nik|wo|"+"\n"+line)
            if notuser == 0:
                await message.answer(text="Пользователь не найден")
        except Exception as e:
            await message.answer(text="Ошибка: {0}".format(e))
    else:
        await message.answer(text="Сообщение начинается на '+' или '@'")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())