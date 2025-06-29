# Real-Time Flight Tracker – Python App Using OpenSky API
# -------------------------------------------------------
# Bu script OpenSky Network API'sinden gerçek zamanlı uçuş verilerini çeker
# ve terminalde tablo şeklinde gösterir. Hafif, sade bir takip aracıdır.
# 10 saniyede bir güncellenir, ilk 10 uçuş listelenir.
# Geliştirilmeye açık: ülke filtreleme, harita gösterimi, GUI gibi şeyler eklenebilir.

import requests
import time  # döngü arası bekletmek için kullanılıyor
from tabulate import tabulate  # tablo şeklinde çıktı vermek için

# OpenSky'dan uçuş verisi çekeceğimiz URL
URL = "https://opensky-network.org/api/states/all"

# API'den veriyi çeken fonksiyon
def fetch_flight_data():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()  # istek başarısızsa hata fırlat
        data = response.json()
        return data.get('states', [])  # sadece 'states' listesini al
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Gelen veriyi tabloya uygun hale getiriyoruz
def parse_flights(states):
    flights = []
    for s in states:
        callsign = s[1].strip() if s[1] else "N/A"  # boşsa 'N/A' yaz
        country = s[2]  # kayıtlı olduğu ülke
        altitude = s[13] or 0  # irtifa, boşsa 0
        velocity = s[9] or 0   # hız, boşsa 0
        lat = s[6]
        lon = s[5]
        # Konum bilgisi varsa listeye ekle
        if lat and lon:
            flights.append([
                callsign, country,
                round(altitude, 1),
                round(velocity, 1),
                round(lat, 3),
                round(lon, 3)
            ])
    return flights

# Ana fonksiyon: döngüyle sürekli veri çekiyor ve yazdırıyor
def main():
    while True:
        print("\nFetching real-time flight data...\n")
        states = fetch_flight_data()
        if states:
            flights = parse_flights(states)
            flights = flights[:10]  # sadece ilk 10 taneyi göster
            headers = ["Callsign", "Country", "Altitude (m)", "Speed (m/s)", "Latitude", "Longitude"]
            print(tabulate(flights, headers=headers))
        else:
            print("No flight data available.")
        
        print("\nNext update in 10 seconds...\n")
        time.sleep(10)  # 10 saniye bekle, sonra tekrar çek

# Script doğrudan çalıştırıldığında main() çağrılır
if __name__ == "__main__":
    main()

    
    # ------------------------------
# Geliştirme Notları / Fikirler
# ------------------------------
# Bu kod şu anda sadece uçakların anlık bilgilerini çekiyor ve liste halinde gösteriyor.
# Gösterilen uçaklar, dünya genelindeki rastgele uçaklardır ve sadece kayıtlı olduğu ülkeye göre filtrelenebilir.
#
# İleride şunlar eklenebilir:
#
# 1. Belirli ülkeye kayıtlı uçakları filtreleme:
#    - Zaten eklenmişti, ama dilersen sadece "Turkey", "Germany" gibi country alanına göre filtre uygulanabilir.
#
# 2. Belirli bir ülkenin hava sahasında uçan uçaklar:
#    - Uçakların enlem ve boylam (latitude/longitude) bilgileri kullanılarak,
#      örneğin Türkiye hava sahası sınırları içindeki uçaklar gösterilebilir.
#    - Bunun için Türkiye'nin koordinat kutusu tanımlanabilir (örneğin: lat 36-42, lon 26-45).
#
# 3. Belirli bir ülkeden kalkıp başka bir ülkeye giden uçaklar:
#    - OpenSky bu bilgiyi doğrudan vermez, ama geçmiş uçuş verisi veya çağrı kodu analiz edilerek tahmin yapılabilir.
#
# 4. Harita üzerinde gösterim:
#    - Folium veya başka harita kütüphaneleriyle uçakların konumları haritada işaretlenebilir.
#
# 5. Grafik arayüz:
#    - Kod şu an sadece terminalde çalışıyor ama Tkinter, PyQt veya web (Flask, Dash) arayüzüyle zenginleştirilebilir.
#
# Özetle, bu kod temel bir uçuş izleme sistemi gibi çalışıyor ama üzerine birçok ek özellik kolayca inşa edilebilir :)

