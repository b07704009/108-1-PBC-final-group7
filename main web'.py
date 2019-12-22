from flask import Flask, redirect, url_for, render_template, flash, request
import dominate
from dominate import document
from dominate import tags


def main1():
<<<<<<< HEAD
    with document(title='Welcome Page') as doc:
=======
    doc = dominate.document(title='Welcome Page')

    with doc.head:
        tags.meta(name='charset', content="utf-8")

    with doc.body:
>>>>>>> master
        tags.h1('welcome to the page')
        tags.button('我是按鈕', onclick="location.href='http://127.0.0.1:5000/jump'")

    fn = 'templates/index1.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)
main1()


def main2():
    doc = dominate.document(title='record page')

    with doc.head:
        tags.meta(name='charset', content="utf-8")

    with doc.body:
        tags.h1('Register Page')
<<<<<<< HEAD
=======

>>>>>>> master
        with tags.div():
            tags.attr(cls='container')

            with tags.form(method='POST', action="/jump"):
<<<<<<< HEAD
                with tags.legend('Please write down your name'):
                    tags.input(type='text', name='name', size=20)
                with tags.legend('Please write down your number'):
                    tags.input(type='text', name='number', size=20)
=======
                with tags.legend('請輸入姓名'):
                    tags.input(type='text', name='name', size=20)
                with tags.legend('請輸入學號'):
                    tags.input(type='text', name='number', size=20)
                with tags.legend('請輸入電話'):
                    tags.input(type='text', name='number', size=20)
                with tags.legend('是否有台大車證(有:Y沒有:N)'):
                    tags.input(type='text', name='number', size=20)
                with tags.legend('腳踏車的密碼(選填)'):
                    tags.input(type='text', name='number', size=20)
                tags.input(type='submit', value='click me')
>>>>>>> master

    fn = 'templates/index2.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
main2()


app = Flask(__name__)


<<<<<<< HEAD
@app.route('/name')
def home():
    return render_template("index.html")


@app.route('/jump', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        return 'Hello! ' + request.values['username'] + ' your download link is XXXXXX.'

    return render_template('htmltry3.html')
=======
@app.route('/')
def home():
    return render_template("index1.html")

a = []
@app.route('/jump', methods=['GET', 'POST'])
def success():

    if request.method == 'POST':
        a.append(request.values['name'])
        return 'Hello! ' + request.values['name'] + ' your download link is XXXXXX.'

    return render_template('index2.html')



>>>>>>> master


if __name__ == "__main__":
    app.run()