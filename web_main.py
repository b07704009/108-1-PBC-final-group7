# 需先安裝dominate/ os/ flask/ mysql
"""
Created on 25 DEC 23:14

@author: 楊梅郁,劉睿哲,毛子晴
"""

import os

import dominate
import mysql
from dominate import tags
from flask import Flask, render_template, request

import sql_function

name_list = [0]
student_id_dict = dict()
telephone_number_dict = dict()
school_bike_license_dict = dict()
bike_lock_number_dict = dict()
password_dict = dict()

name_list_temp = [0]
student_id_temp = [0]
telephone_number_temp = [0]
school_bike_license_temp = ['z']
bike_lock_number_temp = [0]
password_temp = [0]
to_convert = 0

"""
name_list
    variable name: name_list
    variable type: list
    variable obligation: to store the confirmed name

student_id_dict
    variable name: student_id_dict
    variable type: dictionary
    variable obligation: to store the confirmed student_id with the index being confirmed name

telephone_number_dict
    variable name: telephone_number_dict
    variable type: dictionary
    variable obligation: to store the confirmed telephone_number with the index being confirmed name
    
school_bike_license_dict
    variable name: school_bike_license_dict
    variable type: dictionary
    variable obligation: to store the confirmed school_bike_license with the index being confirmed name

bike_lock_number_dict
    variable name: bike_lock_number_dict
    variable type: dictionary
    variable obligation: to store the confirmed bike_lock_number with the index being confirmed name

password_dict
    variable name: password_dict
    variable type: dictionary
    variable obligation: to store the confirmed password with the index being confirmed name

name_list_temp
    variable name: name_list_temp
    variable type: list
    variable obligation: to store the name keyed by the user before confirmation

student_id_temp
    variable name: student_id_temp
    variable type: list
    variable obligation: to store the student_id keyed by the user before confirmation

telephone_number_temp
    variable name: telephone_number_temp
    variable type: list
    variable obligation: to store the telephone_number keyed by the user before confirmation

school_bike_license_temp
    variable name: school_bike_license_temp
    variable type: list
    variable obligation: to store the school_bike_license keyed by the user before confirmation

bike_lock_number_temp
    variable name: bike_lock_number_temp
    variable type: list
    variable obligation: to store the bike_lock_number_temp keyed by the user before confirmation

password_temp
    variable name: password_temp
    variable type: list
    variable obligation: to store the password_temp keyed by the user before confirmation

"""


def dominate_homepage():
    """
    第一頁：歡迎頁面，對應到  @app.route('/')  及其函數  homepage_run()
    目標：利用dominate寫出homepage的html並在templates資料夾中存成index1.html

    分為三個區塊
    doc = dominate.document()
    with doc.head   (包含css的style;meta確保中文可以運行在utf-8下)
    with doc.body   (包含welcome words and a button)

    最後寫入文件中(在templates資料夾中存成index1.html)
    """
    doc = dominate.document(title='homepage')

    with doc.head:
        tags.meta(name='charset', content="utf-8")
        tags.style("""\
                body {
                    background-color: #F9F8F1;
                    color: #2C232A;
                    font-family: sans-serif;
                    font-size: 30;
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
            with tags.div(cls='headline', style='font-size: 30;'):
                tags.h1('Find Your Bike')
            tags.input(type='button', value='click me', onclick="location.href='http://127.0.0.1:5000/jump'",
                       style="width:120px; background-color:pink; font-size: 14;")

    fn = 'templates/index1.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)


dominate_homepage()


def dominate_register_page():
    """
    第二頁：註冊頁面，對應到  @app.route('/jump')  及其函數   registerpage_run
    目標：利用dominate寫出registerpage的html並在templates資料夾中存成index2.html

    分為三個區塊
    doc = dominate.document()
    with doc.head   (包含css的style;meta確保中文可以運行在utf-8下)
    with doc.body   (包含 a form with 7 legends: name/ password/ student_id/
                    telephone_number/ school_bike_license/ bike_lock_number/ picture uploading and a button submit)

    最後寫入文件中(在templates資料夾中存成index2.html)
    """
    doc = dominate.document(title="registerpage")

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
                width: 500px;
                height: 500px;
                position: absolute;
                top: 52%;
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
        with tags.div(clas='headline', style='font-size: 20;'):
            tags.h1('Register Page')
        with tags.section():
            with tags.form(method='POST', action="/jump", enctype="multipart/form-data"):
                with tags.legend():
                    tags.label('請輸入姓名(中文)')
                    tags.input(type='text', name='name', size=20)
                with tags.legend():
                    tags.label('請輸入密碼')
                    tags.input(type='text', name='password', size=20)
                with tags.legend():
                    tags.label('請輸入學號(1個大寫英文字母+8個數字)')
                    tags.input(type='text', name='student_id', size=20)
                with tags.legend():
                    tags.label('請輸入電話(請輸入10位數字)')
                    tags.input(type='text', name='telephone_number', size=20)
                with tags.legend():
                    tags.label('是否有台大車證(Y/N)')
                    tags.input(type='text', name='school_bike_license', size=20)
                with tags.legend():
                    tags.label('腳踏車的密碼(選填、請輸入數字)')
                    tags.input(type='text', name='bike_lock_number', size=20)
                with tags.legend():
                    tags.label('上傳圖片')
                    tags.input(type='file', name='photo', size=20)
                with tags.div(cls='button', style="margin:0 auto; width:250px;"):
                    tags.input(type='submit', value='click me', style="width:120px; background-color:pink;")

    fn = 'templates/index2.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())


dominate_register_page()


def dominate_enter_page():
    """
    第三頁：確認資訊頁面，對應到  @app.route('/jump')  及其函數   registerpage_run [if request.method == 'POST']
    目標：利用dominate寫出 enter_page 的 html並在 templates 資料夾中存成 index3.html

    分為三個區塊
    doc = dominate.document()
    with doc.head   (包含css的style;meta確保中文可以運行在utf-8下)
    with doc.body   (包含 6 information: name/ password/ student_id/
                    telephone_number/ school_bike_license/ bike_lock_number and a button confirm)

    最後寫入文件中(在templates資料夾中存成index3.html)
    """
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
        """)

    with doc.body:
        tags.h1('welcome' + str(name_list_temp[0]))
        tags.h2('please confirm your information')
        with tags.section(cls='information check'):
            with tags.div(cls='name', style="text-align: center"):
                tags.label('your name is' + str(name_list_temp[0]))
            with tags.div(cls='password', style="text-align: center"):
                tags.label('your password is' + str(password_temp[0]))
            with tags.div(cls='student_id', style="text-align: center"):
                tags.label('your student id is' + str(student_id_temp[0]))
            with tags.div(cls='telephone', style="text-align: center"):
                tags.label('your telephone number is' + str(telephone_number_temp[0]))
            with tags.div(cls='license', style="text-align: center"):
                tags.label('the status of your bike_lice' + str(school_bike_license_temp[0]))
            with tags.div(cls='lock_number', style="text-align: center"):
                tags.label('your bike lock number is' + str(bike_lock_number_temp[0]))
            with tags.div(cls='button', style="margin:0 auto; width:250px;"):
                tags.input(type='button', value='confirm', style="width:120px; background-color:pink;",
                           onclick="location.href='http://127.0.0.1:5000/entered'")

    fn = 'templates/index3.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)


dominate_enter_page()


def dominate_final_page():
    """
    第四頁：感謝頁，
    目標：利用dominate寫出 enter_page 的 html並在 templates 資料夾中存成 index4.html

    分為三個區塊
    doc = dominate.document()
    with doc.head   (包含css的style;meta確保中文可以運行在utf-8下)
    with doc.body   (h1)

    最後寫入文件中(在templates資料夾中存成index4.html)
    """

    doc = dominate.document(title="photo_page")
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
        """)

    with doc.body:
        tags.h1('Thank You!')

    fn = 'templates/index4.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)


dominate_final_page()


def dominate_error_page():
    """
        第五頁：資料庫連接錯誤頁面，對應到  @app.route('/entered')  及其函數  eneter_success()
        目標：利用dominate寫出homepage的html並在templates資料夾中存成index5.html

        分為三個區塊
        doc = dominate.document()
        with doc.head   (包含css的style;meta確保中文可以運行在utf-8下)
        with doc.body   (包含 words and a button)

        最後寫入文件中(在templates資料夾中存成index5.html)
        """
    doc = dominate.document(title='error_page')

    with doc.head:
        tags.meta(name='charset', content="utf-8")
        tags.style("""\
                    body {
                        background-color: #F9F8F1;
                        color: #2C232A;
                        font-family: sans-serif;
                        font-size: 30;
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
            with tags.div(cls='headline', style='font-size: 30;'):
                tags.h1('Register failed! Please try again')
            tags.input(type='button', value='return back', onclick="location.href='http://127.0.0.1:5000/'",
                       style="width:120px; background-color:pink; font-size: 14;")

    fn = 'templates/index5.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)


dominate_error_page()


def dominate_error_page():
    """
        第五頁：資料庫連接錯誤頁面，對應到  @app.route('/entered')  及其函數  eneter_success()
        目標：利用dominate寫出homepage的html並在templates資料夾中存成index5.html

        分為三個區塊
        doc = dominate.document()
        with doc.head   (包含css的style;meta確保中文可以運行在utf-8下)
        with doc.body   (包含 words and a button)

        最後寫入文件中(在templates資料夾中存成index5.html)
        """
    doc = dominate.document(title='error_page')

    with doc.head:
        tags.meta(name='charset', content="utf-8")
        tags.style("""\
                    body {
                        background-color: #F9F8F1;
                        color: #2C232A;
                        font-family: sans-serif;
                        font-size: 30;
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
            with tags.div(cls='headline', style='font-size: 30;'):
                tags.h1("wrong information! please try again")
            tags.input(type='button', value='return back', onclick="location.href='http://127.0.0.1:5000/'",
                       style="width:120px; background-color:pink; font-size: 14;")

    fn = 'templates/index6.html'
    with open(file=fn, mode='w', encoding='utf-8') as f:
        f.write(doc.render())
    print(f)

app = Flask(__name__)


@app.route('/')
def homepage_run():
    """
    目標：顯示index1.html，對應到 dominate_homepage的函數
    """
    return render_template("index1.html")


basedir = os.path.abspath(os.path.dirname(__file__))


def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def correct_telephone(strs):
    if strs.isdigit() and len(strs) == 10:
            return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False


def correct_student_id(strs):
    str_num = strs - strs[0]
    if len(strs) == 9 and str_num.isalpha() and is_number(strs[0]):
            return True
    else:
        return False

def correct_school_bike_license(strs):
    if strs == 'Y' or 'Z':
        return True
    else:
        return False



@app.route('/jump', methods=['GET', 'POST'])
def register_page_run():
    """
    目標：先顯示index2.html，對應到 dominate_register_page的函數，儲存使用者在index2.html上輸入的所有資訊及相片
         若request.method為post(代表按下了register頁面的submit按鈕)顯示index3.html，對應到 dominate_enter_page的函數，
         並顯示所有在index2.html暫存的資訊
    """
    if request.method == 'POST':
        index = request.values['name']
        name_list_temp[0] = index
        password_temp[0] = request.values['password']
        student_id_temp[0] = request.values['student_id']
        telephone_number_temp[0] = request.values['telephone_number']
        school_bike_license_temp[0] = request.values['bike_lock_number']
        bike_lock_number_temp[0] = request.values['bike_lock_number']
        password_temp[0] = request.values['password']

        if is_all_chinese(index) and correct_telephone(password_temp[0]) and correct_student_id(student_id_temp[0]) and correct_school_bike_license(school_bike_license_temp[0]):
            # 照片的
            img = request.files.get('photo')
            path = basedir + "/static/photo/"
            file_path = path + img.filename
            img.save(file_path)
            global to_convert
            to_convert = file_path
            print('上傳頭像成功，上傳的使用者是：' + index)

            dominate_enter_page()
            return render_template('index3.html')
        else:
            return render_template('index6.html')

    return render_template('index2.html')



@app.route('/entered')
def enter_success():
    """
    目標：當在index3.html(enter_page)上按下confirm的按鈕，會跳轉到最後一個頁面，對應到dominate_final_page，
    並將該資料傳入資料庫，及寫入本地的dictionary中
    !!! 目前尚未上傳圖片的檔案，需先轉為二進制，後續可以考慮在confirm旁加上back的按鈕
    """
    name_list.append(name_list_temp[0])
    index = name_list_temp[0]
    password_dict[index] = password_temp[0]
    student_id_dict[index] = student_id_temp[0]
    telephone_number_dict[index] = telephone_number_temp[0]
    school_bike_license_dict[index] = bike_lock_number_temp[0]
    try:
        fn = (name_list_temp[0], student_id_temp[0], telephone_number_temp[0], bike_lock_number_temp[0],
              school_bike_license_temp[0], password_temp[0])
        sql_function.user_register(fn, to_convert)
        return render_template('index4.html')

    except mysql.connector.Error:
        return render_template('index5.html')


if __name__ == "__main__":
    app.run()
