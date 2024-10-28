import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
from app import *
from qtm import *

# Veritabanı bağlantı fonksiyonu
def create_connection():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='yaaa2121',
        database='okul'
    )
    return connection

# Tüm kayıtları almak için fonksiyon
def fetch_all_data():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM matlist")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

# Numara'ya göre kayıt almak için fonksiyon
def fetch_by_numara(numara):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM matlist WHERE Numara = %s", (numara,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

# PyQt5 arayüz sınıfı
from qtm import Ui_MainWindow  # qtm.py dosyasından arayüz sınıfını içe aktar

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # qtm.py dosyasındaki setupUi fonksiyonunu çağır

        # Buton bağlantıları
        self.NumaraSorguButton.clicked.connect(self.sorgula_numara_ile)
        self.TumListeButton.clicked.connect(self.tum_listeyi_goster)

    # Tabloyu doldurmak için fonksiyon
    def populate_table(self, data):
        self.TabloCiktisi.setRowCount(0)  # Önce tabloyu temizle

        for row_num, row_data in enumerate(data):
            self.TabloCiktisi.insertRow(row_num)  # Yeni bir satır ekle
            for col_num, col_data in enumerate(row_data):
                self.TabloCiktisi.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

    # Numara ile sorgulama yapma fonksiyonu
    def sorgula_numara_ile(self):
        numara = self.NumaraSorguInput.text()
        if numara:
            data = fetch_by_numara(numara)
            self.populate_table(data)

    # Tüm listeyi gösterme fonksiyonu
    def tum_listeyi_goster(self):
        data = fetch_all_data()
        self.populate_table(data)

# Uygulama başlatma
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())