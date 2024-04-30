#2023.2.3下午，有人拆掉了cy的炸沟机，cy一气之下，拜托我写了这个插件
#我就不信这次还有人偷看我的代码！
#要是谁看到了，就请他吃KFC

from mcdreforged.api.all import *
from mcdreforged.api.command import *
import os
import json
import re
import time

PATH = './config/AutoBackup'
CONFIG_PATH = './config/AutoBackup/config.json'
BACKUP_PLAYER_PATH = './config/AutoBackup/backup_player.json'
DEFAULT_CONFIG = {
    "permission_level": 3,
    "interval_time": 60
}

help_msg = '''§r==============================================
§r当特定玩家加入游戏时实现自动备份功能
§r基于§cquick backup§r插件实现
§r使用§6!!autobackup help§r呼出使用方法
§r使用§6!!autobackup add <玩家名>§r添加玩家到自动备份名单
§r使用§6!!autobackup remove <玩家名>§r从自动备份名单中移除玩家
§r使用§6!!autobackup list§r列出所有在自动备份名单中的玩家
§r示例: §a!!autobackup add can_yi_§r
§r==============================================='''

def json_read(path: str) -> dict:
    with open(path, "r", encoding = "utf-8") as f:
        json_list = json.load(f)
    return json_list

def json_dump(path: str, default_list: list) -> None:
    with open(path, "w", encoding = "utf-8") as f:
        json.dump(default_list, f, indent=4, ensure_ascii = False)

def check_player_name(name: str) -> bool:
    if (re.fullmatch(r"\w+",name) is not None) and len(name)<=16 and not(name.lower().startswith('bot_')):
        return True
    else:
        return False

def send_help_msg(source: CommandSource):
    source.reply(help_msg)

def list_player(source: CommandSource):
    name = ''
    if len(BACKUP_PLAYER_LIST.keys()) == 0:
        source.reply('自动备份名单为空')
    else:
        for i in BACKUP_PLAYER_LIST.keys():
            name = name + ', ' + i
        source.reply('在自动备份名单中的玩家有: §a' + name[2:])

def add_player(source: CommandSource, context):
    player = context['player']
    if not check_player_name(player):
        source.reply('§4玩家名输入有误')
        return
    global BACKUP_PLAYER_LIST
    if not source.has_permission(CONFIG_LIST['permission_level']):
        source.reply('§4权限不足')
        return
    if player in BACKUP_PLAYER_LIST.keys():
        source.reply('§4玩家已在名单中')
        return
    BACKUP_PLAYER_LIST[player] = int(time.time() - 1600000000 - (CONFIG_LIST['interval_time'] * 60))
    json_dump(BACKUP_PLAYER_PATH, BACKUP_PLAYER_LIST)
    source.reply(f'已将玩家§a{player}§f加入自动备份名单')

def remove_player(source: CommandSource, context):
    player = context['player']
    if not check_player_name(player):
        source.reply('§4玩家名输入有误')
        return
    global BACKUP_PLAYER_LIST
    if not source.has_permission(CONFIG_LIST['permission_level']):
        source.reply('§4权限不足')
        return
    if not player in BACKUP_PLAYER_LIST.keys():
        source.reply('§4玩家不在名单中')
        return
    BACKUP_PLAYER_LIST.pop(player)
    json_dump(BACKUP_PLAYER_PATH, BACKUP_PLAYER_LIST)
    source.reply(f'已将玩家§a{player}§f移出自动备份名单')

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    global BACKUP_PLAYER_LIST
    if ENABLE_BACKUP and player in BACKUP_PLAYER_LIST.keys():
        now_time = int(time.time() - 1600000000)
        if now_time - BACKUP_PLAYER_LIST[player] >= (CONFIG_LIST['interval_time'] * 60):
            server.logger.info(f'玩家§a{player}§f加入了游戏, 进行自动备份')
            server.execute_command(f'!!qb make AutoBackup自动备份(玩家{player}加入游戏时创建)')
            BACKUP_PLAYER_LIST[player] = now_time
            json_dump(BACKUP_PLAYER_PATH, BACKUP_PLAYER_LIST)

def on_load(server: PluginServerInterface, old):
    global CONFIG_LIST
    global BACKUP_PLAYER_LIST
    global ENABLE_BACKUP
    ENABLE_BACKUP = True
    if not 'quick_backup_multi' in server.get_plugin_list():
        server.logger.info('§4所需的前置插件§aquick_backup_multi§4不存在')
        ENABLE_BACKUP = False
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    if not os.path.exists(CONFIG_PATH):
        json_dump(CONFIG_PATH, DEFAULT_CONFIG)
    if not os.path.exists(BACKUP_PLAYER_PATH):
        json_dump(BACKUP_PLAYER_PATH, {})
    CONFIG_LIST = json_read(CONFIG_PATH)
    BACKUP_PLAYER_LIST = json_read(BACKUP_PLAYER_PATH)
    server.logger.info('配置文件、自动备份玩家名单已加载')
    server.register_help_message('!!autobackup', server.get_self_metadata().description)
    builder = SimpleCommandBuilder()
    builder.command('!!autobackup', send_help_msg)
    builder.command('!!autobackup help', send_help_msg)
    builder.command('!!autobackup list', list_player)
    builder.command('!!autobackup add <player>', add_player)
    builder.command('!!autobackup remove <player>', remove_player)
    builder.arg('player', Text)
    #builder.print_tree(server.logger.info)
    builder.register(server)