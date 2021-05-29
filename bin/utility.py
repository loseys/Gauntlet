import time
import os
from os import environ
import win32gui
import win32process
import win32con
import win32api
import psutil
import contextlib
from pymem import *
try:
    from Gauntlet.db.offset import *
    from Gauntlet.bin.colors import *
except ModuleNotFoundError:
    from db.offset import *
    from bin.colors import *

if environ.get('PYGAME_HIDE_SUPPORT_PROMPT') is None:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame


class Utility:
    @classmethod
    def game_window(cls):
        """Gets height and weight of AssaultCube window."""
        content = win32gui.FindWindow(None, "AssaultCube")
        windowrect = win32gui.GetWindowRect(content)
        x = windowrect[0] - 5
        y = windowrect[1]
        width = windowrect[2] - x
        height = windowrect[3] - y
        return x, y, width, height

    @classmethod
    def track_game(cls):
        win32gui.SetWindowPos(pygame.display.get_wm_info()['window'],
                              -1, cls.game_window()[0], cls.game_window()[1], 0, 0, 0x0001)

    @staticmethod
    def current_focused_window():
        """Checks what's the current focused window name. Example output: 'ac_client.exe'"""
        time.sleep(1)
        win32gui.GetWindowText(win32gui.GetForegroundWindow())
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return psutil.Process(pid[-1]).name()

    @classmethod
    def team_game(cls, mem):
        return mem.read_int(Pointer.game_mode) in [0, 4, 5, 7, 11, 13, 14, 16, 17, 20, 21]

    @staticmethod
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
            time.sleep(0.8)

    @staticmethod
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

    @staticmethod
    def attach_process(proc_name="ac_client.exe"):
        try:
            with contextlib.redirect_stdout(None):
                mem = Pymem(proc_name)
                return mem
        except:
            sys.exit(f"Unable to attach to Process ({proc_name})")

    @staticmethod
    def reset_overlay(game_window):
        win32gui.SetWindowPos(pygame.display.get_wm_info()["window"], -1, game_window[0], game_window[1], 0, 0, 0x0001)
