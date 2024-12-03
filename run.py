import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QVBoxLayout
from PyQt5 import uic
from stack import *
from qtm import *
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
# Veritabanı bağlantı fonksiyonu
def set_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        port=3306,
        password='yaaa2121',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        database='okul'
    )

# Tüm kayıtları almak için fonksiyon
def fetch_data(connection):
    cursor = connection.cursor()
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
        print("Listelenen satırlar: " + str(i+1))

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
        self.isimSorguButton.clicked.connect(self.isim_sorgula)
        # Kaydet butonuna tıklama olayını bağla
        self.duzenlemeKaydet.clicked.connect(self.duzenlemeleri_kaydet)
        # Tabloya tıklama olayını bağla
        self.TabloCiktisi.itemSelectionChanged.connect(self.satir_secildi)

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
            self.isimSorguInput.clear()
        else:
            print("Numara giriniz.")

    def isim_sorgula(self):
        isim = self.isimSorguInput.text().strip()
        if isim:
            connection = set_connection()
            cursor = connection.cursor()
            # Girilen ismi parçalara ayırın
            isim_parcalari = isim.split()
            # SQL sorgusunu oluşturun
            sql = """
            SELECT * FROM matlist 
            WHERE 
            """
            sql += " AND ".join([
                "LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(isimSoyisim, 'ı', 'i'), 'ü', 'u'), 'ö', 'o'), 'ç', 'c'), 'ş', 's'), 'ğ', 'g')) LIKE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(%s, 'ı', 'i'), 'ü', 'u'), 'ö', 'o'), 'ç', 'c'), 'ş', 's'), 'ğ', 'g'))"
                for _ in isim_parcalari
            ])
            cursor.execute(sql, ['%' + parca + '%' for parca in isim_parcalari])
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            tablo_ciktisi(self.TabloCiktisi, data)
            # Input alanlarını temizle
            self.NumaraSorguInput.clear()
            self.isimSorguInput.clear()
        else:
            print("İsim giriniz.")

    def satir_secildi(self):
        selected_items = self.TabloCiktisi.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.isimGuncelleInput.setText(self.TabloCiktisi.item(row, 0).text())
            self.numaraGuncelleInput.setText(self.TabloCiktisi.item(row, 1).text())
            self.mentorNotuGuncelleInput.setText(self.TabloCiktisi.item(row, 4).text())

    def duzenlemeleri_kaydet(self):
        selected_items = self.TabloCiktisi.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            numara = self.TabloCiktisi.item(row, 1).text()
            yeni_isim = self.isimGuncelleInput.text()
            yeni_numara = self.numaraGuncelleInput.text()
            yeni_mentor_notu = self.mentorNotuGuncelleInput.toPlainText()

            connection = set_connection()
            cursor = connection.cursor()
            sql = "UPDATE matlist SET isimSoyisim = %s, Numara = %s, mentornotu = %s WHERE Numara = %s"
            cursor.execute(sql, (yeni_isim, yeni_numara, yeni_mentor_notu, numara))
            connection.commit()
            cursor.close()
            connection.close()
            self.tumunu_goster()

    def sirala(self):
        index = self.comboBox.currentIndex()
        if index == 1:  # Sınıfa Göre Sırala
            self.sinifa_gore_sirala()
        elif index == 2:  # Numaraya Göre Sırala
            self.TabloCiktisi.sortItems(1, order=0)  # 1: Numara sütununun indeksi
        elif index == 3:  # İsime Göre Sırala
            self.TabloCiktisi.sortItems(0, order=0)  # 0: isimSoyisim sütununun indeksi
        else:  # Default
            self.tumunu_goster()

    def sinifa_gore_sirala(self):
        def sinif_siralama_degeri(sinif):
            sinif_numara_sirasi = {'12': 4, '11': 3, '10': 2, '9': 1}
            sinif_harf_sirasi = {'H': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4}
            try:
                sinif_numarasi, sinif_harfi = sinif.split("/")
                numara_degeri = sinif_numara_sirasi.get(sinif_numarasi, 0)
                harf_degeri = sinif_harf_sirasi.get(sinif_harfi, 5)
                return (numara_degeri, harf_degeri)
            except ValueError:
                return (0, 5)  # Hatalı değerler için varsayılan sıralama değeri

        rows = []
        for row in range(self.TabloCiktisi.rowCount()):
            sinif_item = self.TabloCiktisi.item(row, 2)
            if sinif_item is not None:
                sinif = sinif_item.text()
                rows.append((sinif_siralama_degeri(sinif), row))

        # Sınıf numaralarına göre sıralama
        rows.sort(key=lambda x: x[0], reverse=True)

        # Harfleri en sona atma
        harfler = ['H', 'A', 'B', 'C', 'D']
        rows = [row for row in rows if row[0][1] not in harfler] + [row for row in rows if row[0][1] in harfler]

        for new_row_index, (key, original_row_index) in enumerate(rows):
            for column in range(self.TabloCiktisi.columnCount()):
                item = self.TabloCiktisi.takeItem(original_row_index, column)
                self.TabloCiktisi.setItem(new_row_index, column, item)

# Uygulama başlatma
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())