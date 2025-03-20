import requests
import os

class OrvixGamesAPI:
    def __init__(self, api_key=None):
        """API anahtarını çevre değişkeninden veya parametreden alır."""
        self.api_key = api_key or os.getenv("ORVIX_API_KEY")
        self.base_url = "https://developers.itemshop.com.tr/api/v1/epintda.php"

        if not self.api_key:
            raise ValueError("API anahtarı bulunamadı! Lütfen ORVIX_API_KEY değişkenini ayarlayın.")
    
    def get_data(self):
        """API'den veri çeker ve API anahtarının geçerliliğini doğrular."""
        params = {"key": self.api_key}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "hata" in data:
                return {"hata": f"API doğrulama başarısız! {data['hata']}"}
            
            return data
        except requests.exceptions.RequestException as e:
            return {"hata": f"Bağlantı hatası: {e}"}

# Kullanım Örneği
if __name__ == "__main__":
    api = OrvixGamesAPI()  # API key'i çevre değişkeninden alacak
    print(api.get_data())
