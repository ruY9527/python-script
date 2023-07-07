from textblob import TextBlob

# pip install textblob
# 中文检查使用 SnowNLP 这个依赖
def checkTextBlob():
    a = TextBlob("I dream about workin with goof company")
    a = a.correct()
    print(a)


if __name__ == '__main__':
    checkTextBlob()