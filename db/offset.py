class Pointer:
    player_count = 0x0050F500
    entity_list = 0x0050F4F8
    local_player = 0x00509B74
    view_matrix = 0x00501AE8
    console = 0x4090F0
    game_mode = 0x50F49C


class Offsets:
    name = 0x225
    health = 0xF8
    armor = 0xFC
    team = 0x32C
    viewX = 0x40
    viewY = 0x44
    rifle_ammo = 0x148
    pistol_ammo = 0x13C
    nades = 0x158
    force_attack = 0x224
    viewable = 0x408
    recoil = 0xEE444


# Main player
player_health = (0x00109B74, 0xF8)
player_vest = (0x00109B74, 0xFC)

# Guns
player_grenade = (0x109B74, 0x158)
player_ammo = [
    (0x00109B74, 0x150),  # MTP-57 Assault Rifle
    (0x00109B74, 0x148),  # A-ARD/10 Submachine Gun
    (0x00109B74, 0x14C),  # Precision Tech AD-81 Sniper Rifle
    (0x00109B74, 0x144),  # V-19 Combat Shotgun
    (0x00109B74, 0x140),  # TMP-M&A Carbine
    (0x00109B74, 0x13C),  # MK-77 Pistol
    (0x00109B74, 0x15C)]  # MK-77 Akimbo (double pistol)
