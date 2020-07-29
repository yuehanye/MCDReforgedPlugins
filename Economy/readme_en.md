# Economy

[简体中文](https://github.com/zhang-anzhi/Economy/blob/master/readme.md)

> A Economic Plugin for [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)

## Environment

**Required python module**

- PyYAML

**Required plugin**

- [vault](https://github.com/zhang-anzhi/MCDReforgedPlugins/tree/master/vault)

## Usage

| Command | Function |
|---|---|
| !!money help | Show help message |
| !!money | Check your balance |
| !!pay <player> <amount> | Pay your money to other player |
| !!money top | Show the tops |
| !!money check <player> | Check player balance |
| !!money count <number> | Count top `number` players total balance, `all`can count all players |
| !!money give <player> <amount> | Give money to player |
| !!money take <player> <amount> | Take money from player(If not enough, set to 0) |
| !!money set <player> <amount> | Set balance to player |
| !!money update | Update plugin |
| !!money reload | Reload plugin |

## Config
The config file is`config/economy.yml`

### CMD_PERMISSIONS
Default:
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

The minimum permission needed to use these commands

### DEFAULT_BALANCE
Default:`10`

Default balance when new player joined

### MAXIMAL_TOPS
Default:`10`

Display players when use`!!money top`

### MAX_LIMIT
Default:`1e13`

Max limit of amount parameter, do not exceed `1e26`

### REMINDER
Default:`True`

When balance changed by `take` `give` `set`reminder player
