# импорт из стандартной библиотеки
import datetime

from schedule import every
import schedule
from threading import Event
from random import randrange as rr

# импорт дополнительных модулей текущего пакета
from src.model import creature
from src.model import data
from src.utils import constants


class Controller:
    def __init__(self):
        self.data_active_pet = data.PersistenceManager.read_states()

        start_game_day = datetime.datetime.today().day
        end_game_day = self.data_active_pet.body_last.timestamp.day

        if self.data_active_pet.body_last.health == '':
            self.active_pet = data.StateCalculator().create_new_creature()
        else:
            self.active_pet = data.StateCalculator().revive_creature()

        # ИСПРАВИТЬ: использовать объекты datetime и timedelta
        if end_game_day > start_game_day:
            days_passed = 31 - start_game_day + end_game_day
            print(f' Прожито дней {days_passed}')
            # ...
        else:
            days_passed = start_game_day - end_game_day
            print(f' Прожито дней {days_passed}')
            # ...


    def mainloop(self, tick_interval: int = 900, thread_interval: float = 90):

        stop_background = Event()
        # ...
        mainloop_pet = creature.Creature(self.active_pet.name,
                                         self.active_pet.birthdate,
                                         self.active_pet.body,
                                         self.active_pet.mind,
                                         self.active_pet.kind)

        timestamp = str(datetime.datetime.today()).split('.')[0]

        data.PersistenceManager.write_states({
            # ИСПРАВИТЬ здесь и далее: на mainloop_pet.kind.value
            "kind": str(mainloop_pet.kind.value),
            "name": str(mainloop_pet.name.title()),
            "birthdate": str(mainloop_pet.birthdate),
            "mind_state": {
                "timestamp": timestamp,
                "joy": mainloop_pet.mind.joy,
                "activity": '',
                "anger": mainloop_pet.mind.anger,
                "anxiety": mainloop_pet.mind.anxiety
            },
            "body_state": {
                "timestamp": timestamp,
                "health": mainloop_pet.body.health,
                "stamina": mainloop_pet.body.stamina,
                "hunger": mainloop_pet.body.hunger,
                "thirst": mainloop_pet.body.thirst,
                "intestine": mainloop_pet.body.intestine
            }
        })

        if self.active_pet.body.health > 0:
            while True:
                schedule.every(tick_interval).seconds.do(mainloop_pet.apply_tick_changes)
                schedule.run_pending()
                last_data = self.data_active_pet
                # Я не могу найти причину, по которой у меня неправильно расчитываются значения
                # Засчитываются не текущие расчитанные значение, а разница между двумя последними расчитанными
                # значениями
                print('Список досутпных команд: h/Помощь/Help')
                command = input(' >>> ').lower()

                if command == 'quit' or command == 'q' or command == 'выход':

                    last_timestamp = str(datetime.datetime.today()).split('.')[0]
                    last_pet_state = data.PersistenceManager.read_states()
                    data.PersistenceManager.write_states({
                        "kind": str(last_pet_state.kind.value),
                        "name": str(last_pet_state.name.title()),
                        "birthdate": str(last_pet_state.birthdate),
                        "mind_state": {
                            "timestamp": last_timestamp,
                            "joy": last_pet_state.mind_last.joy,
                            "activity": last_pet_state.mind_last.activity,
                            "anger": last_pet_state.mind_last.anger,
                            "anxiety": last_pet_state.mind_last.anxiety
                        },
                        "body_state": {
                            "timestamp": last_timestamp,
                            "health": last_pet_state.body_last.health,
                            "stamina": last_pet_state.body_last.stamina,
                            "hunger": last_pet_state.body_last.hunger,
                            "thirst": last_pet_state.body_last.thirst,
                            "intestine": last_pet_state.body_last.intestine
                        }
                    })
                    print(f'{last_pet_state.name.title()}: "я тебя буду ждать! Возвращайся поскорее!"')
                    END_GAME = datetime.datetime.today()
                    break

                elif command == 'play' or command =='p':

                    play_delta_stamina = self.active_pet.play()[0]
                    play_delta_joy = self.active_pet.play()[1]
                    play_delta_anger = self.active_pet.play()[2]

                    print(f'{last_data.name.title()} обрадовался! =^_^= <З')
                    print(f'Стамина уменьшилась на {play_delta_stamina} единиц. Текущий уровень стамины '
                          f'{last_data.body_last.stamina - play_delta_stamina}')
                    print(f'Злость уменьшилась на {play_delta_anger} единиц. Текущий уровень злости '
                          f'{last_data.mind_last.anger - play_delta_anger}')
                    print(f'Радость увеличилась на {play_delta_joy} единиц. Текущий уровень радости '
                          f'{last_data.mind_last.joy + play_delta_joy}')
                    data.PersistenceManager.write_states({
                        "kind": str(last_data.kind.value),
                        "name": str(last_data.name.title()),
                        "birthdate": str(last_data.birthdate),
                        "mind_state": {
                            "timestamp": str(last_data.mind_last.timestamp),
                            "joy": last_data.mind_last.joy + play_delta_joy,
                            "activity": last_data.mind_last.activity,
                            "anger": last_data.mind_last.anger - play_delta_anger,
                            "anxiety": last_data.mind_last.anxiety
                        },
                        "body_state": {
                            "timestamp": str(last_data.body_last.timestamp),
                            "health": last_data.body_last.health,
                            "stamina": last_data.body_last.stamina - play_delta_stamina,
                            "hunger": last_data.body_last.hunger,
                            "thirst": last_data.body_last.thirst,
                            "intestine": last_data.body_last.intestine
                        }
                    })

                elif command == 'talk' or command == 't':

                    talk_delta_anger = self.active_pet.talk()[0]
                    talk_delta_joy = self.active_pet.talk()[1]
                    talk_delta_anxiety = self.active_pet.talk()[1]

                    print(f'{last_data.name.title()}: "было приятно с тобой побеседовать! ;)"')
                    print(f'Злость уменьшилась на {talk_delta_anger} единиц. Текущий уровень злости '
                          f'{last_data.mind_last.anger  + talk_delta_anger}')
                    print(f'Радость увеличилась на {talk_delta_joy} единиц. Текущий уровень радости '
                          f'{last_data.mind_last.joy + talk_delta_joy}')
                    print(f'Тревожность уменьшилась на {talk_delta_anxiety} единиц. Текущий уровень тревожности '
                          f'{last_data.mind_last.anxiety - talk_delta_anxiety}')

                    data.PersistenceManager.write_states({
                        "kind": str(last_data.kind.value),
                        "name": str(last_data.name.title()),
                        "birthdate": str(last_data.birthdate),
                        "mind_state": {
                            "timestamp": str(last_data.mind_last.timestamp),
                            "joy": last_data.mind_last.joy + talk_delta_joy,
                            "activity": last_data.mind_last.activity,
                            "anger": last_data.mind_last.anger + talk_delta_anger,
                            "anxiety": last_data.mind_last.anxiety + talk_delta_anxiety
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
                    feed_value_intestine = self.active_pet.feed()[2]
                    # Рандомный 'ключ', что используется для выбора реплик питомца в ответ на действие игрока
                    answer_key = rr(0, 3)
                    # Список ответов
                    # Мне бы, конечно, лучше было бы заняться исправлением логических ошибок в коде, а не этим
                    # заниматься, но решил хотя бы в этот метод добавить такую реализацию интереса ради :)
                    random_answer = [('Было очень вкусно! Спасибо!'),
                                     ('Из тебя повар, как из меня человек! Но всё равно неплохо :P'),
                                     ('Благодарю, кожаный!')]


                    print(f'{last_data.name.title()}: {random_answer[answer_key]}')
                    print(f'Уровень голода уменьшился на {feed_value_hunger}. Текущий уровень голода '
                          f'{last_data.body_last.hunger - feed_value_hunger}')
                    print(f'Злость уменьшилась на {feed_value_anger}. Текущий уровень золости '
                          f'{last_data.mind_last.anger - feed_value_anger}')

                    new_hunger_value = last_data.body_last.hunger - feed_value_hunger
                    new_anger_value = last_data.mind_last.anger - feed_value_anger
                    data.PersistenceManager.write_states({
                        "kind": str(last_data.kind.value),
                        "name": str(last_data.name.title()),
                        "birthdate": str(last_data.birthdate),
                        "mind_state": {
                            "timestamp": str(last_data.mind_last.timestamp),
                            "joy": last_data.mind_last.joy,
                            "activity": last_data.mind_last.activity,
                            "anger": new_anger_value,
                            "anxiety": last_data.mind_last.anxiety
                        },
                        "body_state": {
                            "timestamp": str(last_data.body_last.timestamp),
                            "health": last_data.body_last.health,
                            "stamina": last_data.body_last.stamina,
                            "hunger": new_hunger_value,
                            "thirst": last_data.body_last.thirst,
                            "intestine": last_data.body_last.intestine + feed_value_intestine
                        }
                    })

                elif command == 'clean' or command == 'c':
                    print(f'{last_data.name.title()} вами доволен! :D')

                    clean_value_anger = self.active_pet.clean()

                    data.PersistenceManager.write_states({
                        "kind": str(last_data.kind.value),
                        "name": str(last_data.name.title()),
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
                    if self.active_pet.action() == self.active_pet.get_actions[0]:
                        # Немного криво работает - рандомно реагирует на условие выше
                        print('Ваши действия?: i/ignore - пригнорировать; pun/punish - наказать')
                        command = input(' >>> ')

                        if command == 'punish' or command == 'pun':
                            print(f'{last_data.name.title()} обиделся')
                            rand_anger = rr(10, 21)
                            print(f'Злость увеличилась на {rand_anger} единиц. Текущий уровень злости'
                                  f' {last_data.mind_last.anger + rand_anger}')

                            data.PersistenceManager.write_states({
                                "kind": str(last_data.kind.value),
                                "name": str(last_data.name.title()),
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

        else:
            print('Ваш питомец погиб')
            data.PersistenceManager.write_states({
                        "kind": "cat",
                        "name": '',
                        "birthdate": "2022-11-26 17:30:00",
                        "mind_state": {
                            "timestamp": "2022-11-26 17:30:00",
                            "joy": '',
                            "activity": '',
                            "anger": '',
                            "anxiety": ''
                        },
                        "body_state": {
                            "timestamp": "2022-11-26 17:30:00",
                            "health": '',
                            "stamina": '',
                            "hunger": '',
                            "thirst": '',
                            "intestine": ''
                        }
                    })



if __name__ == '__main__':
    controller = Controller()
    controller.mainloop(5, 1)
