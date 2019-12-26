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


def user_register(userinfo):
    sqlstuff = "INSERT INTO users (name, student_id, phone, bike_password,bike_license,password) " \
               "VALUES (%s,%s,%s,%s,%s,%s)"
    # the data going to be inserted must be tuple
    # the order of the info must be name,id,phone,bike)_license,bike_password
    # checking the data user inputed is needed
    records = userinfo
    cursor.execute(sqlstuff, records)
    dbforpbc.commit()  # or the data inserted won't be saved
    cursor.close()
    dbforpbc.close()  # close the mysql connection or their will show max user connection
