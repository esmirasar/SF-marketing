from aiogram.fsm.state import State, StatesGroup


class FlowerRegistration(StatesGroup):
    name = State()
    graph = State()
