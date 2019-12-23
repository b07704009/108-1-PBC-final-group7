import mysql.connector
# if the connection failed, install 'mysql-connector-python'

# connect to mysql
dbforpbc = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password0987",
    auth_plugin='mysql_native_password',
    database='pbc108_1'
)
cursor = dbforpbc.cursor()


def user_register(userinfo):
    sqlstuff = "INSERT INTO users (name, user_id, phone, bike_license,bike_password) VALUES (%s,%s,%s,%s,%s)"
    # the data going to be inserted must be tuple
    # the order of the info must be name,id,phone,bike)_license,bike_password
    # checking the data user inputed is needed
    records = userinfo
    cursor.execute(sqlstuff, records)
    dbforpbc.commit()

