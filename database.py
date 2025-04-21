import pyodbc

try:
    connection = pyodbc.connect('DRIVER={SQL Server};'+
                                'Server=DESKTOP-M0KCUVC;'+
                                'Database=CarPark;'+
                                'Trusted_Connection=True')
    print('Connected to database')
except pyodbc.Error as ex:
    print('fail', ex)