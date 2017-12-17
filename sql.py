from __future__ import absolute_import, print_function
import random
from pony.orm import *

db = Database("sqlite", "victorina.sqlite3")


class Quiz(db.Entity):
    id = PrimaryKey(int, auto=True)
    question = Required(str)
    answer = Required(str)


class Player(db.Entity):
    chat_id = PrimaryKey(int, auto=True)
    score = Required(int)


db.generate_mapping(create_tables=True)


@db_session
def get_random_question():
    random_question = random.randint(9371, 47105)
    line = Quiz[random_question]
    question = line.question
    answer = line.answer
    return (question, answer)


@db_session
def add_player(player_id):
    Player(chat_id=player_id, score=0)


@db_session
def add_point(player_id):
    player = Player.get(chat_id=player_id)
    player.score += 1
    return player.score