import mysql.connector
from mysql.connector import Error


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(emp_id, name, photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(
            host="johnny.heliohost.org",
            user="pbcbike_root",
            password="password0987",
            database="pbcbike_pbc108")

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO users
                          (student_id, name, image) VALUES (%s,%s,%s)"""

        empPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (emp_id, name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))


insertBLOB(1, 1, '/Users/laipojung/Documents/GitHub/108-1-PBC-final-group7/static/photo/世代年齡曲線-男.png')


# def write_file(data, filename):
#     # Convert binary data to proper format and write it on Hard Disk
#     with open(filename, 'wb') as file:
#         file.write(data)
#
#
# def readBLOB(emp_id, photo):
#     print("Reading BLOB data from python_employee table")
#
#     try:
#         connection = mysql.connector.connect(
#             host="johnny.heliohost.org",
#             user="pbcbike_root",
#             password="password0987",
#             database="pbcbike_pbc108")
#
#         cursor = connection.cursor()
#         sql_fetch_blob_query = """SELECT * from users where student_id = %s"""
#
#         cursor.execute(sql_fetch_blob_query, (emp_id,))
#         record = cursor.fetchall()
#         for row in record:
#             print(row)
#             # print("Id = ", row[0], )
#             # print("Name = ", row[1])
#             # image = row[2]
#             # print("Storing employee image and bio-data on disk \n")
#             # write_file(image, photo)
#
#     except mysql.connector.Error as error:
#         print("Failed to read BLOB data from MySQL table {}".format(error))
#
#
# readBLOB(1, "/Users/laipojung/Documents/GitHub/108-1-PBC-final-group7/static/photo/test.png")
