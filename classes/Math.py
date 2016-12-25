import math

class Math:
	def __init__(self, eq):
		self.equation = eq
		self.equation_list = None

	def print_equation(self):
		print(self.equation)
		
	def remove_spaces(self):
		self.equation = self.equation.replace(" ", "")
		
	def split_equation(self):
		self.equation_list = self.equation.split(" ")
		
	def is_operator(self, char):
		if char is "+" or char is "-" or char is "*" or char is "/":
			return True
		else:
			return False
			
	def remove_spaces(self):
		counter = 0
		eq_list = []
		#equation = ""
		length = len(self.equation)
		
		for char in self.equation:
			eq_list.append(char)
		
		while eq_list.count(" ") is not 0:
			if counter is length:
				counter = 0
			if eq_list[counter] is " ":
				eq_list.pop(counter )
				length -= 1
			counter += 1
			
		self.equation = ""
		for char in eq_list:
			self.equation += char
			
		#return equation
	
	def check_num(self, num):
		check = False
		if num is "(" or num is ")" or num is "+" or num is "-" or num is "*" or num is "/" or num is "^":
			return False
	
		for n in range(0, 10):
			if num == str(n) or num is ".":
				return True


		return False
	
	def prep_equation(self):		
		eq_list = []
		#equation = ""
		#print(self.equation)
		for char in self.equation:
			eq_list.append(char)
			
		counter = 0
		#eq_list[counter] is not " " and eq_list[counter + 1] is not " " and
		# and self.check_num(eq_list[counter]) is False and self.check_num(eq_list[counter + 1]) is not False
		
		#print(self.check_num((".")))
		#print(self.check_num("1"))
		
		while counter is not len(eq_list) - 1:
			if eq_list[counter] is not " " and eq_list[counter + 1] is not " ":
				if self.check_num(eq_list[counter]) is True and self.check_num(eq_list[counter + 1]) is True:
					pass
				else:
					eq_list.insert(counter + 1, " ")
			
		
			counter += 1
			
		self.equation = ""
		for char in eq_list:
			self.equation += char
		
		#print(self.equation)
		#return equation		
	
	def find_operators(self, equation_list):
		add = []
		sub = []
		mul = []
		div = []
		left_par = []
		right_par = []
		pows = []
		operator_count = 0
		counter = 0
		
		for char in equation_list:
			if char is "+":
				add.append(counter)
				operator_count += 1
				
			elif char is "-":
				sub.append(counter)
				operator_count += 1
				
			elif char is "*":
				mul.append(counter)
				operator_count += 1
				
			elif char is "/":
				div.append(counter)
				operator_count += 1
				
			elif char is "(":
				left_par.append(counter)
				
			elif char is ")":
				right_par.append(counter)
				
			elif char is "^":
				pows.append(counter)
				operator_count += 1
				
			counter += 1
				
		#print(add)
		#print(sub)
		#print(mul)
		#print(div)
		#print(left_par)
		#print(right_par)
		#print(equation_list)
		
		return add, sub, mul, div, left_par, right_par, pows, operator_count
		
	#def find_par(self):
		
		
	def solve_equation(self, equation):	
		add, sub, mul, div, left_par, right_par, pows, operator_count = self.find_operators(equation)
		
		#print(add)
		#print(sub)
		#print(mul)
		#print(div)
		#print(left_par)
		#print(right_par)
		#print(operator_count)
		
		solved = self.solve(add, sub, mul, div, pows, operator_count, equation)
		
		return solved
		
	def solve(self, add, sub, mul, div, pows, operator_count, equation):
		#print(equation)
		counter = 0

		while operator_count is not 0:
			if len(pows) is not 0:
				char = "^"
				counter = pows.pop(0)
				
				
			elif len(mul) is not 0:
				char = "*"
				counter = mul.pop(0)
			
			elif len(div) is not 0:
				char = "/"
				counter = div.pop(0)
				
			elif len(add) is not 0:
				char = "+"
				counter = add.pop(0)
				
			elif len(sub) is not 0:
				char = "-"
				counter = sub.pop(0)
				
			#print(char)
			
			x = equation[counter - 1]
			y = equation[counter + 1]
			
			equation.pop(counter - 1)
			equation.pop(counter - 1)
			equation.pop(counter - 1)
			
			if char is "+":
				equation.insert(counter -1, float(x) + float(y))
			elif char is "-":
				equation.insert(counter -1, float(x) - float(y))
			elif char is "*":
				equation.insert(counter -1, float(x) * float(y))
			elif char is "/":
				equation.insert(counter -1, float(x) / float(y))
			elif char is "^":
				equation.insert(counter - 1, pow(float(x), float(y)))
				
	
			while len(add) is not 0:
				add.pop(0)
				
			while len(sub) is not 0:
				sub.pop(0)
				
			while len(mul) is not 0:
				mul.pop(0)
				
			while len(div) is not 0:
				div.pop(0)
				
			while len(pows) is not 0:
				pows.pop(0)

			operator_count -= 1
			
			add, sub, mul, div, left_par, right_par, pows, operator_count = self.find_operators(equation)
			
		return equation[0]
		
		
	def parse_equation(self):
		sub_eq = []
		in_par = False
		try:
			self.remove_spaces()
			self.prep_equation()
			self.split_equation()
			
			#print(self.equation_list)
			
			add, sub, mul, div, left_par, right_par, pows, operator_count = self.find_operators(self.equation_list)
			
			while len(left_par) is not 0:
				for char in self.equation_list:
					if char is ")":
						in_par = False
						break
					if in_par:
						sub_eq.append(char)
					if char is "(":
						in_par = True
				solved_sub = self.solve_equation(sub_eq)
				sub_eq = []
				#print(solved_sub)
				
				placed = left_par_pos = left_par.pop(0)
				right_par_pos = right_par.pop(0)
			
				while left_par_pos < right_par_pos + 1:
					#print(self.equation_list)
					self.equation_list.pop(placed)
					left_par_pos += 1
				
				
				self.equation_list.insert(placed, solved_sub)
				#print(self.equation_list)
				
				while len(left_par) is not 0:
					left_par.pop(0)
					
				while len(right_par) is not 0:
					right_par.pop(0)
				
				add, sub, mul, div, left_par, right_par, pow, operator_count = self.find_operators(self.equation_list)
				
				#print(self.equation_list)
				
				
			value = self.solve_equation(self.equation_list)
			if isinstance(value, (int, float)):
				return(value)
			
			#print(equation)
		#	return equation
			
		except Exception as error:
			#print("Please check your equation.")
			pass
		
	
def main():
	
	eq = "2.4 + 2.6"
	#eq = remove_spaces(eq, len(eq))

	#equation = prep_equation(eq)

	math = Math(eq)
	value = math.parse_equation()
	print(value)
	
	
if __name__ == "__main__":
	main()
		


