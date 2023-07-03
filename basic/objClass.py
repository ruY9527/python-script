#!/usr/bin/python3

# python 的 class 对象 info

class People:
    id = 0
    def __init__(self, id):
        self.id = id
    def spark(self):
        print("people in spark: %d" , (self.id))


class Student(People):
    name = 'BaoYang'
    age = 25
    __hobby = 'bigData'
    def __init__(self,name,hobby):
        self.name = name
        self.__hobby = hobby

    def f(self):
        return "this is baoyang"

    def getHobby(self):
        return self.__hobby

class Parent:
    def myMethod(self):
        print("Parent中进行调用")

class Child(Parent):
    def myMethod(self):
        print("Child中进行调用")

class Site:
    def __init__(self,name,url):
        self.name = name
        self.__url = url

    def who(self):
        print("name... , " , self.name)
        print("url..." , self.__url)

    def __foo(self):
        print("私有方法")
    
    def foo(self):
        self.__foo()


if __name__ == '__main__':
    s = Student("ZhangSan","coding")
    print("Student 类的属性 name 为：", s.name)
    print("Student 类的属性 hobby 为: " + s.getHobby())
    print(" ----------------------------------------")
    c = Child()
    c.myMethod()
    super(Child,c).myMethod()