import mysql.connector
import datetime as dt
from mysql.connector.errors import Error
# if the connection failed, install 'mysql-connector-python'


config = {
        'host': 'johnny.heliohost.org',
        'user': 'pbcbike_root',
        'password': 'password0987',
        'database': 'pbcbike_pbc108'
}
dbforpbc = mysql.connector.connect(**config)
cursor = dbforpbc.cursor()


def connect_to_db():
    global dbforpbc
    dbforpbc = mysql.connector.connect(**config)
    global cursor
    cursor = dbforpbc.cursor()
    # if failed:
    #   print("Error code:", e.errno)  # error number
    #   print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
    #   print("Error message:", e.msg)  # error message
    #   print("Error:", e)  # errno, sqlstate, msg values


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def user_register(userinfo, image):
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        sqlstuff = "INSERT INTO users (name, student_id, phone, bike_password,bike_license,password,image) " \
                   "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        # the data going to be inserted must be tuple
        # the order of the info must be name,id,phone,bike)_license,bike_password
        # checking the data user inputed is needed
        empPicture = convertToBinaryData(image)
        insert_blob_tuple = (userinfo[0], userinfo[1], userinfo[2], userinfo[3], userinfo[4], userinfo[5], empPicture)
        cursor.execute(sqlstuff, insert_blob_tuple)
        dbforpbc.commit()  # or the data inserted won't be saved
        cursor.close()
        dbforpbc.close()  # close the mysql connection or will show max user connection


def login_success(login_id, password):
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("SELECT student_id, password FROM users WHERE student_id = '%s'" % login_id)
        result = cursor.fetchall()
        if len(result) != 1:
            return False
        else:
            if result[0][1] == password:
                return True
            else:
                return False


def update_loction(s_id, cur_location):
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("SELECT place_id FROM parking_space where p_name = '%s' " % cur_location)
        update_id = cursor.fetchall()[0][0]
        cursor.execute("UPDATE users SET current_location_id = '%s' WHERE student_id = '%s'" % (update_id, s_id))
        dbforpbc.commit()
        cursor.close()
        dbforpbc.close()


def check_location(s_id):
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
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
    # encoding: being used => used = 1; not being used => used = 0
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("UPDATE users SET used = '%s' WHERE student_id = '%s'" % (situ, s_id))
        dbforpbc.commit()
        cursor.close()
        dbforpbc.close()


def being_used(s_id):
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
    # showing photo of bikes is still a problem(undone)
    # only return list of the id of available bikes
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
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
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # photo(undone), bike_password, student id of the owner
        cursor.execute("SELECT student_id, bike_password FROM users WHERE student_id = '%s'" % s_id)
        result = cursor.fetchall()
        cursor.close()
        dbforpbc.close()
        bike_info = dict()
        bike_info['student_id'] = result[0][0]
        bike_info['bike_password'] = result[0][1]
        return bike_info


def rent_bike(borrower, bike_owner):
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # remember to change the situation of the borrower's bike to 'being used'
        # add borrow record
        # rent time
        cursor.execute("SELECT current_location_id FROM users WHERE student_id = '%s'" % bike_owner)
        cur_place = cursor.fetchall()[0][0]
        sqlstuff = "INSERT INTO records (borrow_id, lent_id, borrow_time, borrow_place_id) " \
                   "VALUES (%s,%s,%s,%s)"
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
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # change the situation of the bike to free and update the location
        # return time
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
