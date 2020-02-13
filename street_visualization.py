from graphics import *
import time
import datetime
import threading
import queue
import random
import math
from enum import Enum

class RandableEnum(Enum):
	@classmethod
	def rand(self):
		return random.Random().choice(self.list())

	@classmethod
	def list(self):
		return [e for e in self]

	@classmethod
	def values(self):
		return [e.value for e in self]

	@classmethod
	def caseOf(self, value):
		if (value not in self.values()):
			return None
		else:
			return self(value)

class list_2D(list):
	def len_2D(self):
		count = 0
		for eachList in self:
			count += len(eachList)
		return count
	
	def index_2D(self, index):
		index_1 = math.floor(index / len(self))
		index_2 = index % len(self[0])
		return self[index_1][index_2]


class HorizontalStreet():
	def __init__(self, y_value, window, thickness):
		self.y_pos = y_value
		self.window = window
		self.thickness = thickness
		self.rect = Rectangle(Point(0, y_value), Point(window.getHeight(), y_value + thickness))
		self.rect.setFill("black")

	def draw(self):
		self.rect.draw(self.window)

	def getPos(self):
		return self.y_pos

class VerticalStreet():
	def __init__(self, x_value, window, thickness):
		self.x_pos = x_value
		self.window = window
		self.thickness = thickness
		self.rect = Rectangle(Point(x_value, 0), Point(x_value + thickness, window.getHeight()))
		self.rect.setFill("black")

	def draw(self):
		self.rect.draw(self.window)

	def getPos(self):
		return self.x_pos

class StreetLightPosition(RandableEnum):
	RIGHT = 'RIGHT'
	LEFT = 'LEFT'
	TOP = 'TOP'
	BOTTOM = 'BOTTOM'

class StreetLightState(RandableEnum):
	RED = 'RED'
	YELLOW = 'YELLOW'
	GREEN = 'GREEN'
	GREEN_ARROW = 'GREEN_ARROW'
	YELLOW_ARROW = 'YELLOW_ARROW'

class IntersectionChannel(RandableEnum):
	HORIZONTAL = 'HORIZONTAL'
	VERTICAL = 'VERTICAL'
	HORIZONTAL_LEFT_TURN = 'HORIZONTAL_LEFT_TURN'
	VERTICAL_LEFT_TURN = 'VERTICAL_LEFT_TURN'

class IntersectionState(RandableEnum):
	HORIZONTAL_GREEN = 'HORIZONTAL_GREEN'
	HORIZONTAL_LEFT_TURN = "HORIZONTAL_LEFT_TURN"
	HORIZONTAL_YELLOW = 'HORIZONTAL_YELLOW'
	HORIZONTAL_LEFT_TURN_YELLOW = 'HORIZONTAL_LEFT_TURN_YELLOW'
	VERTICAL_GREEN = 'VERTICAL_GREEN'
	VERTICAL_LEFT_TURN = 'VERTICAL_LEFT_TURN'
	VERTICAL_YELLOW = 'VERTICAL_YELLOW'
	VERTICAL_LEFT_TURN_YELLOW = 'VERTICAL_LEFT_TURN_YELLOW'
	RED = 'RED'

class Turn(RandableEnum):
	RIGHT = -1
	STRAIGHT = 0
	LEFT = 1

class Direction(RandableEnum):
	UP = 1
	LEFT = 2
	DOWN = 3
	RIGHT = 4
	
	def turn(self, turn):
		if (self == Direction.UP and turn == Turn.RIGHT):
			return Direction.RIGHT
		elif (self == Direction.RIGHT and turn == Turn.LEFT):
			return Direction.UP
		else:
			return Direction.caseOf(self.value + turn.value)

class StreetLight():
	def __init__(self, horizontal_street, vertical_street, position, window):
		self.state = StreetLightState.RED
		if (isinstance(position, StreetLightPosition)):
			self.position = position
		else: 
			raise TypeError(f"StreetLight() was passed a {type(position)} as its 'position' argument. Expected a StreetLightPosition.")
		self.window = window
		self.vertical_street = vertical_street
		self.horizontal_street = horizontal_street
		if position == StreetLightPosition.RIGHT:
			self.main_rect = Rectangle(Point(vertical_street.getPos() + 10, horizontal_street.getPos() - 5), Point(vertical_street.getPos() + 15, horizontal_street.getPos() + 5))
			self.left_rect = Rectangle(Point(vertical_street.getPos() + 10, horizontal_street.getPos() + 5), Point(vertical_street.getPos() + 15, horizontal_street.getPos() + 10))
		elif position == StreetLightPosition.LEFT:
			self.main_rect = Rectangle(Point(vertical_street.getPos() - 5, horizontal_street.getPos()), Point(vertical_street.getPos() - 10, horizontal_street.getPos() + 10))
			self.left_rect = Rectangle(Point(vertical_street.getPos() - 5, horizontal_street.getPos() - 5), Point(vertical_street.getPos() - 10, horizontal_street.getPos()))
		elif position == StreetLightPosition.TOP:
			self.main_rect = Rectangle(Point(vertical_street.getPos() - 5, horizontal_street.getPos() - 10), Point(vertical_street.getPos() + 5, horizontal_street.getPos() - 5))
			self.left_rect = Rectangle(Point(vertical_street.getPos() + 5, horizontal_street.getPos() - 10), Point(vertical_street.getPos() + 10, horizontal_street.getPos() - 5))
		elif position == StreetLightPosition.BOTTOM:
			self.main_rect = Rectangle(Point(vertical_street.getPos(), horizontal_street.getPos() + 10), Point(vertical_street.getPos() + 10, horizontal_street.getPos() + 15))
			self.left_rect = Rectangle(Point(vertical_street.getPos() - 5, horizontal_street.getPos() + 10), Point(vertical_street.getPos(), horizontal_street.getPos() + 15))
		self.main_rect.setFill("red")
		self.left_rect.setFill("red")

	def draw(self):
		if self.state == StreetLightState.RED:
			self.main_rect.setFill("red")
			self.left_rect.setFill("red")
		elif self.state == StreetLightState.YELLOW:
			self.main_rect.setFill("yellow")
			self.left_rect.setFill("red")
		elif self.state == StreetLightState.GREEN:
			self.main_rect.setFill("green")
			self.left_rect.setFill("red")
		elif self.state == StreetLightState.GREEN_ARROW:
			self.main_rect.setFill("red")
			self.left_rect.setFill("green")
		elif self.state == StreetLightState.YELLOW_ARROW:
			self.main_rect.setFill("red")
			self.left_rect.setFill("yellow")
		self.main_rect.undraw()
		self.main_rect.draw(self.window)
		self.left_rect.undraw()
		self.left_rect.draw(self.window)

	def updateState(self, newstate):
		if isinstance(newstate, StreetLightState):
			self.state = newstate
			self.draw()
		else:
			raise TypeError(f"StreetLight.draw() was passed a {type(newstate)} as its 'newstate' argument. Expected a StreetLightState.")

class Intersection():
	def __init__(self, horizontal_street, vertical_street, window, state=IntersectionState.HORIZONTAL_GREEN):
		if(isinstance(horizontal_street, HorizontalStreet)):
			self.horizontal_street = horizontal_street
		else: 
			raise TypeError(f"Intersection() was passed a {type(horizontal_street)} as its horizontal_street parameter. Expected a HorizontalStreet.")

		if(isinstance(vertical_street, VerticalStreet)):
			self.vertical_street = vertical_street
		else:
			raise TypeError(f"Intersection() was passed a {type(vertical_street)} as its vertical_street parameter. Expected a VerticalStreet.")

		if(isinstance(state, IntersectionState)):
			self.state = state
		else: 
			self.state = IntersectionState.HORIZONTAL_GREEN
			print(f"Intersection() was passed a {type(state)} as its state argument. It has been assigned to its default value, IntersectionState.HORIZONTAL_GREEN. In the future, please pass the function an IntersectionState.")
		self.window = window
		self.top_light = StreetLight(horizontal_street, vertical_street, StreetLightPosition.TOP, window)
		self.bottom_light = StreetLight(horizontal_street, vertical_street, StreetLightPosition.BOTTOM, window)
		self.left_light = StreetLight(horizontal_street, vertical_street, StreetLightPosition.LEFT, window)
		self.right_light = StreetLight(horizontal_street, vertical_street, StreetLightPosition.RIGHT, window)
		self.updateState()

	def updateState(self, state=None):
		if state is None:
			state = self.state
		if (isinstance(state, IntersectionState)):
			self.state = state
		else:
			raise TypeError(f"Intersection.updateState() was passed a {type(state)} as its state argument. An IntersectionState was expected.")

		if (self.state == IntersectionState.HORIZONTAL_GREEN):
			self.left_light.updateState(StreetLightState.GREEN)
			self.right_light.updateState(StreetLightState.GREEN)
			self.top_light.updateState(StreetLightState.RED)
			self.bottom_light.updateState(StreetLightState.RED)
		elif (self.state == IntersectionState.HORIZONTAL_YELLOW):
			self.left_light.updateState(StreetLightState.YELLOW)
			self.right_light.updateState(StreetLightState.YELLOW)
			self.top_light.updateState(StreetLightState.RED)
			self.bottom_light.updateState(StreetLightState.RED)
		elif (self.state == IntersectionState.HORIZONTAL_LEFT_TURN):
			self.left_light.updateState(StreetLightState.GREEN_ARROW)
			self.right_light.updateState(StreetLightState.GREEN_ARROW)
			self.top_light.updateState(StreetLightState.RED)
			self.bottom_light.updateState(StreetLightState.RED)
		elif (self.state == IntersectionState.HORIZONTAL_LEFT_TURN_YELLOW):
			self.left_light.updateState(StreetLightState.YELLOW_ARROW)
			self.right_light.updateState(StreetLightState.YELLOW_ARROW)
			self.top_light.updateState(StreetLightState.RED)
			self.bottom_light.updateState(StreetLightState.RED)
		elif (self.state == IntersectionState.VERTICAL_GREEN):
			self.left_light.updateState(StreetLightState.RED)
			self.right_light.updateState(StreetLightState.RED)
			self.top_light.updateState(StreetLightState.GREEN)
			self.bottom_light.updateState(StreetLightState.GREEN)
		elif (self.state == IntersectionState.VERTICAL_YELLOW):
			self.left_light.updateState(StreetLightState.RED)
			self.right_light.updateState(StreetLightState.RED)
			self.top_light.updateState(StreetLightState.YELLOW)
			self.bottom_light.updateState(StreetLightState.YELLOW)
		elif (self.state == IntersectionState.VERTICAL_LEFT_TURN):
			self.left_light.updateState(StreetLightState.RED)
			self.right_light.updateState(StreetLightState.RED)
			self.top_light.updateState(StreetLightState.GREEN_ARROW)
			self.bottom_light.updateState(StreetLightState.GREEN_ARROW)
		elif (self.state == IntersectionState.VERTICAL_LEFT_TURN_YELLOW):
			self.left_light.updateState(StreetLightState.RED)
			self.right_light.updateState(StreetLightState.RED)
			self.top_light.updateState(StreetLightState.YELLOW_ARROW)
			self.bottom_light.updateState(StreetLightState.YELLOW_ARROW)
		elif (self.state == IntersectionState.RED):
			self.left_light.updateState(StreetLightState.RED)
			self.right_light.updateState(StreetLightState.RED)
			self.top_light.updateState(StreetLightState.RED)
			self.bottom_light.updateState(StreetLightState.RED)

class ManageableIntersection():
	def __init__(self, intersection, nextchannel=None, delay=0):
		if(isinstance(intersection, Intersection)):
			self.intersection = intersection
		else:
			raise TypeError(f"ManageableIntersection() was passed a {type(intersection)} as its 'intersection' argument. Expected an Intersection.")

		if(isinstance(nextchannel, IntersectionChannel)):
			self.nextchannel = nextchannel
		else:
			self.nextchannel = None

		if(isinstance(delay, int)):
			self.delay = delay
		else:
			self.delay = 0

		self.backlog = []
		self.lastUpdatedTime = datetime.datetime.now() # used by IntersectionManager to time operations

	@property
	def currentstate(self):
		return self.intersection.state
	

	def pushOperation(self, nextchannel, delay):
		if(not isinstance(nextchannel, IntersectionChannel)):
			raise TypeError(f"ManageableIntersection.pushOperation was passed a {type(nextchannel)} as its 'nextchannel' argument. Expected an IntersectionChannel.")

		if(not isinstance(delay, int)):
			raise TypeError(f"ManageableIntersection.pushOperation was passed a {type(nextchannel)} as its 'delay' argument. Expected an int.")

		if(self.nextchannel == None and self.backlog == []):
			self.nextchannel = nextchannel
			self.delay = delay
		elif(self.nextchannel == None and self.backlog != []):
			self.popOperation()

			newItem = (nextchannel, delay)
			self.backlog.append(newItem)
		elif(self.nextchannel != None):
			newItem = (nextchannel, delay)
			self.backlog.append(newItem)

	def popOperation(self):
		if (self.backlog != []):
			backlogItem = self.backlog.pop(0)
			self.nextchannel = backlogItem[0]
			self.delay = backlogItem[1]
		else:
			self.nextchannel = None
			self.delay = 0

	def stateMatchesNextChannel(self):
		if (self.nextchannel == IntersectionChannel.HORIZONTAL and self.currentstate == IntersectionState.HORIZONTAL_GREEN):
			return True
		elif (self.nextchannel == IntersectionChannel.VERTICAL and self.currentstate == IntersectionState.VERTICAL_GREEN):
			return True
		elif (self.nextchannel == IntersectionChannel.HORIZONTAL_LEFT_TURN and self.currentstate == IntersectionState.HORIZONTAL_LEFT_TURN):
			return True
		elif (self.nextchannel == IntersectionChannel.VERTICAL_LEFT_TURN and self.currentstate == IntersectionState.VERTICAL_LEFT_TURN):
			return True
		else:
			return False

	def readyToUpdate(self):
		if(self.nextchannel == None):
			return False
		else:
			delta = datetime.datetime.now() - self.lastUpdatedTime
			if (delta.seconds >= self.delay):
				return True
			else:
				return False

class IntersectionManager():
	def __init__(self, intersections):
		if (isinstance(intersections, list)):
			if(len(intersections) <= 0):
				raise ValueError("IntersectionManager() was passed an empty list as its 'intersections' parameter. An empty list cannot be processed.")
			elif(not isinstance(intersections[0], list)):
				raise TypeError(f"IntersectionManager() was passed a list of {type(intersections[0])} as its 'intersections' parameter. Expected a 2D list (that is, a list of lists) of Intersections.")
			elif(not isinstance(intersections[0][0], Intersection)):
				raise TypeError(f"IntersectionManager() was passed a 2D list of {type(intersectoins[0][0])} as its 'intersections' parameter. Expected a 2D list of Intersections.")
			else:
				self.intersections = []
				for eachList in intersections:
					active_list = []
					for item in eachList:
						manageable = ManageableIntersection(intersection=item)
						active_list.append(manageable)
					self.intersections.append(active_list)
				try:
					assert len(self.intersections) == len(intersections)
				except AssertionError:
					print("An internal error ocurred while initializing an IntersectionManager. One or more intersections that were passed to the initializer were not able to be initialized into ManageableIntersections.")
					raise
				try:
					for eachList in self.intersections:
						assert len(eachList) == len(intersections[0])
				except AssertionError:
					print("An internal error ocurred while initializing an IntersectionManager. One or more intersections that were passed to the initializer were not able to be intialized into ManageableIntersections.")
					raise
				self.intersections = list_2D(self.intersections)
		else:
			raise TypeError(f"IntersectionManager() was passed a {type(intersections)} as its 'intersections' parameter. Expected a 2D list of Intersections.")

	def pushOperation(self, index, nextchannel, delay):
		if (isinstance(index, int)):
			if (0 <= index < self.intersections.len_2D()):
				pass
			else: 
				raise ValueError(f"IntersectionManager.pushOperation() was passed an out of range value as its 'index' parameter. Please pass a value between 0 and {len(self.intersections)} (inclusive).")
		else:
			raise TypeError(f"IntersectionManager.pushOperation() was passed a {type(index)} as its 'index' parameter. Expected an int.")

		if (not isinstance(nextchannel, IntersectionChannel)):
			raise TypeError(f"IntersectionManager.pushOperation() was passed a {type(nextchannel)} as its 'nextchannel' parameter. Expected an IntersectionChannel.")

		if (not isinstance(delay, int)):
			raise TypeError(f"IntersectionManager.pushOperation() was passed a {type(delay)} as its 'delay' parameter. Expected an int.")

		self.intersections.index_2D(index).pushOperation(nextchannel, delay)	

	def update(self):
		for eachList in self.intersections:
			for intersection in eachList:
				if (intersection.stateMatchesNextChannel()):
					intersection.popOperation()
				if (intersection.readyToUpdate() and not intersection.stateMatchesNextChannel()):
					if (intersection.currentstate == IntersectionState.HORIZONTAL_GREEN):
						newstate = IntersectionState.HORIZONTAL_YELLOW
					elif (intersection.currentstate == IntersectionState.HORIZONTAL_LEFT_TURN):
						newstate = IntersectionState.HORIZONTAL_LEFT_TURN_YELLOW
					elif (intersection.currentstate == IntersectionState.VERTICAL_GREEN):
						newstate = IntersectionState.VERTICAL_YELLOW
					elif (intersection.currentstate == IntersectionState.VERTICAL_LEFT_TURN):
						newstate = IntersectionState.VERTICAL_LEFT_TURN_YELLOW
					elif (intersection.currentstate == IntersectionState.HORIZONTAL_YELLOW or intersection.currentstate == IntersectionState.HORIZONTAL_LEFT_TURN_YELLOW or intersection.currentstate == IntersectionState.VERTICAL_YELLOW or intersection.currentstate == IntersectionState.VERTICAL_LEFT_TURN_YELLOW):
						newstate = IntersectionState.RED
					elif (intersection.currentstate == IntersectionState.RED):
						if (intersection.nextchannel == IntersectionChannel.HORIZONTAL):
							newstate = IntersectionState.HORIZONTAL_GREEN
						elif (intersection.nextchannel == IntersectionChannel.VERTICAL):
							newstate = IntersectionState.VERTICAL_GREEN
						elif (intersection.nextchannel == IntersectionChannel.VERTICAL_LEFT_TURN):
							newstate = IntersectionState.VERTICAL_LEFT_TURN
						elif (intersection.nextchannel == IntersectionChannel.HORIZONTAL_LEFT_TURN): 
							newstate = IntersectionState.HORIZONTAL_LEFT_TURN
						intersection.popOperation()
					intersection.intersection.updateState(newstate)
					intersection.lastUpdatedTime = datetime.datetime.now()

class Route():
	def __init__(self, manager, initial_intersection, initial_direction, turns):
		if (isisntance(manager, IntersectionManager)):
			self.manager = manager
		else:
			raise TypeError(f"Route() was passed a {type(manager)} as its 'manager' argument. Expected an IntersectionManager.")

		if (isinstance(initial_intersection, int)):
			if (0 <= initial_intersection < len(self.manager.intersections)):
				self.active_intersection = initial_intersection
			else:
				raise ValueError(f"Route() was passed {initial_intersection} as its 'initial_intersection' argument. Please pass a valid index of self.manager.")
		else:
			raise TypeError(f"Route() was passed a {type(initial_intersection)} as its 'initial_intersection' argument. Expected an int.")

		if (isinstance(initial_direction, Direction)):
			self.active_direction = initial_direction
		else:
			raise TypeError(f"Route() was passed a {type(initial_direction)} as its 'initial_direction' argument. Expected a Direction.")

		if (isinstance(turns, list)):
			if (isinstance(turns[0], Turn)):
				self.turns = turns
			else:
				raise TypeError(f"Route() was passed a list of {type(turns[0])} as its 'turns' argument. Expected a list of Turns.")
		else:
			raise TypeError(f"Route() was passed a {type(turns)} as its 'turns' argument. Expected a list of Turns.")

def getUpdates(intersection_count, queue):
	while True:
		correct_input = False
		while (not correct_input):
			intersection = input("Which intersection would you like to change? Input 0-15: ")
			try:
				intersection = int(intersection)
				if intersection in range(0, 16):
					correct_input = True
				else:
					print("Please type an integer from 0 to 15.")
			except ValueError: 
				print("Please type an integer")

		correct_input = False
		while (not correct_input):
			channel = input("What should be the new IntersectionChannel? Input an IntersectionChannel: ")
			channel = channel.upper()
			if (IntersectionChannel.caseOf(channel) != None):
				channel = IntersectionChannel.caseOf(channel)
				correct_input = True
			else: 
				print("Please type a valid IntersectionChannel.")
		queue.put((intersection, channel))

def main(): 
	win = GraphWin("Street Visualization", 500, 500)
	win.setBackground(color_rgb(143, 242, 229))

	horizontal_street_1 = HorizontalStreet(100, win, 5)
	horizontal_street_1.draw()

	horizontal_street_2 = HorizontalStreet(200, win, 5)
	horizontal_street_2.draw()

	horizontal_street_3 = HorizontalStreet(300, win, 5)
	horizontal_street_3.draw()

	horizontal_street_4 = HorizontalStreet(400, win, 5)
	horizontal_street_4.draw()

	vertical_street_1 = VerticalStreet(100, win, 5)
	vertical_street_1.draw()

	vertical_street_2 = VerticalStreet(200, win, 5)
	vertical_street_2.draw()

	vertical_street_3 = VerticalStreet(300, win, 5)
	vertical_street_3.draw()

	vertical_street_4 = VerticalStreet(400, win , 5)
	vertical_street_4.draw()

	intersection_1_1 = Intersection(horizontal_street_1, vertical_street_1, win)
	intersection_1_2 = Intersection(horizontal_street_1, vertical_street_2, win)
	intersection_1_3 = Intersection(horizontal_street_1, vertical_street_3, win)
	intersection_1_4 = Intersection(horizontal_street_1, vertical_street_4, win)

	intersection_2_1 = Intersection(horizontal_street_2, vertical_street_1, win)
	intersection_2_2 = Intersection(horizontal_street_2, vertical_street_2, win)
	intersection_2_3 = Intersection(horizontal_street_2, vertical_street_3, win)
	intersection_2_4 = Intersection(horizontal_street_2, vertical_street_4, win)

	intersection_3_1 = Intersection(horizontal_street_3, vertical_street_1, win)
	intersection_3_2 = Intersection(horizontal_street_3, vertical_street_2, win)
	intersection_3_3 = Intersection(horizontal_street_3, vertical_street_3, win)
	intersection_3_4 = Intersection(horizontal_street_3, vertical_street_4, win)

	intersection_4_1 = Intersection(horizontal_street_4, vertical_street_1, win)
	intersection_4_2 = Intersection(horizontal_street_4, vertical_street_2, win)
	intersection_4_3 = Intersection(horizontal_street_4, vertical_street_3, win)
	intersection_4_4 = Intersection(horizontal_street_4, vertical_street_4, win)

	manager = IntersectionManager([[intersection_1_1, intersection_1_2, intersection_1_3, intersection_1_4], [intersection_2_1, intersection_2_2, intersection_2_3, intersection_2_4], [intersection_3_1, intersection_3_2, intersection_3_3, intersection_3_4], [intersection_4_1, intersection_4_2, intersection_4_3, intersection_4_4]])

	operation_queue = queue.Queue()
	operation_get_thread = threading.Thread(target=getUpdates, args=(16, operation_queue))
	operation_get_thread.start()

	while True:
		if not operation_queue.empty():
			operation = operation_queue.get()
			manager.pushOperation(operation[0], operation[1], 5)
		manager.update()

main()