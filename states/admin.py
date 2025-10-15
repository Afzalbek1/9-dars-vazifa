from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class BookAdd(StatesGroup):
    title = State()
    description = State()
    author = State()
    price = State()
    genre = State()
    quantity = State()

class BookEdit(StatesGroup):
    book_id = State()
    title = State()
    description = State()
    author = State()
    price = State()
    genre = State()
    quantity = State()