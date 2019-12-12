import sys
from dominate import document
from dominate import tags


def main():
    with document(title='Welcome Page') as doc:
        tags.h1('welcome to the page')
        tags.button('我是按鈕', onclick="location.href='http://127.0.0.1:5000/jump'")
        print(doc.render())
    fn = 'templates/index1.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f = doc.render()
