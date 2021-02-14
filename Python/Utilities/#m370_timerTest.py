#m370_timerTest.py

import time

def main():
	'''Tst using perf_counter from the time module'''
	timerr = 0.0
	interval = 0.5 #in seconds
	while 1:
		tic = time.perf_counter()
		if tic - timerr >  interval:
			print("bep", tic)
			timerr = time.perf_counter()
		time.sleep(0.01)

if __name__  == "__main__":
	main()
