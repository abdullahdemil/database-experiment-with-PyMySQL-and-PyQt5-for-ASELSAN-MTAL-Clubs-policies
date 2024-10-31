import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
from stack import *
from qtm import *

# Veritabanı bağlantı fonksiyonu
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

# Tüm kayıtları almak için fonksiyon
def fetch_data(connection): # Veritabanından veri çeksin diye connectionu başta veriyom
    cursor = connection.cursor() # fonksiyona özel açılır kapanır cursor <33
    # Verileri çek
    cursor.execute("SELECT * FROM okul.matlist")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

#TabloCiktisi QTableWidgetItem ile dolduruluyor.
def tablo_ciktisi(tablo, data):
    if not data:
        tablo.clearContents()
        tablo.setRowCount(0)
        tablo.setColumnCount(0)
        return

    tablo.setRowCount(len(data))
    tablo.setColumnCount(len(data[0]))
    tablo.setHorizontalHeaderLabels(data[0].keys())
    print("uygulama buraya kadar geldi 2")
    
    for i, row in enumerate(data):
        for j, (key, value) in enumerate(row.items()):
            tablo.setItem(i, j, QTableWidgetItem(str(value)))
        print("Listelenen satırlar: " + str(i+1)) #konsolda log almak için koydum. Doğru satır numarasını versin diye de "i+1" yaptım.

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("uygulama buraya kadar geldi 5")
        # Başlangıçta tabloyu boş bırak
        tablo_ciktisi(self.TabloCiktisi, [])
        print("uygulama buraya kadar geldi 6")
        # Butona basıldığında tabloyu güncelle
        self.TumunuGoster_Tablo.clicked.connect(self.tumunu_goster)
        # Numara sorgulama butonuna tıklama olayını bağla
        self.NumaraSorguButton.clicked.connect(self.numara_sorgula)
        # İsim sorgulama butonuna tıklama olayını bağla
        self.pushButton.clicked.connect(self.isim_sorgula)

    def tumunu_goster(self):
        tablo_ciktisi(self.TabloCiktisi, fetch_data(set_connection()))

    def numara_sorgula(self):
        numara = self.NumaraSorguInput.text()
        if numara:
            connection = set_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM matlist WHERE Numara = %s"
            cursor.execute(sql, (numara,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            tablo_ciktisi(self.TabloCiktisi, data)
            # Input alanlarını temizle
            self.NumaraSorguInput.clear()
            self.bilgiDuzenleme_2.clear()
        else:
            print("Numara giriniz.")

    def isim_sorgula(self):
        isim = self.bilgiDuzenleme_2.text().strip()
        if isim:
            connection = set_connection()
            cursor = connection.cursor()
            # Türkçe karakter duyarlılığı için sorguyu düzenleyin
            sql = """
            SELECT * FROM matlist 
            WHERE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(isimSoyisim, 'ı', 'i'), 'ü', 'u'), 'ö', 'o'), 'ç', 'c'), 'ş', 's'), 'ğ', 'g')) 
            LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'ı', 'i'), 'ü', 'u'), 'ö', 'o'), 'ç', 'c'), 'ş', 's'), 'ğ', 'g'))
            """
            cursor.execute(sql, ('%' + isim + '%',))
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            tablo_ciktisi(self.TabloCiktisi, data)
            # Input alanlarını temizle
            self.NumaraSorguInput.clear()
            self.bilgiDuzenleme_2.clear()
        else:
            print("İsim giriniz.")

# Uygulama başlatma
app = QApplication(sys.argv)
print("uygulama buraya kadar geldi 2")
window = MainWindow()
print("uygulama buraya kadar geldi 4")
window.show()
sys.exit(app.exec_())