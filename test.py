import source.ASA.strucutres.teleporter as teleporter
import source.gacha_bot.structures.cargo_ledger as cargo_ledger
import time
import source.gacha_bot.gacha as gacha
import source.ASA.stations.custom_stations as custom_stations
import settings

gacha_metadata = custom_stations.get_station_metadata("GACHAPAIR1")
gacha_metadata.side = "left"

cargo_metadata = custom_stations.get_station_metadata(settings.cargo_pickup)


#cargo pickup
cargo_ledger.get_y_from_cargo()

#go to gacha and deposit into gacha
teleporter.teleport_not_default(gacha_metadata)
gacha.cargo_drop(gacha_metadata)