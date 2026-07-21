import time 
import settings
import json
from source.utility import utils ,template , windows ,variables ,screen ,local_player
from source.logs import gachalogs as logs
from source.ASA.strucutres import teleporter , inventory
from source.ASA.stations import custom_stations
from source.ASA.player import player_inventory , player_state
import source.gacha_bot.config 

def is_open():
    return template.check_template_no_bounds("cargo_ledger")

def get_y_from_cargo():
    utils.turn_down(20)
    inventory.open()
    if is_open():
        inventory.search_in_object("Trap")
        inventory.transfer_all_from() 
    inventory.close()
    utils.turn_up(20)
    ...
