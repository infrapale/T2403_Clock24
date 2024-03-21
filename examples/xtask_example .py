import time


class Xtask: 
    def __init__(self, label, interval, cb ):       
        self.label =  label
        self.interval = interval
        self.cb = cb
        self.next = time.monotonic() + self.interval
    
    def run(self):
        self.next = time.monotonic() + self.interval
        self.cb()

    def is_ready(self):
        return (self.next < time.monotonic())



example code
cntr = 0

def task_a():
    global cntr
    # print("TaskA")
    cntr = cntr + 1

def task_b():
    global cntr
    # print("TaskB")
    print(cntr)

task_a = Xtask("taskA", 0.0001, task_a)
task_b = Xtask("taskB", 10.0, task_b)

tasks = [task_a,task_b]

while 1:
    for task in tasks:
        if task.is_ready():
            task.run()


        
        