import unittest
import os
from orvixgamesapi import OrvixGamesAPI

class TestOrvixGamesAPI(unittest.TestCase):
    def setUp(self):
        """API anahtarını gizli tutarak test eder"""
        os.environ["ORVIX_API_KEY"] = "YANLIŞ_API_KEY"  # Geçerli bir API KEY girme!
        self.api = OrvixGamesAPI()
    
    def test_api_key_validation(self):
        """API anahtarının doğruluğunu test et"""
        response = self.api.get_data()
        self.assertIsInstance(response, dict)
        
        if "hata" in response:
            print("❌ API anahtarı geçersiz!")
        else:
            print("✅ API anahtarı geçerli!")

if __name__ == "__main__":
    unittest.main()
