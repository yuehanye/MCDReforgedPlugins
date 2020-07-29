# -*- coding: utf-8 -*-
# v0.1.7
import os
import requests
import json

group_id = [1234561, 1234562]
admin_id = [1234563, 1234564]
whitelist_add_with_bound = False
whitelist_remove_with_leave = True

qq_bound = {}
group_help_msg = '''命令帮助如下:
/list 获取在线玩家列表
/bound <ID> 绑定你的游戏ID
/mc <msg> 向游戏内发送消息
'''
admin_help_msg = '''管理员命令帮助如下
/bound 查看绑定相关帮助
/whitelist 查看白名单相关帮助
/forward 查看转发消息相关帮助
/command <command> 执行任意指令
'''
bound_help = '''/bound list 查看绑定列表
/bound check <qq number> 查询绑定ID
/bound unbound <qq number> 解除绑定
/bound <qq number> <ID> 绑定新ID
'''
whitelist_help = '''/whitelist add <target> 添加白名单成员
/whitelist list 列出白名单成员
/whitelist off 关闭白名单
/whitelist on 开启白名单
/whitelist reload 重载白名单
/whitelist remove <target> 删除白名单成员
<target> 可以是玩家名/目标选择器/UUID
'''
forward_help = '''/forward info 查看info转发状态
/forward info <type> <qq number> on 开启info转发
/forward info <qq number> off 关闭info转发
/forward message 查看message转发状态
/forward message <type> <qq number> on 开启message转发
/forward message <qq number> off 关闭message转发
/forward qq 查看qq转发状态
/forward qq on 开启qq转发
/forward qq off 关闭qq转发
'''


def on_qq_load(server, bot):
    global qq_bound
    if not os.path.isdir('./plugins/QQChat'):
        os.mkdir('./plugins/QQChat')
    if os.path.isfile('./plugins/QQChat/qq_bound.json'):
        with open('./plugins/QQChat/qq_bound.json', encoding='utf-8') as f:
            qq_bound = json.load(f)
    else:
        qq_bound = {}

    if not os.path.isfile('./plugins/QQChat/forward.json'):
        with open('./plugins/QQChat/forward.json', 'w', encoding='utf-8') as f:
            json.dump({'info': {}, 'message': {}, 'qq': False}, f, indent=4)


def on_qq_notice(server, info, bot):
    if info.source_id not in group_id:
        return
    if info.notice_type == 'group_decrease' and whitelist_remove_with_leave:
        global qq_bound
        if str(info.user_id) in qq_bound.keys():
            c = f'whitelist remove {qq_bound[str(info.user_id)]}'
            if server.is_rcon_running():
                server.rcon_query(c)
            else:
                server.execute(c)
            bot.reply(info, f'{qq_bound[str(info.user_id)]} 已退群，移除他的白名单')
            del qq_bound[str(info.user_id)]
            save_bound()


def on_qq_info(server, info, bot):
    forward = get_forward()
    if forward['qq'] and info.source_id in group_id:
        if str(info.user_id) in qq_bound.keys():
            return server.say(
                f'§7[QQ] [{qq_bound[str(info.user_id)]}] {info.content}')
        else:
            bot.reply(info, f'[CQ:at,qq={info.user_id}] 您未绑定游戏ID, 无法转发您的消息到游戏内')


def on_qq_command(server, info, bot):
    if not (info.source_id in group_id or info.source_id in admin_id):
        return
    command = info.content.split(' ')
    command[0] = command[0].replace('/', '')

    if info.content == '/list':
        online_player_api = server.get_plugin_instance('OnlinePlayerAPI')
        if online_player_api is None:
            server.logger.info('缺少OnlinePlayerAPI')
            with open('.\\plugins\\OnlinePlayerAPI.py', 'wb') as f:
                f.write(requests.get(
                    'https://raw.githubusercontent.com/zhang-anzhi/MCDReforgedPlugins/'
                    'master/OnlinePlayerAPI/OnlinePlayerAPI.py').content)
            server.refresh_changed_plugins()
            server.logger.info('已自动下载并重载插件')
            online_player_api = server.get_plugin_instance('OnlinePlayerAPI')
        bot.reply(info, '在线玩家共{}人，玩家列表: {}'.format(
            len(online_player_api.get_player_list()),
            ', '.join(online_player_api.get_player_list())))
    elif command[0] == 'mc':
        if str(info.user_id) in qq_bound.keys():
            server.say(
                f'§7[QQ] [{qq_bound[str(info.user_id)]}] {info.content[4:]}')
        else:
            bot.reply(info, f'[CQ:at,qq={info.user_id}] 请使用/bound <ID>绑定游戏ID')
    if info.source_type == 'private':
        private_command(server, info, bot, command)
    elif info.source_type == 'group':
        group_command(server, info, bot, command)


def private_command(server, info, bot, command):
    global qq_bound
    if info.content == '/help':
        bot.reply(info, admin_help_msg)
    # bound
    elif info.content.startswith('/bound'):
        if info.content == '/bound':
            bot.reply(info, bound_help)
        elif len(command) == 2 and command[1] == 'list':
            bound_list = [f'{a} - {b}' for a, b in qq_bound.items()]
            reply_msg = ''
            for i in range(0, len(bound_list)):
                reply_msg += f'{i + 1}: {bound_list[i]}\n'
            reply_msg = '还没有人绑定' if reply_msg == '' else reply_msg
            bot.reply(info, reply_msg)
        elif len(command) == 3 and command[1] == 'check':
            if command[2] in qq_bound:
                bot.reply(info,
                          f'{command[2]} 绑定的ID是{qq_bound[command[2]]}')
            else:
                bot.reply(info, f'{command[2]} 未绑定')
        elif len(command) == 3 and command[1] == 'unbound':
            if command[2] in qq_bound:
                del qq_bound[command[2]]
                save_bound()
                bot.reply(info, f'已解除 {command[2]} 绑定的ID')
            else:
                bot.reply(info, f'{command[2]} 未绑定')
        elif len(command) == 3 and command[1].isdigit():
            qq_bound[command[1]] = command[2]
            save_bound()
            bot.reply(info, '已成功绑定')
    # whitelist
    elif info.content.startswith('/whitelist'):
        if info.content == '/whitelist':
            bot.reply(info, whitelist_help)
        if command[1] in ['add', 'remove', 'list', 'on', 'off', 'reload']:
            if server.is_rcon_running():
                bot.reply(server.rcon_query(info.content))
            else:
                server.execute(info.content)
    # forward
    elif info.content.startswith('/forward'):
        if info.content == '/forward':
            bot.reply(info, forward_help)
        elif len(command) == 2 and command[1] in ['info', 'message', 'qq']:
            forward = get_forward()[command[1]]
            if command[1] == 'qq':
                if forward:
                    bot.reply(info, 'qq消息将会转发到游戏中')
                else:
                    bot.reply(info, 'qq消息不行进行转发')
            elif len(forward) == 0:
                bot.reply(info, f'{command[1]}不会进行转发')
            else:
                bot.reply(info, '{}转发的列表有 {}'.format(
                    command[1], ', '.join([str(i) for i in forward])))
        elif len(command) >= 4 and command[1] in ['info', 'message']:
            if len(command) == 5 and command[4] == 'on':
                mode = True
                forward_type = command[1]
                id = command[3]
                message_type = command[2]
            elif len(command) == 4 and command[3] == 'off':
                mode = False
                forward_type = command[1]
                id = command[2]
                message_type = ''
            else:
                bot.reply(info, '命令参数错误')
                return bot.reply(info, forward_help)
            if set_forward(forward_type, id, message_type, mode):
                bot.reply(info,
                          f'已将 {id} 的 {forward_type} 转发设为 {mode}')
            else:
                bot.reply(
                    info,
                    f"{id}'s {forward_type} forward have already been {mode}"
                )
        elif len(command) == 3 and command[1] == 'qq':
            forward = get_forward()
            if command[2] == 'on':
                forward['qq'] = True
                bot.reply(info, f'已将qq消息转发设为 True')
            elif command[2] == 'off':
                forward['qq'] = False
                bot.reply(info, f'已将qq消息转发设为 False')
            else:
                bot.reply(info, '命令参数错误')
                return bot.reply(info, forward_help)
            with open('./plugins/QQChat/forward.json', 'w',
                      encoding='utf-8') as f:
                json.dump(forward, f, indent=4)
    # command
    elif info.content.startswith('/command '):
        c = info.content[9:]
        c = c.replace('&#91;', '[').replace('&#93;', ']')
        if server.is_rcon_running():
            bot.reply(info, server.rcon_query(c))
        else:
            server.execute(c)


def group_command(server, info, bot, command):
    global qq_bound
    if info.content == '/help':
        bot.reply(info, group_help_msg)
    # bound
    elif len(command) == 2 and command[0] == 'bound':
        try:
            bot.reply(info,
                      f'[CQ:at,qq={info.user_id}] 您已绑定ID: {qq_bound[str(info.user_id)]}, 请联系管理员修改')
        except KeyError:
            qq_bound[str(info.user_id)] = command[1]
            save_bound()
            bot.reply(info, f'[CQ:at,qq={info.user_id}] 已成功绑定')
            if whitelist_add_with_bound:
                c = f'whitelist add {command[1]}'
                if server.is_rcon_running():
                    server.rcon_query(c)
                else:
                    server.execute(c)
                bot.reply(info, f'[CQ:at,qq={info.user_id}] 已将您添加到服务器白名单')


def on_load(server, old):
    server.add_help_message('!!qq <msg>', '向QQ群发送消息')
    cq_api = server.get_plugin_instance('CoolQAPI-MCDR')
    if cq_api is None:
        server.logger.error('未安装CoolQAPI')
    else:
        global host, port
        config = cq_api.get_config()
        host = config['api_host']
        port = config['api_port']


def on_info(server, info):
    if info.content.startswith('!!qq '):
        for i in group_id:
            send_group_msg(f'[{info.player}] {info.content[5:]}', i)
    forward_list = get_forward()
    if len(forward_list['info'].keys()) > 0:
        for a, b in forward_list['info'].items():
            if b == 'private':
                send_private_msg(info.raw_content, a)
            else:
                send_group_msg(info.raw_content, a)
    if len(forward_list['message'].keys()) > 0 and info.is_player:
        for a, b in forward_list['message'].items():
            if b == 'private':
                send_private_msg(f'[{info.player}] {info.content}', a)
            else:
                send_group_msg(f'[{info.player}] {info.content}', a)


def on_server_startup(server):
    for i in group_id:
        send_group_msg('Server is starting up', i)


def send_group_msg(msg, group):
    data = {
        'group_id': group,
        'message': msg
    }
    requests.post(f'http://{host}:{port}/send_group_msg', json=data)


def send_private_msg(msg, user):
    data = {
        'user_id': user,
        'message': msg
    }
    requests.post(f'http://{host}:{port}/send_private_msg', json=data)


def save_bound():
    with open('./plugins/QQChat/qq_bound.json', 'w', encoding='utf-8') as f:
        json.dump(qq_bound, f, indent=4)


def get_forward():
    with open('./plugins/QQChat/forward.json', encoding='utf-8') as f:
        return json.load(f)


def set_forward(forward_type, id, message_type, mode):
    forward = get_forward()
    if mode:
        if id in forward[forward_type].keys():
            if message_type == forward[forward_type][id]:
                return False
        else:
            forward[forward_type][id] = message_type
    else:
        if id not in forward[forward_type].keys():
            return False
        else:
            del forward[forward_type][id]
    with open('./plugins/QQChat/forward.json', 'w', encoding='utf-8') as f:
        json.dump(forward, f, indent=4)
    return True
