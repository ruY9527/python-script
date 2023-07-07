
import webview

# pip install pywebview -i https://mirror.baidu.com/pypi/simple/


def createWebview():
    window = webview.create_window(
        title='百度一下,全是广告',
        url='http://www.baidu.com',
        width=850,
        height=600,
        resizable=False,    # 固定窗口大小
        text_select=False,   # 禁止选择文字内容
        confirm_close=True   # 关闭时提示
    )
    webview.start()

if __name__ == '__main__':
    createWebview()