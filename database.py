import pyodbc

try:
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'+
                                'Server=DESKTOP-PEG8VKH;'+
                                'Database=CarPark;'+
                                'Trusted_Connection=True')
    print('Connected to database')
except pyodbc.Error as ex:
    print('fail', ex)