from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import hints
import sql
import information
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
counter = 0

logging.basicConfig(format="%(levelname)-8s [%(asctime)s] %(message)s", level=logging.INFO, filename="bot.log")


def hello(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Приветсвую Вас в игре "Викторина". Для того чтобы в Ваш сундук начали падать моентки,'
                          ' нужно зарегистрироваться /reg \nЗатем, напишите /go'
                     )


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Не знаю такой команды")


def add_new_player(bot, update):
    sql.add_player(update.message.from_user.id)
    update.message.reply_text('Вы в игре')


def get_question(bot, update, job_queue, chat_data):
    global counter
    if counter == 0:
        counter = 0
        quiz = sql.get_random_question()
        bot.send_message(chat_id=update.message.chat_id, text='Вопрос: ' + quiz[0])
        global answer
        answer = quiz[1]
        global hint_list
        hint_list = hints.hints(answer)
        hints_job = job_queue.run_repeating(print_hint, 5, context=update.message.chat_id)
        chat_data['hints_job'] = hints_job


def comparison(bot, update, job_queue, chat_data):
    global jq
    global counter
    if update.message.text.lower() == answer.lower():
        player = sql.add_point(update.message.from_user.id)
        gold = morph.parse('монета')[0]
        correct_word = gold.make_agree_with_number(player).word
        update.message.reply_text('Правилный ответ! В твоем сундуке {} {}.'.format(player, correct_word))
        counter = 0
        chat_data['hints_job'].schedule_removal()
        get_question(bot, update, job_queue, chat_data)


def print_hint(bot, job):
    global counter
    # if counter == len(answer) - 1:
    #     bot.send_message(chat_id=update.message.from_user.id, text='Никто не отгадал: ' + answer)
    #     counter = 0
    #     chat_data['hints_job'].schedule_removal()
    #     get_question(bot, update, job_queue, chat_data)
    if counter <= len(answer) - 1:
        bot.send_message(
            chat_id=job.context,
            text=hint_list[counter]
        )
        counter += 1


def stop_bot(bot, update):
    updater.stop()


def alive(bot, update):
    updater.start_polling()
    updater.idle()


def start_bot():
    global updater
    updater = Updater(information.token)
    dp = updater.dispatcher

    hello_handler = CommandHandler('start', hello)
    dp.add_handler(hello_handler)

    add_player_handler = CommandHandler('reg', add_new_player)
    dp.add_handler(add_player_handler)

    stop_handler = CommandHandler('stop', stop_bot)
    dp.add_handler(stop_handler)

    alive_handler = CommandHandler('alive', alive)
    dp.add_handler(alive_handler)

    global jq
    jq = updater.job_queue

    dp.add_handler(CommandHandler('go', get_question, pass_chat_data=True, pass_job_queue=True))

    comparison_handler = MessageHandler(Filters.text, comparison, pass_chat_data=True, pass_job_queue=True)
    dp.add_handler(comparison_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    start_bot()
