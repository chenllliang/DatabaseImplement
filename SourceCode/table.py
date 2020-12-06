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
    4字节总长度+ 4字节schema长度 + schema + head + result
    head: 32位起始位置+32位数据长度
    '''

    def __init__(self, schema: Schema):
        self.schema = schema
        self.record = {}
    def serialize(self):
        length = 0
        headMove = len(self.record) * 8
        head = b''
        result = b''
        for i in self.record.values():
            head += struct.pack('I', (length + headMove)) # 数据起始位置
            head += struct.pack('I', i.length) # 数据长度
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
            print(total_length,schema_length)
            # 使用反射找到类型
            for i,j in enumerate(schema.keys()):
                dataHeader =data[8+schema_length+i*8:8+schema_length+(i+1)*8]
                dataStartPlace = struct.unpack("I",dataHeader[0:4])[0]
                dataLength = struct.unpack("I", dataHeader[4:8])[0]
                print([i,j,dataStartPlace,dataLength])
                ret.record[j] = unserialize(data[8+schema_length+dataStartPlace:
                                                 8+schema_length+dataStartPlace+dataLength],schema[j],dataLength)
            print(ret.record)
        return ret


if __name__ == '__main__':
    a = Record(Schema({"age": "INT32", "name": "CHAR","email": "VARCHAR"}))
    a.record = {"age": TypeInt32(32), "name": TypeChar("chenliang"),"email": TypeVarchar("547205480@qq.com", 16)}
    with open("../TestCase/tableTest.bin","wb") as f:
        f.write(a.serialize())

    with open("../TestCase/tableTest.bin","rb") as f:
        r = Record.unserialize(f.read())

    print(r.record)