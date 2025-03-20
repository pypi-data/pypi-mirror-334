import json
import os

class LuziGPT:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "data.json")
        self.data = self._verileri_yukle()

    def _verileri_yukle(self):
        """JSON dosyasını yükler ve sözlük olarak döndürür."""
        if not os.path.exists(self.data_path):
            return {}  # Dosya yoksa boş bir sözlük döndür

        with open(self.data_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Bozuk dosya varsa boş döndür

    def cevap_ver(self, soru):
        """Sorunun cevabını döndürür, yoksa varsayılan mesaj verir."""
        return self.data.get(soru, "Üzgünüm, bu soruya yanıtım yok.")