#!/usr/bin/python3

class Student:
	# This is a public variable, it can be read and write outside #
	distinctive_features = ""
	
	# This is a private variable, declared with the initial __ #
	# It can be read and write only from/by this class #
	__age = 0
	
	# Class constructor #
	# Every instance method has the self reference as firt parameter #
	def __init__(self, name, age, sex, d_features):
		self.name = name
		self.__age = age
		self.sex = sex
		self.distinctive_features = d_features
	
	# The age varibale is private, we need specific methods for read/write #
	def get_age(self):
		return self.__age
	def getting_old(self):
		self.__age += 1
	
	# Static methods do not reference the object instance "self" #
	def scream():
		print("Arrrrrgh!!!")

	# It returns a strign representing the instance #
	# It is comparable to the .toString() method of Java #
	def __repr__(self):
		return '|'+str(self.name)+','+str(self.__age)+','+str(self.sex)+'|'

	# It returns an hash value for the instance, #
	# it is useful for improving performace when data structures are used #
	def __hash__(self):
		return str(self.__repr__()).__hash__()

	# Private function for object comparison. #
	# It is not a language construct, note the missing trailing __ #
	def __cmp(self, other):
		assert isinstance(other, Student)
		if self.__age == other.__age:
			if self.name == other.name:
				return 0
			elif self.name < other.name:
				return -1
			else:
				return 1
		else:
			return self.__age - other.__age

	# Overloading of comparison operators #
	def __lt__(self, other):
		return self.__cmp(other) < 0
	def __gt__(self, other):
		return self.__cmp(other) > 0
	def __eq__(self, other):
		return self.__cmp(other) == 0
	def __le__(self, other):
		return self.__cmp(other) <= 0
	def __ge__(self, other):
		return self.__cmp(other) >= 0
	def __ne__(self, other):
		return self.__cmp(other) != 0

	# It corresponds to the + operator #
	def __add__(self, other):
		"""
		Add the years of other to the age of this instance.
		"""
		assert isinstance(other, Student)
		# self.__age += other.__age
		# return self
		# the previous two rows modify the self instance #
		# however, arithmetic operators usually return a new object as result of the operation #
		return Student(self.name, self.__age + other.__age, self.sex, self.distinctive_features)



s = Student('S', 22, 'M', "no features")

print(s.name)
# print(s.__age) # private variables of Student can not be referenced here #
print(s.get_age())
s.getting_old()
print(s.get_age())
# s.scream() # static methods can not be called from instances #
Student.scream()

s1 = Student('S1', 21, 'M', "no features")
s2 = Student('S2', 21, 'M', "no features")

# the operator == can be overloaded by rewriting the __eq__ function #
print( s == s2 )
print( s1 == s2 )
print( s1 < s )

# ordering operators allow for sorting, too #
students = [s,s1,s2]
print(sorted(students))

# there is a specific class function to overload for every operator #
# in this case it is __add__ #
print(s + s1)
