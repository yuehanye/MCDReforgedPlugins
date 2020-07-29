# -*- coding: utf-8 -*-
# v0.2.1

import os
import json

from decimal import Decimal, ROUND_HALF_UP

# 可修改内容开始
create_expenditure = Decimal(10)
PERMISSIONS = {
    'list': 2,
    'reload': 2
}
# 可修改内容结束

FILE_PATH = 'plugins/TeamAccount/'
HelpMsg = '''
--------TeamAccount 团队账号--------
§6!!team §7查看帮助
§6!!team <§6§oname§6> create §7创建团队账户
§6!!team <§6§oname§6> remove §7删除团队账户
§6!!team <§6§oname§6> member §7管理团队成员
§6!!team <§6§oname§6> balance §7管理团队余额
§6!!team list §7显示所有团队
§6!!team reload §7重载插件'''

MemberMsg = '''
§6!!team <§6§oname§6> member list §7显示团队成员列表
§6!!team <§6§oname§6> member add <§6§oplayer§6> §7向团队添加成员
§6!!team <§6§oname§6> member remove <§6§oplayer§6> §7从团队中删除成员
§6!!team <§6§oname§6> member check <§6§oplayer§6> §7设置团队成员等级
§6!!team <§6§oname§6> member set <§6§oplayer§6> <§6§opermission§6> §7设置团队成员等级'''

BalanceMsg = '''
§6!!team <§6§oname§6> balance check §7显示团队余额
§6!!team <§6§oname§6> balance add <§6§oamount§6> §7向团队添加余额
§6!!team <§6§oname§6> balance pay <§6§oteam §6| §oplayer§6> <§6§oname§6> <§6§oamount§6> §7使用团队账户支付'''


def init_data():
    global team_data
    if not os.path.isfile(FILE_PATH + 'TeamAccount.json'):
        with open(FILE_PATH + 'TeamAccount.json', 'w') as create:
            create.write(json.dumps({}, indent=1))
    with open(FILE_PATH + 'TeamAccount.json') as init:
        team_data = json.load(init)


def save_data():
    with open(FILE_PATH + 'TeamAccount.json', 'w') as save:
        save.write(json.dumps(team_data, indent=4))
        save.flush()


def on_load(server, old_module):
    # add help msg
    server.add_help_message('!!team', '团队账号帮助')
    # vault check
    if 'vault.py' not in server.get_plugin_list():
        server.logger.error('你没有安装前置vault！')
    else:
        global vault
        vault = server.get_plugin_instance('vault')
    # check folder
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)
    # init data
    init_data()


def on_user_info(server, info):
    if info.content.rstrip(' ') == '!!team':
        server.reply(info, HelpMsg)
        return
    if info.content.startswith('!!team'):
        commands(server, info, info.content.rstrip(' ').split(' '))


def commands(server, info, content):
    del content[0]

    # reload
    if len(content) == 1 and content[0] == 'reload' and server.get_permission_level(info) >= PERMISSIONS['reload']:
        init_data()
        return server.reply(info, '§a已重载所有团队数据')
    elif len(content) == 1 and content[0] == 'reload' and server.get_permission_level(info) < PERMISSIONS['reload']:
        return server.reply(info, '§c权限不足!')

    if len(content) == 1 and content[0] == 'list' and server.get_permission_level(info) >= PERMISSIONS['list']:
        for team in team_data.keys():
            server.reply(info, '§7 - §e' + team)
        return
    elif len(content) == 1 and content[0] == 'list' and server.get_permission_level(info) < PERMISSIONS['list']:
        return server.reply(info, '§c权限不足!')

    # create
    if len(content) == 2 and content[1] == 'create':
        if content[0] in team_data.keys():
            return server.reply(info, '§c团队已存在!')
        if vault.take(info.player, create_expenditure) == -3:
            return server.reply(info, '§c余额不足a!')
        team_data[content[0]] = {
            'members': {
                'Management': [info.player],
                'Cashier': [],
                'Member': []
            },
            'balance': '0'
        }
        save_data()
        return server.reply(info, '§a已成功创建团队§e' + content[0])

    # check team
    if content[0] not in team_data.keys():
        none_team(server, info)

    # remove
    elif len(content) == 2 and content[1] == 'remove':
        permission = get_permission(content[0], info.player)
        if permission != 'Management':
            permission_denied(server, info)
        else:
            team = content[0]
            amount = Decimal(team_data[team]['balance'])
            vault.give(info.player, amount)
            del team_data[team]
            save_data()
            server.reply(info, '§a已成功删除团队§e' + content[0] + '§a, 团队余额§e' + str(amount) + '§a已返还到您的账户')

    # member
    elif len(content) >= 2 and content[1] == 'member':
        member(server, info, content)

    # balance
    elif len(content) >= 2 and content[1] == 'balance':
        balance(server, info, content)
    else:
        server.reply(info, '§c命令格式错误! 使用!!team查看帮助')


def member(server, info, content):
    # help msg
    if len(content) == 2:
        return server.reply(info, MemberMsg)

    team = content[0]
    permission = get_permission(team, content[3]) if len(content) >= 4 else None

    # not in team
    if get_permission(team, info.player) == 0:
        return not_in_team(server, info, '您')

    # list
    if len(content) == 3 and content[2] == 'list':
        server.reply(info, '§7[§eManagement§7]')
        for Management in team_data[team]['members']['Management']:
            server.reply(info, '§7 - §r' + Management)
        server.reply(info, '§7[§eCashier§7]')
        for Cashier in team_data[team]['members']['Cashier']:
            server.reply(info, '§7 - §r' + Cashier)
        server.reply(info, '§7[§eMember§7]')
        for Member in team_data[team]['members']['Member']:
            server.reply(info, '§7 - §r' + Member)
        return

    # add
    if len(content) == 4 and content[2] == 'add':
        if get_permission(team, info.player) != 'Management':
            permission_denied(server, info)
        elif permission != 0:
            server.reply(info, '§c该玩家已在队伍中!')
        else:
            team_data[team]['members']['Member'].append(content[3])
            save_data()
            server.reply(info, '§a已向团队§e' + team + '§a中添加玩家§e' + content[3])

    # remove
    elif len(content) == 4 and content[2] == 'remove':
        if get_permission(team, info.player) != 'Management':
            permission_denied(server, info)
        elif permission == 0:
            not_in_team(server, info, content[3])
        else:
            team_data[team]['members'][permission].remove(content[3])
            save_data()
            server.reply(info, '§a已从团队§e' + team + '§a中删除玩家§e' + content[3])

    # check
    elif len(content) == 4 and content[2] == 'check':
        if permission == 0:
            not_in_team(server, info, content[3])
        else:
            server.reply(info, '§e' + content[3] + '§a的权限等级为: §e' + get_permission(team, content[3]))

    # set
    elif len(content) == 5 and content[2] == 'set':
        if get_permission(team, info.player) != 'Management':
            permission_denied(server, info)
        elif permission == 0:
            not_in_team(server, info, content[3])
        else:
            permission_list = {
                '3': 'Management',
                '2': 'Cashier',
                '1': 'Member'
            }
            if content[4] not in list(permission_list.keys()):
                server.reply(info, '§c权限错误!')
            else:
                new_permission = permission_list[content[4]]
                team_data[team]['members'][permission].remove(content[3])
                team_data[team]['members'][new_permission].append(content[3])
                save_data()
                server.reply(info, '§a已将玩家§e' + content[3] + '§a的权限设置为§e' + new_permission)
    else:
        server.reply(info, '§c命令格式错误! 使用!!team <name> member查看帮助')


def balance(server, info, content):
    # help msg
    if len(content) == 2:
        return server.reply(info, BalanceMsg)

    team = content[0]
    permission = get_permission(team, info.player)

    # not in team
    if get_permission(team, info.player) == 0:
        return not_in_team(server, info, '您')

    # check
    if len(content) == 3 and content[2] == 'check':
        server.reply(info, '§a团队§e' + team + '§a的余额为: §e' + get_balance(team))

    # add
    elif len(content) == 4 and content[2] == 'add':
        amount = Decimal(content[3]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        if permission == 0:
            not_in_team(server, info, '您')
        elif amount <= 0:
            wrong_amount(server, info)
        elif amount > vault.check(info.player):
            server.reply(info, '§c余额不足!')
        else:
            vault.take(info.player, amount)
            add_balance(team, amount)
            save_data()
            server.reply(info, '§a向团队§e' + team + '§a的余额中添加了§e' + str(amount) + '§a, 团队余额: §e' + team_data[team]['balance'])

    # pay
    elif len(content) == 6 and content[2] == 'pay':
        amount = Decimal(content[5]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        if permission == 0:
            not_in_team(server, info, '您')
        elif permission == 'Member':
            permission_denied(server, info)
        elif amount <= 0:
            wrong_amount(server, info)
        elif Decimal(get_balance(team)) < amount:
            server.reply(info, '§c余额不足!')
        else:
            if content[3] == 'team':
                team_to = content[4]
                if team_to not in team_data.keys():
                    none_team(server, info)
                else:
                    team_data[team]['balance'] = str(Decimal(team_data[team]['balance']) - amount)
                    team_data[team_to]['balance'] = str(Decimal(team_data[team_to]['balance']) + amount)
                    save_data()
                    server.reply(info, '§a使用团队账户向§e' + team_to + '§a支付了§e' + str(amount) + '§a, 团队余额: §e' + team_data[team]['balance'])
                    for player in team_data[team_to]['members']['Management']:
                        server.tell(player, '§a团队§e' + team + '§a向你的团队支付了§e' + str(amount) + '§a, 团队余额: §e' + team_data[team_to]['balance'])
                    for player in team_data[team_to]['members']['Cashier']:
                        server.tell(player, '§a团队§e' + team + '§a向你的团队支付了§e' + str(amount) + '§a, 团队余额: §e' + team_data[team_to]['balance'])
                    for player in team_data[team_to]['members']['Member']:
                        server.tell(player, '§a团队§e' + team + '§a向你的团队支付了§e' + str(amount) + '§a, 团队余额: §e' + team_data[team_to]['balance'])
            elif content[3] == 'player':
                if vault.check(content[4]) == -1:
                    server.reply(info, '§c玩家不存在!')
                elif permission == 'Member':
                    permission_denied(server, info)
                elif amount <= 0:
                    wrong_amount(server, info)
                elif Decimal(get_balance(team)) < amount:
                    server.reply(info, '§c余额不足!')
                else:
                    team_data[team]['balance'] = str(Decimal(team_data[team]['balance']) - amount)
                    vault.give(content[4], amount)
                    save_data()
                    server.reply(info, '§a使用团队账户向§e' + content[4] + '§a支付了§e' + str(amount) + '§a, 团队余额: §e' + team_data[team]['balance'])
                    server.tell(content[4], '§a团队§e' + team + '§a向你支付了§e' + str(amount) + '§a, 你的余额: §e' + str(vault.check(content[4])))
    else:
        server.reply(info, '§c命令格式错误! 使用!!team <name> balance查看帮助')


def get_permission(team, player):
    if player in team_data[team]['members']['Management']:
        return 'Management'
    elif player in team_data[team]['members']['Cashier']:
        return 'Cashier'
    elif player in team_data[team]['members']['Member']:
        return 'Member'
    else:
        return 0


# for Economy api
def get_team_list():
    return list(team_data.keys())


def get_team_data(team):
    return team_data[team]


def add_balance(team, amount):
    team_data[team]['balance'] = str(Decimal(get_balance(team)) + amount)


def get_balance(team):
    return team_data[team]['balance']


# for Economy api end
def none_team(server, info):
    server.reply(info, '§c团队不存在!')


def not_in_team(server, info, player):
    print(player)
    if player == '您':
        server.reply(info, '§c' + player + '不在队伍中!')
    else:
        server.reply(info, '§e' + player + '§c 不在队伍中!')


def permission_denied(server, info):
    server.reply(info, '§c权限不足!')


def wrong_amount(server, info):
    server.reply(info, '§c非法金额!')
