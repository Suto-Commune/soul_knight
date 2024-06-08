import base64
import json
import os
import re
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# File 类：处理文件加密和解密逻辑。
#
# encrypt 方法：根据文件名选择合适的加密方式。
# decrypt 方法：根据文件名选择合适的解密方式。
# is_json_encrypted 方法：判断文件是否需要进行JSON加密。
# get_key 方法：根据文件名获取对应的DES密钥。
# decrypt_xml 方法：处理XML文件的解密。
# encrypt_des 方法：使用DES算法加密数据。
# decrypt_des 方法：使用DES算法解密数据。
# xor 方法：使用异或操作加密/解密数据。
# Config 类：管理配置，如加密目录路径。
#
# Convert 类：处理文件的读取、保存、加密和解密。
#
# de_open 方法：打开文件并解密。
# de_save 方法：解密文件并保存为JSON格式。
# en_save 方法：从JSON文件加密并保存。
# encode 方法：使用 File 类的 encrypt 方法加密数据。
# decode 方法：使用 File 类的 decrypt 方法解密数据。


class File:
    def __init__(self):
        self.Const = self.Const()

    class Const:
        encryptedJsonGameFiles = [
            "game.data", "item_data.data", "item_data_backups.bytes", "setting.data",
            "statistic.data", "season_data.data", "season_data_backups.bytes",
            "task.data"
        ]

    # 加密文件
    def encrypt(self, data, file_name):
        result = data.encode('utf-8')
        if self.is_json_encrypted(file_name):
            # 如果文件是JSON加密的，则将其压缩格式化
            result = json.dumps(json.loads(data), separators=(',', ':')).encode('utf-8')
        key = self.get_key(file_name)
        if key:
            # 如果有对应的DES密钥，则进行DES加密
            result = self.encrypt_des(result, key)
        if "game" in file_name and "data" in file_name:
            # 如果文件是游戏数据，则进行异或加密
            result = self.xor(result)
        return result

    # 解密文件
    def decrypt(self, data, file_name):
        if file_name.endswith(".xml"):
            # 如果是XML文件，使用特殊的XML解密方法
            return self.decrypt_xml(data)
        result = data
        key = self.get_key(file_name)
        if key:
            # 如果有对应的DES密钥，则进行DES解密
            result = self.decrypt_des(result, key)
        if "game" in file_name and "data" in file_name:
            # 如果文件是游戏数据，则进行异或解密
            result = self.xor(result)
        if self.is_json_encrypted(file_name):
            # 如果文件是JSON加密的，则将其格式化
            result = json.dumps(json.loads(result.decode('utf-8')), separators=(',', ':')).encode('utf-8')
        return result.decode('utf-8')

    def is_json_encrypted(self, file_name):
        # 判断文件是否需要进行JSON加密
        return ("battle" in file_name and "data" in file_name) or file_name in self.Const.encryptedJsonGameFiles

    def get_key(self, file_name):
        # 获取文件对应的DES密钥
        if "item_data" in file_name or ("task" in file_name and "data" in file_name) or (
                "setting" in file_name and "data" in file_name) or "season_data" in file_name:
            return bytes([0x69, 0x61, 0x6d, 0x62, 0x6f, 0x0, 0x0, 0x0])
        if "statistic" in file_name and "data" in file_name:
            return bytes([0x63, 0x72, 0x73, 0x74, 0x31, 0x0, 0x0, 0x0])
        return None

    def decrypt_xml(self, data):
        # 解密XML文件
        attrs_regex = re.compile("(<.*?/>|<.*?</.*?>)")
        attrs_matcher = attrs_regex.finditer(data.decode('utf-8'))
        attrs = [match.group(0) for match in attrs_matcher]
        attrs.sort(key=lambda x: x.lower())
        final_xml = "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>\n<map>\n"
        final_xml += "\n".join(attrs)
        final_xml += "\n</map>"
        return final_xml

    def encrypt_des(self, data, key):
        # 使用DES算法加密数据
        cipher = DES.new(key, DES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(pad(data, DES.block_size)))

    def decrypt_des(self, data, key):
        # 使用DES算法解密数据
        data = base64.b64decode(data)
        cipher = DES.new(key, DES.MODE_ECB)
        return unpad(cipher.decrypt(data), DES.block_size)

    def xor(self, data):
        # 使用异或操作加密/解密数据
        key = b'WIZARD'
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


class Config:
    def __init__(self, encrypt_path='./com.ChillyRoom.DungeonShooter/files/encrypt'):
        self.encrypt_path = encrypt_path


class Convert:
    def __init__(self, config=Config()):
        self.File = File()
        self.config = config
        self.FileName = ""
        self.FileName_decrypt = ""
        self.FileName_encrypt = ""
        self.Id = 0

    def de_open(self):
        # 打开文件并解密
        with open(self.FileName, "rb") as f:
            decode_data = self.decode(f.read())
        return decode_data

    def de_save(self):
        # 解密文件并保存为JSON格式
        with open(self.FileName, "rb") as f:
            decode_data = self.decode(f.read())
        with open(self.FileName + ".json", "w") as f:
            will_write = json.dumps(json.loads(decode_data), ensure_ascii=False, indent=4)
            f.write(will_write.encode("gbk", 'ignore').decode("gbk", "ignore"))
        return will_write

    def en_save(self):
        # 从JSON文件加密并保存
        if not os.path.exists(self.FileName + ".json"):
            print("找不到文件 " + self.FileName + "。请检查文件是否存在，或者使用 de_save() 创建它。")
            return "文件未找到。"
        with open(self.FileName + ".json", "r") as f:
            encode_data = json.dumps(json.loads(f.read()), ensure_ascii=False, separators=(',', ':'))
            encode_data = self.encode(encode_data)

        # 判断是否创建文件夹
        if not os.path.exists(self.config.encrypt_path):
            os.makedirs(self.config.encrypt_path)

        mode = "wb" if "game" in self.FileName and "data" in self.FileName else "w"
        with open(self.FileName_encrypt, mode) as f:
            f.write(encode_data)
        return encode_data

    def encode(self, data: str):
        # 使用 File 类的 encrypt 方法加密数据
        return self.File.encrypt(data, self.FileName)

    def decode(self, data: bytes):
        # 使用 File 类的 decrypt 方法解密数据
        return self.File.decrypt(data, self.FileName)
