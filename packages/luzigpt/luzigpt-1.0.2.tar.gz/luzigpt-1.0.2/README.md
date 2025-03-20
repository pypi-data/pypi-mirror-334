# LuziGPT

**LuziGPT**, önceden tanımlı soru-cevap verileri ile çalışan basit bir yapay zeka modülüdür. Harici API'ler kullanmadan, kendi içinde bulunan verilerden cevaplar üretir. Telegram botları, sohbet uygulamaları ve eğitsel projelerde kullanılabilir.

## 🚀 Özellikler
- 📌 **Önceden Tanımlı Cevaplar**: JSON dosyasında saklanan soru-cevap çiftleriyle çalışır.
- ⚡ **Hızlı ve Hafif**: Harici API'lere bağımlı değildir, tamamen yerel çalışır.
- 🛠 **Kolay Entegrasyon**: Telegram botları, Discord botları veya diğer projelerde kolayca kullanılabilir.

## 🔧 Kurulum
LuziGPT'yi yüklemek için aşağıdaki komutu çalıştırın:
```sh
pip install luzigpt
```

## 📌 Kullanım
```python
from luzigpt import LuziGPT

gpt = LuziGPT()
soru = "Merhaba"
cevap = gpt.cevap_ver(soru)
print(cevap)
```
### Örnek Çıktı:
```
Merhaba! Nasıl yardımcı olabilirim?
```



## 📜 Lisans
Bu proje **MIT Lisansı** ile lisanslanmıştır. Dilediğiniz gibi kullanabilir ve geliştirebilirsiniz.

---
🎯 **Geliştirici:** [LuziTool](https://t.me/luzitool)  
📬 **İletişim:** t.me/luzitool

