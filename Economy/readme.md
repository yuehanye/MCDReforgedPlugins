# Economy

[English](https://github.com/zhang-anzhi/MCDReforgedPlugins/blob/master/Economy/readme_en.md)

> [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 经济插件

## 环境要求

**依赖的Python模块**

- PyYAML

**前置插件**

- [vault](https://github.com/zhang-anzhi/MCDReforgedPlugins/tree/master/vault)

## 使用方法

| 命令 | 功能 |
|---|---|
| !!money help | 查看帮助 |
| !!money | 查询你的余额 |
| !!pay <player> <amount> | 将你的钱支付给他人 |
| !!money top | 查看财富榜 |
| !!money check <player> | 查询他人余额 |
| !!money count <number> | 计算特定数量玩家总余额，all可以计算所有人 |
| !!money give <player> <amount> | 给予他人钱 |
| !!money take <player> <amount> | 拿取他人钱（余额不足时设为0） |
| !!money set <player> <amount> | 设置他人余额 |
| !!money update | 更新插件 |
| !!money reload | 重载插件 |

## 配置文件
配置文件为`config/economy.yml`

### CMD_PERMISSIONS
默认值:
```
'top': 1
'check': 2
'count': 1
'give': 3
'take': 3
'set': 3
'update': 2
'reload': 3
```

最低可以使用这些指令的权限等级

### DEFAULT_BALANCE
默认值:`10`

新玩家进入时的默认余额

### MAXIMAL_TOPS
默认值:`10`

使用`!!money top`时显示的数量

### MAX_LIMIT
默认值:`1e13`

金额参数的最大值，不要超过`1e26`

### REMINDER
默认值:`True`

余额被 `take` `give` `set`时是否提醒玩家