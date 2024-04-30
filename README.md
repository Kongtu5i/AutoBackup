# AutoBackup
当名单中的玩家加入我的世界服务器时进行自动备份
存档备份依靠fanllen_breath的QuickBackupM
[QuickBackupM仓库地址](https://github.com/TISUnion/QuickBackupM)

## 依赖

`QuickBackupM >= 1.8.0`

## 指令


`!!autobackup` 显示指令帮助

`!!autobackup help` 显示指令帮助

`!!autobackup add <player>` 添加玩家到自动备份名单

`!!autobackup remove <player>` 从自动备份名单中移除玩家

## 配置文件

### permission_level

默认值: 3

进行备份名单增删操作的最低权限

### interval_time

默认值: 60 单位：分

玩家自上次加入游戏后，多长时间再次加入游戏不会进行备份
（防止有的玩家猛烈抽插服务器）
