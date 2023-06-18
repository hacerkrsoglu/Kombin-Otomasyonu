# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 02:34:23 2023

@author: Hacer
"""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtGui import QPixmap 
import sqlite3
import random

class KullaniciBilgileriDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Kullanıcı Bilgileri")
        self.setFixedSize(400, 200)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.ad_label = QtWidgets.QLabel("Ad:")
        self.ad_edit = QtWidgets.QLineEdit()

        self.soyad_label = QtWidgets.QLabel("Soyad:")
        self.soyad_edit = QtWidgets.QLineEdit()

        self.kilo_label = QtWidgets.QLabel("Kilo:")
        self.kilo_edit = QtWidgets.QLineEdit()

        self.boy_label = QtWidgets.QLabel("Boy:")
        self.boy_edit = QtWidgets.QLineEdit()

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.addWidget(self.ad_label, 0, 0)
        self.grid_layout.addWidget(self.ad_edit, 0, 1)
        self.grid_layout.addWidget(self.soyad_label, 1, 0)
        self.grid_layout.addWidget(self.soyad_edit, 1, 1)
        self.grid_layout.addWidget(self.kilo_label, 2, 0)
        self.grid_layout.addWidget(self.kilo_edit, 2, 1)
        self.grid_layout.addWidget(self.boy_label, 3, 0)
        self.grid_layout.addWidget(self.boy_edit, 3, 1)
        self.grid_layout.addWidget(self.button_box, 4, 0, 1, 2)

    def get_kullanici_bilgileri(self):
        ad = self.ad_edit.text()
        soyad = self.soyad_edit.text()
        kilo = self.kilo_edit.text()
        boy = self.boy_edit.text()

        return ad, soyad, kilo, boy


class VucutTipiSecimiDialog(QtWidgets.QDialog):
    def __init__(self, vucut_tipi_resimler, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Vücut Tipi Seçimi")
        self.setFixedSize(600, 400)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.vucut_tipi_resimler = vucut_tipi_resimler

        self.grid_layout = QtWidgets.QGridLayout(self)

        self.selected_tip = None

        for row, (vucut_tipi, resim) in enumerate(self.vucut_tipi_resimler.items()):
            image_label = QtWidgets.QLabel()
            pixmap = QPixmap(resim).scaledToWidth(200)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(QtCore.Qt.AlignHCenter)

            button = QtWidgets.QPushButton()
            button.setFixedSize(200, 30)
            button.setText(vucut_tipi)
            button.clicked.connect(lambda checked, tip=vucut_tipi: self.vucut_tipi_secildi(tip))

            self.grid_layout.addWidget(image_label, row, 0)
            self.grid_layout.addWidget(button, row, 1)

    def vucut_tipi_secildi(self, vucut_tipi):
        self.selected_tip = vucut_tipi
        self.accept()

    def get_selected_tip(self):
        return self.selected_tip


class KategoriSecimiDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Kategori Seçimi")
        self.setFixedSize(300, 200)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())

        self.kategori_label = QtWidgets.QLabel("Kategori Seçiniz:")
        self.kategori_combo = QtWidgets.QComboBox()
        self.kategori_combo.addItem("Spor")
        self.kategori_combo.addItem("Klasik")
        self.kategori_combo.addItem("Şık")

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.addWidget(self.kategori_label, 0, 0)
        self.grid_layout.addWidget(self.kategori_combo, 0, 1)
        self.grid_layout.addWidget(self.button_box, 1, 0, 1, 2)

    def get_selected_kategori(self):
        return self.kategori_combo.currentText()


class AnaPencere(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kombin Asistanı")

        vucut_tipi_resimler = {
            "dikdortgen": "vucut-tipi-dikdortgen-olan.jpg",
            "elma": "indir.jpg",
            "armut": "vucut-tipi-ters-armut-olan.jpg",
            "kum saati": "vucut-tipi-ters-kum-saati-olan.jpg"
        }

        self.kullanici_bilgileri_dialog = KullaniciBilgileriDialog()
        if self.kullanici_bilgileri_dialog.exec_() == QtWidgets.QDialog.Accepted:
            ad, soyad, kilo, boy = self.kullanici_bilgileri_dialog.get_kullanici_bilgileri()
            self.vucut_tipi_secimi_dialog = VucutTipiSecimiDialog(vucut_tipi_resimler)
            if self.vucut_tipi_secimi_dialog.exec_() == QtWidgets.QDialog.Accepted:
                vucut_tipi = self.vucut_tipi_secimi_dialog.get_selected_tip()
                self.kategori_secimi_dialog = KategoriSecimiDialog()
                if self.kategori_secimi_dialog.exec_() == QtWidgets.QDialog.Accepted:
                    kategori = self.kategori_secimi_dialog.get_selected_kategori()
                    self.kombinleri_getir(ad, soyad, kilo, boy, vucut_tipi, kategori)
                    self.show()

    def kombinleri_getir(self, ad, soyad, kilo, boy, vucut_tipi, kategori):
        conn = sqlite3.connect("kullanici_veritabani.db")
        cursor = conn.cursor()
    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanici (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT,
                soyad TEXT,
                kilo REAL,
                boy REAL,
                vucut_tipi TEXT
            )
        """)
    
        cursor.execute("""
            INSERT INTO kullanici (ad, soyad, kilo, boy, vucut_tipi)
            VALUES (?, ?, ?, ?, ?)
        """, (ad, soyad, kilo, boy, vucut_tipi))
        conn.commit()
    
        kullanici_id = cursor.lastrowid
    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kiyafetler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_id INTEGER,
                kategori TEXT,
                foto_url TEXT,
                detaylar TEXT,
                vucut_tipi TEXT,
                FOREIGN KEY (kullanici_id) REFERENCES kullanici (id)
            )
        """)
        conn.commit()
    
        cursor.execute("""
            SELECT * FROM kiyafetler
            WHERE kategori = ? AND vucut_tipi = ?
        """, (kategori, vucut_tipi))
    
        kiyafetler = cursor.fetchall()
        if len(kiyafetler) > 0:
            kombin = random.choice(kiyafetler)
            foto_url = kombin[3]
            detaylar = kombin[4]
    
            # Kategoriye göre resim klasörünü belirle
            if kategori == "spor":
                resim_klasor = "spor"
            elif kategori == "klasik":
                resim_klasor = "klasik"
            elif kategori == "sık":
                resim_klasor = "sık"
            else:
                print("Geçersiz kategori seçimi.")
    
            resimler = []
            for i in range(1, 3):
                resim_adresi = f"C:/Users/Hacer/Desktop/PROJE/{resim_klasor}/{resim_klasor}{i}.jpg"
                resimler.append(resim_adresi)
    
            # Kombini göstermek için QLabel kullanarak bir resim görüntüleyin
            kombin_label = QtWidgets.QLabel()
            pixmap = QPixmap(foto_url).scaledToWidth(200)
            kombin_label.setPixmap(pixmap)
    
            self.setCentralWidget(kombin_label)
        else:
            print("Bu kategori ve vücut tipine uygun kombin bulunamadı.")
    
        conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = AnaPencere()
    sys.exit(app.exec_())