# The application is made for quick testing puposes
# Tests are made with microcontroller module STM32

from flask import Flask, request
import asyncio
import python_weather as pw
from datetime import datetime
import logging
import wakeonlan as wl
import random
import re


#def parse_token_mac(data_to_parse:str) -> bool:



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


# The coroutine is called to obtain weather. Called in "weather" endpoint
async def async_get_weather():

	async with pw.Client(unit=pw.METRIC) as cl:
		weather = await cl.get('Tomsk')

	return (weather.current.temperature, 
			    weather.current.description,
			    weather.current.date)


app = Flask(__name__)


# the endpoint for fetching current weather
@app.route("/weather", methods=['GET'])
def weather():
	t, d, date = asyncio.run(async_get_weather())
	return {'temp':t, 
			'desc':d,
			'date':date}


# the endpoint for fetching current machine time
@app.route("/time", methods=['GET'])
def curr_time():
	curr = datetime.now()
	current_time = curr.strftime("%H:%M:%S")
	d = {'current_server_time':current_time}
	return d


# Testing request object properties for GET and POST methods
@app.route('/test_req_get', methods=['GET'])
def test_req_get():
	print(f'request:\n{request}\n')
	print(f'dir(request):\n{dir(request)}\n')
	print(f'request.args:\n{request.args}\n')
	if request.args:
		print(f"request.args['arg1']:\n{request.args['arg1']}\n")
		print(f"dir(request.args):\n{dir(request.args)}\n")
		print(f"request.args.keys():\n{request.args.keys()}\n")
		print(f"dir(request.args.keys()):\n{dir(request.args.keys())}\n")
		print(f"list(request.args.keys()):\n{list(request.args.keys())}\n")

	print(f"request.method:\n{request.method}\n")
	print(f"request.view_args:\n{request.view_args}\n")
	print(f"request.data:\n{request.data}\n")
	return {"flask_response":"OK"}


@app.route('/test_req_post', methods=['POST'])
def test_req_post():
	print(f'request:\n{request}\n')
	print(f'dir(request):\n{dir(request)}\n')
	print(f'request.args:\n{request.args}\n')

	print(f"request.method:\n{request.method}\n")
	print(f"request.view_args:\n{request.view_args}\n")
	print(f"request.data:\n{request.data}\n")
	print(f"request.values:\n{request.values}\n")

	#print(f"request.content_type:\n{request.content_type}\n")

	decoded_data = request.data.decode("utf-8")
	print(f"decoded_data:\n{decoded_data}\n")
	logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
	logging.debug(f'{decoded_data}')

	return {"flask_response":"OK"}


@app.route('/get_token', methods=['GET'])
def get_token():
	rand_idx = random.randint(0, len(token_db)-1)
	current_token = token_db[rand_idx]


	return {"generated_token":f"{current_token}"}


@app.route('/wake', methods=['POST'])
def wake():
	
	decoded_data = request.data.decode("utf-8")
	print(f"decoded_data:\n{decoded_data}\n")

	m = re.search(r'\?token=(.*)&mac=(.*)', decoded_data)
	if m:
		token, mac = m.groups()
	else:
		return {"server_response":"couldn't parse the query"}

	if token in token_db:
		return {"server_response":"your token is valid",
				"mac_address":f"{mac}"}
	else:
		return {"server_response":"your token is not valid",
				"mac_address":f"{mac}"}


@app.route('/log_data', methods=['POST'])
def log_data():
	decoded_data = request.data.decode("utf-8")
	print(f"decoded_data:\n{decoded_data}\n")

	m = re.search(r'\?filename=(.*)&data=(.*)$', decoded_data)

	if m:
		filename, data = m.groups()
	else:
		return {"server_response":"couldn't parse the query"}

	print(f'data:{data}')
	print(f'filename: {filename}')

	#logging.basicConfig(filename=f'{filename}.log', encoding='utf-8', level=logging.INFO)
	#logging.info(f'{data}')
	with open(f'{filename}.txt', 'a') as f:
		f.write(f'{data}\n')

	return {"server_response":"your data has been logged"}


