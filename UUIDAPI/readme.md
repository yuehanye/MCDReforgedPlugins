# UUIDAPI

使用 `get_uuid(name: str)` 获取玩家UUID, 未查到返回 `None`

你不需要考虑服务器正盗版问题, UUIDAPI会自己判断

如果使用了 `BungeeCord` 并开启了正版验证, 或实际的UUID与 `server.properties` 中的 `online-mode` 并不匹配

将插件的 `manual_mode` 手动模式设置为一个布尔值即可覆盖 `server.properties` 的在线模式

---------

Use `get_uuid(name: str)` to get player UUID, return `None` if can not find

You don't have to think about online mode, UUIDAPI will judge it

If using the  `BungeeCord` and turned on the online mode, or actual UUID is not same as `online-mode` in `server.properties`

Set the `manual_mode` to a bool can cover online mode in `server.properties`
