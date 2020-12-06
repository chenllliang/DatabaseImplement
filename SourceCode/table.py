from SourceCode.types import *


class Schema(Data):
    def __init__(self,arg:dict):
        self.schema = arg

    def serialize(self):
        return str(self.schema).encode()

    def unserialize(self,data):
        pass


class Record(Data):
    '''
    记录类，一条记录由多种类型的数据组成，使用变长+定长的方式，变长字段在定长字段之后
    32位总长度+ 32位schema长度 + schema + head + result
    '''

    def __init__(self, schema: Schema):
        self.schema = schema
        self.record = None
    def serialize(self):
        length = 0
        headMove = len(self.record) * 2
        head = b''
        result = b''
        for i in self.record.values():
            head += struct.pack('I', (length + headMove) * 4)
            head += struct.pack('I', i.length)
            length += i.length
            result += i.serialize()
        content = self.schema.serialize()+head + result
        schema_length = struct.pack('I',len(self.schema.serialize()))
        content = schema_length + content
        total_length = len(content)
        ret = struct.pack('I',total_length)+content
        return ret

    @classmethod
    def unserialize(self,data):
        ret = Record(None)
        if not isinstance(data,bytes):
            raise ValueError("unserialize has to have bytes input")
        else:
            total_length = struct.unpack("I",data[0:4])[0]
            schema_length = struct.unpack("I", data[4:8])[0]
            schema = eval(data[8:8+schema_length].decode())
            ret.schema = schema
            # 使用反射找到类型



if __name__ == '__main__':
    a = Record(Schema({"age": "TypeInt32", "name": "TypeChar","email": "TypeVarchar"}))
    a.record = {"age": TypeInt32(32), "name": TypeChar("chenliang"),"email": TypeVarchar("547205480@qq.com", 16)}
    with open("../TestCase/tableTest.bin","wb") as f:
        f.write(a.serialize())

    with open("../TestCase/tableTest.bin","rb") as f:
        r = Record.unserialize(f.read())