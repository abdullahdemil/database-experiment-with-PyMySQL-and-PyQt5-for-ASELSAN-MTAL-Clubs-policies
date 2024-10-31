#buraya ham haldeki temize tam çekilmemiş ama çalışan kodlar stoklanacak. 

import pymysql
import pymysql.cursors

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

def database_tablo_olustur(connection): #? ölü fonksiyon
    cursor = connection.cursor() 
    cursor.execute('CREATE DATABASE IF NOT EXISTS okul')# Veritabanı oluştur
    print("Veritabanı oluşturuldu")
    connection.select_db('okul') #!Veritabanını seç
    cursor.execute('CREATE TABLE IF NOT EXISTS ogrenciler (id INT, name VARCHAR(20))')#* Tablo oluştur
    print("Tablo oluşturuldu")

def ogrenci_ara(connection, numara): #!kodun başında bir hosta ve database'e baglandiğim için extra olarak bağlanmama gerek yok.
    # Sorguyu oluştur ve çalıştır
    sql = "SELECT * FROM matlist WHERE Numara = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (numara))
    # Sonuçları al
    sonuc = cursor.fetchone()
    if sonuc:
        print("Öğrenci Bilgileri:", sonuc)
    else:
        print("Bu numaraya ait öğrenci bulunamadı.")
    connection.close()
    # Bağlantıyı kapat

def ogrenci_numara_guncelle(connection ,eski_numara, yeni_numara):
    cursor = connection.cursor()
    sql = "UPDATE matlist SET Numara = %s WHERE Numara = %s" # Sorguyu oluştur ve çalıştır
    cursor.execute(sql, (yeni_numara, eski_numara))

    # Değişiklikleri kaydet
    connection.commit()
    
    print(f"Öğrenci numarası {eski_numara} olan kayıt, {yeni_numara} olarak güncellendi.")

def sutun_ekle(connection): #*Sütun oluşturma kodu
    cursor = connection.cursor()
    
    # Sütunu eklemek için SQL sorgusunu oluştur
    sql = "ALTER TABLE matlist ADD COLUMN `!!!sütun adı!!!!` TEXT;" #sütun adı buraya yazılcak
    
    # Sorguyu çalıştır
    cursor.execute(sql)
    
    # Değişiklikleri kaydet
    connection.commit()
    
    print("Sütun 'sütun adı' başarıyla eklendi.") #burayı da değiştir de log boka benzemesin

def mentor_notu_guncelle(connection, numara, not_metni): #Oluşturulmuş sütundaki text verisini girme kodu.
    cursor = connection.cursor()
    
    # Mentor notunu güncellemek için SQL sorgusunu oluştur
    sql = "UPDATE matlist SET `mentor notu` = %s WHERE Numara = %s;"
    
    # Sorguyu çalıştır
    cursor.execute(sql, (not_metni, numara))
    
    # Değişiklikleri kaydet
    connection.commit()
    
    if cursor.rowcount > 0:
        print(f"Numarası {numara} olan öğrencinin mentor notu güncellendi.")
    else:
        print(f"Numarası {numara} olan öğrenci bulunamadı.")
    
    # Cursor'u kapat
    cursor.close()

def fetch_data(connection): #! Veritabanından veri çeksin diye connectionu başta veriyom
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

def isim_sorgula(self): #!Türkçe İngilizce harf ve space sorunu yaratmayan isim sorgusu. ÇOK İYİ
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
    else:
        print("İsim giriniz.")




#numsorgu = int(input("Öğrenci numarasını girin: "))
#ogrenci_ara(cursor, numsorgu)
# mentornot = input("Yazılacak notu giriniz: ")
#mentor_notu_guncelle(conn, numsorgu, mentornot)
#print("halloldu")
#conn.close()# Bağlantıyı kapat
