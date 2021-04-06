"""PART 2

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
from parser_bs import Parser
import re
import os


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


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    # напишите вашу реализацию логики по вычисления кратчайшего пути здесь
    files = create_tree(path)
    level = dict.fromkeys(files, -1)
    level[start_page] = 0
    queue = Queue()
    queue.enqueue(start_page)

    while not queue.isEmpty():
        v = queue.dequeue()
        for w in files[v]:
            if level[w] == -1:
                queue.enqueue(w)
                level[w] = level[v] + 1

    bridge = [end_page]
    pos = level[end_page]

    while pos != 0:
        for lv in level.keys():
            if level[lv] != pos - 1 or bridge[len(bridge) - 1] not in files[lv]:
                continue
            bridge.append(lv)
            pos -= 1
            break
    bridge.reverse()
    return bridge


if __name__ == '__main__':
    result = build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age')
    print(result)
