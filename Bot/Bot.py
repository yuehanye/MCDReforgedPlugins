# -*- coding: utf-8 -*-
import os
import json
from utils import rtext as r


bot_list = {}
config_path = 'config\\Bot.json'
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
help_msg = {
    '': '',
    '§6!!bot': '§7显示机器人列表',
    '§6!!bot spawn <name>': '§7生成机器人',
    '§6!!bot kill <name>': '§7移除机器人',
    '§6!!bot reload': '§7从文件重载机器人列表',
    '§6!!bot add <name> <dim> <pos> <facing>': '§7添加机器人到机器人列表',
    '§6!!bot remove <name>': '§7从机器人列表移除机器人'
}


def on_load(server, old):
    server.add_help_message('!!bot', r.RText(
        '显示机器人列表').c(r.RAction.run_command, '!!bot').h('点击显示机器人列表'))
    if not os.path.isfile(config_path):
        save()
    else:
        read()


def on_user_info(server, info):
    if info.content.startswith('!!bot'):
        arg = info.content.split(' ')
        summon_bot(server, info, arg)


def summon_bot(server, info, arg):
    global bot_list
    permission = server.get_permission_level(info)
    if len(arg) == 1:
        c = ['']
        for a, b in bot_list.items():
            bot_info = r.RTextList(
                '\n'
                f'§7----------- §6{a}§7 -----------\n',
                f'§7Dimension:§6 {b["dim"]}\n',
                r.RText(
                    f'§7Position:§6 {b["pos"]}\n', ).c(
                    r.RAction.run_command,
                    '[x:{}, y:{}, z:{}, name:{}, dim{}]'.format(
                        *[int(i) for i in b['pos']], a, b['dim'])).h(
                    '点击显示可识别坐标点'),
                f'§7Facing:§6 {b["facing"]}\n',
                r.RText(
                    '§d点击放置\n').c(
                    r.RAction.run_command, f'!!bot spawn {a}').h(f'放置§6{a}'),
                r.RText(
                    '§d点击移除\n').c(
                    r.RAction.run_command, f'!!bot kill {a}').h(f'移除§6{a}')
            )
            c.append(bot_info)
        server.reply(info, r.RTextList(*c))
    elif len(arg) == 2:
        if arg[1] == 'help':
            c = [r.RText(f'{a} {b}\n').c(
                r.RAction.suggest_command, a.replace('§6', '')).h(b)
                 for a, b in help_msg.items()]
            server.reply(info, r.RTextList(*c))
        elif arg[1] == 'reload' and permission >= 3:
            read()
            server.reply(info, '§a已从配置文件重新载入机器人列表')
        else:
            server.reply(info, '§c命令格式不正确或权限不足')
    elif len(arg) == 3:
        if arg[1] == 'spawn' and permission >= 1:
            if arg[2] in bot_list.keys():
                server.execute(spawn_command(arg[2]))
            else:
                server.reply(info, '§c机器人名称不正确')
        elif arg[1] == 'kill' and permission >= 1:
            if arg[2] in bot_list.keys():
                server.execute(f'player {arg[2]} kill')
            else:
                server.reply(info, '§c机器人名称不正确')
        elif arg[1] == 'remove' and permission >= 2:
            if arg[2] in bot_list.keys():
                del bot_list[arg[2]]
                save()
                server.reply(info, f'§a已删除机器人{arg[2]}')
            else:
                server.reply(info, '§c机器人名称不正确')
        else:
            server.reply(info, '§c命令格式不正确或权限不足')
    elif len(arg) == 9:
        if arg[1] == 'add' and permission >= 3:
            if arg[3] in dimension_convert.keys():
                dim = dimension_convert[arg[3]]
                pos = [int(i) for i in [arg[4], arg[5], arg[6]]]
                facing = f'{arg[7]} {arg[8]}'
                bot_list[arg[2]] = {
                    'dim': dim,
                    'pos': pos,
                    'facing': facing
                }
                save()
                server.reply(info, f'§a已添加机器人{arg[2]}')
            else:
                server.reply(info, '§c无法识别的维度')
        else:
            server.reply(info, '§c命令格式不正确或权限不足')


def spawn_command(name):
    dim = bot_list[name]['dim']
    pos = ' '.join([str(i) for i in bot_list[name]['pos']])
    facing = bot_list[name]['facing']
    return f'/player {name} spawn at {pos} facing {facing} in {dim}'


def read():
    global bot_list
    with open(config_path, encoding='utf8') as f:
        bot_list = json.load(f)


def save():
    with open(config_path, 'w', encoding='utf8') as f:
        json.dump(bot_list, f, indent=4, ensure_ascii=False)
