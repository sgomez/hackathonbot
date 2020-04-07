from application import bot
from random import randint
from model.chat import Chat


@bot.message_handler(commands=['play'])
def game_play(message):
    chat_id = message.chat.id
    reply = bot.send_message(
        chat_id, "Adivina el número que he pensado del 1 al 100")

    number = randint(1, 10)
    Chat.set(chat_id, "game_number", number)
    Chat.set(chat_id, "game_steps", 1)

    bot.register_next_step_handler(reply, game_process_response)


def game_process_response(message):
    chat_id = message.chat.id

    number = int(Chat.get(chat_id, 'game_number'))
    steps = int(Chat.get(chat_id, 'game_steps'))
    guess_number = int(message.text)

    if (number == guess_number):
        bot.send_message(
            chat_id, f"Enhorabuena has acertado en {steps} pasos")
        return

    if (guess_number > number):
        reply = bot.send_message(chat_id, "El número es más pequeño")
    else:
        reply = bot.send_message(chat_id, "El número es más grande")

    Chat.set(chat_id, "game_steps", 1 + steps)
    bot.register_next_step_handler(reply, game_process_response)
