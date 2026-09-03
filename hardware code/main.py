import time
import machine
import dht
import network
import urequests

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="esp32", password="12345678")
sensor = dht.DHT22(machine.Pin(4))
relay = machine.Pin(13, machine.Pin.OUT)
waktu_start = time.time()
sudah_lapor_lonjakan = False

while True:
    sensor.measure()
    if sensor.temperature() > 30:
        relay.off()
        if sudah_lapor_lonjakan == False:
            hasil = {"suhu": sensor.temperature(), "kelembapan": sensor.humidity()}
            r = urequests.post("http://192.168.4.2:8000/lapor", json=hasil)
            r.close()
            sudah_lapor_lonjakan = True
            
    else:
        relay.on()
        sudah_lapor_lonjakan = False
    waktu_cek = time.time()
    if waktu_cek - waktu_start >= 120:
        hasil = {"suhu": sensor.temperature(), "kelembapan": sensor.humidity()}
        p = urequests.post("http://192.168.4.2:8000/lapor", json=hasil)
        p.close()
        waktu_start = time.time()
    time.sleep(5)