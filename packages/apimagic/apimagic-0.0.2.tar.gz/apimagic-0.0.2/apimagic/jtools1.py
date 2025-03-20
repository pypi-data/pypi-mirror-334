
import numpy as np 

class Sorter:
	def __init__(self):
		self.x = np.array([])  
	def sort_things(self,things):
		idx = np.argsort(things) 
		return np.array(things)[idx] 


Notes = '''

S = Sorter()
things1 = [5,1,4,2,3]
things2 = S.sort_things(things1)


'''






