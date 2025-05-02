## CÁCH TẢI
- Chạy file carPark.sql trong SQL server
- Mở project
- pip install pyodbc
- pip install sqlacodegen
- pip install sqlalchemy
- Mở terminal và paste "sqlacodegen "mssql+pyodbc://@(TÊN MÁY xem ở PC -> properties VD: DESKTOP-M0KCUVC)/CarPark?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes" --outfile BusinessObject/models.py"
- Project cần API, thư viện gì thì hãy cứ tải
- Chạy main.py
