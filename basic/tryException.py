import sys

class MyError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def fileException():
    try:
        f = open("1.txt")
        s = f.readline()
        i = int(s.strip())
    except ValueError:
        print("catch valueError info....")
    except:
        print("catch exception...")
    finally:
        print("finnaly执行的代码")


if __name__ == '__main__':
    print("123")
    fileException()