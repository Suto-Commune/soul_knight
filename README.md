[![Pypi](https://img.shields.io/pypi/v/soul-knight-data-processing)](https://pypi.org/project/soul-knight-data-processing/)
[![Upload Python Package](https://github.com/Suto-Commune/soul_knight/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Suto-Commune/soul_knight/actions/workflows/python-publish.yml)


使用方法看`example.py`  或者 `example.py`，或者自己翻源码

使用GPL V3协议


```
pip install soul-knight-data-processing
```

将存档放入项目的com.ChillyRoom.DungeonShooter/files/
（没有就自建）

存档文件说明
主要解密的六个
files/game.data # 游戏基础数据 加密方式 1
files/item_data.data # 物品存档 加密方式 2
files/season_data.data # 赛季数据 加密方式 2
files/setting.data # 游戏设置 加密方式 2
files/statistics.data # 地下室统计 加密方式 2
files/task.data # 任务数据 加密方式 2
——————————
存档的其他文件说明
——————————
files/battles.data # 未完成的游戏 明文 JSON
files/net_battle.data # 在线联机数据 明文 JSON
files/sandbox_config.data # 电脑配置 明文 JSON
files/sandbox_maps.data # 电脑地图 明文 JSON
shared_prefs/com.ChillyRoom.DungeonShooter.v2.playerprefs.xml # 游戏数据 明文 XML

files/backup.data # 游戏数据备份 加密方式 1
files/mall_reload_data.data # 商城刷新数据 加密方式 2
files/monsrise_data.data # 怪兽崛起数据 加密方式 2


