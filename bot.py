import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType


bot = Bot(token='')
pay_token = ''
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()


class GetGroup(StatesGroup):
    purchase = State()


db = sqlite3.connect("../baza.db")
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INT,
    userName TEXT,
    VideoKarti TEXT,
    timeMining INT,
    balance TEXT
)""")

groups = types.ReplyKeyboardMarkup(resize_keyboard=True)
set_group = types.ReplyKeyboardMarkup(resize_keyboard=True)

group_one = types.KeyboardButton("Купить видео карты")
group_two = types.KeyboardButton("Сколько майнится?")
group_three = types.KeyboardButton("Баланс")
group_four = types.KeyboardButton("Поддержать))")
groups.add(group_one, group_two, group_three, group_four)

cards = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_one = types.KeyboardButton("rtx3090, цена: 50000 KlimCoinов")
card_two = types.KeyboardButton("rtx2090, цена: 30000 KlimCoinов")
card_three = types.KeyboardButton("rtx1660ti, цена: 20000 KlimCoinов")
back_btn = types.KeyboardButton("Вернуться назад")
cards.add(card_one, card_two, card_three, back_btn)

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=100000000)  # в копейках (руб)


@dp.message_handler(Command('start'), state=None)
async def welcome(message):
    if message.from_user.id == message.chat.id:
        sql.execute(f"SELECT * FROM users WHERE user_id = {message.from_user.id}")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                        (message.from_user.id, message.from_user.username, None, 1, 0))
            db.commit()
    await message.answer('Привет! В этом боте ты будешь майнить KlimCoinы!', reply_markup=groups)


@dp.message_handler(content_types=['text'])
async def lalala(message):
    if message.text == 'Баланс':
        await message.answer(f'У вас на балансе {sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[4]} KlimCoinов')

    elif message.text == 'Сколько майнится?':
        await message.answer(f'Вы майните {sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[3]} KlimCoinов в секунду!')

    elif message.text == 'Купить видео карты':
        await message.answer('Выбирете видео карту: ', reply_markup=cards)
        await GetGroup.purchase.set()
    else:
        await bot.send_message(message.chat.id, 'Можешь поддержать меня, как тебе удобно: +79168870045 (Сбер) Клим Олегович Щ.')
        await bot.send_message(message.chat.id, "Платеж с низу - не натсоящий..., можешь поддежать меня понарошку...")
        await bot.send_message(message.chat.id, "Чтобы это сделать в номер карты введи: 4242 4242 4242 4242424\n"
                                                "Любой день, любой месяц и любой cvc")
        await bot.send_invoice(message.chat.id,
                               title="ТЫ КРУТОЙ!",
                               description="Лучший!",
                               provider_token=pay_token,
                               currency="rub",
                               photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                               photo_width=416,
                               photo_height=234,
                               photo_size=416,
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="one-month-subscription",
                               payload="test-invoice-payload")


async def mining():
    for users in sql.execute(f"SELECT user_id FROM users").fetchall():
        for user in users:
            balance = int(sql.execute(f'SELECT balance FROM users WHERE user_id = {user}').fetchone()[0])
            mine = int(sql.execute(f'SELECT timeMining FROM users WHERE user_id = {user}').fetchone()[0])
            sql.execute(f'UPDATE users SET balance = {balance + mine} WHERE user_id = "{user}"')
            db.commit()


@dp.message_handler(state=GetGroup.purchase)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy():
        await state.finish()
        plus = 0
        if message.text == 'rtx3090, цена: 50000 KlimCoinов':
            if int(sql.execute(f'SELECT balance FROM users WHERE user_id = {message.from_user.id}').fetchone()[0]) > 50000:
                balance = int(sql.execute(f'SELECT balance FROM users WHERE user_id = {message.from_user.id}').fetchone()[0])
                sql.execute(f'UPDATE users SET balance = {balance - 50000} WHERE user_id = "{message.from_user.id}"')
                db.commit()
                plus = 10
            else:
                await message.answer('У вас не достаточно средств для покупки этой видеокарты(')
        elif message.text == 'rtx2090, цена: 30000 KlimCoinов':
            if int(sql.execute(f'SELECT balance FROM users WHERE user_id = {message.from_user.id}').fetchone()[0]) > 30000:
                balance = int(sql.execute(f'SELECT balance FROM users WHERE user_id = {message.from_user.id}').fetchone()[0])
                sql.execute(f'UPDATE users SET balance = {balance - 30000} WHERE user_id = "{message.from_user.id}"')
                db.commit()
                plus = 7
            else:
                await message.answer('У вас не достаточно средств для покупки этой видеокарты(')
        elif message.text == 'rtx1660ti, цена: 20000 KlimCoinов':
            if int(sql.execute(f'SELECT balance FROM users WHERE user_id = {message.from_user.id}').fetchone()[0]) > 20000:
                balance = int(sql.execute(f'SELECT balance FROM users WHERE user_id = {message.from_user.id}').fetchone()[0])
                sql.execute(f'UPDATE users SET balance = {balance - 20000} WHERE user_id = "{message.from_user.id}"')
                db.commit()
                plus = 5
            else:
                await message.answer('У вас не достаточно средств для покупки этой видеокарты(')
        elif message.text == "Вернуться назад":
            await message.answer(f"Вернулись)", reply_markup=groups)
            return
        if plus:
            time_mining = int(sql.execute(f'SELECT timeMining FROM users WHERE user_id = {message.from_user.id}').fetchone()[0])
            sql.execute(f"UPDATE users SET timeMining = '{time_mining + plus}' WHERE user_id = {message.from_user.id}")
            db.commit()
            await message.answer(f"Вы успешно преобрили видео карту! Теперь вы майните на {plus} KlimCoinов больше!",
                                 reply_markup=groups)
        else:
            await message.answer(f"Приходите, когда будет больше KlimCoinов!", reply_markup=groups)


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await bot.send_message(message.chat.id, f"Платёж на сумму {message.successful_payment.total_amount // 100}"
                                            f" {message.successful_payment.currency} прошел успешно!!!")


async def on_startup(_):
    scheduler.add_job(mining, "interval", seconds=1)
    print('Бот запущен')


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
