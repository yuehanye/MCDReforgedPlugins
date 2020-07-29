# -*- coding: utf-8 -*-
# v1.8.1

import requests


HelpMessage ='''------MCDR pget插件------
§7!!pget [url] -下载这个插件
--------------------------------'''


def on_load(server, old):
    server.add_help_message('!!pget', '下载插件')


def on_info(server, info):
    content = info.content.rstrip(' ')
    content = content.split(' ')
    if content[0] == '!!pget':
        if server.get_permission_level(info) >= 3:
            if len(content) == 1:
                server.reply(info, HelpMessage)
            elif len(content) == 2:
                link = content[1]
                download(server, info, link)
            else:
                server.reply(info, '§c命令格式错误！请使用!!pget查看帮助§r')
        else:
            server.reply(info, '§c权限不足！§r')


def download(server, info, link):
    name = link.split('/')
    if name[-1].split('.')[-1] == 'py':
        file = requests.get(url=link, verify=False)
        if file.status_code == 200:
            with open('./plugins/' + name[-1], 'wb') as write:
                write.write(file.content)
            finish_download_msg(server, info, name)
        else:
            server.reply(info, '§c下载失败§r')
    else:
        server.reply(info, '§c您下载的不是python文件§r')


def finish_download_msg(server, info, name):
    server.refresh_changed_plugins()
    server.reply(info, '§a下载成功!§r')
    server.reply(info, '§a已自动重载插件！§r')
    if info.is_player:
        server.logger.info('管理员' + info.player + '下载了插件' + name[-1])
    else:
        server.logger.info('有人通过控制台下载了插件' + name[-1])
