import win32gui
import win32con
import win32api
import sys
import contextlib
from time import sleep
from pymem import Pymem, logger

try:
    from Gauntlet.bin.colors import *
    from Gauntlet.db.offset import *
except ModuleNotFoundError:
    from bin.colors import *
    from db.offset import *

with contextlib.redirect_stdout(None):
    import pygame


def get_game_window(hwnd_name="AssaultCube"):
    while True:
        try:
            hwnd = win32gui.FindWindow(None, hwnd_name)
            window_rect = win32gui.GetWindowRect(hwnd)
            x = window_rect[0] - 5
            y = window_rect[1]
            width = window_rect[2] - x
            height = window_rect[3] - y
            return x, y, width, height, hwnd
        except:
            pass
        sleep(0.5)


def create_overlay(game_window):
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((game_window[2], game_window[3]), pygame.NOFRAME | pygame.DOUBLEBUF)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(
        hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
    )
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*Colors.invisible), 0, win32con.LWA_COLORKEY)
    return screen


def reset_overlay(game_window):
    win32gui.SetWindowPos(pygame.display.get_wm_info()["window"], -1, game_window[0], game_window[1], 0, 0, 0x0001)


def attach_process(proc_name="ac_client.exe"):
    try:
        with contextlib.redirect_stdout(None):
            logger.disabled = True
            mem = Pymem(proc_name)
            return mem
    except:
        sys.exit(f"Unable to attach to Process ({proc_name})")


def team_game(mem):
    return mem.read_int(Pointer.game_mode) in [0, 4, 5, 7, 11, 13, 14, 16, 17, 20, 21]


class Entity:
    def __init__(self, address, mem):
        self.address = address
        self.mem = mem
        self.pos = None
        self.name = None
        self.health = 0
        self.armor = 0
        self.team = 0
        self.alive = False
        self.esp = None

        self.update()

    def update(self):
        self.pos = self.get_pos()
        try:
            self.name = self.mem.read_string(self.address + Offsets.name)
        except UnicodeDecodeError:
            pass
        self.health = self.mem.read_int(self.address + Offsets.health)
        self.armor = self.mem.read_int(self.address + Offsets.armor)
        self.team = self.mem.read_int(self.address + Offsets.team)
        self.alive = 101 > self.health > 1
        self.esp = wts(view_matrix(self.mem), self.pos)

    def get_pos(self):
        pos = pygame.math.Vector3()
        pos.x = self.mem.read_float(self.address + 4)
        pos.y = self.mem.read_float(self.address + 8)
        pos.z = self.mem.read_float(self.address + 12)
        return pos

    def get_screen_location(self, local_player, aimbot=False):
        if aimbot:
            rect_w = 30
            rect_h = 60
            team_color = None

            if self.team == 0:
                team_color = 0
            elif self.team == 1:
                team_color = 1

            if team_game(self.mem):
                rect_color = Colors.blue if self.team else Colors.red
            else:
                rect_color = Colors.white

            if self.esp:
                scaling = self.pos.distance_to(local_player.pos) / 55
                position = self.esp.x - rect_w / 2, self.esp.y, rect_w / scaling, rect_h / scaling
                final = [scaling, rect_color, position, rect_color, self.name, self.health, 1, self.alive,
                         self.esp.x - rect_w / 2 + self.esp.y + rect_w / scaling + rect_h / scaling]
                return final

        rect_w = 30  # 20
        rect_h = 60  # 50
        enemy = False

        if self.team:
            enemy = True

        if team_game(self.mem):
            rect_color = Colors.blue if self.team else Colors.red
        else:
            rect_color = Colors.white

        if self.esp:
            scaling = self.pos.distance_to(local_player.pos) / 55
            # scaling = self.pos.distance_to(local_player.pos) / 23
            position = self.esp.x - rect_w / 2, self.esp.y, rect_w / scaling, rect_h / scaling
            # position = self.esp.x - 2, self.esp.y, rect_w / scaling, rect_h / scaling
            final = [scaling, rect_color, position, rect_color, self.name, self.health, enemy, self.alive,
                     self.esp.x - 2 + self.esp.y + rect_w / scaling + rect_h / scaling]
            return final


def view_matrix(mem):
    """
    reads 16 (16 * 4 bytes) floats from the view matrix pointer
    """
    matrix = list()
    offset = 0
    for _ in range(16):
        matrix.append(mem.read_float(Pointer.view_matrix + offset))
        offset += 4
    return matrix


def wts(v_matrix, pos):
    """
    world 2 screen
    returns a 2d vector
    """
    game_window = get_game_window()

    clip_x = pos.x * v_matrix[0] + pos.y * v_matrix[4] + pos.z * v_matrix[8] + v_matrix[12]
    clip_y = pos.x * v_matrix[1] + pos.y * v_matrix[5] + pos.z * v_matrix[9] + v_matrix[13]
    clip_w = pos.x * v_matrix[3] + pos.y * v_matrix[7] + pos.z * v_matrix[11] + v_matrix[15]

    if clip_w < 0.1:
        return False

    nds = pygame.math.Vector2()
    nds.x = clip_x / clip_w
    nds.y = clip_y / clip_w

    screen = pygame.math.Vector2()
    screen.x = ((nds.x / 2) + 0.5) * game_window[2]
    screen.y = ((-nds.y / 2) + 0.5) * game_window[3]
    return screen


def matrix_to_screen():
    mem = attach_process()

    while True:
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
                p.get_screen_location(local_player)
