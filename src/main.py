# импорт из стандартной библиотеки
from schedule import every
from threading import Event

# импорт дополнительных модулей текущего пакета
from . import creature
from . import data
from . import states


class Controller:
    def __init__(self):
        active_pet = data.PersistenceManager.read_states('../data/states.json')
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

