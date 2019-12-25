import dominate
import sql_function
from dominate import tags
from flask import Flask, render_template, request

name_list = [0]
student_id_dict = dict()
telephone_number_dict = dict()
school_bike_license_dict = dict()
bike_lock_number_dict = dict()
passport_dict = dict()

name_list_temp = [0]
student_id_temp = [0]
telephone_number_temp = [0]
school_bike_license_temp = [0]
bike_lock_number_temp = [0]
passport_temp = [0]


def dominate_homepage():
    doc = dominate.document(title='homepage')

    with doc.head:
        tags.meta(name='charset', content="utf-8")
        tags.style("""\
                body {
                    background-color: #F9F8F1;
                    color: #2C232A;
                    font-family: sans-serif;
                    font-size: 14;
                    text-align: center;
                }
                 section{
                      width: 300px;
                      height: 300px;
                      position: absolute;
                      top: 50%;
                      left: 50%;
                      overflow: auto;
                      text-align: center;
                      margin-left:-150px;
                      margin-top:-150px;
                }

               
             """)

    with doc.body:
        with tags.section():
            tags.h1('welcome to the page')
            tags.input(type='button', value='click me', onclick="location.href='http://127.0.0.1:5000/jump'",
                       style="width:120px; background-color:pink;")

    fn = 'templates/index1.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)


dominate_homepage()


def dominate_registerpage():
    doc = dominate.document(title="registerpage")

    with doc.head:
        tags.meta(name='charset', content="utf-8")
        tags.style("""\
                        body {
                            background-color: #F9F8F1;
                            color: #2C232A;
                            font-family: sans-serif;
                            font-size: 14;
                        }
                        section{
                            width: 500px;
                            height: 500px;
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            overflow: auto;
                            text-align: center;
                            margin-left:-250px;
                            margin-top:-250px;
                            text-align: center;
                        }
                        label{
                            cursor: pointer;
                            display: inline-block;
                            padding: 3px 6px;
                            text-align: center;
                            width: 200px;
                            vertical-align: top;
                        }

                        input{
                            font-size: inherit;
                        }      

                     """)

    with doc.body:
        tags.h1('Register Page')
        with tags.section():
            with tags.form(method='POST', action="/jump"):
                with tags.legend():
                    tags.label('請輸入姓名')
                    tags.input(type='text', name='name', size=20)
                with tags.legend():
                    tags.label('請輸入密碼')
                    tags.input(type='text', name='passport', size=20)
                with tags.legend():
                    tags.label('請輸入學號')
                    tags.input(type='text', name='student_id', size=20)
                with tags.legend():
                    tags.label('請輸入電話')
                    tags.input(type='text', name='telephone_number', size=20)
                with tags.legend():
                    tags.label('是否有台大車證(Y/N)')
                    tags.input(type='text', name='school_bike_license', size=20)
                with tags.legend():
                    tags.label('腳踏車的密碼(選填)')
                    tags.input(type='text', name='bike_lock_number', size=20)
                with tags.div(cls='button', style="margin:0 auto; width:250px;"):
                    tags.input(type='submit', value='click me', style="width:120px; background-color:pink;")

    fn = 'templates/index2.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())


dominate_registerpage()


def dominate_enter_page():
    doc = dominate.document(title="entered")

    with doc.head:
        tags.meta(name='charset', content="utf-8")
        tags.style("""\
                    body {
                        background-color: #F9F8F1;
                        color: #2C232A;
                        font-family: sans-serif;
                        font-size: 14;
                        text-align: center;
                    }
                    section{
                            width: 250px;
                            height: 250px;
                            position: absolute;
                            overflow: auto;
                            text-align: center;
                    }

                 """)

    with doc.body:
        tags.h1('welcome' + str(name_list_temp[0]))
        tags.h2('please confirm your information')
        with tags.section():
            with tags.section(cls='information check'):
                with tags.legend():
                    tags.label('your name is' + str(name_list_temp[0]))
                with tags.legend():
                    tags.label('your passport is' + str(passport_temp[0]))
                with tags.legend():
                    tags.label('your student id is' + str(student_id_temp[0]))
                with tags.legend():
                    tags.label('your telephone number is' + str(telephone_number_temp[0]))
                with tags.legend():
                    tags.label('the status of your bike_lice' + str(school_bike_license_temp[0]))
                with tags.legend():
                    tags.label('your bike lock number is' + str(bike_lock_number_temp[0]))
                with tags.div(cls='button', style="margin:0 auto; width:250px;"):
                    tags.input(type='button', value='confirm', onclick="location.href='http://127.0.0.1:5000/entered'",
                               style="width:120px; background-color:pink;")
    fn = 'templates/index3.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)


def dominate_final_page_photo_upload():
    doc = dominate.document(title="photo_page")


app = Flask(__name__)


@app.route('/')
def homepage_run():
    return render_template("index1.html")


@app.route('/jump', methods=['GET', 'POST'])
def registerpage_run():
    if request.method == 'POST':
        index = request.values['name']
        name_list_temp[0] = index
        passport_temp[0] = request.values['passport']
        student_id_temp[0] = request.values['student_id']
        telephone_number_temp[0] = request.values['telephone_number']
        school_bike_license_temp[0] = request.values['bike_lock_number']
        bike_lock_number_temp[0] = request.values['bike_lock_number']

        dominate_enter_page()
        return render_template('index3.html')
    return render_template('index2.html')


@app.route('/entered')
# /entered 介面要在上傳照片
def enter_success():
    name_list.append(name_list_temp[0])
    index = name_list_temp[0]
    student_id_dict[index] = student_id_temp[0]
    telephone_number_dict[index] = telephone_number_temp[0]
    school_bike_license_dict[index] = bike_lock_number_temp[0]
    fn = tuple(name_list_temp[0], student_id_temp[0], telephone_number_temp[0], bike_lock_number_temp[0], school_bike_license_temp[0])
    sql_function.user_register((1, 2))

    return 'thank you'


if __name__ == "__main__":
    app.run()
