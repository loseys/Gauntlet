# coding: utf-8

import time
import threading
import keyboard
from operator import itemgetter
from pymem.process import *
try:
    from Gauntlet.bin.utility import Utility
    from Gauntlet.bin.message import Message
    from Gauntlet.plugins.matrix import *
    from Gauntlet.bin.memory import *
except ModuleNotFoundError:
    from bin.utility import Utility
    from bin.message import Message
    from plugins.matrix import *
    from bin.memory import *

# Disabling the Pymem verbose.
logger = logging.getLogger("pymc3")
logger.propagate = False


class Trainer:
    """Gauntlet main class."""
    def __init__(self):
        pygame.init()
        pygame.font.init()

        # Checks if the AssaultCube is open.
        try:
            self.screen = pygame.display.set_mode((Utility.game_window()[2], Utility.game_window()[3]), pygame.NOFRAME)
            self.active = True
            self.overlay_font = pygame.font.SysFont('Courier', size=17)
        except Exception as error:
            if str(error).startswith("(1400, 'GetWindowRect'"):
                print(Message.ac_not_found)
                quit()

        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                               win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*Colors.invisible), 0, win32con.LWA_COLORKEY)

        # Self variables.
        self.trainer_menu_page = 0  # Page of trainer menu.
        self.exit_trainer = False
        self.hide_menu = None
        self.focused = None
        self.current_team = None

        # Starts a threading process to detect if the user has pressed some key.
        thread_process = threading.Thread(target=self.pressed_key, args=())
        thread_process.daemon = True
        thread_process.start()
        self.start()

    def trainer_menu(self):
        if self.trainer_menu_page == 0:
            text = self.overlay_font.render(f"◄ F1         F2 ►", False, StatusColor.menu_arrows)
            self.screen.blit(text, (15, 230))
            text = self.overlay_font.render("[F3] " + "health + 100", False, StatusColor.page_0_option_0)
            self.screen.blit(text, (15, 250))
            text = self.overlay_font.render("[F4] " + "Vest + 50", False, StatusColor.page_0_option_1)
            self.screen.blit(text, (15, 265))
            text = self.overlay_font.render("[F5] " + "Ammo + 80", False, StatusColor.page_0_option_2)
            self.screen.blit(text, (15, 280))
            text = self.overlay_font.render("[F6] " + "Grenade + 15", False, StatusColor.page_0_option_3)
            self.screen.blit(text, (15, 295))
            text = self.overlay_font.render("[F8] " + "Hide menu", False, StatusColor.page_0_option_4)
            self.screen.blit(text, (15, 320))
            text = self.overlay_font.render("[F9] " + "Exit", False, StatusColor.page_0_option_5)
            self.screen.blit(text, (15, 335))

        elif self.trainer_menu_page == 1:
            text = self.overlay_font.render(f"◄ F1         F2 ►", False, StatusColor.menu_arrows)
            self.screen.blit(text, (15, 230))
            text = self.overlay_font.render("[F3] " + "Inf. health", False, StatusColor.page_1_option_0)
            self.screen.blit(text, (15, 250))
            text = self.overlay_font.render("[F4] " + "Inf. vest", False, StatusColor.page_1_option_1)
            self.screen.blit(text, (15, 265))
            text = self.overlay_font.render("[F5] " + "Inf. ammo", False, StatusColor.page_1_option_2)
            self.screen.blit(text, (15, 280))
            text = self.overlay_font.render("[F6] " + "Inf. grenade", False, StatusColor.page_1_option_3)
            self.screen.blit(text, (15, 295))
            text = self.overlay_font.render("[F8] " + "Hide menu", False, StatusColor.page_1_option_4)
            self.screen.blit(text, (15, 320))
            text = self.overlay_font.render("[F9] " + "Exit", False, StatusColor.page_1_option_5)
            self.screen.blit(text, (15, 335))

        elif self.trainer_menu_page == 2:
            text = self.overlay_font.render(f"◄ F1         F2 ►", False, StatusColor.menu_arrows)
            self.screen.blit(text, (15, 230))
            text = self.overlay_font.render("[F3] " + "ESP", False, StatusColor.page_3_option_0)
            self.screen.blit(text, (15, 250))
            text = self.overlay_font.render("[F4] " + "Inside floor", False, StatusColor.page_3_option_1)
            self.screen.blit(text, (15, 265))
            text = self.overlay_font.render("[F5] " + "Ghost mode", False, StatusColor.page_3_option_2)
            self.screen.blit(text, (15, 280))
            text = self.overlay_font.render("[F6] " + "Aimbot (ctrl)", False, StatusColor.page_3_option_3)
            self.screen.blit(text, (15, 295))
            text = self.overlay_font.render("[F8] " + "Hide menu", False, StatusColor.page_3_option_4)
            self.screen.blit(text, (15, 320))
            text = self.overlay_font.render("[F9] " + "Exit", False, StatusColor.page_3_option_5)
            self.screen.blit(text, (15, 335))

    def pressed_key(self):
        """Detects if some key has pressed and do something (threading)."""
        pm = pymem.Pymem("ac_client.exe")
        game_module = module_from_name(pm.process_handle, "ac_client.exe").lpBaseOfDll

        # Variables
        self.current_team = pm.read_int(Memory.get_ptr_addr(game_module + 0x109B74, [0x1D8]))
        infinite_health = False
        infinite_vest = False
        infinite_ammo = False
        infinite_health = False
        infinite_grenade = False
        esp_view = False
        inside_floor = False
        current_position = None
        pressed_key_time_sleep = 1
        ghost_mode = False
        aimbot = False
        current_player_aimbot = []
        ctrl_aimbot = False

        class ThreadingFunctions:
            """Class that store functions that will be called with threading mode."""
            @staticmethod
            def func_infinity_health():
                while infinite_health:
                    pm.write_int(Memory.get_ptr_addr(game_module + player_health[0], [player_health[1]]), 999)
                    time.sleep(0.2)

            @staticmethod
            def func_infinity_vest():
                while infinite_vest:
                    pm.write_int(Memory.get_ptr_addr(game_module + player_vest[0], [player_vest[1]]), 999)
                    time.sleep(0.2)

            @staticmethod
            def func_infinity_ammo():
                while infinite_ammo:
                    for content in player_ammo:
                        pm.write_int(Memory.get_ptr_addr(game_module + content[0], [content[1]]), 999)
                    time.sleep(0.2)

            @staticmethod
            def func_infinity_grenade():
                while infinite_grenade:
                    pm.write_int(Memory.get_ptr_addr(game_module + player_grenade[0], [player_grenade[1]]), 999)
                    time.sleep(0.2)

        class FunctionsPage3:
            @classmethod
            def esp_box(cls):
                cls.mem = attach_process()
                mem = cls.mem
                if self.focused:
                    position_group = []
                    local_address = mem.read_int(Pointer.local_player)
                    local_player = Entity(local_address, mem)
                    entity_player = list()
                    offset = 0
                    entity_count = mem.read_int(Pointer.player_count)
                    entity_list = mem.read_int(Pointer.entity_list)

                    for _ in range(entity_count):
                        entity = mem.read_int(entity_list + offset)
                        if entity:
                            entity_player.append(Entity(mem.read_int(entity_list + offset), mem))
                        offset += 4  # Next entity is 4 bytes apart

                    for p in entity_player:
                        if p.alive:
                            content = p.get_screen_location(local_player)
                            if content:
                                location = content[2]
                                p0 = location[0]
                                p1 = location[1]
                                p2 = location[2]
                                p3 = location[3]

                                distance = int(int(p2) / 2)
                                if distance > 30:
                                    distance = 30
                                elif distance < 10:
                                    distance = 11

                                health = content[5]
                                player_color = content[3]
                                position_group.append([p0, p1, p2, p3])
                                pygame.draw.rect(self.screen, player_color, (p0, p1, p2, p3), 1)

                                # Health
                                self.overlay_font_health = pygame.font.SysFont('Courier', size=distance)
                                text = self.overlay_font_health.render(str(health), False, Colors.white)

                                self.screen.blit(text, (p0, p1-p1/10))
                    pygame.display.flip()
                    self.screen.fill((255, 0, 128))
                    # pygame.display.flip()

                    # for coordinates in position_group:
                    #    pygame.draw.rect(self.screen, Colors.invisible, (coordinates[0], coordinates[1],
                    #                                                     coordinates[2], coordinates[3]), 1)
                    Trainer.trainer_menu(self)

            @classmethod
            def aimbot(cls, ctrl_status):
                # Move the mouse to the player.
                if current_player_aimbot and ctrl_status:
                    cd3 = current_player_aimbot[5]
                    cd4 = current_player_aimbot[6]
                    cd1 = int(current_player_aimbot[2]+cd3/5.5)
                    cd2 = int(current_player_aimbot[3]+cd4/5.5)

                    win32api.SetCursorPos((cd1, cd2))
                    # win32api.SetCursorPos(((cd1-cd2), (cd3-cd4)))

                cls.mem = attach_process()
                mem = cls.mem
                if self.focused:
                    local_address = mem.read_int(Pointer.local_player)
                    local_player = Entity(local_address, mem)
                    entity_player = list()
                    offset = 0
                    entity_count = mem.read_int(Pointer.player_count)
                    entity_list = mem.read_int(Pointer.entity_list)
                    player_list = []

                    for _ in range(entity_count):
                        entity = mem.read_int(entity_list + offset)
                        if entity:
                            entity_player.append(Entity(mem.read_int(entity_list + offset), mem))
                        offset += 4  # Next entity is 4 bytes apart

                    for p in entity_player:
                        content = p.get_screen_location(local_player)
                        if content:
                            player_list.append(content)

                    player_list = sorted(player_list, key=itemgetter(8))

                    for i in player_list:
                        content = i

                        # Verifys if is enemy.
                        if self.current_team == 1 and content[6]:
                            continue
                        if self.current_team == 0 and content[6]:
                            continue

                        if content:
                            location = content[2]
                            p0 = location[0]
                            p1 = location[1]
                            p2 = location[2]
                            p3 = location[3]

                            if not content[4] in player_list[0]:
                                if content[5] <= 0:
                                    continue
                                current_player_aimbot.clear()
                                current_player_aimbot.append(content[4])
                                current_player_aimbot.append(content[5])
                                current_player_aimbot.append(int(p0))
                                current_player_aimbot.append(int(p1))
                                current_player_aimbot.append(content[6])
                                current_player_aimbot.append(int(p2))
                                current_player_aimbot.append(int(p3))

                            if not current_player_aimbot:
                                current_player_aimbot.append(content[4])
                                current_player_aimbot.append(content[5])
                                current_player_aimbot.append(int(p0))
                                current_player_aimbot.append(int(p1))
                                current_player_aimbot.append(content[6])
                                current_player_aimbot.append(int(p2))
                                current_player_aimbot.append(int(p3))

                            if current_player_aimbot[0] == content[4]:
                                current_player_aimbot.clear()
                                current_player_aimbot.append(content[4])
                                current_player_aimbot.append(content[5])
                                current_player_aimbot.append(int(p0))
                                current_player_aimbot.append(int(p1))
                                current_player_aimbot.append(content[6])
                                current_player_aimbot.append(int(p2))
                                current_player_aimbot.append(int(p3))

                                if current_player_aimbot[1] <= 0:
                                    current_player_aimbot.clear()

        while True:
            if esp_view:
                FunctionsPage3.esp_box()

            if aimbot:
                if keyboard.is_pressed("ctrl"):
                    if not ctrl_aimbot:
                        ctrl_aimbot = True
                        time.sleep(pressed_key_time_sleep)
                    else:
                        ctrl_aimbot = False
                        time.sleep(pressed_key_time_sleep)
                FunctionsPage3.aimbot(ctrl_status=ctrl_aimbot)

            if ghost_mode:
                increase_value = 0.30
                if keyboard.is_pressed("w"):
                    y = pm.read_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x38]))
                    pm.write_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x38]), y + increase_value)
                if keyboard.is_pressed("a"):
                    x = pm.read_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x34]))
                    pm.write_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x34]), x - increase_value)
                if keyboard.is_pressed("s"):
                    y = pm.read_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x38]))
                    pm.write_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x38]), y - increase_value)
                if keyboard.is_pressed("d"):
                    x = pm.read_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x34]))
                    pm.write_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x34]), x + increase_value)
                if keyboard.is_pressed("space"):
                    z = pm.read_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x3C]))
                    pm.write_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x3C]), z + 1)
                if keyboard.is_pressed("ctrl"):
                    z = pm.read_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x3C]))
                    pm.write_float(Memory.get_ptr_addr(game_module + 0x10F4F4, [0x3C]), z - increase_value)

            # Back page.
            if keyboard.is_pressed("F1"):
                if (self.trainer_menu_page - 1) >= 0:
                    self.trainer_menu_page -= 1
                    time.sleep(pressed_key_time_sleep)

            # Next page.
            elif keyboard.is_pressed("F2"):
                if (self.trainer_menu_page + 1) <= 4:
                    self.trainer_menu_page += 1
                    time.sleep(pressed_key_time_sleep)

            # Trainer menu hide.
            elif keyboard.is_pressed("F8"):
                if not self.hide_menu:
                    StatusColor.page_0_option_4 = Colors.white
                    self.hide_menu = True
                    time.sleep(pressed_key_time_sleep)
                else:
                    StatusColor.page_0_option_4 = Colors.green
                    self.hide_menu = False
                    time.sleep(pressed_key_time_sleep)

            # Trainer exit.
            elif keyboard.is_pressed("F9"):
                self.exit_trainer = True

            try:
                if self.trainer_menu_page == 0:
                    pass
            except AttributeError:
                exit()

            if self.trainer_menu_page == 0:
                # Health + 100
                if keyboard.is_pressed("F3"):
                    print(player_health[0], player_health[1])
                    current_health = pm.read_int(Memory.get_ptr_addr(game_module + player_health[0],
                                                                     [player_health[1]]))
                    pm.write_int(Memory.get_ptr_addr(game_module + player_health[0], [player_health[1]]),
                                 current_health + 100)
                    time.sleep(pressed_key_time_sleep)

                # Vest + 50
                elif keyboard.is_pressed("F4"):
                    current_vest = pm.read_int(Memory.get_ptr_addr(game_module + player_vest[0], [player_vest[1]]))
                    pm.write_int(Memory.get_ptr_addr(game_module + player_vest[0], [player_vest[1]]), current_vest + 50)
                    time.sleep(pressed_key_time_sleep)

                # Ammo + 80
                elif keyboard.is_pressed("F5"):
                    for item in player_ammo:
                        current_ammo = pm.read_int(Memory.get_ptr_addr(game_module + item[0], [item[1]]))
                        pm.write_int(Memory.get_ptr_addr(game_module + item[0], [item[1]]), current_ammo + 80)
                    time.sleep(pressed_key_time_sleep)

                # Grenade + 15
                elif keyboard.is_pressed("F6"):
                    current_vest = pm.read_int(Memory.get_ptr_addr(game_module + player_grenade[0],
                                                                   [player_grenade[1]]))
                    pm.write_int(Memory.get_ptr_addr(game_module + player_grenade[0], [player_grenade[1]]),
                                 current_vest + 15)
                    time.sleep(pressed_key_time_sleep)

            elif self.trainer_menu_page == 1:
                # Infinite health.
                if keyboard.is_pressed("F3"):
                    if infinite_health:
                        StatusColor.page_1_option_0 = Colors.green
                        SnapShot.page_1_option_0 = Colors.green
                        infinite_health = False
                        time.sleep(pressed_key_time_sleep)

                    # Calls a loop threading.
                    elif not infinite_health:
                        StatusColor.page_1_option_0 = Colors.select
                        SnapShot.page_1_option_0 = Colors.select
                        infinite_health = True
                        thread_process_ih = threading.Thread(target=ThreadingFunctions.func_infinity_health, args=())
                        thread_process_ih.daemon = True
                        thread_process_ih.start()
                        time.sleep(pressed_key_time_sleep)

                # Infinite vest.
                elif keyboard.is_pressed("F4"):
                    if infinite_vest:
                        StatusColor.page_1_option_1 = Colors.green
                        SnapShot.page_1_option_1 = Colors.green
                        infinite_vest = False
                        time.sleep(pressed_key_time_sleep)

                    # Calls a loop threading.
                    elif not infinite_vest:
                        StatusColor.page_1_option_1 = Colors.select
                        SnapShot.page_1_option_1 = Colors.select
                        infinite_vest = True
                        thread_process_iv = threading.Thread(target=ThreadingFunctions.func_infinity_vest, args=())
                        thread_process_iv.daemon = True
                        thread_process_iv.start()
                        time.sleep(pressed_key_time_sleep)

                # Infinite ammo.
                elif keyboard.is_pressed("F5"):
                    if infinite_ammo:
                        StatusColor.page_1_option_2 = Colors.green
                        SnapShot.page_1_option_2 = Colors.green
                        infinite_ammo = False
                        time.sleep(pressed_key_time_sleep)

                    # Calls a loop threading.
                    elif not infinite_ammo:
                        StatusColor.page_1_option_2 = Colors.select
                        SnapShot.page_1_option_2 = Colors.select
                        infinite_ammo = True
                        thread_process_ia = threading.Thread(target=ThreadingFunctions.func_infinity_ammo, args=())
                        thread_process_ia.daemon = True
                        thread_process_ia.start()
                        time.sleep(pressed_key_time_sleep)

                # Infinite grenade.
                elif keyboard.is_pressed("F6"):
                    if infinite_grenade:
                        StatusColor.page_1_option_3 = Colors.green
                        SnapShot.page_1_option_3 = Colors.green
                        infinite_grenade = False
                        time.sleep(pressed_key_time_sleep)

                    # Calls a loop threading.
                    elif not infinite_grenade:
                        StatusColor.page_1_option_3 = Colors.select
                        SnapShot.page_1_option_3 = Colors.select
                        infinite_grenade = True
                        thread_process_ig = threading.Thread(target=ThreadingFunctions.func_infinity_grenade, args=())
                        thread_process_ig.daemon = True
                        thread_process_ig.start()
                        time.sleep(pressed_key_time_sleep)

            elif self.trainer_menu_page == 2:
                # ESP box
                if keyboard.is_pressed("F3"):
                    if not esp_view:
                        StatusColor.page_3_option_0 = Colors.select
                        SnapShot.page_3_option_0 = Colors.select
                        esp_view = True
                    else:
                        StatusColor.page_3_option_0 = Colors.green
                        SnapShot.page_3_option_0 = Colors.green
                        esp_view = False
                    time.sleep(pressed_key_time_sleep)

                # Inside floor.
                elif keyboard.is_pressed("F4"):
                    if not inside_floor:
                        StatusColor.page_3_option_1 = Colors.select
                        SnapShot.page_3_option_1 = Colors.select
                        inside_floor = True
                        if not current_position:
                            current_position = pm.read_float(Memory.get_ptr_addr(game_module + 0x109B74, [0x5C]))
                        pm.write_float(Memory.get_ptr_addr(game_module + 0x109B74, [0x5C]), current_position-15.0)
                    else:
                        StatusColor.page_3_option_1 = Colors.green
                        SnapShot.page_3_option_1 = Colors.green
                        inside_floor = False
                        pm.write_float(Memory.get_ptr_addr(game_module + 0x109B74, [0x5C]), current_position)
                    time.sleep(pressed_key_time_sleep)

                # Ghost mode.
                elif keyboard.is_pressed("F5"):
                    if not ghost_mode:
                        StatusColor.page_3_option_2 = Colors.select
                        SnapShot.page_3_option_2 = Colors.select
                        ghost_mode = True
                    else:
                        StatusColor.page_3_option_2 = Colors.green
                        SnapShot.page_3_option_2 = Colors.green
                        ghost_mode = False
                    time.sleep(pressed_key_time_sleep)

                # Aimbot.
                elif keyboard.is_pressed("F6"):
                    if not aimbot:
                        StatusColor.page_3_option_3 = Colors.select
                        SnapShot.page_3_option_3 = Colors.select
                        aimbot = True
                    else:
                        StatusColor.page_3_option_3 = Colors.green
                        SnapShot.page_3_option_3 = Colors.green
                        aimbot = False
                    time.sleep(pressed_key_time_sleep)

    def start(self):
        try:
            while self.active:
                # Checks if the exit button has been pressed.
                if self.exit_trainer:
                    exit()

                # Checks if the AssaultCube window (ac_client.exe) are focused by user, if not it hide the menu of
                # options.
                if Utility.current_focused_window().startswith('ac_client'):
                    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
                    self.focused = True
                    if self.hide_menu:
                        hide_menu()
                    else:
                        unhide_menu()
                else:
                    self.focused = False
                    hide_menu()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.active = False

                Utility.track_game()
                self.screen.fill(Colors.invisible)

                # Gauntlet menu vvv
                self.trainer_menu()
                # Gauntlet menu ^^^

                pygame.display.update()

                if keyboard.is_pressed("F9"):
                    self.active = False
                    pygame.quit()
                    quit()

        except Exception as error:
            print(error)


if __name__ == '__main__':
    app = Trainer()
    app.__init__()
