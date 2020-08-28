# -*- coding: utf-8 -*-
import psutil
import os

from utils.rtext import *

WORLD_NAMES = [
    'world'
]


def on_load(server, old):
    server.add_help_message('!!info', '获取服务器信息')


def round_size(size):
    if size < (2 ** 30):
        return f'{round(size / (2 ** 20), 2)} MB'
    else:
        return f'{round(size / (2 ** 30), 2)} GB'


def average(*args):
    count = 0
    for i in args:
        count += i
    return round(count / len(args), 2)


def get_used_memory():
    return round_size(psutil.virtual_memory().used)


def get_total_memory():
    return round_size(psutil.virtual_memory().total)


def get_this_used_memory():
    # MCDR process
    p = psutil.Process()
    mem = 0
    # cmd process
    for i in p.children():
        # java process
        for e in i.children():
            mem += e.memory_info().rss
    return round_size(mem)


def get_world_size():
    def get_dir_size(dir_name):
        s = 0
        for root, dirs, files in os.walk(f'server\\{dir_name}'):
            s += sum(
                [os.path.getsize(os.path.join(root, name)) for name in files])
        return s

    size = 0
    for i in WORLD_NAMES:
        size += get_dir_size(i)
    return round_size(size)


def on_info(server, info):
    if info.content == '!!info':
        server.reply(
            info,
            RTextList(
                '\n§7============ §6服务器信息 §7============\n',
                f'§7CPU利用率:§6 {average(*psutil.cpu_percent(percpu=True))}%\n',
                f'§7内存使用量:§6 {get_used_memory()} / {get_total_memory()}\n',
                f'§7服务器内存占用:§6 {get_this_used_memory()}\n',
                f'§7存档大小:§6 {get_world_size()}'
            )
        )
