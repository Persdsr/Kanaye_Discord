import sqlite3


def register_profile(answers, user_discord_id):
    db = sqlite3.connect('database/Kanaye.db')
    cursor = db.cursor()

    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()
    if all_users:
        for id_user in range(len(all_users[0])):
            if all_users[0][id_user] == user_discord_id:
                print('Такой уже есть!')
                return None

        last_user = all_users[-1]
        user_id = last_user[0] + 1
    else:
        user_id = 1

    username = answers[0]
    age = answers[1]
    description = answers[2]
    photo = answers[3]
    is_active = 0
    level = 0
    message_count = 0
    cursor.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, user_discord_id, username, age, description, photo, level, message_count, is_active))
    print('Регистрация прошла')
    db.commit()
    return True


def get_profile(user_id):
    db = sqlite3.connect('database/Kanaye.db')
    cursor = db.cursor()

    user_info = cursor.execute('SELECT username, age, description, photo, chat_level FROM users WHERE user_id=?',
                               (user_id,)).fetchall()[0]
    profile = {
        'username': user_info[0],
        'age': user_info[1],
        'description': user_info[2],
        'photo': user_info[3],
        'lvl': user_info[4]
    }
    return profile


def get_is_admin(user_id):
    db = sqlite3.connect('database/Kanaye.db')
    cursor = db.cursor()

    cursor.execute('SELECT is_admin FROM users WHERE user_id=?', (user_id,))
    answer = cursor.fetchall()[0][0]
    return answer


def get_level(user_id):
    db = sqlite3.connect('database/Kanaye.db')
    cursor = db.cursor()
    response = ''
    user_info = cursor.execute('SELECT chat_level, message_count FROM users WHERE user_id=?', (user_id, )).fetchall()[0]
    cursor.execute('UPDATE users SET message_count=? WHERE user_id=?', (user_info[1] + 1, user_id))
    if user_info[1] % 30 == 0:
        cursor.execute('UPDATE users SET chat_level=? WHERE user_id=?', (user_info[0] + 1, user_id))
        response = f'Ваш лвл был повышен до {user_info[0] + 1}'
    db.commit()
    return response


