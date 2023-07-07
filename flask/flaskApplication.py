from flask import  Flask , render_template , redirect, url_for, request  #导入Flask类
from userApi import user_api
from studentApi import student_api

app=Flask(__name__)         #实例化并命名为app实例

app.register_blueprint(user_api)
app.register_blueprint(student_api)

@app.route('/')
def hello():
    msg="my name is caojianhua, China up!"
    return render_template("login.html", data=msg)
    #return 'Welcome BaoYang!!!'
    
@app.route('/blog/<int:postID>')
def showPostId(postID):
    return 'Blog Number %d' % postID

@app.route('/hello/<name>')
def callName(name):
    return 'Hello ---> %s' %name

@app.route('/admin')
def hello_admin():
    return 'Hello Admin'

@app.route('/user/<name>')
def user(name):
    if name =='admin':
        return redirect(url_for('hello_admin'))
    else:
        return "This is not admin"

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success',name = user))
    else:
        user = request.args.get('name')
        return redirect(url_for('success', name = user))

@app.route('/result')
def resultView():
    dictData = {'phy':59,'che':60,'maths':90}
    return render_template('result.html', result = dictData)
    
if __name__=="__main__":
    app.run(port=8899,host="127.0.0.1",debug=True) 