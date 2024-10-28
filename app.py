#buraya ham haldeki temize tam çekilmemiş ama çalışan kodlar stoklanacak. 

import pymysql
import pymysql.cursors

conn = pymysql.connect( # Bağlantıyı kur (bunu main.py'de tutmak en iyisi)
    host='localhost',
    user='root',
    port=3306,
    password='yaaa2121',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    database = 'okul'
)
cursor = conn.cursor()# Cursor oluştur (klasik hareket)
def database_tablo_olustur():
    cursor.execute('CREATE DATABASE IF NOT EXISTS okul')# Veritabanı oluştur
    print("Veritabanı oluşturuldu")
    conn.select_db('okul') #!Veritabanını seç
    cursor.execute('CREATE TABLE IF NOT EXISTS ogrenciler (id INT, name VARCHAR(20))')#* Tablo oluştur
    print("Tablo oluşturuldu")

def ogrenci_ara(cursor, numara): #!kodun başında bir hosta ve database'e baglandiğim için extra olarak bağlanmama gerek yok.
    # Sorguyu oluştur ve çalıştır
    sql = "SELECT * FROM matlist WHERE Numara = %s"
    cursor.execute(sql, (numara))

    # Sonuçları al
    sonuc = cursor.fetchone()
    if sonuc:
        print("Öğrenci Bilgileri:", sonuc)
    else:
        print("Bu numaraya ait öğrenci bulunamadı.")
    
    # Bağlantıyı kapat

def ogrenci_numara_guncelle(conn ,eski_numara, yeni_numara):
    
    sql = "UPDATE matlist SET Numara = %s WHERE Numara = %s" # Sorguyu oluştur ve çalıştır
    cursor.execute(sql, (yeni_numara, eski_numara))

    # Değişiklikleri kaydet
    conn.commit()
    
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

def fetch_data(connection): # Veritabanından veri çeksin diye connectionu başta veriyom
    cursor = connection.cursor() #fonksiyona özel açılır kapanır cursor <33
    # Verileri çek
    cursor.execute("SELECT * FROM okul.matlist")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data




#numsorgu = int(input("Öğrenci numarasını girin: "))
#ogrenci_ara(cursor, numsorgu)
# mentornot = input("Yazılacak notu giriniz: ")
#mentor_notu_guncelle(conn, numsorgu, mentornot)
#print("halloldu")
#conn.close()# Bağlantıyı kapat