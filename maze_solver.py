import math
import random
from collections import defaultdict
import pygame as pg
import os
from math import inf

global dim, tmp_maze, visited, maze, box_size, win, s, start, end, tru_path
dim = (70, 40)
box_size = 20
tru_path = []
tmp_maze = defaultdict(lambda: [])
maze = defaultdict(lambda: [])
start = None
end = None


def pre_draw():
    global start, end, dim, s, win, box_size, maze

    win.fill((0, 0, 0))
    s = pg.Surface(win.get_size(), pg.SRCALPHA, 32)
    draw_field()

    for i in maze.items():
        x, y = i[0][0] * box_size + box_size//2, i[0][1] * box_size + box_size//2
        for j in i[1]:
            x1, y1 = j[0] * box_size + box_size // 2, j[1] * box_size + box_size // 2
            pg.draw.line(s, (255, 255, 255), (x, y), (x1, y1), box_size//2)


    x, y = box_size * start[0] + box_size // 2, box_size * start[1] + box_size // 2
    pg.draw.circle(s, (255, 0, 0), (x, y), box_size // 2)

    x, y = box_size * end[0] + box_size // 2, box_size * end[1] + box_size // 2
    pg.draw.circle(s, (0, 255, 0), (x, y), box_size // 2)



    win.blit(s, (0, 0))
    pg.display.flip()


def draw_path():
    pass

def draw_get_graph(current):
    global s, win, box_size

    x, y = box_size * current[0] + box_size // 2, box_size * current[1] + box_size // 2
    pg.draw.circle(s, (0, 255, 255), (x, y), box_size // 3, 1)

    win.blit(s, (0, 0))
    pg.display.flip()

def get_graph():
    global start, end, s, win, box_size, maze
    graph = defaultdict(lambda: [])
    visited = set()

    visited.add(start)
    # [ ((came_fome), (to), len), () () ]
    queue = []
    for i in maze[start]:
        queue.append((start, i, 1))


    current = None
    while current != end:
        came_from, current, len = queue.pop(-1)
        visited.add(current)

        if check_needed(current) or current == end:
            graph[came_from].append((current, len))
            graph[current].append((came_from, len))
            draw_get_graph(current)


            came_from = current
            len = 0

        for i in maze[current]:
            if i not in visited:
                queue.append((came_from, i, len + 1))

    # def recurc(current, came_from, len):
    #     visited.add(current)
    #     if check_needed(current) or current == end:
    #         graph[came_from].append((current, len))
    #         graph[current].append((came_from, len))
    #         came_from = current
    #         len = 0
    #
    #
    #     for i in maze[current]:
    #         if i not in visited:
    #             recurc(i, came_from, len + 1)
    # visited.add(start)
    # for i in maze[start]:
    #     recurc(i, start, 1)

    # for i in graph.items():
    #     print(i)
    # print(len(graph.keys()))

    return graph



def check_needed(current):
    global  maze

    if len(maze[current]) != 2:
        return True
    tmp1 = maze[current][0]
    tmp2 = maze[current][1]
    if tmp1[0] == tmp2[0] or tmp1[1] == tmp2[1]:
        return False

    return True

def dijkstra():
    global start, end, true_path
    pre_draw()
    tree = get_graph()

    ans = defaultdict(lambda : inf)
    ans[start] = 0
    visited = set()
    all_vertices = set(tree.keys())
    path = defaultdict()
    while  not all_vertices.issubset(visited):  # marked out all vertices
        v = min([x for x in (all_vertices - visited)], key=lambda x: ans[x])
        visited.add(v)

        for u, wu in tree[v]:
            if u == end:
                path[u] = v

                tmp_vert = end
                true_path = [end]
                while tmp_vert != start:
                    tmp_vert = path[tmp_vert]
                    true_path = [tmp_vert] + true_path


                return
            if ans[u] > wu + ans[v]:
                ans[u] = wu + ans[v]
                path[u] = v



def get_friends(pos):
    global tmp_maze, visited
    ans = []

    if tmp_maze[(pos[0] + 1, pos[1])] == 0 and (pos[0] + 1, pos[1]) not in visited :
        ans.append((pos[0] + 1, pos[1]))

    if tmp_maze[(pos[0], pos[1] + 1)] == 0 and (pos[0], pos[1] + 1) not in visited:
        ans.append((pos[0], pos[1] + 1))

    if tmp_maze[(pos[0] - 1, pos[1])] == 0 and (pos[0] - 1, pos[1]) not in visited:
        ans.append((pos[0] - 1, pos[1]))

    if tmp_maze[(pos[0], pos[1] - 1)] == 0 and (pos[0], pos[1] - 1) not in visited:
        ans.append((pos[0], pos[1] - 1))

    return ans


def gen_maze():
    global dim, tmp_maze, visited, maze


    start = (random.randint(0, dim[0] - 1), random.randint(0, dim[1] - 1))
    #start = (0, 0)
    for y in range(dim[1]):
        for x in range(dim[0]):
            tmp_maze[(x, y)] = 0

    queue = [start]
    visited= set()
    prev_vert = start
    now_vert = None
    while queue:

        visited.add(prev_vert)

        now_vert = get_friends(prev_vert)

        if not now_vert:
            prev_vert = queue.pop(-1)
            continue

        now_vert = random.choice(now_vert)
        queue.append(now_vert)
        if tmp_maze[prev_vert] != 0:
            tmp_maze[prev_vert].append(now_vert)
            tmp_maze[now_vert] = [prev_vert]
        else:
            tmp_maze[prev_vert] = [now_vert]
            tmp_maze[now_vert] = [prev_vert]
        prev_vert = now_vert

    for i in tmp_maze.items():
        if not i[1] == 0 and len(i[1]) > 0:
            maze[i[0]] = i[1]

def draw_field():
    global win, s, dim
    for i in range(dim[0]):
        pg.draw.line(s, (0, 0, 0), (i * box_size, 0), (i * box_size, win.get_size()[1]))
    for i in range(dim[1]):
        pg.draw.line(s, (0, 0, 0), (0, i * box_size), (win.get_size()[0], i * box_size))
    pass


def just_draw():
    global s, win, maze, box_size, true_path
    win.fill((0, 0, 0))
    s = pg.Surface(win.get_size(), pg.SRCALPHA, 32)
    draw_field()


    for i in maze.items():
        x, y = i[0][0] * box_size + box_size//2, i[0][1] * box_size + box_size//2
        for j in i[1]:
            x1, y1 = j[0] * box_size + box_size // 2, j[1] * box_size + box_size // 2
            pg.draw.line(s, (255, 255, 255), (x, y), (x1, y1), box_size//2)


    try:
        x, y = box_size * start[0] + box_size // 2, box_size * start[1] + box_size // 2
        pg.draw.circle(s, (255, 0, 0), (x, y), box_size//2)
    except Exception:
        pass

    try:
        x, y = box_size * end[0] + box_size // 2, box_size * end[1] + box_size // 2
        pg.draw.circle(s, (0, 255, 0), (x, y), box_size//2)
    except Exception:
        pass

    try:
        for i in range(len(true_path) - 1):
            x, y = box_size * true_path[i][0] + box_size // 2, box_size * true_path[i][1] + box_size // 2
            x1, y1 = box_size * true_path[i + 1][0] + box_size // 2, box_size * true_path[i + 1][1] + box_size // 2
            pg.draw.line(s, (255, 0, 255), (x, y), (x1, y1), 3)
    except Exception:
        pass




    win.blit(s, (0, 0))
    pg.display.flip()


def reset():
    global maze, tmp_maze, start, end, true_path
    start = None
    end = None
    true_path = []
    maze = dict()
    tmp_maze = defaultdict(lambda: [])

def mouse_pos_to_dosochka(pos):
    global box_size
    return (pos[0] // box_size , pos[1] // box_size )

def set_start_end(pos):

    global start, end

    if mouse_pos_to_dosochka(pg.mouse.get_pos()) == start:
        start = None

    elif mouse_pos_to_dosochka(pg.mouse.get_pos()) == end:
        end = None

    else:
        if not start:
            start = pos

        elif not end:
            end = pos


def draw():
    global dim, win, s, start, end, true_path
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)

    pg.init()
    pg.RESIZABLE = False

    win = pg.display.set_mode((dim[0] * box_size + 1, dim[1] * box_size + 1), pg.RESIZABLE)
    s = pg.Surface(win.get_size(), pg.SRCALPHA, 32)
    pg.display.set_caption("Path Finder")

    going = True
    while going:
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    if start and end:
                        true_path = []
                        dijkstra()

                if e.key == pg.K_ESCAPE:
                    reset()
                    gen_maze()


            if (e.type == pg.MOUSEBUTTONDOWN) and e.button == 1:
                set_start_end(mouse_pos_to_dosochka(pg.mouse.get_pos()))

            if e.type == pg.QUIT:
                going = False

        just_draw()

    pg.quit()
    raise SystemExit


gen_maze()
draw()