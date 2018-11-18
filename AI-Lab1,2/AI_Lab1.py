# -*- coding: utf-8 -*-

"""
定义状态类State
"""
class State:
    def __init__(self, monkey=-1, box=0, banana=1, if_on_box=-1):
        # 默认的初始状态是猴子在A处，箱子在B处，香蕉在C处，猴子没有站在箱子上
        # -1：猴子在A处，0：猴子在B处，1：猴子在C处
        if monkey is "A":
            self.monkey = -1
        elif monkey is "B":
            self.monkey = 0
        elif monkey is "C":
            self.monkey = 1
        else:
            self.monkey = monkey
        # -1：箱子在A处，0：箱子在B处，1：箱子在C处
        if box is "A":
            self.box = -1
        elif box is "B":
            self.box = 0
        elif box is "C":
            self.box = 1
        else:
            self.box = box
        # -1：香蕉在A处，0：香蕉在B处，1：香蕉在C处
        if banana is "A":
            self.banana = -1
        elif banana is "B":
            self.banana = 0
        elif banana is "C":
            self.banana = 1
        else:
            self.banana = banana
        self.if_on_box = if_on_box  # -1：猴子没有站在箱子上，1：猴子站在箱子上


"""
表示猴子运动的函数
"""
def monkey_goto(b, i):
    a = b
    # 在状态列表里添加状态
    if a == -1:
        route_save.insert(i, "猴子到A处。")
        States.append(State(-1, States[i].box, States[i].banana, States[i].if_on_box))
    elif a == 0:
        route_save.insert(i, "猴子到B处。")
        States.append(State(0, States[i].box, States[i].banana, States[i].if_on_box))
    elif a == 1:
        route_save.insert(i, "猴子到C处。")
        States.append(State(1, States[i].box, States[i].banana, States[i].if_on_box))


"""
表示猴子推箱子的函数
"""
def move_box(a, i):
    b = a
    # 在状态列表里添加状态
    if b == -1:
        route_save.insert(i, "猴子推着箱子到A处。")
        States.append(State(-1, -1, States[i].banana, States[i].if_on_box))
    elif b == 0:
        route_save.insert(i, "猴子推着箱子到B处。")
        States.append(State(0, 0, States[i].banana, States[i].if_on_box))
    elif b == 1:
        route_save.insert(i, "猴子推着箱子到C处。")
        States.append(State(1, 1, States[i].banana, States[i].if_on_box))


"""
表示猴子爬上箱子的函数
"""
def climb_onto(i):
    # 添加路线说明
    route_save.insert(i, "猴子爬上箱子。")
    # 添加状态
    States.append(State(States[i].monkey, States[i].box, States[i].banana, 1))


"""
表示猴子从箱子上爬下来的函数
"""
def climbdown(i):
    # 添加路线说明
    route_save.insert(i, "猴子从箱子上爬下来。")
    # 添加状态
    States.append(State(States[i].monkey, States[i].box, States[i].banana, -1))


"""
表示猴子拿到香蕉的函数
"""
def reach(i):
    # 添加路线说明
    route_save.insert(i, "猴子拿到了香蕉。")


"""
打印问题结果的函数
"""
def show_solution(i):
    print ("问题结果：")
    for c in range(i + 1):
        print("第 %d 步 : %s " % (c + 1, route_save[c]))


"""
寻找路径的函数
"""

def next_step(i):
    if (States[i].if_on_box == 1 and States[i].monkey == States[i].banana and
            States[i].box == States[i].banana):
        reach(i)
        show_solution(i)
        exit(0)
    if States[i].box == States[i].banana:
        if States[i].monkey == States[i].banana:
            if States[i].if_on_box == -1:
                climb_onto(i)
                reach(i + 1)
                show_solution(i + 1)
                exit(0)
            else:
                reach(i + 1)
                show_solution(i + 1)
                exit(0)
        else:
            monkey_goto(States[i].box, i)
            next_step(i + 1)
    else:
        if States[i].monkey == States[i].box:
            if States[i].if_on_box == -1:
                move_box(States[i].banana, i)
                next_step(i + 1)
            else:
                climbdown(i)
                next_step(i + 1)
        else:
            monkey_goto(States[i].box, i)
            next_step(i + 1)


if __name__ == "__main__":
    print("===========================说明==========================")
    print("1表示猴子在箱子上  -1表示猴子不在箱子上")
    # 定义输入
    s = raw_input("请按如下顺序输入状态: 猴子的位置(A/B/C), 箱子的位置(A/B/C), 香蕉的位置(A/B/C), 猴子是否在箱子上(1/-1): \n")
    states = s.split(" ")
    if states[0] is not "A" and states[0] is not "B" and states[0] is not "C":
        print("输入不符合格式0！")
        exit(0)
    if states[1] is not "A" and states[1] is not "B" and states[1] is not "C":
        print("输入不符合格式1！")
        exit(0)
    if states[2] is not "A" and states[2] is not "B" and states[2] is not "C":
        print("输入不符合格式2！")
        exit(0)
    if int(states[3]) != 1 and int(states[3]) != -1:
        print("输入不符合格式3！")
        exit(0)
    if int(states[3]) == 1 and states[0] != states[1]:
        print("输入不符合逻辑，猴子跟箱子不在一个位置时却在箱子上！")
        exit(0)
    state = State(states[0], states[1], states[2], int(states[3]))
    States = []
    route_save = []
    States.append(state)
    next_step(0)
