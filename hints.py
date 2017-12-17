import random
import time


def hints(answer):
    answer_list = list(answer)
    hint = ''
    space_list = []
    total_list = []
    # hint = '#'*len(x)

    # Перевод ответа в шарпы
    for elem in answer:
        if elem != ' ':
            hint += '#'
        else:
            hint += ' '

    # Записывает индекс пробелов в список
    for i in range(len(answer)):
        if answer[i] == ' ':
            space_list.append(i)

    hint_list = list(hint)

    answer_indexes = list(range(len(answer)))
    random.shuffle(answer_indexes)

    for number in answer_indexes:
        if number not in space_list:
            hint_list[number] = answer_list[number]
            hint = ''.join(hint_list)
            # time.sleep(2)
            # print(hint)
            total_list.append(hint)

    return total_list