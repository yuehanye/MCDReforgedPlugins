# QQChat

一个用于连接QQ和MC的聊天插件，附带查看在线玩家列表功能

发送/help查看机器人帮助

## 前置插件

- [CoolQAPI](https://github.com/zhang-anzhi/CoolQAPI)

- [OnlinePlayerAPI](https://github.com/zhang-anzhi/MCDReforgedPlugins/tree/master/OnlinePlayerAPI)

## 配置

`group_id`

允许交互的群组列表

`admin_id`

可以私聊执行管理员指令的qq号

`whitelist_add_with_bound`

默认值: `False`

玩家绑定游戏ID时添加白名单

`whitelist_remove_with_leave`

默认值: `True`

玩家退群时移除白名单

## 功能

### 普通玩家命令

`/list` 获取在线玩家列表

`/bound <ID>` 绑定你的游戏ID

`/mc <msg>` 向游戏内发送消息

`!!qq <msg>` 向qq群发送消息

需要注意普通玩家只能在群里执行指令，而管理可以私聊执行`/list`和`/mc`

### 管理员命令

#### 基础帮助

`/bound` 查看绑定相关帮助

`/whitelist` 查看白名单相关帮助

`/forward` 查看转发消息相关帮助

`/command <command>` 执行任意指令

#### 绑定相关

`/bound list` 查看绑定列表

`/bound check <qq number>` 查询绑定ID

`/bound unbound <qq number>` 解除绑定

`/bound <qq number> <ID>` 绑定新ID

#### 白名单相关

`/whitelist add <target>` 添加白名单成员

`/whitelist list` 列出白名单成员

`/whitelist off` 关闭白名单

`/whitelist on` 开启白名单

`/whitelist reload` 重载白名单

`/whitelist remove <target>` 删除白名单成员

`<target>` 可以是玩家名/目标选择器/UUID

#### 转发消息相关

`/forward info` 查看info转发状态

`/forward info <type> <qq number> on` 开启info转发

`/forward info <qq number> off` 关闭info转发

`/forward message` 查看message转发状态

`/forward message <type> <qq number> on` 开启message转发

`/forward message <qq number> off` 关闭message转发

`/forward qq` 查看qq转发状态

`/forward qq on` 开启qq转发

`/forward qq off` 关闭qq转发

`<qq number>`是qq号, `<type>`决定是群号还是管理的qq号

`<type>` 是`group`或者`private`, 用于标记群组或者私聊

`info`: 每一条触发on_info的消息

`message`: 游戏内的玩家聊天
