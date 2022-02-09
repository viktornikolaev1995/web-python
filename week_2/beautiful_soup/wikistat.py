import os
import re
import sys
from collections import deque
from bs4 import BeautifulSoup
import unittest


def parse(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
        search_div = soup.find("div", {'id': 'bodyContent'})
        search_img = search_div.find_all('img')
        imgs = []
        headers = []
        for i in search_img:
            try:
                if int(i['width']) >= 200:
                    imgs.append(i)
            except KeyError as error:
                pass
                # print(error)
        search_headers = search_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for i in search_headers:
            if i.text[0] in ['E', 'T', 'C']:
                headers.append(i.text)

        adj = {}
        search_a = search_div.find_all('a')

        for idx, i in enumerate(search_a):

            if i.find_previous_sibling():
                try:
                    if i.find_previous_sibling().name == 'a':
                        # print(i.find_previous_sibling().name)
                        if idx not in adj.keys():
                            adj[idx] = set()
                            adj[idx].add(idx-1)
                        else:
                            adj[idx].add(idx-1)
                except AttributeError as error:
                    pass
                    # print(error)

            if i.find_next_sibling():
                try:
                    if i.find_next_sibling().name == 'a':
                        if idx not in adj.keys():
                            adj[idx] = set()
                            adj[idx].add(idx+1)
                        else:
                            adj[idx].add(idx+1)
                except AttributeError as error:
                    pass
                    # print(error)
        # print(adj)

        distances = {i: None for i in adj.keys()}
        start_vertex = 0
        distances[start_vertex] = 0
        queue = deque(list(adj.keys()))
        # print(queue)
        queue1 = deque([])

        while queue:
            # print('************************')
            cur_v = queue.popleft()
            queue1.append(cur_v)
            # print(f'cur_v: {cur_v}')
            distances[cur_v] = 1
            for i in adj[cur_v]:
                if i in queue1:
                    distances[cur_v] = distances[i] + 1
        # print(adj)
        # print(distances)
        linkslen = [distances[key] for key in distances.keys()]



        # print(search_ul_ol)
        lists = []
        search_ul_ol = search_div.find_all(['ul', 'ol'])
        ch = []
        # print(len(search_ul_ol))
        count = 0
        for child in search_div.recursiveChildGenerator():
            if child.name in ['ul', 'ol']:
                count += 1
                child['id'] = count
                ch.append(child)
                # print(child.name, child['id'])
        # print(len(ch))
        children = {}
        for i in search_ul_ol:
            children[i['id']] = {e['id'] for e in i.descendants if e.name is not None and e.name in ['ul', 'ol']}
        # print(children)
        distances1 = {i: None for i in children.keys()}
        queue2 = deque(list(children.keys()))
        nested_tags = []
        require_tags = []
        while queue2:
            # print("************************")
            # print(f'queue2: {queue2}')
            # print(f'children: {children}')
            cur = queue2.popleft()
            # print(f'cur: {cur}')
            if len(children[cur]) == 0 and (cur not in nested_tags):
                require_tags.append(cur)
                # print(1, True)
            elif len(children[cur]) > 0 and (cur not in nested_tags):
                require_tags.append(cur)
                for tag in children[cur]:
                    if tag not in nested_tags:
                        nested_tags.append(tag)
                # print(2, True)
            elif len(children[cur]) > 0 and (cur in nested_tags):
                for tag in children[cur]:
                    if tag not in nested_tags:
                        nested_tags.append(tag)
            #     print(3, True)
            # print(f'require_tags: {require_tags}')
            # print(f'nested_tags: {nested_tags}')
            # print("************************")

                    # for i in lists:
        #     print("******************")
        #     print(f'element: {i}')
        #     print(f'parent: {i.parent}')
        #     print("*****************")
        # print(len(lists))
        # print(len(search_ul_ol))
        # print(len(require_tags))
        # print(len(nested_tags))
        return [len(imgs), len(headers), max(linkslen), len(require_tags)]
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    # return [imgs, headers, linkslen, lists]


# class TestParse(unittest.TestCase):
#     def test_parse(self):
#         test_cases = (
#             ('wiki/Stone_Age', [13, 10, 12, 40]),
#             ('wiki/Brain', [19, 5, 25, 11]),
#             ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
#             ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
#             ('wiki/Spectrogram', [1, 2, 4, 7]),)
#
#         for path, expected in test_cases:
#             with self.subTest(path=path, expected=expected):
#                 self.assertEqual(parse(path), expected)



# print(parse('wiki/Stone_Age'))


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = init_graph
        # self.construct_graph(nodes, init_graph) симметричность в данной задачи не требуется

    def construct_graph(self, nodes, init_graph):
        '''
        Этот метод обеспечивает симметричность графика. Другими словами, если существует путь от узла A к B со значением V, должен быть путь от узла B к узлу A со значением V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Возвращает узлы графа"
        return self.nodes

    def get_outgoing_edges(self, node):
        "Возвращает соседей узла"
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Возвращает значение ребра между двумя узлами."
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    # Мы будем использовать этот словарь, чтобы сэкономить на посещении каждого узла и обновлять его по мере продвижения по графику
    shortest_path = {}

    # Мы будем использовать этот dict, чтобы сохранить кратчайший известный путь к найденному узлу
    previous_nodes = {}

    # Мы будем использовать max_value для инициализации значения "бесконечности" непосещенных узлов
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # Однако мы инициализируем значение начального узла 0
    shortest_path[start_node] = 0

    # Алгоритм выполняется до тех пор, пока мы не посетим все узлы
    while unvisited_nodes:
        # Приведенный ниже блок кода находит узел с наименьшей оценкой
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # После посещения его соседей мы отмечаем узел как "посещенный"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Добавить начальный узел вручную
    path.append(start_node)

    # print("Найден следующий лучший маршрут с ценностью {}.".format(shortest_path[target_node]))
    # print(" -> ".join(reversed(path)))
    path.reverse()
    return path



def build_bridge(path, start, end):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    with open(os.path.join(path, start), encoding="utf-8") as file:
        # print(ascii(os.path.join(path,start)))
        start_links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
    nested_start_links = {}
    all_files = {}
    all_nested_files = {}
    all_indices = {}
    for path, dirs, files in os.walk(path):
        for idx, file in enumerate(files):
            all_files[idx] = file
            all_indices[file] = idx
        for key, value in all_files.items():
            with open(os.path.join(path, value), encoding="utf-8") as nested_file:
                nested_links = re.findall(r"(?<=/wiki/)[\w()]+", nested_file.read())
                exist_nested_links = {link: 1 for link in set(nested_links) if link in files and link != value}
                all_nested_files[value] = exist_nested_links

    # print(all_nested_files[index])
    # links = [all_files[idx] for idx in all_nested_files[index]]
    # print(links)
    # print(all_nested_files[index1])
    # print(all_files)
    # print(all_indices)
    nodes = list(all_nested_files.keys())
    init_graph = all_nested_files
    graph = Graph(nodes, init_graph)
    # print(graph.graph)
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=start)
    return print_result(previous_nodes, shortest_path, start_node=start, target_node=end)


# print(build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age'))
# print(build_bridge('wiki/', 'Stone_Age', 'Python_(programming_language)'))
# print(build_bridge('wiki/', 'Artificial_intelligence', 'Mei_Kurokawa'))
# print(build_bridge('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing"))


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    statistic = {}
    for link in pages:
        link_statistic = parse(os.path.join(path, link))
        statistic[link] = link_statistic
    return statistic

# print(get_statistics('wiki/', 'Stone_Age', 'Python_(programming_language)'))