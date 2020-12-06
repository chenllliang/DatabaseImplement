import threading
import struct
from types import *

from .constants import BLOCK_NUM, BLOCK_SIZE
from .utils import memLog, timeLog


class Pointer:
    types = {'NULL': b'00', 'SHIFT': b"01", "DISK": b"10", "MEMORY": b"11"}

    def __init__(self):
        self.type = b''
        self.data = b''

    def serialize(self):
        raise NotImplementedError


class NullPointer(Pointer):
    def serialize(self):
        pass


class ShiftPointer(Pointer):
    def __init__(self, dataStart: int, dataLength: int):
        super(ShiftPointer, self).__init__()
        self.type = Pointer.types['SHIFT']
        self.dataStart = dataStart
        self.dataLength = dataLength

    def serialize(self):
        return self.type+struct.pack('i',self.dataStart)+struct.pack('i',self.dataLength)


class Record:
    pass





class MemoryWatcher:
    pass


class MemoryBlock:
    """
    内存块类
    """

    def __init__(self, BLOCK_SIZE, id):
        self.data = '0'.encode('utf-8') * BLOCK_SIZE  # 初始化块内空间为BLOCK_SIZE个字节 ， utf-8编码英文和数字1字节，中文3字节
        self.max_size = BLOCK_SIZE
        self.used = False
        self.id = id

    def initailize(self):
        self.data = '0'.encode('utf-8') * BLOCK_SIZE  # 初始化块内空间为BLOCK_SIZE个字节 ， utf-8编码英文和数字1字节，中文3字节
        self.max_size = BLOCK_SIZE
        self.used = False
        self.id = id

    def addRecord(self,Record:Record):
        pass

    def deleteRecord(self,RecordIndex:int):
        pass

    def getRecord(self,RecotdIndex:int):
        pass



class DB_Cache:
    """
    数据缓冲区类
    """
    # 线程安全的单例确保所有表共享一个内存，不会有多个内存
    _instance_lock = threading.Lock()

    @memLog
    def __init__(self):
        self.memoryblocks = [MemoryBlock(BLOCK_SIZE, i) for i in range(BLOCK_NUM)]

    def __new__(cls, *args, **kwargs):
        if not hasattr(DB_Cache, "_instance"):
            with DB_Cache._instance_lock:
                if not hasattr(DB_Cache, "_instance"):
                    DB_Cache._instance = object.__new__(cls)
        return DB_Cache._instance
