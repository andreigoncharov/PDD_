import urllib.request
from bs4 import BeautifulSoup
import requests
from lxml import html
import fileinput
import time

url_for_download = "https://vodiy.ua"


class download_imgs:
    @staticmethod
    def download_first(url, links_file, nums_file, folder_name):
        with open(f"{links_file}.txt", "r", encoding='windows-1251') as file:
            first_link = file.readline()
            print(first_link)

        with open(f"{nums_file}.txt", "r", encoding='windows-1251') as file:
            first_num = file.read(3)
            print(first_num)

        url += first_link
        img = urllib.request.urlopen(url).read()
        out = open(f"C:/Users/andre/PycharmProjects/driving_lesson_bot/Розметка/{folder_name}/{first_num}_.png",
                   "wb")
        out.write(img)
        out.close()
        print(first_num + ' : скачан')

    @staticmethod
    def download_rest(url, links_file, nums_file):
        with open(f"{links_file}.txt", "r", encoding='windows-1251') as file:
            for line in file:
                links = [line.rstrip('\n') for line in file]

        with open(f"{nums_file}.txt", "r", encoding='windows-1251') as file:
            for line in file:
                nums = [line.rstrip('\n') for line in file]

        for link, num in zip(links, nums):
            url += link
            img = urllib.request.urlopen(url).read()
            out = open(
                f"C:/Users/andre/PycharmProjects/driving_lesson_bot/Розметка/{folder_name}/{num}_.png",
                "wb")
            out.write(img)
            out.close()
            url = "https://vodiy.ua"
            print(num + ' : скачан')

    @staticmethod
    def get_links(url, links_name, number):
        response = requests.get(f'https://vodiy.ua/ru/znaky/{number}/')
        parsed_body = html.fromstring(response.text)

        links = open(f'C:/Users/andre/PycharmProjects/driving_lesson_bot/theory_files/{links_name}.txt', 'w')

        # Парсим ссылки с картинками
        images = parsed_body.xpath('//ul/li/a/img/@src')
        for im in images:
            links.write(str(im) + '\n')
        print('Ссылок на картинки: ' + str(len(images)))
        links.close()

    @staticmethod
    def get_nums(url, nums_name, number):
        response = requests.get(f'https://vodiy.ua/ru/znaky/{number}/')
        parsed_body = html.fromstring(response.text)

        nums = open(f'theory_files/{nums_name}.txt', 'w')

        # Парсим ссылки с картинками
        images = parsed_body.xpath('//ul/li/a/span/mark')
        l = len(images)
        for im in images:
            nums.write(str(im.text) + '\n')
            time.sleep(0.1)
            # Update Progress Bar
        nums.close()


    @staticmethod
    def get_html(url):
        response = urllib.request.urlopen(url)
        return response.read()

    def parse_text(html):
        soup = BeautifulSoup(html)
        table = soup.find('div', class_='mark_markpage_block')
        cols = table.find('p')
        print(cols.text)
        return cols.text + '\n'

    @staticmethod
    def parse_name(html):
        soup = BeautifulSoup(html)
        table = soup.find('div', class_='mark-markpage')
        cols = table.find('h2')
        print(cols.text)
        return cols.text

    @staticmethod
    def save(projects, path):
        with open(path, 'a') as file:
            file.write(str(projects))

    @staticmethod
    def main_to_text(num, num_file, name_file, new_text_file):
        BASE_URL = f'https://vodiy.ua/ru/znaky/{num}/'

        projects = ''

        with open(f"{num_file}.txt", "r", encoding='windows-1251') as file:
            first_num = file.read(3)
            print(first_num)

        with open(f"{num_file}.txt", 'r', encoding='windows-1251') as file:
            for line in file:
                nums = [line.rstrip('\n') for line in file]

        projects += download_imgs.parse_text(download_imgs.get_html(BASE_URL + first_num))

        for numb in nums:
            projects += download_imgs.parse_text(download_imgs.get_html(BASE_URL + numb))

        print('Сохранение...')

        download_imgs.save(projects, f'{new_text_file}.txt')

    @staticmethod
    def main_to_name(num, num_file, new_names_file):
        BASE_URL = f'https://vodiy.ua/ru/znaky/{num}/'

        projects = ''

        with open(f"{num_file}.txt", "r", encoding='windows-1251') as file:
            first_num = file.read(3)
            print(first_num)

        with open(f"{num_file}.txt", 'r', encoding='windows-1251') as file:
            for line in file:
                nums = [line.rstrip('\n') for line in file]
        print(first_num)
        projects += download_imgs.parse_name(download_imgs.get_html(BASE_URL + first_num))

        for numb in nums:
            projects += download_imgs.parse_name(download_imgs.get_html(BASE_URL + numb))

        print('Сохранение...')

        download_imgs.save(projects, f'{new_names_file}.txt')

    @staticmethod
    def edit(filename):
        with fileinput.FileInput(f'{filename}.txt', inplace=True) as file:
            for line in filename:
                print(line.replace('									', ''), end='')
        clean_lines = []
        with open(f'{filename}.txt', "r") as f:
            lines = f.readlines()
            clean_lines = [l.strip() for l in lines if l.strip()]

        with open(f'{filename}.txt', "w") as f:
            f.writelines('\n'.join(clean_lines))

    @staticmethod
    def clean_nums(what, filename):
        with fileinput.FileInput(f'{filename}.txt', inplace=True) as file:
            for line in file:
                print(line.replace(f'{what}', ''), end='')


url = 'https://vodiy.ua/ru/znaky/'
number = '5'
nums_filename = 'Numbers_5'
links_filename = ''
names_file = 'Names_5'
text_file = 'Text_5'
folder_name = '5_Информационно-указательные знаки'


download_imgs.get_nums(url_for_download, nums_filename, number)
#download_imgs.get_links(url_for_download, links_filename, number)
download_imgs.edit(nums_filename)
#download_imgs.download_first(url_for_download, links_filename, nums_filename, folder_name)
#download_imgs.download_rest(url_for_download, links_filename, nums_filename)
download_imgs.main_to_name(number, nums_filename, names_file)
download_imgs.edit(names_file)
download_imgs.main_to_text(number, nums_filename, names_file, text_file)


