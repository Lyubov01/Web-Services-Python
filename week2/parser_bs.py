from bs4 import BeautifulSoup
import unittest

"""
PART 1

В этом задании вам необходимо реализовать парсер для сбора статистики со страниц Википедии. Чтобы упростить вашу 
задачу, необходимые страницы уже скачаны и сохранены на файловой системе в директории wiki/ (Например, 
страница https://en.wikipedia.org/wiki/Stone_Age сохранена файле wiki/Stone_Age).Парсер реализован в виде функции 
parse, которая принимает на вход один параметр: path_to_file — путь до файла, содержащий html код страницы википедии. 
Гарантируется, что такой путь существует. Ваша задача — прочитать файл, пройтись Beautiful Soup по статье, 
найти её тело (это <div id="bodyContent">) и внутри него подсчитать ... 

PART 2 

В этом задании продолжаем работать со страницами из wikipedia. Необходимо реализовать механизм сбора статистики по 
нескольким страницам. Сложность задачи состоит в том, что сначала нужно будет определить страницы, с которых 
необходимо собирать статистику. В качестве входных данных служат названия двух статей(страниц). Гарантируется, 
что файлы обеих статей есть в папке wiki и из первой статьи можно попасть в последнюю, переходя по ссылкам только на 
те статьи, копии которых есть в папке wiki. 

Например, на вход подаются страницы: Stone_Age и Python_(
programming_language). В статье Stone_Age есть ссылка на Brain, в ней на Artificial_intelligence, а в ней на Python_(
programming_language) и это кратчайший путь от Stone_Age до Python_(programming_language). Ваша задача — найти самый 
короткий путь (гарантируется, что существует только один путь минимальной длины), а затем с помощью функции parse из 
предыдущего задания собрать статистику по всем статьям в найденном пути. """
import os
import re


class Parser:
    def __init__(self, path_to_file):
        with open(path_to_file, "r", encoding='utf-8') as f:
            soup = BeautifulSoup(f, "lxml")
            self.body = soup.find(id='bodyContent')

    def img_count(self):
        """Количество картинок (img) с шириной (width) не меньше 200. Например: <img width="200">, но не <img> и не
        <img width="199"> """
        counter = 0
        tags = self.body('img')
        for tag in tags:
            try:
                if int(tag['width']) >= 200:
                    counter += 1
            except KeyError:
                continue

        return counter

    def header_count(self):
        """Количество заголовков (h1, h2, h3, h4, h5, h6), первая буква текста внутри которых соответствует заглавной
        букве E, T или C. Например: <h1>End</h1> или <h5><span>Contents</span></h5>, но не <h1>About</h1> и не
        <h2>end</h2> и не <h3><span>1</span><span>End</span></h3> """
        counter = 0
        tags = dict(zip([f"h{i}" for i in range(1, 7)], [self.body(f"h{i}") for i in range(1, 7)]))
        for head in tags:
            for tag in tags[head]:
                for t in tag.children:
                    t = str(t.string)
                    if t[0] in 'ETC':
                        counter += 1
        return counter

    @staticmethod
    def link_len(links):
        max_len = 1
        for i in range(len(links)):
            if str(links[i])[1] == 'a':
                max_len += 1
            else:
                break
        return max_len

    def max_link_len(self):
        """Длина максимальной последовательности ссылок, между которыми нет других тегов, открывающихся или
        закрывающихся. Например: <p><span><a></a></span>, <a></a>, <a></a></p> - тут 2 ссылки подряд,
        т.к. закрывающийся span прерывает последовательность. <p><a><span></span></a>, <a></a>, <a></a></p> - а тут 3
        ссылки подряд, т.к. span находится внутри ссылки, а не между ссылками. """
        len_ = 0
        tags = self.body('a')
        for tag in tags:
            temp = self.link_len(tag.find_next_siblings())
            if temp > len_:
                len_ = temp
        return len_

    def lists_count(self):
        """Количество списков (ul, ol), не вложенных в другие списки. Например: <ol><li></li></ol>,
        <ul><li><ol><li></li></ol></li></ul> - два не вложенных списка (и один вложенный) """
        counter = 0
        tags = self.body.find_all(['ul', 'ol'])
        for tag in tags:
            if not tag.find_parents(['ul', 'ol']):
                counter += 1
        return counter


def create_tree(path):
    """построение дерева в виде словаря имя файла: список файлов, на которые он содержит ссылки"""
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # поиск ссылок
    files = dict.fromkeys(os.listdir(path))  # словарь, который нужно заполнить :)

    for file in files:
        files[file] = []
        with open(os.path.join(path, file), encoding="utf-8") as reader:
            refs_list = link_re.findall(reader.read())

        for ref in set(refs_list):
            if ref not in files:
                continue
            files[file].append(ref)
    return files

    # files = dict.fromkeys(os.listdir(path))
    # for file in files:
    #    files[file] = []
    #    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
    #        refs_list = re.findall(r"(?<=/wiki/)[\w()]+", f.read())
    #    for ref in set(refs_list):
    #        try:
    #            open(os.path.join(path, ref), 'r')
    #            files[file].append(ref)
    #        except FileNotFoundError:
    #            continue
    #

    # d = {}
    # first_file = os.path.join(path, start_page)
    # last_file = os.path.join(path, end_page)
    # with open(first_file, 'r') as first:
    #    links = set(re.findall(r"(?<=/wiki/)[\w()]+", first.read()))
    # for link in links:
    #    try:
    #        with open(os.path.join(path, link), 'r') as link_file:
    #            d[link] = set(re.findall(r"(?<=/wiki/)[\w()]+", link_file.read()))
    #    except FileNotFoundError:
    #        continue


#
# return links
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.items:
            deq_item = self.items[0]
            self.items.pop(0)
            return deq_item





def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь

    return statistic


def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    parser = Parser(path_to_file)
    imgs = parser.img_count()
    headers = parser.header_count()
    linkslen = parser.max_link_len()
    lists = parser.lists_count()
    return [imgs, headers, linkslen, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)
        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    # unittest.main()
    result = build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age')
    print(result)

    # print('Stone_Age' in os.listdir('wiki'))
    # print(create_tree('wiki', None, None))
