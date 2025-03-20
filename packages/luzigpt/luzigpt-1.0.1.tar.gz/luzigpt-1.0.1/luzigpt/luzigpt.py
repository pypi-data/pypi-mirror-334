import requests

class LuziGPT:
    def __init__(self):
        self.api_url = "https://luzitool.ct.ws/data.php?soru="
    
    def cevap_ver(self, soru):
        """API'den cevabı alır, yoksa varsayılan mesaj verir."""
        try:
            response = requests.get(self.api_url + soru)
            if response.status_code == 200:
                data = response.json()  # API'den gelen JSON cevabı
                return data.get("cevap", "Üzgünüm, bu soruya yanıtım yok.")
            else:
                return "API isteği başarısız oldu."
        except requests.exceptions.RequestException:
            return "Bir hata oluştu, lütfen tekrar deneyin."
