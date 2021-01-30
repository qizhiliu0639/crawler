# for i in range(1,41049):
#     try:
#         file_name = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/data_txt/"+str(i)+'.txt'
#         # print(file_name)
#         f = open(file_name,"r")
#         s= f.read()
#         print(str(i)+".txt")
#         print(len(s))
#     except:
#         pass
#     continue

# file_name = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/data_txt/23224.txt"
# f = open(file_name)
# s = f.read()
# print(s)

import re
import os


def replace_comma(data):
    """
    Remove the comma,\t from a string
    """
    return re.sub("[ \t]+"," ", data)


def remove_old(filename_old, filename_new):
    """
    remove old file only new file exists!
    """
    aa = os.path.exists
    if aa(filename_old) and aa(filename_new):
        os.remove(filename_old)
    else:
        print("Not allowed!")


def deal_file(filename_old, filename_new):
    try:
        with open(filename_old, encoding="utf8") as f1:
            with open(filename_new, "a", encoding="utf8") as f2:
                for i in f1:
                    if i.strip(): f2.write(replace_comma(i))
        remove_old(filename_old, filename_new)
        print("Successfully!")
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    for i in range(1,41049):
        filename1 = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/data_txt/"+str(i)+".txt"
        filename2 = "/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/new_data_txt/"+str(i)+".txt"
        deal_file(filename1, filename2)
