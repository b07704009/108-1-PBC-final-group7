import sys
from dominate import document
from dominate import tags
import dominate


def main():
    doc = dominate.document(title='record page')
    with doc.body:
        tags.h1('welcome to the page')
        tags.button('我是按鈕', onclick="location.href='http://127.0.0.1:5000/jump'")
    print(doc.render())
main()