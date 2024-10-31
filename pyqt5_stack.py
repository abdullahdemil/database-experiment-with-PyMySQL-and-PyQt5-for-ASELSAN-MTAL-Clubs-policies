#PYQT5 kodlarını burada ayrı olarak stoklamaya karar verdim.

class MainWindow(QMainWindow, Ui_MainWindow): #butona tıklandığında alınan verileri tabloya yazdırır.
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("uygulama buraya kadar geldi 5")
        # Başlangıçta tabloyu boş bırak
        tablo_ciktisi(self.TabloCiktisi, [])
        print("uygulama buraya kadar geldi 6")
        # Butona basıldığında tabloyu güncelle
        self.TumunuGoster_Tablo.clicked.connect(self.tumunu_goster)

    def tumunu_goster(self): #bu fonksiyonu ana dosyada tanıtmak lazım.
        tablo_ciktisi(self.TabloCiktisi, fetch_data(set_connection()))