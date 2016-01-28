import urllib, urllib2
from lxml import html
import re
from random import random
from time import time

def stringy(num):
	s = str(num)
	if len(s)==1:
		s = '0' + s
	return s

orden = 4
muestra = 2
dias = [stringy(num) for num in range(1, 29)]
meses = [stringy(num) for num in range(1, 13)]
signos = ['acuario', 'aries', 'cancer', 'capricornio', 'escorpio', 'geminis', 'leo', 'libra', 'piscis', 'sagitario', 'tauro', 'virgo']
mayu = 'QWERTYUIOPLKJHGFDSAZXCVBNM'
minu = 'qwertyuioplkjhgfdsazxcvbnm'

def get_html(some_url):
	"""except urllib2.HTTPError, e:print e.fp.read()return 'muymal'"""
	try:
		page = urllib2.urlopen(some_url)
		return page.read()
	except:
		#print 'Los rusos han tratado de detener al crawler. Muy pero que muy mal.'
		return ''
	return page.read()

def get_text(url):
	ans = get_html(url)
	ans = html.fromstring(ans)
	ans = ans.xpath('//p')
	if type(ans[2].text)!=type(None):
		return ans[2].text
	return ans[1].text

def mierda(d, m, s):
	return 'http://www.20minutos.es/horoscopo/solar/prediccion/' + s + '/' + d + '/' + m + '/2015/'

def get2015data():
	archivo = open("2015data.txt", "w")
	count = 0
	for dia,mes,signo in [(dia,mes,signo) for dia in dias for mes in meses for signo in signos]:
		archivo.write(get_text(mierda(dia, mes, signo)).encode('utf8') + '\n')
		count += 1
		if count%10==0:
			print count, "de", 12*12*28, "horoscopos"
	archivo.close()

def procesar(strin):
	ans = "start "*orden
	for ii in strin:
		if ii=='\n':
			ans += " end"*orden
		elif ii=='.' or ii==',' or ii==':':
			ans += " " + ii
		elif ii in mayu:
			ans += minu[mayu.index(ii)]
		else:
			ans += ii
	return ans.split(' ')

def cadena(lista, cu, order):
	return ' '.join(lista[cu-order:cu])#lista[cu - 2] + ' ' + lista[cu - 1]

def prefijos(lista):
	return list(set([ cadena(lista, ii, orden) for ii in range(orden, len(lista)) ]))

def juntar(cosas):
	return reduce(lambda x, y: x + y, cosas)

def random_pick(lista):
	r = int(random()*sum(lista))
	suma = 0
	for ii in range(len(lista)):
		suma += lista[ii]
		if suma>r:
			return ii

def convertir(mierda):
	#prov = ' '.join(mierda)
	#prov.replace(' .', '.')
	#prov.replace(' ,', ',')
	#prov.replace(' :', ':')
	#for ii in range(len(mayu)):
	#	prov.replace('. ' + minu[ii], '. ' + mayu[ii])
	prov = ''
	prev = '.'
	for el in mierda[orden:]:
		if el in ['.', ',', ':']:
			prov += el
		else:
			if prev == '.' and el[0] in minu:
				el = mayu[minu.index(el[0])] + el[1:]
			prov += ' ' + el
		prev = el
	return "=" + prov

#get2015data()
t0 = time()
horoscopos = open('2015data.txt', 'r')
coleccion = horoscopos.readlines()[:336*muestra]
coleccion = map(procesar, coleccion)
words = list(set(juntar(coleccion)))

prefs = list(set(juntar([prefijos(el) for el in coleccion])))
if False:
	print coleccion
	print words
	print len(words)
	print prefs, len(prefs)

matriz = []
for item in prefs:
	matriz.append([0 for bla in words])
count = len(coleccion)
for hor in coleccion:
	count -= 1
	if count%50==0:
		print count, ' samples remaining...'
	for ii in range(orden, len(hor)):
		matriz[prefs.index(cadena(hor, ii, orden))][words.index(hor[ii])] += 1

t0 = time() - t0
t1 = time()

def generate():
	new_hor = ['start']*orden
	while True:
		ind = random_pick(matriz[ prefs.index(cadena(new_hor, len(new_hor), orden)) ])
		#print words[ind]
		if words[ind]=='end':
			print convertir(new_hor)
			return
		new_hor.append(words[ind])

for jjj in range(60):
	generate()

t1 = (time() - t1)/60

print 'Formatting time: ', t0
print 'Generating time: ', t1
