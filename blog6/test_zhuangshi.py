import time

def timer(n):
	def wrap1(func):
		def wrap2(*args,**kwargs):
			time1 = time.time()
			for i in range(n):
				result = func(*args,**kwargs)
			time2 = time.time()
			print(time2-time1)
			return result
		return wrap2
	return wrap1
@timer(10000000)
def  foo(x,y):
	return x ** y

foo(9,3)