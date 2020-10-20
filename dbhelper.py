import sqlite3
import constants
import asyncio


async def get_top10(metric):
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    c.execute(''' select id,''' + metric + ''' from users order by ''' + metric + ''' desc ''')

    res = c.fetchall()[:10]
    if not res:
        return []

    return res
    db.close()


async def get_user_ranks(user):
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    data = []

    for metric in constants.METRICS:
        c.execute(''' select id,''' + metric + ''' from users order by ''' + metric + ''' desc ''')

        lst = c.fetchall()
        if not lst:
            data.append((metric, "-", 0))
        else:
            rank = [x for x,y in enumerate(lst) if y[0] == user][0]
            score = lst[rank][1]

            data.append((metric, rank, score))

    return data
    db.close()


async def get_total_data():
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    data = []

    for metric in constants.METRICS:
        c.execute(''' select sum(''' + metric + ''') from users ''')

        lst = c.fetchall()
        if not lst:
            data.append((metric, 0))
        else:
            data.append((metric, lst[0][0]))

    return data
    db.close()


async def add_data(user_id, metric):
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    if metric == "tea":
        values = "(?, 1, 0, 0, 0, 0)"
    elif metric == "coffee":
        values = "(?, 0, 1, 0, 0, 0)"
    elif metric == "thanks":
        values = "(?, 0, 0, 1, 0, 0)"
    elif metric == "thanks_at":
        values = "(?, 0, 0, 0, 1, 0)"
    else:
        values = "(?, 0, 0, 0, 0, 1)"


    c.execute(''' insert into users (id, tea, coffee, thanks, thanks_at, no_thanks) values ''' + values + ''' on conflict(id) do update set ''' + metric + ''' = ''' + metric + ''' + 1 ''', (user_id, ))

    db.commit()
    db.close()

async def remove_data(user_id, metric):
    db = sqlite3.connect(constants.DATABASE)
    c = db.cursor()

    c.execute(''' update users set ''' + metric + ''' = ''' + metric + ''' - 1 ''')

    db.commit()
    db.close()
