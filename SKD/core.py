import base64
import json
import os.path
import re

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad


class File:
    def __init__(self) -> None:
        pass

    class Const:
        encryptedJsonGameFiles = ["game.data", "item_data.data", "item_data_backups.bytes", "setting.data",
                                  "statistic.data", "season_data.data", "season_data_backups.bytes",
                                  "task.data"]  # 添加其他文件名到列表中

    # 加密文件
    def encrypt(self, data, file_name):
        result = data.encode('utf-8')
        if ("battle" in file_name and "data" in file_name) or file_name in self.Const.encryptedJsonGameFiles:
            result = json.dumps(json.loads(data), separators=(',', ':')).encode('utf-8')
        if "item_data" in file_name or ("task" in file_name and "data" in file_name) or (
                "setting" in file_name and "data" in file_name) or "season_data" in file_name:
            result = self.encrypt_des(result, bytes([0x69, 0x61, 0x6d, 0x62, 0x6f, 0x0, 0x0, 0x0]))
        if "statistic" in file_name and "data" in file_name:
            result = self.encrypt_des(result, bytes([0x63, 0x72, 0x73, 0x74, 0x31, 0x0, 0x0, 0x0]))
        if "game" in file_name and "data" in file_name:
            result = self.xor(result)
        return result

    # 解密文件
    def decrypt(self, data, file_name):
        result = data.decode('utf-8')
        if ".xml" in file_name:
            attrs_regex = re.compile("(<.*?/>|<.*?</.*?>)")
            attrs_matcher = attrs_regex.finditer(data.decode('utf-8'))
            attrs = []
            final_xml = "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>\n<map>"
            for attrs_match in attrs_matcher:
                for i in range(attrs_match.lastindex):
                    attrs.append(attrs_match.group(i))
            attrs.sort(key=lambda x: x.lower())
            attrs_arr = attrs
            for attr in attrs_arr:
                final_xml += "\n    " + attr
            final_xml += "\n</map>"
            result = final_xml
        if "item_data" in file_name or ("task" in file_name and "data" in file_name) or (
                "setting" in file_name and "data" in file_name) or "season_data" in file_name:
            result = self.decrypt_des(data, bytes([0x69, 0x61, 0x6d, 0x62, 0x6f, 0x0, 0x0, 0x0]))
        if "statistic" in file_name and "data" in file_name:
            result = self.decrypt_des(data, bytes([0x63, 0x72, 0x73, 0x74, 0x31, 0x0, 0x0, 0x0]))
        if "game" in file_name and "data" in file_name:
            result = self.xor(data)
        if ("battle" in file_name and "data" in file_name) or file_name in self.Const.encryptedJsonGameFiles:
            result = json.dumps(json.loads(result), indent=4)
        return result

    @staticmethod
    def xor(data):
        key = bytes([115, 108, 99, 122, 125, 103, 117, 99, 127, 87, 109, 108, 107, 74, 95])
        output = bytearray(len(data))
        for i in range(len(data)):
            output[i] = key[i % 15] ^ data[i]
        return bytes(output)

    @staticmethod
    def decrypt_des(data, key):
        iv = bytes([0x41, 0x68, 0x62, 0x6f, 0x6f, 0x6c, 0x0, 0x0])
        cipher_bytes = base64.b64decode(data)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        result_bytes = cipher.decrypt(cipher_bytes)
        result = unpad(result_bytes, DES.block_size).decode('utf-8')
        return result

    @staticmethod
    def encrypt_des(data, key):
        iv = bytes([0x41, 0x68, 0x62, 0x6f, 0x6f, 0x6c, 0x0, 0x0])
        cipher = DES.new(key, DES.MODE_CBC, iv)
        padded_data = pad(data, DES.block_size)
        result_bytes = cipher.encrypt(padded_data)
        result = base64.b64encode(result_bytes).decode('utf-8')
        return result


class Convert:
    File = File()
    FilePath = str()
    FileName_decrypt = str()
    FileName_encrypt = str()
    ChillyRoom = './com.ChillyRoom.DungeonShooter/files/'
    Id = int()

    def de_open(self):
        f = open(self.FilePath, "rb")
        decode_data = self.decode(f.read())
        f.close()
        return decode_data

    def de_save(self):
        f = open(self.FilePath, "rb")
        decode_data = self.decode(f.read())
        f.close()
        f = open(self.FilePath + ".json", "w",encoding="utf-8")
        decode_data = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', decode_data)
        will_write = json.dumps(json.loads(decode_data), ensure_ascii=False, indent=4)
        # 加了忽略无法转换的gbk内容.encode("gbk", 'ignore').decode("gbk", "ignore")
        f.write(will_write.encode("gbk", 'ignore').decode("gbk", "ignore"))
        f.close()
        return will_write

    def en_save(self):
        if not os.path.exists(self.FilePath + ".json"):
            print(
                "Cannot ind the file called " + self.FilePath + ".Check if the file exists or use de_save() to create "
                                                                "it.")
            return "File Not Found."
        f = open(self.FilePath + ".json", "r",encoding="utf-8")
        encode_data = json.dumps(json.loads(f.read()), ensure_ascii=False, separators=(',', ':'))

        encode_data = self.encode(encode_data)
        f.close()
        # 判断是否创建文件夹
        if not os.path.exists(self.ChillyRoom+'/encrypt/'):
            os.makedirs(self.ChillyRoom+'/encrypt/')
        f = open(self.ChillyRoom+'/encrypt/'+self.FileName_encrypt, "w",encoding='utf-8')
        # game单独的读写
        if "game" in self.FilePath and "data" in self.FilePath:
            f = open(self.ChillyRoom+'/encrypt/'+self.FileName_encrypt, "wb")
        will_write = encode_data
        f.write(will_write)
        f.close()
        return will_write

    def encode(self, data: str):
        byte = data
        return self.File.encrypt(byte, self.FilePath)

    def decode(self, data: bytes):
        byte = data
        return self.File.decrypt(byte, self.FilePath)
