import data
import creature
import states


class Controller:
    def __init__(self):
        active_pet = data.PersistenceManager.read_states('states.json')
        if active_pet:
            states.StateCalculator.revive_creature()


# КОММЕНТАРИЙ: жаль, что вы не услышали сообщение о том, что основная работа в этом проекте проходит с моделью и от модели — за одиннадцать коммитов ни одной правки в модель
