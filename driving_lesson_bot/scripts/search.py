from scripts.db_manager import UsersDbManager as db
import urllib.request
import requests
from lxml import html
import re
import asyncio


async def get_item_description(item, loop):
    category = item[0]
    name = item[1]
    id = item[4]
    text = item[3]
    image_url = f'https://vodiy.ua/media/trafficsign_image/{str(item[4])}.png'
    cat = 0
    if category == 'Предупреждающие':
        cat = 1
    elif category == 'Приоритета':
        cat = 2
    elif category == 'Запрещающие':
        cat = 3
    elif category == 'Предписывающие':
        cat = 4
    elif category == 'Инф-Указ':
        cat = 5
    elif category == 'Сервис':
        cat = 6
    elif category == 'Таблички':
        cat = 7

    theory = await sign_description(cat, id)

    text = '''<b>{0}</b>

<i>Категория:</i>: {1}

Описание: {2}
{3}
'''.format(name, category, text, theory)

    if image_url != 'https://www.service-market.com.ua/uploads/shop/products/../nophoto/nophoto.jpg':
        text += '''<a href="{0}">Картинка</a>'''.format(image_url)
    return text

async def get_description(item, loop):
    category = item[0]
    name = item[1]
    id = item[4]
    text = item[3]
    image_url = None
    image_url = f'https://vodiy.ua/media/trafficsign_image/{str(item[4])}r.png'
    if image_url == None:
        image_url = f'https://vodiy.ua/media/trafficsign_image/{str(item[4])}_r.png'
    cat = 0
    if category == 'Горизонтальная':
        cat = 1
    elif category == 'Вертикальная':
        cat = 2
    theory = ''
    th = await razm_description(cat, id)
    if th == 'None':
        theory = ' '
    elif th != 'None':
        theory = th

    text = '''<b>{0}</b>

<i>Категория:</i>: {1}

Описание: {2}
{3}
'''.format(name, category, text, theory)

    if image_url != 'https://www.service-market.com.ua/uploads/shop/products/../nophoto/nophoto.jpg':
        text += '''<a href="{0}">Картинка</a>'''.format(image_url)
    return text

async def sign_description(cat, num):
    response = requests.get(f'https://vodiy.ua/ru/znaky/{cat}/{num}')
    parsed_body = html.fromstring(response.text)
    text_string = ''
    text = parsed_body.xpath(f"//div[@class='mark_markpage_block']/p")
    for st in text:
        text_string += str(st.text)
    return text_string

async def razm_description(cat, num):
    response = requests.get(f'https://vodiy.ua/ru/rozmitka/{cat}/{num}')
    parsed_body = html.fromstring(response.text)
    text_string = ''
    text = parsed_body.xpath(f"//div[@class='mark_markpage_block']/p")
    for st in text:
        text_string += str(st.text)
    if text_string == None:
        return ' '
    else:
        return text_string



async def main_to_text(num, number):
    response = requests.get(f'https://vodiy.ua/ru/pdr/{num}/')
    parsed_body = html.fromstring(response.text)
    text_string = ''
    text = parsed_body.xpath(f"//div[@id='elem{number}']/span[2]")
    for st in text:
        text_string += str(st.text_content())
    text_string.rstrip()
    text_string = re.sub(r'\s+', '  ', text_string)

    return text_string

async def get_count(num):
    response = requests.get(f'https://vodiy.ua/ru/pdr/{num}/')
    parsed_body = html.fromstring(response.text)
    count = parsed_body.xpath("//span[@class='number']/a")
    return len(count)

async def get_html(url):
        response = urllib.request.urlopen(url)
        return response.read()

async def parse_text(num):
        response = requests.get(f'https://vodiy.ua/ru/pdr/{num}/')
        parsed_body = html.fromstring(response.text)
        text = parsed_body.xpath("//span/p[1]")
        return
loop = asyncio.get_event_loop()

