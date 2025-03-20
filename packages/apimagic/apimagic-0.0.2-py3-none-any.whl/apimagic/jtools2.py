
import numpy as np 

class Adder:
	def __init__(self):
		self.x = np.array([])  
	def add_things(self,things1,things2):
		a = np.array(things1)
		b = np.array(things2)
		return a+b


Notes = '''

things1 = [5,1,4,2,3]
things2 = [1,2,3,4,5] 

A = Adder()
things3 = A.add_things(things1)

'''






