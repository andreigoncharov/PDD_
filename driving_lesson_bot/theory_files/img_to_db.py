import aiomysql
from config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD
import asyncio

class final_step:
    loop = asyncio.get_event_loop()

    @staticmethod
    async def create_con(loop):
        con = await aiomysql.connect(host=DB_HOST, user=DB_USER, db=DB_NAME, password=DB_PASSWORD, loop=loop)
        cur = await con.cursor()
        return con, cur

    @staticmethod
    async def start(nums_name, names_name, texts_name, category, folder_name):
        with open(f"D:/driving_lessons_bot/driving_lesson_bot/theory_files/{nums_name}.txt", "r", encoding='windows-1251') as file:
            for line in file:
                nums = '2.1'
                #nums = [line.rstrip('\n') for line in file]

        with open(f"D:/driving_lessons_bot/driving_lesson_bot/theory_files/{names_name}.txt", "r", encoding='windows-1251') as file:
            for line in file:
                names = '2.1 Уступить дорогу'
                #names = [line.rstrip('\n') for line in file]

        with open(f"D:/driving_lessons_bot/driving_lesson_bot/theory_files/{texts_name}.txt", "r", encoding='windows-1251') as file:
            for line in file:
                text = 'Знак 2.1 При знаке 2.1 "Уступить дорогу" водитель должен уступить дорогу транспортным средствам, которые подъезжают к нерегулируемому перекрестку по главной дороге, а при наличии таблички 7.8  — транспортным средствам, движущимся по главной дороге. Знак устанавливается непосредственно перед перекрестком или узким участком дороги.'
                #text = [line.rstrip('\n') for line in file]

        await final_step.insert_img(nums, names, text, category, folder_name, loop)
                
    
    @staticmethod
    async def insert_img(nums, names, texts, category, folder_name, loop):
        con, cur = await final_step.create_con(loop)
        try:
            #for name, num, text in zip(names, nums, texts):
                        photo = f'D:/driving_lessons_bot/driving_lesson_bot/Знаки/{folder_name}/2.1'+'.png'

                        sql_insert_blob_query = """ INSERT INTO theory
                                          (category ,zn_name, img, text, id_zn) VALUES (%s,%s,%s,%s,%s)"""

                        Picture = final_step.convertToBinaryData(photo)

                        insert_blob_tuple = (category, names, Picture, texts, '2.1')
                        result = await cur.execute(sql_insert_blob_query, insert_blob_tuple)
                        await con.commit()
                        print(nums, ' добавлен')

        except aiomysql.connection.Error as error:
            print(error)
        finally:
                await cur.close()
                con.close()
                print('!!!!!!!ВЫРУБАЙ!!!!!!!!')


    '''@staticmethod
    async def start():
        s='Табличка 7.1.1 "Расстояние до объекта" обозначает дистанцию от знака до начала опасного участка, места введения соответствующего ограничения или определенного объекта (места), расположенного впереди по ходу движения.'
        await final_step.insert_img('7.1.1', '7.1.1 Расстояние до объекта', s, 'Таблички', '7_Таблички к дорожным знакам', final_step.loop)

    @staticmethod
    async def insert_img(num, name, text, category, folder_name, loop):
        con, cur = await final_step.create_con(loop)
        try:
            photo = f'D:/driving_lessons_bot/driving_lesson_bot/Знаки/{folder_name}/{str(num)}' + '_.png'
            sql_insert_blob_query = """ INSERT INTO theory
                                          (category ,zn_name, img, text, id_zn) VALUES (%s,%s,%s,%s,%s)"""
            Picture = final_step.convertToBinaryData(photo)
            insert_blob_tuple = (category, name, Picture, text, num)
            result = await cur.execute(sql_insert_blob_query, insert_blob_tuple)
            await con.commit()
            print(num, ' добавлен')

        except aiomysql.connection.Error as error:
            print(error)
        finally:
            await cur.close()
            con.close()
            print('!!!!!!!ВЫРУБАЙ!!!!!!!!')'''


    @staticmethod
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

nums_filename = 'nums_2'
names_file = 'names_2'
text_file = 'texts_2'
folder_name = '2_Приоритета'
category = 'Приоритета'

loop = asyncio.get_event_loop()
asyncio.ensure_future(final_step.start(nums_filename, names_file, text_file, category, folder_name))
loop.run_forever()
