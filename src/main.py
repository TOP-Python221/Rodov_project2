# импорт из стандартной библиотеки
from schedule import every
from threading import Event
from random import randrange as rr

# импорт дополнительных модулей текущего пакета
from model import creature
from model import data
from model import states
from utils import constants


class Controller:
    def __init__(self):
        self.data_active_pet = data.PersistenceManager.read_states()
        if self.data_active_pet:
            self.active_pet = states.StateCalculator().revive_creature()
        else:
            self.active_pet = states.StateCalculator().create_new_creature()

    def mainloop(self, tick_interval: int = 900, thread_interval: float = 90):
        every(tick_interval).seconds.do(creature.Creature.tick_changes)
        stop_background = Event()
        # ...

        while True:
            print('Если Вы хотите узнать доступные команды введите Помощь/Help')
            command = input(' >>> ').lower()

            if command == 'quit' or command == 'q' or command == 'выход':
                break

            elif command == 'watch' or command == 'w' or command == 'посмотреть':
                print(self.active_pet.action())
                if self.active_pet.action() == "Ваша кошка сдирает диван >:X":
                    # Немного криво работает - рандомно реагирует на условие выше
                    print('Ваши действия?: ignore - пригнорировать; hit - дать по сраке')
                    command = input(' >>> ')
                    if command == 'hit':
                        print('Котик обиделся')
                        rand_anger = rr(10, 21)

                        last_data = self.data_active_pet
                        print(f'Уровень злости вырос на {rand_anger}. Текущий уровень злости'
                              f' {last_data.mind_last.anger + rand_anger}')
#                       Я чё-то не додумался как можно более лаконично и красиво всё это записать :(
#                       Совсем уже отупел :P
# ========================================================================
                        data.PersistenceManager.write_states({
                            "kind": "cat",
                            "name": "Кусик",
                            "birthdate": "2022-11-24 10:00:00",
                            "mind_state": {
                                "timestamp": "2022-11-26 17:30:00",
                                "joy": 60 - 15,
                                "activity": 1.3,
                                "anger": last_data.mind_last.anger + rand_anger,
                                "anxiety": 0.9
                            },
                            "body_state": {
                                "timestamp": "2022-11-26 17:30:00",
                                "health": 19,
                                "stamina": 28,
                                "hunger": 5,
                                "thirst": 0,
                                "intestine": 14
                            }
                        })
# ========================================================================
            elif command == 'help' or command == 'помощь':
                print(*constants.HELP)

            elif command == 's' or command == 'state' or command == 'состояние':
                # health = self.active_pet.body.health
                # hunger = self.active_pet.body.hunger
                # stamina = self.active_pet.body.stamina
                # thirst = self.active_pet.body.thirst
                # print(f'Уровень здоровья Вашего питомца: {health}\n',
                #       f'Уровень энергии Вашего питомца: {stamina}\n',
                #       f'Уровень голода Вашего питомца: {hunger}\n',
                #       f'Уровень жажды Вашего питомца: {thirst}\n',)
                for k, v in self.active_pet.body.__dict__.items():
                    if not k == 'timestamp':
                        print(f'Уровень {k} = {v}')

            else:
                print('Нет такой команды.')

        stop_background.set()


if __name__ == '__main__':
    controller = Controller()
    controller.mainloop(5, 1)
