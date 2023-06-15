import SKD
import os
import fnmatch


def find_files(path, patterns):
    for root, dirs, files in os.walk(path):
        for pattern_ in patterns:
            for filename in fnmatch.filter(files, pattern_):
                yield os.path.join(root, filename)


USE = SKD.core.Convert()

directory = './'

pattern = ['*.data', "*.bytes"]

for file_path in find_files(directory, pattern):
    USE.FileName = file_path
    print("---"+file_path+"---")
    print(USE.de_open())
    print("++++++++++++")
