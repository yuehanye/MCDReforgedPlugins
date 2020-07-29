# -*- coding: utf-8 -*-
# v0.0.1
import requests
import os

properties_path = 'server\\server.properties'
online_mode = True


def on_load(server, old):
    global online_mode
    if not os.path.isfile(properties_path):
        return server.error('未找到服务器配置文件')
    with open(properties_path) as f:
        for i in f.readlines():
            if 'online-mode' in i:
                break
        server.logger.debug(f'查找到配置项: {i}')
        i = i.split('=')[1].replace('\n', '')
    if i == 'true':
        online_mode = True
    elif i == 'false':
        online_mode = False
    else:
        return server.logger.error('服务器配置项错误')
    server.logger.debug(f'服务器在线模式为: {online_mode}')


def online_uuid(name):
    url = f'http://api.mojang.com/users/profiles/minecraft/{name}'
    r = get_try(url)
    if r is None:
        return None
    else:
        return r['id']


def offline_uuid(name):
    url = f'http://tools.glowingmines.eu/convertor/nick/{name}'
    r = get_try(url)
    if r is None:
        return None
    else:
        return r['offlineuuid']


def get_try(url):
    for i in range(0, 5):
        try:
            r = requests.get(url).json()
            return r
        except:
            pass
    return None


def get_uuid(name: str):
    if online_mode:
        uuid = online_uuid(name)
    else:
        uuid = offline_uuid(name)
    return uuid
