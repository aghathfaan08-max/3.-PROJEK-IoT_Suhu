import time
import machine
import dht
import network
import urequests
from machine import WDT

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="esp32", password="12345678")
sensor = dht.DHT22(machine.Pin(4))
relay = machine.Pin(13, machine.Pin.OUT)
waktu_start = time.time()
sudah_lapor_lonjakan = False
wdt = WDT(timeout=10000)

while True:
    sensor.measure()
    if sensor.temperature() > 30:
        relay.off()
        if sudah_lapor_lonjakan == False:
            hasil = {"suhu": sensor.temperature(), "kelembapan": sensor.humidity()}
            try:
                r = urequests.post("http://192.168.4.2:8000/lapor", json=hasil)
                r.close()
                sudah_lapor_lonjakan = True
            except:
                pass
            
    else:
        relay.on()
        sudah_lapor_lonjakan = False
    waktu_cek = time.time()
    if waktu_cek - waktu_start >= 120:
        hasil = {"suhu": sensor.temperature(), "kelembapan": sensor.humidity()}
        try:
            p = urequests.post("http://192.168.4.2:8000/lapor", json=hasil)
            p.close()
            waktu_start = time.time()
        except:
            pass
    wdt.feed()
    time.sleep(5)
