import os
import shutil
address = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia"
os.chdir(address)
os.getcwd()
for i in range(1,41049):
    try:
        file_name = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/"+str(i)+'.txt'
        shutil.move(file_name, "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/data_txt")
    except:
        pass
    continue