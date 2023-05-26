import logging



logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('the message goes to file')

def gg(x, y):
	z = x + y
	print(f'z = {z}')
	return z

x = 7
y = 15
z = gg(x, y)
print(z)


logging.info('this is logging.info')
logging.warning('warning of logging.warning')
logging.error('error logging.error')