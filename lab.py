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

def ogrenci_ara(connection, sorgu): #* optimize edildi.

    cursor = connection.cursor()     # Cursor oluştur

    sql = "SELECT * FROM matlist WHERE Numara = %s"# Sorguyu oluştur 
    cursor.execute(sql, (sorgu,)) #ve çalıştır

    sonuc = cursor.fetchone() # Sonuçları al. Fetchone yalnızda 1 satır sonuç çekiyormuş. 1'den fazla da sonuç çıksa yalnızca ilkini alıyor.
    if sonuc:
        print("Öğrenci Bilgileri:", sonuc)
    else:
        print("Bu sorguya ait öğrenci bulunamadı.")
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

def tablo_ciktisi_yansit(tablo, data): #!Bu kod muazzam. Veritabanından çekilen verileri tabloya yansıtıyor. Ve satır ve sütun sayısını da otomatize bir şekilde ayarlıyor. İnanılmaz bir şey bu fatihcim.
#* self.TabloCiktisi, fetch_data(set_connection()) parametrelerini alarak kullanılıyor.
    if not data:
        return
    
    tablo.setRowCount(len(data)) #row sayısını ayarla
    tablo.setColumnCount(len(data[0])) #column sayısını ayarla
    tablo.setHorizontalHeaderLabels(data[0].keys()) #column başlıklarını ayarla
    print("uygulama buraya kadar geldi 2")#debugum

    for i, row in enumerate(data):
        for j, (key, value) in enumerate(row.items()): #row.items() ile row'un key ve value'larını alıyoruz ama row valuemuz yok chill.
            tablo.setItem(i, j, QTableWidgetItem(str(value))) #tabloya value'ları yazıyoruz.
        print("uygulama buraya kadar geldi 3")
