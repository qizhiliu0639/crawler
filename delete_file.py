import os
for i in range(1,41049):
    try:
        file_name = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/data_txt/"+str(i)+'.txt'
        # print(file_name)
        f = open(file_name,"r")
        s= f.read()
        # print(str(i)+".txt")
        # print(len(s))
        if len(s) == 0:
            print("delete file:"+str(i)+".txt")
            os.remove(file_name)
    except:
        pass
    continue