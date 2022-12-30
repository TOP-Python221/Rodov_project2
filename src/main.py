# импорт из стандартной библиотеки
from schedule import every
from threading import Event

# импорт дополнительных модулей текущего пакета
from model import creature
from model import data
from model import states


class Controller:
    def __init__(self):
        data_active_pet = data.PersistenceManager.read_states()
        if data_active_pet:
            revive_active_pet = states.StateCalculator()
            revive_active_pet.revive_creature()
        else:
            creat_active_pet = states.StateCalculator()
            creat_active_pet.create_new_creature()


    def mainloop(self, tick_interval: int = 900, thread_interval: float = 90):
        every(tick_interval).seconds.do(creature.Creature.tick_changes)
        stop_background = Event()
        # ...

        while True:
            command = input(' >>> ').lower()

            if command == 'quit':
                break

            elif command == 'watch':
                creature.Creature.action()

        stop_background.set()


if __name__ == '__main__':
    controller = Controller()
    controller.mainloop()
