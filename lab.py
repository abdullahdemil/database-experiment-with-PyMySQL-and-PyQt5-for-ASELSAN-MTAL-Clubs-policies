#*Kod iyileştirmelerini burada yapıyorum. ayrıca dış kaynaklardan çektiğim kodları da burada test ediyorum.

import pymysql

def set_connection():
    return pymysql.connect( # Bağlantıyı kur (bunu main.py'de tutmak en iyisi)
        host='localhost',
        user='root',
        port=3306,
        password='yaaa2121',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        database='okul'
    )

def ogrenci_ara(connection, numara):
    # Cursor oluştur
    cursor = connection.cursor()
    # Sorguyu oluştur ve çalıştır
    sql = "SELECT * FROM matlist WHERE Numara = %s"
    cursor.execute(sql, (numara,))
    # Sonuçları al
    sonuc = cursor.fetchone()
    if sonuc:
        print("Öğrenci Bilgileri:", sonuc)
    else:
        print("Bu numaraya ait öğrenci bulunamadı.")
    # Bağlantıyı kapat
    connection.close()

def fetch_data(connection): # Veritabanından veri çeksin diye connectionu başta veriyom
    cursor = connection.cursor() #fonksiyona özel açılır kapanır cursor <33
    # Verileri çek
    cursor.execute("SELECT * FROM okul.matlist")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
