def get_data():
    import requests
    import re
    import wget
    import os
    import zipfile
    import shutil

    URL = "http://www.chillyroom.com/zh"
    INFO = requests.get(URL)

    regex = r"https:\/\/apk(.*).apk"

    matches = re.finditer(regex, INFO.text, re.MULTILINE)
    link = str()
    for matchNum, match in enumerate(matches, start=1):
        link = match.group()

    # 创建data
    if not os.path.exists("data"):
        os.mkdir("data")
    # 下载元气骑士文件
    if not os.path.exists("./data/sk.apk"):
        print("正在下载最新的APK")
        wget.download(link, "./data/sk.apk")
    # 解压文件
    if not os.path.exists("./data/sk"):
        print("解压中")
        with zipfile.ZipFile("./data/sk.apk", "r") as f:
            for file in f.namelist():
                f.extract(file, "./data/sk")
            f.close()

    if not os.path.exists("./data/CNStudio.zip"):
        print("下载CNStudio")
        wget.download("https://github.com/Razmoth/CNStudio/releases/download/v0.16.1.0/net472.zip",
                      "./data/CNStudio.zip")

    if not os.path.exists("./data/CNStudio"):
        print("解压中")
        with zipfile.ZipFile("./data/CNStudio.zip", "r") as f:
            for file in f.namelist():
                f.extract(file, "./data/CNStudio")
            f.close()

    if not os.path.exists("./data/export"):
        os.mkdir("./data/export")

    os.system("cd data/CNStudio&AssetStudioCLI ../sk ../export --key_index 1 --types TextAsset")
    for a, b, c in os.walk("./data/export/TextAsset"):
        for i in c:
            if "#" in i or ".asset" in i or ".bytes" in i:
                os.remove(a + "/" + i)
    os.system("cd ../..")
    os.rename("data/export/TextAsset", "sk_info_data")
    shutil.rmtree("data")
