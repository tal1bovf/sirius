from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, String, Column, Numeric, Integer

engine = create_engine("postgresql://talibov:1@localhost/sirius_db")

Base = declarative_base()

DBSession = sessionmaker(bind=engine)
session = DBSession()


bot = Bot('5617866046:AAH8xj5kEA8UihbQPCwtizOFcg0gV_YRAAM')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

lst = []


class Form(StatesGroup):
    first_name = State()
    last_name = State()
    st_ball = State()
    nd_ball = State()
    thball = State()
    foball = State()
    fball = State()


class User(Base):
    __tablename__ = 'userss'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    last_name = Column(String(255))
    first_ball = Column(Numeric())
    second_ball = Column(Numeric())
    third_ball = Column(Numeric())
    fourth_ball = Column(Numeric())
    fifth_ball = Column(Numeric())


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    Base.metadata.create_all(engine)
    await Form.first_name.set()
    await message.reply("Enter student's first name: ")


@dp.message_handler(state=Form.first_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with state.proxy() as data:
        data['first_name'] = message.text
    await Form.next()
    await message.reply(f"Enter second name: ")


@dp.message_handler(state=Form.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await Form.next()
    await message.reply(f"Enter 1 ball : ")


@dp.message_handler(state=Form.st_ball)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_ball'] = message.text

    await Form.next()
    await message.answer(f"Enter 2 ball: ")


@dp.message_handler(state=Form.nd_ball)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_ball'] = message.text

    await Form.next()
    await message.answer(f"Enter 3 ball: ")


@dp.message_handler(state=Form.thball)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['third_ball'] = message.text

    await Form.next()
    await message.answer(f"Enter 4 ball: ")


@dp.message_handler(state=Form.foball)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fourth_ball'] = message.text

    await Form.next()
    await message.answer(f"Enter 5 ball: ")


@dp.message_handler(state=Form.fball)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fifth_ball'] = message.text

    # d = {
    #     "name": data['first_name'],
    #     'last_name': data['last_name'],
    #     'first_ball': data['first_ball'],
    #     'second_ball': data['second_ball'],
    #     'third_ball': data['third_ball'],
    #     'fourth_ball': data['fourth_ball'],
    #     'fifth_ball': data['fifth_ball']
    # }
    user = User(
        name=data['first_name'],
        last_name=data['last_name'],
        first_ball=data['first_ball'],
        second_ball=data['second_ball'],
        third_ball=data['third_ball'],
        fourth_ball=data['fourth_ball'],
        fifth_ball=data['fifth_ball'],
    )

    session.add(user)
    session.commit()

    # lst.append(d)
    # with open('sirius.json', 'w') as file:
    #     json.dump(lst, file, indent=3)

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
