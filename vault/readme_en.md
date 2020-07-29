# vault

[简体中文](https://github.com/zhang-anzhi/vault/blob/master/readme.md)

> Economic plugin preposition
>
> It provides the API needed by other economic plugins

## Develop Document

**Import**

Add these things to`on_load`:
```
global vault
vault = server.get_plugin_instance('vault')
```

**Call**

| Method | Function |
|---|---|
| new(player) | Create account for `player`, the balance will be `0`, you can call it in `on_player_joined` |
| pay(player_from, player_to, amount) | Take`amount` from `player_from` and give to `player_to`, return `1`. If can not find player, return `-1`; if balance is not enough, return `-3` |
| check(player) | Check balance from `player`, then return the balance. If can not find player, return `-1` |
| give(player, amount) | Give `amount` to  `player`, return `1`. If can not find player, return `-1` |
| take(player, amount) | Take`amount` from `player`, return `1`. If can not find player, return `-1`; if balance is not enough, return `-3` |
| set(player, amount) | Set `player`'s balance to `amount`，return `1`. If can not find player, return `-1` |
| top() | Return a dictionary sorted by balance from top to bottom |

`top()` will return a dictionary like this:
```
{
    'player1': 10
    'player2': 9
    'player3': 8
    'player4': 7
    ......
}
```

**Tips**

- About the return value：
    
    1.If return `1`, which means success
    
    2.If return `-1`, which means this player has no account
    
    3.If return `-2`, which means input is illegal
    
    4.If return `-3`, which means the balance is not enough
    
- When you call methods which needs to pass the information`amount`, use`Decimal(amount)'`to have more precision

- If you want to control the precision of `amount`, use`Decimal(amount).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)`to pass`amount`
