import urllib.request
import json

class DirecTV: 
	#http://stackoverflow.com/questions/6924519/error-when-parsing-json-data
	#Get JSON data from DTV STB
	def contact(n):
		url = n
		req = urllib.request.urlopen(url)
		encoding = req.headers.get_content_charset()
		return json.loads(req.read().decode(encoding)) #res contains json data

	#Example of parsing
	def get_info():
		res = DirecTV.contact('http://192.168.1.100:8080/tv/getTuned') #10.43.112.22
		return(str(res['callsign']), str(res['major']), str(res['title']))
		#print('INFO:', res['title'])

	def chng_chnl(n):
		url = 'http://192.168.1.100:8080/tv/tune?major=' + n
		res = DirecTV.contact(url)
		return res['status']['msg']

	def keyInput(ip, n):
		url = 'http://' + ip + ":8080/remote/processKey?key=" + n
		res = DirecTV.contact(url)
	#end
#end