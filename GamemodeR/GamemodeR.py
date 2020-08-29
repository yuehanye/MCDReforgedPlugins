# -*- coding: utf-8 -*-
# v0.3.0

import os
import json
import time
from math import ceil

from decimal import Decimal

enable_free = True
spec_price = 10
tp_price = 20

free_flag = True
FILE_PATH = './plugins/GamemodeR/'
dimension_convert = {
    '0': 'minecraft:overworld',
    '-1': 'minecraft:the_nether',
    '1': 'minecraft:the_end',
    'overworld': 'minecraft:overworld',
    'the_nether': 'minecraft:the_nether',
    'the_end': 'minecraft:the_end',
    'nether': 'minecraft:the_nether',
    'end': 'minecraft:the_end',
    'minecraft:overworld': 'minecraft:overworld',
    'minecraft:the_nether': 'minecraft:the_nether',
    'minecraft:the_end': 'minecraft:the_end'
}
help_msg = '''
§6!!spec §7旁观/生存切换
§6!!tp <dimension> [position] §7传送至指定地点
§6!!back §7返回上个地点'''


def init_data():
    if not os.path.isfile(FILE_PATH + 'GamemodeR.json'):
        with open(FILE_PATH + 'GamemodeR.json', 'w') as create:
            create.write(json.dumps({}, indent=1))
    global data
    with open(FILE_PATH + 'GamemodeR.json') as init:
        data = json.load(init)


def save_data():
    with open(FILE_PATH + 'GamemodeR.json', 'w') as save:
        save.write(json.dumps(data, indent=1))
        save.flush()


def on_load(server, old):
    # add help msg
    server.add_help_message('!!spec help', 'GamemodeR帮助')

    # vault
    if enable_free or 'vault.py' not in server.get_plugin_list():
        global free_flag
        free_flag = True
        server.logger.info('GamemodeR已设置为免费模式')
    else:
        global vault
        vault = server.get_plugin_instance('vault')
        server.logger.info('GamemodeR已设置为收费模式')

    # Player Info api
    if 'PlayerInfoAPI.py' not in server.get_plugin_list():
        server.logger.error('你没有安装前置PlayerInfoAPI! ')
    else:
        global api
        api = server.get_plugin_instance('PlayerInfoAPI')

    # file folder
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)

    # init data
    init_data()


def on_player_joined(server, player):
    if player in data.keys():
        server.execute('gamemode spectator ' + player)


def on_user_info(server, info):
    # help
    if info.content == '!!spec help':
        server.reply(info, help_msg)
    # spec
    elif info.is_player and info.content == '!!spec':
        change_mode(server, info)
    # tp
    elif info.is_player and info.content.startswith('!!tp'):
        tp(server, info)
    # back
    elif info.is_player and info.content == '!!back':
        back(server, info)


def change_mode(server, info):
    # 当前为生存
    if info.player not in data.keys():
        sur_to_spec(server, info)
        if free_flag:
            server.reply(info, '§a已切换至旁观模式')
        else:
            server.reply(info, f'§a欢迎使用本插件, 价格§e{spec_price}/min§a, 请注意余额')
            if vault.check(info.player) < spec_price:
                server.reply(info, '§c余额不足, 您可能将无法切换回生存模式')
    # 当前为旁观
    elif info.player in data.keys():
        use_time = ceil((time.time() - data[info.player]['time']) / 60)
        if free_flag:
            server.reply(info, f'§a您使用了§e{use_time}min')
            spec_to_sur(server, info)
        else:
            balance = vault.check(info.player)
            amount = use_time * spec_price
            if balance < amount:
                server.reply(info, '§c余额不足')
                return server.reply(info,
                                    '§7您需要支付: §e{}§c, 您的余额: §e{}§c, 请联系管理人员'
                                    .format(amount, balance))
            else:
                spec_to_sur(server, info)
                vault.take(info.player, Decimal(amount))
                server.reply(info,
                             f'§a您使用了§e{use_time}min§a, 共支付: §e{use_time}')


def tp(server, info):
    # 检查
    if not free_flag and vault.check(info.player) < tp_price:
        return server.reply(info, '§c余额不足')
    if info.player not in data.keys():
        return server.reply(info, '§c您只能在旁观模式下传送')
    r = info.content.split(' ')
    # 检查长度
    if len(r) == 2:
        pos = '0 80 0'
    elif len(r) == 5:
        pos = ' '.join(r[2:])
    else:
        server.reply(info, '§c错误的命令参数')
        return server.reply(info, '§7!!tp <dimension> [position]')
    if r[1] not in dimension_convert.keys():
        return server.reply(info, '§c没有此维度')
    # 解析指令
    dim = dimension_convert[r[1]]
    # 记录back数据
    data[info.player]['back'] = {
        'dim': dimension_convert[
            str(api.getPlayerInfo(server, info.player, path='Dimension'))],
        'pos': api.getPlayerInfo(server, info.player, path='Pos')
    }
    server.execute(f'execute in {dim} run tp {info.player} {pos}')
    if free_flag:
        server.reply(info, f'§a传送至§e{dim}§a, 坐标§e{dim}')
    else:
        vault.take(info.player, Decimal(tp_price))
        server.reply(info, f'§a传送至§e{dim}§a, 坐标§e{dim}§a, 消费§e{tp_price}')
    save_data()


def back(server, info):
    # 检查
    if not free_flag and vault.check(info.player) < tp_price:
        return server.reply(info, '§c余额不足')
    if info.player not in data.keys():
        return server.reply(info, '§c您只能在旁观模式下传送')
    # 读取back数据
    dim = data[info.player]['back']['dim']
    pos = [str(x) for x in data[info.player]['back']['pos']]
    # 记录新back数据
    data[info.player]['back'] = {
        'dim': dimension_convert[
            str(api.getPlayerInfo(server, info.player, path='Dimension'))],
        'pos': api.getPlayerInfo(server, info.player, path='Pos')
    }
    # 传送
    server.execute(f'execute in {dim} run tp {info.player} {" ".join(pos)}')
    if free_flag:
        server.reply(info, '§a已将您传送至上个地点')
    else:
        vault.take(info.player, Decimal(tp_price))
        server.reply(info, '§a已将您传送至上个地点, 消费§e{}'.format(tp_price))
    save_data()


def sur_to_spec(server, info):
    # 记录初始坐标
    dim = dimension_convert[
        str(api.getPlayerInfo(server, info.player, path='Dimension'))]
    pos = api.getPlayerInfo(server, info.player, path='Pos')
    data[info.player] = {
        'dim': dim,
        'pos': pos,
        'time': time.time(),
        'back': {
            'dim': dim,
            'pos': pos
        }
    }
    server.execute('gamemode spectator ' + info.player)
    save_data()


def spec_to_sur(server, info):
    dim = data[info.player]['dim']
    pos = [str(x) for x in data[info.player]['pos']]
    server.execute(
        'execute in {} run tp {} {}'.format(dim, info.player, ' '.join(pos)))
    server.execute('gamemode survival ' + info.player)
    del data[info.player]
    save_data()
