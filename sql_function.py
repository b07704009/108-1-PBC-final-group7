# 需先安裝 mysql-connector-python
"""
Created on 30 DEC 16:00

@author : 賴柏融
"""
import mysql.connector
import datetime as dt
from mysql.connector.errors import Error


# 建立資料庫連接資訊
config = {
        'host': 'johnny.heliohost.org',
        'user': 'pbcbike_root',
        'password': 'password0987',
        'database': 'pbcbike_pbc108'
}
dbforpbc = mysql.connector.connect(**config)
# 建立游標（資料庫運作用）
cursor = dbforpbc.cursor()

"""
！！！這段註解區間中的code是用於建立資料庫以及輸入停車地點資料所用到的程式碼，重複執行會導致error！！！

建立表格
cursor.execute("CREATE TABLE users(student_id VARCHAR(255) PRIMARY Key, name VARCHAR(255),phone VARCHAR(10),"
                "bike_license VARCHAR(255), bike_password VARCHAR(255), used VARCHAR(255), "
                "sharing VARCHAR(255), image LONGBLOB, password VARCHAR(255), current_location_id INTEGER)")
cursor.execute("CREATE TABLE records( record_id INTEGER AUTO_INCREMENT PRIMARY KEY, borrow_id VARCHAR(255), "
                "lent_id VARCHAR(255), borrow_time datetime, return_time datetime, borrow_place_id INTEGER,"
                "return_place_id INTEGER )")
cursor.execute("CREATE TABLE parking_space( place_id INTEGER AUTO_INCREMENT PRIMARY KEY, p_name VARCHAR(255),"
                "p_image LONGBLOB) ")
輸入停車地點資料
sql = "INSERT INTO parking_space(p_name) VALUE (%s)"
record = [("Management Building II (Parking Lot)",), ("Management Building II (Roosevelt Road)",),
          ("Management Building II (Inside the campus)",), ("Management Building I",), ("Common Subject Building",)]
cursor.executemany(sql, record)
dbforpbc.commit()
"""


def connect_to_db():
    """
    目標：建立資料庫連接，並且開啟游標
    """
    global dbforpbc
    dbforpbc = mysql.connector.connect(**config)
    global cursor
    cursor = dbforpbc.cursor()


def convertToBinaryData(filename):
    """
    目標：將所選路徑之照片轉為二元編碼，以利於後續以BLOB的形式存於資料庫中
    """
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def user_register(userinfo, image):
    """
    目標：使用者註冊，在資料庫中建立使用者資訊以及將使用者上傳之腳踏車圖片轉為二元（透過convertToBinaryData()）
    並儲存，需注意傳入之資料格式必須為tuple，順序為（姓名,學號,電話,腳踏車密碼,是否有車證,登入密碼）以及傳入腳踏
    車照片之路徑（取得過程寫在網頁裡）。

    所有有更改資料庫中資料內容的都要加上dbforpbc.commit()才會儲存於資料庫中。
    和資料庫連線的function最後都會加上cursor.close()、dbforpbc.close()關閉與資料庫的連線，避免過多使用者
    同時連線
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        sqlstuff = "INSERT INTO users (name, student_id, phone, bike_password,bike_license, \
                   password,image) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        empPicture = convertToBinaryData(image)
        insert_blob_tuple = (userinfo[0], userinfo[1], userinfo[2], userinfo[3], userinfo[4],
                             userinfo[5], empPicture)
        cursor.execute(sqlstuff, insert_blob_tuple)
        dbforpbc.commit()
        cursor.close()
        dbforpbc.close()


def login_success(login_id, password):
    """
    目的：當使用者傳入學號以及密碼時，判斷是否與資料庫內的學號密碼相同，相同的話回傳TRUE，反之回傳FALSE
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        cursor.execute("SELECT student_id, password FROM users WHERE student_id = '%s'"
                       % login_id)
        result = cursor.fetchall()
        if len(result) != 1:
            return False
        else:
            if result[0][1] == password:
                return True
            else:
                return False


def update_loction(s_id, cur_location):
    """
    目的：更新使用者目前車輛停放之位置，傳入值為使用者之學號以及目前停車地點，會將目前地點轉成相對應的地點編號
    進行儲存。
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        cursor.execute("SELECT place_id FROM parking_space where p_name = '%s' " % cur_location)
        update_id = cursor.fetchall()[0][0]
        cursor.execute("UPDATE users SET current_location_id = '%s' WHERE student_id = '%s'"
                       % (update_id, s_id))
        dbforpbc.commit()
        cursor.close()
        dbforpbc.close()


def check_location(s_id):
    """
    目的：傳入使用者學號後，回傳目前腳踏車所在地。
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        sql = "SELECT \
          parking_space.p_name\
          FROM users \
          INNER JOIN parking_space ON users.current_location_id = parking_space.place_id \
          WHERE users.student_id = '%s'"
        cursor.execute(sql % s_id)
        locat = cursor.fetchall()
        cursor.close()
        dbforpbc.close()
        if len(locat) != 1:
            return "Something wrong"
        else:
            return locat[0][0]


def use_situation(s_id, situ):
    """
    定義：腳踏車如果正在被使用，資料庫中對應的used=1，反之=0。
    目的：腳踏車借用與歸還時更改使用狀態。
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        cursor.execute("UPDATE users SET used = '%s' WHERE student_id = '%s'" % (situ, s_id))
        dbforpbc.commit()
        cursor.close()
        dbforpbc.close()


def being_used(s_id):
    """
    目的：確認腳踏車使用狀態，如果正在被使用回傳TRUE，反之則回傳FALSE。
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("SELECT used FROM users WHERE student_id = '%s'" % s_id)
        used = cursor.fetchall()
        cursor.close()
        dbforpbc.close()
        if len(used) != 1:
            return False
        else:
            if used[0][0] == "1":
                return True
            else:
                return False


def available_bike(locat):
    """
    目的：將該地點可以被借用的腳踏車顯示出來。
    目前狀況：目前還無法顯示出能借用腳踏車之照片，只能回傳該地點所有能借用之腳踏車的車主學號
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        # show all the bike in the selected location
        cursor.execute("SELECT \
          users.student_id\
          FROM users \
          INNER JOIN parking_space ON users.current_location_id = parking_space.place_id \
          WHERE parking_space.p_name = '%s' and users.used <> 1" % locat)
        result = cursor.fetchall()
        cursor.close()
        dbforpbc.close()
        available_list = []
        for i in range(len(result)):
            available_list.append(result[i][0])
        return available_list


def show_bike_info(s_id):
    """
    目的：使用者選定要借用的腳踏車後，回傳dictionary包含車主學號以及腳踏車密碼。
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        cursor.execute("SELECT student_id, bike_password FROM users WHERE student_id = '%s'"
                       % s_id)
        result = cursor.fetchall()
        cursor.close()
        dbforpbc.close()
        bike_info = dict()
        bike_info['student_id'] = result[0][0]
        bike_info['bike_password'] = result[0][1]
        return bike_info


def rent_bike(borrower, bike_owner):
    """
    目的：使用者確定借用該腳踏車後，在借用紀錄上增加該筆資料，並且登記腳踏車原先所在位置，以及借用時間，最後回傳借用
    紀錄之編號（輸入紀錄後會自動產生，由1開始。）
    同時將該腳踏車的使用狀態更改為1(使用中)
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("SELECT current_location_id FROM users WHERE student_id = '%s'"
                       % bike_owner)
        cur_place = cursor.fetchall()[0][0]
        sqlstuff = "INSERT INTO records (borrow_id, lent_id, borrow_time, borrow_place_id) \
                   VALUES (%s,%s,%s,%s)"
        b_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert = (borrower, bike_owner, b_time, cur_place)
        cursor.execute(sqlstuff, insert)
        dbforpbc.commit()
        cursor.execute("SELECT record_id FROM records WHERE borrow_id = '%s'\
                       AND borrow_time ='%s'" % (borrower, b_time))
        the_record = cursor.fetchall()[0][0]
        cursor.close()
        dbforpbc.close()
        use_situation(bike_owner, 1)
        return the_record


def return_bike(rec_id, r_place):
    """
    目的：歸還車輛，傳入借用編號以及停車地點後，在該筆借用紀錄中登記歸還時間以及停車地點。
    並且將車輛狀態改為0(非使用中)，以及將車輛的地點更新為歸還地點。
    """
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)
        print("Please try again later")
    else:
        cursor.execute("SELECT place_id FROM parking_space WHERE p_name = '%s'" % r_place)
        r_place_id = cursor.fetchall()[0][0]
        cursor.execute("SELECT lent_id FROM records WHERE record_id = '%s'" % rec_id)
        owner = cursor.fetchall()[0][0]
        r_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE records SET return_time = '%s', return_place_id ='%i' \
                       WHERE record_id = '%i'" % (r_time, r_place_id, rec_id))
        dbforpbc.commit()
        cursor.close()
        dbforpbc.close()
        use_situation(owner, 0)
        update_loction(owner, r_place)


"""
其他資料庫用到之程式碼：
顯示所有使用者：
cursor.execute("SELECT * FROM records")
for row in cursor.fetchall():
    print(row)
    
顯示所有可停車地點：
cursor.execute("SELECT * FROM parking_space")
for row in cursor.fetchall():
    print(row)
    
顯示所有借用紀錄：
cursor.execute("SELECT * FROM records")
for row in cursor.fetchall():
    print(row)
    
清空表格（刪除測試資料用）：
cursor.execute("TRUNCATE TABLE parking_space")
# (可將parking_space改成其他表格名稱）
dbforpbc.commit()
"""
