# -- coding:utf-8 --
import re
def get_data(file_address):
    f = open(file_address,"r")
    s = f.read()
    return s

def remove_switchline(data):
    return re.sub("[\n]+","", data)


def get_school(data):
    show_school = r"申请学校:(.*?)学位"
    slotList = re.findall(show_school,data)
    return slotList

def get_year(data):
    show_year = r"入学年份:(.*?)入学学期:"
    slotList = re.findall(show_year,data)
    show_semester = r"入学学期:(.*?)通知时间:"
    slotList_1 = re.findall(show_semester,data)
    show = []
    for i in range(len(slotList_1)):
        show.append(slotList[i]+slotList_1[i])
    return show
def get_result(data):
    show_result = r"申请结果:(.*?)入学年份:"
    slotList = re.findall(show_result,data)
    return slotList

if __name__ == "__main__":
    data = get_data("/home/liuzhiqi/Over/39800.txt")
    # print(data)
    # show = r"The(.*?)Sheffield"
    data = remove_switchline(data)
    # print(data)
    school = get_school(data)
    # print(school)
    year =get_year(data)
    # print(year)
    result = get_result(data)
    # print(result)
    num = len(school)
    graph_data = []
    for i in range(num):
        app=[]
        app = [school[i]]+[year[i]]+[result[i]]
        graph_data.append(app)
    print(graph_data)


    # for i in range(4,20):
    #     try:
    #         data = get_data("/home/liuzhiqi/PycharmProjects/tensorflow-lr/jituotianxia/"+str(i)+".txt")
    #         print(type(data))
    #     except:
    #         pass
    #     continue