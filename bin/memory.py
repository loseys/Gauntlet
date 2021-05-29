from pymem import *


class Memory:
    @staticmethod
    def get_ptr_addr(base, offsets):
        pm = pymem.Pymem("ac_client.exe")
        addr = pm.read_int(base)
        for i in offsets:
            if i in offsets:
                if i != offsets[-1]:
                    addr = pm.read_int(addr + i)
        return addr + offsets[-1]
