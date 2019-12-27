import sys
import dominate
from dominate import document
from dominate import tags


def main2():
    doc = dominate.document(title='record page')

    with doc.head:
        tags.meta(name='charset', content="utf-8")

    with doc.body:
        tags.h1('Register Page')
        with tags.div():
            tags.attr(cls='container')

            with tags.form(method='POST', action="/jump"):
                with tags.legend('Please write down your name'):
                    tags.input(type='text', name='name', size=20)
                with tags.legend('Please write down your number'):
                    tags.input(type='text', name='number', size=20)

    fn = 'templates/index2.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
main2()