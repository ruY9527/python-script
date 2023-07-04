import pandas as pd

mydataset = {
  'sites': ["Google", "Runoob", "Wiki"],
  'number': [1, 2, 3]
}

def pandasVersion():
    print(pd.__version__)

def oneRowSerial():
    a = [1,2,3,4]
    aVar = pd.Series(a)
    print(aVar)

def showDataByFrame():
    frameVar = pd.DataFrame(mydataset)
    print(frameVar)
    
def showDictFrame():
    sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
    sitesVar = pd.Series(sites,index = [1,2], name="BaoYangTest")
    print(sitesVar)

def showDictListFrame():
    data = {'Site':['Google', 'Runoob', 'Wiki'], 'Age':[10, 12, 13]}
    df = pd.DataFrame(data)
    print(df)

def showListDictFrame():
    data = [{'a': 1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]
    df = pd.DataFrame(data)
    print(df)

if __name__ == '__main__':
    showListDictFrame()