import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# --- FONKSİYONLAR ---

def kaydet_ve_ac():
    ad = entry_ad.get()
    soyad = entry_soyad.get()
    no = entry_no.get()
    sifre = entry_sifre.get()

    if not all([ad, soyad, no, sifre]):
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
        return

    dosya_adi = "kullanici_listesi.xlsx"
    yeni_veri = pd.DataFrame({
        "Ad": [ad], 
        "Soyad": [soyad], 
        "Numara": [no], 
        "Şifre": [sifre]
    })

    try:
        if os.path.exists(dosya_adi):
            df_eski = pd.read_excel(dosya_adi, engine='openpyxl')
            df_son = pd.concat([df_eski, yeni_veri], ignore_index=True)
            df_son.to_excel(dosya_adi, index=False, engine='openpyxl')
        else:
            yeni_veri.to_excel(dosya_adi, index=False, engine='openpyxl')
        
        # Excel'i aç
        if os.name == 'nt': os.startfile(dosya_adi)
        else: os.system(f'open "{dosya_adi}"')

        # Girişleri temizle
        entry_ad.delete(0, tk.END); entry_soyad.delete(0, tk.END)
        entry_no.delete(0, tk.END); entry_sifre.delete(0, tk.END)

    except PermissionError:
        messagebox.showerror("Hata", "Excel açık! Lütfen Excel dosyasını kapatıp tekrar deneyin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir sorun oluştu: {e}")

def sifirdan_dosya_olustur():
    dosya_adi = "kullanici_listesi.xlsx"
    soru = messagebox.askyesno("Onay", "Mevcut dosya silinecek ve sıfırdan yeni bir liste açılacak. Emin misiniz?")
    
    if soru:
        try:
            # Boş sütunlarla yeni bir DataFrame oluştur
            df_bos = pd.DataFrame(columns=["Ad", "Soyad", "Numara", "Şifre"])
            df_bos.to_excel(dosya_adi, index=False, engine='openpyxl')
            
            # Excel'i aç
            if os.name == 'nt': os.startfile(dosya_adi)
            else: os.system(f'open "{dosya_adi}"')
            
            messagebox.showinfo("Başarılı", "Eski veriler temizlendi ve yeni dosya oluşturuldu!")
        except PermissionError:
            messagebox.showerror("Hata", "Excel açıkken dosyayı sıfırlayamam. Lütfen Excel'i kapatın.")

# --- ARAYÜZ TASARIMI ---
root = tk.Tk()
root.title("Gelişmiş Kayıt Paneli")
root.geometry("350x450")
root.configure(bg="#f0f0f0")

# Input Alanları
tk.Label(root, text="İsim:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(pady=2)
entry_ad = tk.Entry(root, width=30); entry_ad.pack(pady=5)

tk.Label(root, text="Soyisim:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(pady=2)
entry_soyad = tk.Entry(root, width=30); entry_soyad.pack(pady=5)

tk.Label(root, text="Numara:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(pady=2)
entry_no = tk.Entry(root, width=30); entry_no.pack(pady=5)

tk.Label(root, text="Şifre Oluştur:", bg="#f0f0f0", font=("Arial", 9, "bold")).pack(pady=2)
entry_sifre = tk.Entry(root, width=30, show="*"); entry_sifre.pack(pady=5) # Şifreyi gizli gösterir

# Butonlar
btn_kaydet = tk.Button(root, text="KAYDET VE LİSTEYE EKLE", command=kaydet_ve_ac, 
                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), height=2, width=25)
btn_kaydet.pack(pady=20)

btn_yeni = tk.Button(root, text="SIFIRDAN YENİ DOSYA AÇ", command=sifirdan_dosya_olustur, 
                     bg="#f44336", fg="white", font=("Arial", 10, "bold"), height=1, width=25)
btn_yeni.pack(pady=5)

root.mainloop()