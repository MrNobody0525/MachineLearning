#哲学家就餐（解决死锁问题）
import threading,time

rlock1 = threading.RLock()
rlock2 = threading.RLock()
rlock3 = threading.RLock()
rlock4 = threading.RLock()
rlock5 = threading.RLock()

class Chopsticks():
    def __init__(self,rlock):
        self.rlock = rlock
        self.key = 0

    def pick(self):
        self.key = 1
        self.rlock.acquire()

    def put(self):
        self.key = 0
        self.rlock.release()

    def isable(self):
        if self.key == 0:
            return 1
        else:
            return 0


class Zhexuejia():
    def __init__(self,left,right):
        self.left = Chopsticks(left)
        self.right = Chopsticks(right)
z1 = Zhexuejia(rlock5,rlock1)
z2 = Zhexuejia(rlock1,rlock2)
z3 = Zhexuejia(rlock2,rlock3)
z4 = Zhexuejia(rlock3,rlock4)
z5 = Zhexuejia(rlock4,rlock5)



def run(z,name):
    while True:
        if z.left.isable():
            print("左筷子可取")
            z.left.pick()
            print(name,"获取左筷子")
            if z.right.isable():
                print("右筷子可取")
                z.right.pick()
                print(name,"获取右筷子")
                print("哲学家开始就餐",name)
                time.sleep(0.01)
                z.right.put()
                print(name,"放下右筷子")
                z.left.put()
                print(name,"放下左筷子")
            else:
                print("右筷子不可取")
                z.left.put()
                if name == "a1":
                    time.sleep(0.1)
                if name == 'a3':
                    time.sleep(0.2)
                if name == '5':
                    time.sleep(0.3)
                print(name,"不吃了，放下筷子ksndvjkndjknvkjndfjkvnjkdfnjkvnjfdnvjkndkjvnksdnvjkndfvjn")


t1 = threading.Thread(target=run,args=(z1,"z1"))
t2 = threading.Thread(target=run,args=(z2,"z2"))
t3 = threading.Thread(target=run,args=(z3,"z3"))
t4 = threading.Thread(target=run,args=(z4,"z4"))
t5 = threading.Thread(target=run,args=(z5,"z5"))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
