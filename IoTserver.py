# The application is made for quick testing puposes
# Tests are made with microcontroller module STM32

from flask import Flask, request
import asyncio
import python_weather as pw
from datetime import datetime


# The coroutine is called to obtain weather
async def async_get_weather():

	async with pw.Client(unit=pw.METRIC) as cl:
		weather = await cl.get('Tomsk')

	return (weather.current.temperature, 
			    weather.current.description,
			    weather.current.date)


app = Flask(__name__)

@app.route("/weather")
def weather():
	t, d, date = asyncio.run(async_get_weather())
	return {'temp':t, 
			'desc':d}


@app.route("/time")
def curr_time():
	curr = datetime.now()
	current_time = curr.strftime("%H:%M:%S")
	return {'current_time/\n':current_time}


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
	return {5:1}


@app.route('/test_req_post', methods=['POST'])
def test_req_post():
	print(f'request:\n{request}\n')
	print(f'dir(request):\n{dir(request)}\n')
	print(f'request.args:\n{request.args}\n')

	print(f"request.method:\n{request.method}\n")
	print(f"request.view_args:\n{request.view_args}\n")
	print(f"request.data:\n{request.data}\n")
	print(f"request.values:\n{request.values}\n")
	for i in request.values:
		print(i)

	return {5:1}