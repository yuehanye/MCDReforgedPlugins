# vault

[English](https://github.com/zhang-anzhi/vault/blob/master/readme_en.md)

> 经济类插件前置
>
> 它为其他的需要基于经济系统的插件提供了所需的API

## 开发文档

**导入**

在`on_load`中加入以下内容:
```
global vault
vault = server.get_plugin_instance('vault')
```

**调用**

| 方法 | 功能 |
|---|---|
| new(player) | 为`player`新建账户并将余额设置为`0`，你可以在`on_player_joined`中调用它 |
| pay(player_from, player_to, amount) | 将`player_from`的余额拿取`amount`给予`player_to`，然后返回`1`。如果没有查询到该玩家，返回`-1`；如果余额不足，返回`-3` |
| check(player) | 查询`player`的余额，然后返回余额。如果没有查询到该玩家，返回`-1` |
| give(player, amount) | 将`amount`给予`player`，然后返回`1`。如果没有查询到该玩家，返回`-1` |
| take(player, amount) | 将`amount`从`player`的余额中拿取，然后返回`1`。如果没有查询到该玩家，返回`-1`；如果余额不足，返回`-3` |
| set(player, amount) | 将`player`的余额设置为`amount`，然后返回`1`。如果没有该玩家，返回`-1` |
| top() | 返回一个玩家数据按余额高低排序后的字典|

`top()`将会返回字典如下:
```
{
    'player1': 10
    'player2': 9
    'player3': 8
    'player4': 7
    ......
}
```

**提示**
- 关于返回值：
    
    1.如果返回`1`，表示操作成功
    
    2.如果返回`-1`，表示该玩家没有账户
    
    3.如果返回`-2`，表示输入不合法
    
    4.如果返回`-3`，表示余额不足
    
- 当传递实参`amount`时，使用`Decimal(amount)`传入一个Decimal类型的数据以达到更多的精度

- 如果你想控制`amount`的精度，使用`Decimal(amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)`来传入`amount`