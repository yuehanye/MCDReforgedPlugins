# -*- coding: utf-8 -*-
# v0.0.1

import re
import os
import json
import time

FILE_PATH = './plugins/AdvancedBan/'
PERMISSIONS = {
    'kick': 2,
    'ban': 3,
    'tempban': 3,
    'unban': 3,
    'banlist': 3
}

adv_data = {}
HelpMessage = '''
------AdvancedBan 玩家管理插件------
§6!!ab §7显示帮助
§6!!kick <§6§oplayer§6> [§6§oreason§6] §7踢出玩家
§6!!ban <§6§oplayer§6> [§6§oreason§6] §7封禁玩家
§6!!tempban <§6§oplayer§6> <§6§otime§6> [§6§oreason§6] §7封禁玩家一段时间
§6!!unban <§6§oplayer§6> §7解禁玩家
§6!!banlist §7封禁列表'''


def init_data():
    global adv_data
    with open(FILE_PATH + 'AdvancedBan.json') as init:
        adv_data = json.load(init)


def on_load(server, old):
    # load data
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
    if not os.path.isfile(FILE_PATH + 'AdvancedBan.json'):
        with open(FILE_PATH + 'AdvancedBan.json', 'w') as create:
            create.write('{}')
    init_data()


def on_player_joined(server, player):
    baned_check(server, player)


def on_user_info(server, info):
    if info.content.rstrip(' ') == '!!ab':
        return server.reply(info, HelpMessage)

    # kick
    permission = server.get_permission_level(info)
    content = info.content.split(' ')

    # kick
    if info.content.startswith('!!kick '):
        if len(content) >= 2 and permission >= PERMISSIONS['kick']:
            player = content[1]
            reason = f'§c你被踢出游戏! 原因: {content[2]}' if len(content) == 3 else None
            kick(server, player, reason)

    # ban
    elif info.content.startswith('!!ban '):
        if len(content) >= 2 and permission >= PERMISSIONS['ban']:
            player = content[1]
            if player in adv_data.keys():
                return server.reply(info, '§c该玩家已被封禁')
            reason = content[2] if len(content) == 3 else None
            ban_time = int(time.time())
            adv_data[player] = {
                'operator': info.player,
                'ban_time': ban_time,
                'unban_time': -1,
                'reason': reason
            }
            save_data()
            baned_check(server, player)
            server.reply(info, f'§c已封禁{player}')

    # temp ban
    elif info.content.startswith('!!tempban '):
        if len(content) >= 3 and permission >= PERMISSIONS['tempban']:
            player = content[1]
            if player in adv_data.keys():
                return server.reply(info, '§c该玩家已被封禁')
            reason = content[3] if len(content) == 4 else None
            ban_time = int(time.time())
            try:
                unban_time = ban_time + calc_time(content[2])
            except:
                return server.reply(info, '§c时间不合法')
            adv_data[player] = {
                'operator': info.player,
                'ban_time': ban_time,
                'unban_time': unban_time,
                'reason': reason
            }
            save_data()
            baned_check(server, player)
            server.reply(info, f'§c已封禁{player}')

    # unban
    elif info.content.startswith('!!unban '):
        if len(content) == 2 and permission >= PERMISSIONS['unban']:
            player = content[1]
            if player in adv_data.keys():
                del adv_data[player]
                server.reply(info, '§a已解禁' + player)
                save_data()
            else:
                server.reply(info, '§c该玩家未被封禁')

    # banlist
    elif info.content == '!!banlist' and permission >= PERMISSIONS['banlist']:
        i = 0
        server.reply(info, '§8>>> §7Banlist:')
        server.reply(info, '§cPlayer §8| §e Duration §8| §7Banned by')
        server.reply(info, '§cType §8> §7Reason')
        for player, data in adv_data.items():
            i += 1
            if data['unban_time'] == -1:
                duration = 'permanent'
                ban_type = 'Ban'
            else:
                duration = f'{int(data["unban_time"] - time.time())}秒'
                ban_type = 'Tempban'
            server.reply(info, '')
            server.reply(
                info, '§8[§e{}§8]'.format(time.strftime(
                    "%Y.%m.%d-%H:%M", time.localtime(data['ban_time']))))
            server.reply(info, f'§c{player} §8| §e{duration} §8| §7{data["operator"]}')
            server.reply(info, f'§c{ban_type} §8> §7{data["reason"]}')


def kick(server, player, reason):
    if reason is None:
        reason = ''
    server.execute(' '.join(['kick', player, reason]).rstrip(' '))


def save_data():
    global adv_data
    with open(FILE_PATH + 'AdvancedBan.json', 'w', encoding='utf-8') as save:
        json.dump(adv_data, save, indent=4, ensure_ascii=False)
        save.flush()


def calc_time(s):
    time_list = re.findall(r'[0-9]+|[a-z]{1,3}', s)
    total_time = 0

    if not time_list[0].isdigit() or len(time_list) % 2 != 0:
        raise ValueError('Not one value and one unit')

    while not len(time_list) == 0:
        unit = time_list[1]
        value = int(time_list[0])
        if unit == 's':
            total_time += value
        elif unit == 'm':
            total_time += value * 60
        elif unit == 'h':
            total_time += value * 60 * 60
        elif unit == 'd':
            total_time += value * 60 * 60 * 24
        elif unit == 'w':
            total_time += value * 60 * 60 * 24 * 7
        elif unit == 'mon':
            total_time += value * 60 * 60 * 24 * 30
        elif unit == 'y':
            total_time += value * 60 * 60 * 24 * 365
        else:
            raise ValueError('Unit of time is undefined')
        time_list.remove(time_list[0])
        time_list.remove(time_list[0])
    return total_time


def baned_check(server, player):
    global adv_data
    if player in adv_data.keys():
        reason = adv_data[player]['reason']
        if adv_data[player]['unban_time'] == -1:
            reason = f'§c永久封禁原因: {reason}'
            return kick(server, player, reason)
        elif adv_data[player]['unban_time'] > time.time():
            duration = adv_data[player]['unban_time'] - time.time()
            reason = '§c封禁原因: {} §c解禁时间: {}'.format(reason, time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(
                    adv_data[player]['unban_time'])))
            kick(server, player, reason)
        if adv_data[player]['unban_time'] < time.time():
            del adv_data[player]
            save_data()
