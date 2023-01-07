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
            last_data = self.data_active_pet
            # Я не могу найти причину, по которой у меня неправильно расчитываются значения
            # Засчитываются не текущие расчитанные значение, а разница между двумя последними текущими расчитанными
            # значениями
            print('Если Вы хотите узнать доступные команды введите h/Помощь/Help')
            command = input(' >>> ').lower()

            if command == 'quit' or command == 'q' or command == 'выход':
                break

            elif command == 'play' or command =='p':

                play_value_stamina = self.active_pet.play()[0]
                play_value_joy = self.active_pet.play()[1]
                play_value_anger = self.active_pet.play()[2]

                print(f'{last_data.name} обрадовался! =^_^= <З')
                print(f'Стамина уменьшилась на {play_value_stamina} единиц. Текущий уровень стамины '
                      f'{last_data.body_last.stamina - play_value_stamina}')
                print(f'Злость уменьшилась на {play_value_anger} единиц. Текущий уровень злости '
                      f'{last_data.mind_last.anger - play_value_anger}')
                print(f'Радость увеличилась на {play_value_joy} единиц. Текущий уровень радости '
                      f'{last_data.mind_last.joy + play_value_joy}')
                data.PersistenceManager.write_states({
                    "kind": str(last_data.kind.value),
                    "name": str(last_data.name),
                    "birthdate": str(last_data.birthdate),
                    "mind_state": {
                        "timestamp": str(last_data.mind_last.timestamp),
                        "joy": last_data.mind_last.joy + play_value_joy,
                        "activity": last_data.mind_last.activity,
                        "anger": last_data.mind_last.anger - play_value_anger,
                        "anxiety": last_data.mind_last.anxiety
                    },
                    "body_state": {
                        "timestamp": str(last_data.body_last.timestamp),
                        "health": last_data.body_last.health,
                        "stamina": last_data.body_last.stamina - play_value_stamina,
                        "hunger": last_data.body_last.hunger,
                        "thirst": last_data.body_last.thirst,
                        "intestine": last_data.body_last.intestine
                    }
                })

            elif command == 'talk' or command == 't':
                talk_value_anger = self.active_pet.talk()[0]
                talk_value_joy = self.active_pet.talk()[1]
                talk_value_anxiety = self.active_pet.talk()[1]

                print(f'{last_data.name}: "было приятно с тобой побеседовать! ;)"')
                print(f'Злость уменьшилась на {talk_value_anger} единиц. Текущий уровень злости '
                      f'{last_data.mind_last.anger + talk_value_anger}')
                print(f'Радость увеличилась на {talk_value_joy} единиц. Текущий уровень радости '
                      f'{last_data.mind_last.joy + talk_value_joy}')
                print(f'Тревожность уменьшилась на {talk_value_anxiety} единиц. Текущий уровень тревожности '
                      f'{last_data.mind_last.anxiety - talk_value_anxiety}')

                data.PersistenceManager.write_states({
                    "kind": str(last_data.kind.value),
                    "name": str(last_data.name),
                    "birthdate": str(last_data.birthdate),
                    "mind_state": {
                        "timestamp": str(last_data.mind_last.timestamp),
                        "joy": last_data.mind_last.joy + talk_value_joy,
                        "activity": last_data.mind_last.activity,
                        "anger": last_data.mind_last.anger + talk_value_anger,
                        "anxiety": last_data.mind_last.anxiety + talk_value_anxiety
                    },
                    "body_state": {
                        "timestamp": str(last_data.body_last.timestamp),
                        "health": last_data.body_last.health,
                        "stamina": last_data.body_last.stamina,
                        "hunger": last_data.body_last.hunger,
                        "thirst": last_data.body_last.thirst,
                        "intestine": last_data.body_last.intestine
                    }
                })

            elif command == 'feed' or command == 'f':

                feed_value_hunger = self.active_pet.feed()[0]
                feed_value_anger = self.active_pet.feed()[1]

                print(f'{last_data.name}: "было очень вкусно! Спасибо!"')
                print(f'Уровень голода уменьшился на {feed_value_hunger}. Текущий уровень голода '
                      f'{last_data.body_last.hunger - feed_value_hunger}')
                print(f'Злость уменьшилась на {feed_value_anger}. Текущий уровень золости '
                      f'{last_data.mind_last.anger - feed_value_anger}')

                data.PersistenceManager.write_states({
                    "kind": str(last_data.kind.value),
                    "name": str(last_data.name),
                    "birthdate": str(last_data.birthdate),
                    "mind_state": {
                        "timestamp": str(last_data.mind_last.timestamp),
                        "joy": last_data.mind_last.joy,
                        "activity": last_data.mind_last.activity,
                        "anger": last_data.mind_last.anger + feed_value_anger,
                        "anxiety": last_data.mind_last.anxiety
                    },
                    "body_state": {
                        "timestamp": str(last_data.body_last.timestamp),
                        "health": last_data.body_last.health,
                        "stamina": last_data.body_last.stamina,
                        "hunger": last_data.body_last.hunger + feed_value_hunger,
                        "thirst": last_data.body_last.thirst,
                        "intestine": last_data.body_last.intestine
                    }
                })

            elif command == 'clean' or command == 'c':
                print(f'{last_data.name} вами доволен! :D')
                clean_value_anger = self.active_pet.clean()
                data.PersistenceManager.write_states({
                    "kind": str(last_data.kind.value),
                    "name": str(last_data.name),
                    "birthdate": str(last_data.birthdate),
                    "mind_state": {
                        "timestamp": str(last_data.mind_last.timestamp),
                        "joy": last_data.mind_last.joy,
                        "activity": last_data.mind_last.activity,
                        "anger": last_data.mind_last.anger - clean_value_anger,
                        "anxiety": last_data.mind_last.anxiety
                    },
                    "body_state": {
                        "timestamp": str(last_data.body_last.timestamp),
                        "health": last_data.body_last.health,
                        "stamina": last_data.body_last.stamina,
                        "hunger": last_data.body_last.hunger,
                        "thirst": last_data.body_last.thirst,
                        "intestine": last_data.body_last.intestine
                    }
                })

            elif command == 'watch' or command == 'w' or command == 'посмотреть':
                print(self.active_pet.action())
                if self.active_pet.action() == "Ваша кошка сдирает диван >:X":
                    # Немного криво работает - рандомно реагирует на условие выше
                    print('Ваши действия?: i/ignore - пригнорировать; p/punish - наказать')
                    command = input(' >>> ')

                    if command == 'punish' or command == 'pun':
                        print(f'{last_data.name} обиделся')
                        rand_anger = rr(10, 21)
                        print(f'Злость увеличилась на {rand_anger} единиц. Текущий уровень злости'
                              f' {last_data.mind_last.anger + rand_anger}')
#                       Я чё-то не додумался как можно более лаконично и красиво всё это записать :(
#                       Совсем уже отупел :P
# ========================================================================
                        data.PersistenceManager.write_states({
                            "kind": str(last_data.kind.value),
                            "name": str(last_data.name),
                            "birthdate": str(last_data.birthdate),
                            "mind_state": {
                                "timestamp": str(last_data.mind_last.timestamp),
                                "joy": last_data.mind_last.joy,
                                "activity": last_data.mind_last.activity,
                                "anger": last_data.mind_last.anger + rand_anger,
                                "anxiety": last_data.mind_last.anxiety
                            },
                            "body_state": {
                                "timestamp": str(last_data.body_last.timestamp),
                                "health": last_data.body_last.health,
                                "stamina": last_data.body_last.stamina,
                                "hunger": last_data.body_last.hunger,
                                "thirst": last_data.body_last.thirst,
                                "intestine": last_data.body_last.intestine
                            }
                        })
# ========================================================================
            elif command == 'help' or command == 'помощь' or command == 'h':
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
