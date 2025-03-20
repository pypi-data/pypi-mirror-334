import unittest
import io
import sys
from luziapi.core import show_banner  # Eğer gerçekten varsa

class TestCore(unittest.TestCase):
    def test_show_banner(self):
        # Çıktıyı yakalamak için stdout'u değiştiriyoruz
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Fonksiyonu çağır
        show_banner()

        # Orijinal stdout'u geri yükle
        sys.stdout = sys.__stdout__

        # Beklenen çıktıyı kontrol et
        expected_output = "# LUZİ APİ İLE GELİŞTİRİLDİ - TÜM HAKLARI SAKLIDIR\n"
        self.assertEqual(captured_output.getvalue(), expected_output, "Banner çıktısı hatalı!")

if __name__ == "__main__":
    unittest.main()
