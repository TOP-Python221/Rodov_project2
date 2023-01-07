# импорт из стандартной библиотеки
from schedule import every
from threading import Event
from random import randrange as rr

# импорт дополнительных модулей текущего пакета
from src.model import creature
from src.model import data
from src.utils import constants


class Controller:
    def __init__(self):
        self.data_active_pet = data.PersistenceManager.read_states()
        if self.data_active_pet:
            self.active_pet = data.StateCalculator().revive_creature()
        else:
            self.active_pet = data.StateCalculator().create_new_creature()

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
                            "kind": last_data.kind,
                            "name": last_data.name,
                            "birthdate": last_data.birthdate,
                            "mind_state": {
                                "timestamp": last_data.mind_last.timestamp,
                                "joy": last_data.mind_last.joy,
                                "activity": last_data.mind_last.activity,
                                "anger": last_data.mind_last.anger + rand_anger,
                                "anxiety": last_data.mind_last.anxiety
                            },
                            "body_state": {
                                "timestamp": last_data.body_last.timestamp,
                                "health": last_data.body_last.health,
                                "stamina": last_data.body_last.stamina,
                                "hunger": last_data.body_last.hunger,
                                "thirst": last_data.body_last.thirst,
                                "intestine": last_data.body_last.intestine
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
