# The application is made for quick testing puposes
# Tests are made with microcontroller module STM32

from flask import Flask, request
from wakeonlan import send_magic_packet
import random
import re

token_db = ['ad34931a1b8984d54cc92a339f7a16946d65dc58c9704b9e472dc056e5eb4648',
			'97ee79c42d41f01f8a89c11e17880676f01e792401fbb15158443b31a736d74f',
			'38dfac9a8cd1b03033757b98212a136f4f8e644d9308c444a1d854e92534805d',
			'948c4bae682b174278a980d32c38d6afbc2fb38dcc79da530ac89652da01e644',
			'4c3010eb62450b1f93063cfbdf5fb98cf006bee45a49714d805b7bd810c72b61',
			'8bf3d52058d9eba99de9a7847369fe7bd26eabf2046cde27ac1e1910e62a8f2a',
			'd287e187d620557758063e62fa21f9e49a855167fa2e178b6e492d7f0b05f775',
			'8a527e328e0c641d3168252a7c369a2d115624b5eb5f2cdea1eff64de13b9fe2',
			'dc536175d3ab89d4a013be3ae392e02f6134ffa05c571fcae122e37ed3e059f2',
			'9d6cddfa80776fc8729cef0576842458467deb997d62edac1667d85d4b335fe7']


app = Flask(__name__)


# the endpoint for fetching current weather
@app.route("/weather", methods=['GET'])
def get_weather():

	with open('weather.txt', 'r') as f:
		try:
			x = f.read()
		except Exception as er:
			return {"server_response":f'{er}'}			

	return {"server_response":f'{x}'}



@app.route("/time", methods=['GET'])
def curr_time():
	with open('time.txt', 'r') as f:
		try:
			x = f.read()
		except Exception as er:
			return {"server_response":f'{er}'}		

	return {"server_response":f'{x}'}



@app.route('/get_token', methods=['GET'])
def get_token():
	rand_idx = random.randint(0, len(token_db)-1)
	current_token = token_db[rand_idx]

	return {"generated_token":f"{current_token}"}



@app.route('/wake', methods=['POST'])
def wake():
	decoded_data = request.data.decode("utf-8")

	m = re.search(r'\?token=(.*)&mac=(.*)', decoded_data)

	if m:
		token, mac = m.groups()
		mac_splitted = mac.split('-')

		if (len(mac_splitted) != 6):
			return {"server_response":"mac_address must contain 6 number pairs"}
			
		if token in token_db:
			mac_joined = '.'.join(mac_splitted)

			try:
				send_magic_packet(mac_joined)
			except Exception as er:
				return {"server_response":f"{er}"}

			return {"server_response": "execute wakeonlan"}
		else:
			return {"server_response":"your token is NOT valid"}

	else:
		return {"server_response":"couldn't parse the query"}

	

@app.route('/log_data', methods=['POST'])
def log_data():
	decoded_data = request.data.decode("utf-8")

	m = re.search(r'\?filename=(.*)&data=(.*)$', decoded_data)

	if m:
		filename, data = m.groups()
	else:
		return {"server_response":"couldn't parse the query"}


	with open(f'{filename}.txt', 'a') as f:
		try:
			f.write(f'{data}\n')
		except Exception as er:
			return {"server_response":f"{er}"}

	return {"server_response":"your data has been logged"}



@app.route('/schedule', methods=['GET'])
def schedule():
	with open('schedule.txt', 'r') as f:
		try:
			x = f.read()
		except Exception as er:
			return {"server_response":f'{er}'}			

	return {"server_response":f'{x}'}