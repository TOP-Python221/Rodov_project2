import creature
from src import data, states
from schedule import every
from threading import Event


class Controller:
    def __init__(self):
        active_pet = data.PersistenceManager.read_states('states.json')
        if active_pet:
            states.StateCalculator.revive_creature()
        else:
            states.StateCalculator.create_new_creature()

    def mainloop(self, tick_interval: int = 900, thread_interval: float = 90):
        every(tick_interval).seconds.do(creature.Creature.tick_changes())
        stop_background = Event()
        # ...

        while True:
            command = input(' >>> ').lower()

            if command == 'quit':
                break

            elif command == 'watch':
                creature.Creature.action()

        stop_background.set()
# КОММЕНТАРИЙ: жаль, что вы не услышали сообщение о том, что основная работа в этом проекте проходит с моделью и от модели — за одиннадцать коммитов ни одной правки в модель

# Прошу прощения :`(
