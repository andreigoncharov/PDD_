import aiomysql
from pymysql import connect
from config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD
from scripts.models import User
import asyncio
import datetime
import random

'''
SET SQL_SAFE_UPDATES = 0;
для того, чтоб удалять можно было
'''


async def create_con(loop):
    con = await aiomysql.connect(host=DB_HOST, user=DB_USER, db=DB_NAME, password=DB_PASSWORD, loop=loop)
    cur = await con.cursor()
    return con, cur


def create_sync_con():
    con = connect(host=DB_HOST, user=DB_USER, db=DB_NAME,
                  password=DB_PASSWORD)
    cur = con.cursor()
    return con, cur

class UsersDbManager:
    @staticmethod
    def clear():
        con, cur = create_sync_con()
        cur.execute('delete from users')
        con.commit()
        con.close()

    @staticmethod
    async def user_exist(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(*) from users where tel_id = %s', tel_id)
        r = await cur.fetchone()
        count = r[0]
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    async def add_user(tel_id, username, zn_name, loop):
        con, cur = await create_con(loop)
        await cur.execute('insert into users values(%s, %s, %s, %s, %s, %s, %s)', (tel_id, username, '', zn_name, 0, 0, datetime.datetime.now().date()))
        await con.commit()
        await cur.execute('insert into history values(%s, %s, %s, %s)', (tel_id, 0, 0, 0))
        await con.commit()
        con.close()

    @staticmethod
    async def get_user(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from users where tel_id = %s', (tel_id))
        user = await cur.fetchone()
        con.close()

        if user is None:
            return None

        return User(user[0], user[1], user[2])

    @staticmethod
    async def update_language(tel_id, new_language, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set language = %s where tel_id = %s', (new_language, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_context(tel_id, context, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set context = %s where tel_id = %s', (context, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_phone(tel_id, new_phone, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set phone = %s where tel_id = %s', (new_phone, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_context(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select context from users where tel_id = {0}'.format(tel_id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    def sync_get_context(tel_id):
        con, cur = create_sync_con()
        cur.execute('select context from users where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        con.close()

        if context is None:
            return None

        return context[0]

    @staticmethod
    async def insert_img(name, photo, text, loop):
        con, cur = await create_con(loop)
        try:
            sql_insert_blob_query = """ INSERT INTO theory
                              (name, img, text) VALUES (%s,%s,%s)"""

            Picture = UsersDbManager.convertToBinaryData(photo)

            insert_blob_tuple = (name, Picture, text)
            result = await cur.execute(sql_insert_blob_query, insert_blob_tuple)
            await con.commit()
            return True

        except aiomysql.connection.Error as error:
            print(error)
            return False

        finally:
                await cur.close()
                con.close()

    @staticmethod
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    @staticmethod
    async def show_img(name, loop):
        connection, cursor = await create_con(loop)
        try:
            await cursor.execute(f"SELECT * from theory where zn_name like '%{name}%'")

            record = await cursor.fetchall()
            for row in record:
                cat = row[0]
                nam = row[1]
                image = row[2]
                tex = row[3]
                id = row[4]
                return cat, nam, image, tex, id

        except aiomysql.connection.Error as error:
            return  False

        finally:
            connection.close()

    @staticmethod
    async def update_zn_text(tel_id , text, loop):
        con, cur = await create_con(loop)
        name = await UsersDbManager.get_zn_name(tel_id, loop)
        await cur.execute('update theory set text = %s where name = %s', (text, name))
        await con.commit()
        con.close()

    @staticmethod
    async def set_zn_name(tel_id, zn_name, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set zn_name = %s where tel_id = %s', (zn_name, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_zn_name(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select zn_name from users where tel_id=%s', (tel_id))
        name = await cur.fetchone()
        con.close()
        return name[0]

    @staticmethod
    async def update_pp(tel_id, p, pp, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set num_p = %s where tel_id = %s', (p, tel_id))
        await cur.execute('update users set num_pp = %s where tel_id = %s', (pp, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_pp(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select num_p,num_pp from users where tel_id=%s', (tel_id))
        nums = await cur.fetchone()
        con.close()
        return nums

    @staticmethod
    async def get_sign(cat, loop):
        con, cur = await create_con(loop)
        cat= cat[3:]
        await cur.execute('select * from theory where category=%s', (cat))
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def get_sign_2(cat, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from theory where category=%s', (cat))
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def get_sign_text(cat, loop):
        con, cur = await create_con(loop)
        cat = cat[3:]
        await cur.execute('select text from theory where category=%s', (cat))
        result = await cur.fetchall()
        con.close()
        return result


    @staticmethod
    async def name(loop):
        con, cur = await create_con(loop)
        await cur.execute('select id_zn from theory where category=%s', ('Таблички'))
        name = await cur.fetchall()
        con.close()

    @staticmethod
    async def sel(loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from test where id=1')
        result = await cur.fetchone()
        con.close()
        return result

    @staticmethod
    async def get_q(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from test where cat=%s', (id))
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def get_rand_q(loop):
        con, cur = await create_con(loop)
        print(00000000)
        await cur.execute('SELECT * FROM driving_lessons_bot.test ORDER BY RAND() LIMIT 20;')
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def add_to_q(tel_id, nums, loop):
        con, cur = await create_con(loop)
        s = ''
        for num in nums:
          s += str(num[0])
          s += ','
        await cur.execute('insert into for_test values(%s, %s, %s, %s, %s, %s)', (tel_id, datetime.datetime.now(), 0, s, 20, 0))
        await con.commit()
        con.close()

    @staticmethod
    async def update_error(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update for_test set er = er+1 where tel_id = %s', (tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_right_answer(tel_id, right_answ, loop):
        con, cur = await create_con(loop)
        await cur.execute('update for_test set right_answ = %s where tel_id = %s', (right_answ, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def for_new_q(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select num from for_test where tel_id=%s', (id))
        result = await cur.fetchall()
        s = str(result[0])
        s = s.replace(')', '')
        s = s.replace("\\", '')
        s = s.replace("'", '')
        d= s.find(',')
        num = s[:d]
        s = s[d+1:]
        await cur.execute('update for_test set num = %s where tel_id = %s', (s,id))
        await con.commit()
        await cur.execute('update for_test set count = count-1 where tel_id = %s', (id))
        await con.commit()
        await cur.execute('select count from for_test where tel_id=%s', (id))
        result = await cur.fetchone()
        await cur.execute('select time from for_test where tel_id=%s', (id))
        time = await cur.fetchone()
        time = time[0]
        time = (datetime.datetime.now() - time)
        time = time.seconds/60
        await cur.execute('select er from for_test where tel_id=%s', (id))
        errors = await cur.fetchone()
        await cur.execute('select right_answ from for_test where tel_id=%s', (id))
        right_answer = await cur.fetchone()
        con.close()
        return num[1:], result[0], time, errors[0], right_answer[0]

    @staticmethod
    async def new_q(d, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from test where id=%s', (d))
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def update_history_s(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update history set count = count+1 where tel_id = %s', (tel_id))
        await con.commit()
        await cur.execute('update history set count_s = count_s+1 where tel_id = %s', (tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_history_e(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update history set count = count+1 where tel_id = %s', (tel_id))
        await con.commit()
        await cur.execute('update history set count_e = count_e+1 where tel_id = %s', (tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_errors(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update for_test set er = er+1 where tel_id = %s', (tel_id))
        await con.commit()
        con.close()

    @staticmethod
    def clear_test(tel_id):
        con, cur = create_sync_con()
        cur.execute('delete from for_test where tel_id = %s', (tel_id))
        con.commit()
        con.close()

    @staticmethod
    async def history(d, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from history where tel_id=%s', (d))
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def for_stat(loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(*) from users')
        count =  await cur.fetchone()
        await cur.execute("select count(tel_id) from users where date_format(date_r, '%Y%m') = date_format(now(), '%Y%m')")
        count_new = await cur.fetchone()
        await cur.execute('select count(*) from history')
        count_t = await cur.fetchone()
        await cur.execute('SELECT sum(count_s) FROM history')
        count_r = await cur.fetchone()
        await cur.execute('SELECT sum(count_e) FROM history')
        count_e = await cur.fetchone()
        await cur.execute('SELECT avg(count) FROM driving_lessons_bot.history')
        sr = await cur.fetchone()
        con.close()
        return count[0], count_new[0], count_t[0], count_r[0], count_e[0], sr[0]

    @staticmethod
    async def all_users(loop):
        con, cur = await create_con(loop)
        await cur.execute('select tel_id from users')
        result = await cur.fetchall()
        con.close()
        return result

    @staticmethod
    async def get_sign_for_detection(name, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'SELECT * FROM theory where zn_name like "%{name}%"')
        result = await cur.fetchall()
        con.close()
        return result
