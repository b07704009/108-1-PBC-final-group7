import mysql.connector
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
    # cur_location must be the id of the location
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        cursor.execute("UPDATE users SET current_location_id = '%s' WHERE student_id = '%s'" % (cur_location, s_id))
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
        cursor.execute("SELECT current_location_id FROM users WHERE student_id = '%s'" % s_id)
        # using join to return the name of the parking space instead of id would be better
        locat = cursor.fetchall()
        cursor.close()
        dbforpbc.close()
        return locat[0][0]


def being_used():
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        pass


def select_bike():
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # show all the bike in the selected location
        pass


def show_bike_info():
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # photo, bike_password, student id of the owner
        pass


def rent_bike():
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # remember to change the situation of the borrower's bike to 'being used'
        # add borrow record
        # rent time
        pass


def return_bike():
    try:
        connect_to_db()
    except mysql.connector.Error as e:
        print("Error:", e)  # errno, sqlstate, msg values
        print("Please try again later")
    else:
        # change the situation of the bike to free and update the location
        # return time
        pass
