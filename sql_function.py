import mysql.connector
# if the connection failed, install 'mysql-connector-python'

# connect to mysql
dbforpbc = mysql.connector.connect(
    host="johnny.heliohost.org",
    user="pbcbike_root",
    password="password0987",
    database="pbcbike_pbc108"
)
cursor = dbforpbc.cursor()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def user_register(userinfo, image):
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
    dbforpbc.close()  # close the mysql connection or their will show max user connection


def login_success(login_id, password):
    cursor.execute("SELECT student_id, password FROM users WHERE student_id = '%s'" % login_id)
    result = cursor.fetchall()
    if len(result) != 1:
        return False
    else:
        if result[0][1] == password:
            return True
        else:
            return False
