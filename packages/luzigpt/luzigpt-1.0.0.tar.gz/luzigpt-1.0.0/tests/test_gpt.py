from luzigpt import LuziGPT

# LuziGPT sınıfını başlat
gpt = LuziGPT()

# Kullanıcıdan giriş al
soru = input("Lütfen sorunuzu yazın: ")

# Cevabı al ve yazdır
cevap = gpt.cevap_ver(soru)
print(cevap)
