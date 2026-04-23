import pandas as pd


def readCsvStr():
    df = pd.read_csv('nba.csv')
    print(df.head(2))


def saveToCsv():
    name = ["Google", "Runoob", "Taobao", "Wiki"]
    st = ["www.google.com", "www.runoob.com", "www.taobao.com", "www.wikipedia.org"]
    ag = [90, 40, 80, 98]

    dictCsv = {'name': name , 'str': st, 'age': ag}
    df = pd.DataFrame(dictCsv)
    df.to_csv('1.csv')

def readCsvFor():
    nameList = []
    df = pd.read_csv('nba.csv')
    for index,value in df.iterrows():
        print(value['Name'])
        nameList.append(value['Name'])
    print(len(nameList))    

if __name__ == '__main__':
    readCsvFor()