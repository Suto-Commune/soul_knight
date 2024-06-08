import SKD
import os
import fnmatch


def find_files(path, patterns):
    for root, dirs, files in os.walk(path):
        for pattern_ in patterns:
            for filename in fnmatch.filter(files, pattern_):
                print(filename)
                yield filename
                # yield os.path.join(root, filename)


USE = SKD.core.Convert()

# 存档文件目录
# 目录结尾一定要加上'/'
directory = './data/'
if not os.path.exists(directory):
    os.makedirs(directory)

pattern = ['*.data', "*.bytes"]

abc = int(input("0解密 1加密："))

for file_path in find_files(directory, pattern):
    USE.FilePath = directory + file_path
    USE.FileName_encrypt = file_path
    if abc == 0:
        USE.de_save()  # 解密 不可同时使用
    if abc == 1:
        USE.en_save()  # 加密 不可同时使用
    # print(USE.de_open())
