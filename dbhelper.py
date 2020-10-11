import sqlite3
import constants


def get_top10(metric):
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    c.execute(''' select id,''' + metric + ''' from users order by ''' + metric + ''' desc ''')

    return c.fetchall()[:10]

    db.close()


def get_user_ranks(user):
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    data = []

    for metric in constants.METRICS:
        c.execute(''' select id,''' + metric + ''' from users order by ''' + metric + ''' desc ''')

        lst = c.fetchall()
        rank = [x for x,y in enumerate(lst) if y[0] == user][0]
        score = lst[rank][1]

        data.append((metric, rank, score))

    return data

    db.close()


def add_data(user_id, metric):
    db = sqlite3.connect(constants.DATABASE)
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