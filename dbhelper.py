import sqlite3

DATABASE = "database.db"

def get_data(user_id, metric):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute(''' select ''' + metric + ''' from users where id = ? ''', (user_id, ))

    res = c.fetchall()
    if res:
        return res[0][0]
    else:
        return 0

    db.close()

def get_hiscores():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute(''' select * from users ''')

    return c.fetchall()

    db.close()

def add_data(user_id, metric):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    if metric == "tea":
        values = "(?, 1, 0, 0, 0)"
    elif metric == "coffee":
        values = "(?, 0, 1, 0, 0)"
    elif metric == "thanks":
        values = "(?, 0, 0, 1, 0)"
    else:
        values = "(?, 0, 0, 0, 1)"


    c.execute(''' insert into users (id, tea, coffee, thanks, thanks_at) values ''' + values + ''' on conflict(id) do update set ''' + metric + ''' = ''' + metric + ''' + 1 ''', (user_id, ))

    db.commit()
    db.close()
