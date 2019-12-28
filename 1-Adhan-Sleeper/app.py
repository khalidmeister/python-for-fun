import os
import requests
import datetime
import time
from dateutil.parser import parse

class Waktu:
	def __init__(self, waktu):
		self.waktu = waktu
		self.jam = int(waktu.hour)
		self.menit = int(waktu.minute)
		self.detik = int(waktu.second)

	def get_time(self):
		if self.jam < 10:
			self.jam = "0" + str(self.jam)
		else:
			self.jam = str(self.jam)

		if self.menit < 10:
			self.menit = "0" + str(self.menit)
		else:
			self.menit = str(self.menit)

		return self.jam + self.menit

def new_time(i):
	jam = int(i[0:2])
	menit = int(i[2:])
	menit -= 5
	if menit < 0:
		jam -= 1
		menit = 60 + menit
	
	if jam < 10:
		jam = "0"+str(jam)
	else:
		jam = str(jam)
	
	if menit < 10:
		menit = "0"+str(menit)
	else:
		menit = str(menit)

	return jam + menit

# Requests data from API (Al-Adhan)
kota= input("Masukkan nama kota mu: ")
negara = input("Masukkan nama negara mu: ")
address = 'http://api.aladhan.com/v1/calendarByCity?city=' + kota + '&country='+ negara +'Indonesia&method=11'
json_data = requests.get(address).json()
adhan_time = json_data['data'][0]['timings']
names = adhan_time

# Buat Jadwal Adzan
# Delete beberapa waktu
del names['Sunrise']
del names['Sunset']
del names['Imsak']
del names['Midnight']

# Cetak Waktu Adzan
waktu = []
for k, v in names.items():
	print(k + "		" + v[0:5]) # Ngambil Waktu
	temp = parse(v[0:5])
	waktu.append(Waktu(temp))

# Mengambil waktu adzan berikutnya
now = Waktu(datetime.datetime.now().time()).get_time()
over = False
for i in waktu:
	i = i.get_time()
	flag = new_time(i)
	check = i >= now
	if check:
		flag = new_time(i)
		break
	else:
		over = True

# Real-Time
# Ketika 5 menit sebelum adzan masuk, laptop hibernate
while True:
	if now == flag and over == False:
		now = Waktu(datetime.datetime.now().time()).get_time()
		os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
		quit()

	time.sleep(1)