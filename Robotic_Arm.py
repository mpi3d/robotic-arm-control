# coding=utf-8
import Adafruit_PCA9685
import math
import time

frequency = 50

class base:
	name = 'base'
	port = 0
	reverse = True
	adjust = 5
	min = 130
	max = 475

class shoulder:
	name = 'shoulder'
	class rigth:
		port = 1
		adjust = 0
	class left:
		port = 2
		adjust = 20
	reverse = True
	min = 130
	max = 475

class elbow:
	name = 'elbow'
	port = 3
	reverse = True
	adjust = -5
	min = 150
	max = 500

class wrist:
	name = 'wrist'
	port = 4
	reverse = True
	adjust = -5
	min = 125
	max = 540

class wrench:
	name = 'wrench'
	port = 5
	reverse = False
	adjust = 0
	min = 280
	max = 450

class all:
	name = 'all'
	list_articulations = [
	base, 
	shoulder, 
	elbow, 
	wrist, 
	wrench
	]

if frequency > 1526 or frequency < 24:
	raise ValueError('The variable "frequency" must be beteewn 24Hz and 1526Hz.')

class Utils:

	def degrees_to_toff(articulation, degrees):
		return round((articulation.max - articulation.min) / 180 * degrees + articulation.min)

	def toff_to_degrees(articulation, toff):
		return round(180 / (articulation.max - articulation.min) * (toff - articulation.min))

	def percent_to_toff(articulation, percent):
		return round((articulation.max - articulation.min) / 100 * percent + articulation.min)

	def toff_to_percent(articulation, toff):
		return round(100 / (articulation.max - articulation.min) * (toff - articulation.min))

	def get_middle_toff(articulation):
		return round((articulation.max - articulation.min) / 2 + articulation.min)

class File:

	def __init__(self, arm, filename, new=True):
		self.arm = arm
		self.filename = filename
		if new:
			file = open(self.filename,  "w")
			file.write("## "+self.filename+" ##")
			file.close()

	def start_record(self):
		self.arm.record_list = []
		self.arm.record = True
		file = open(self.filename,  "a")
		file.write("\ns, base, "+str(self.arm.get_toff(base)))
		file.write("\ns, shoulder, "+str(self.arm.get_toff(shoulder)))
		file.write("\ns, elbow, "+str(self.arm.get_toff(elbow)))
		file.write("\ns, wrist, "+str(self.arm.get_toff(wrist)))
		file.write("\ns, wrench, "+str(self.arm.get_toff(wrench)))
		file.close()

	def stop_record(self):
		self.arm.record = False
		file = open(self.filename,  "a")
		for event in self.arm.record_list:
			file.write("\n"+event)
		file.close()
		self.arm.record_list = []

	def add_delay(self, delay):
		if self.arm.record:
			self.arm.record_list.append("t, "+str(delay))
		else:
			file = open(self.filename,  "a")
			file.write("\nt, "+str(delay))
			file.close()

	def add_position(self):
		if self.arm.record:
			self.arm.record_list.append("\ns, base, "+str(self.arm.get_toff(base)))
			self.arm.record_list.append("\ns, shoulder, "+str(self.arm.get_toff(shoulder)))
			self.arm.record_list.append("\ns, elbow, "+str(self.arm.get_toff(elbow)))
			self.arm.record_list.append("\ns, wrist, "+str(self.arm.get_toff(wrist)))
			self.arm.record_list.append("\ns, wrench, "+str(self.arm.get_toff(wrench)))
		else:
			file = open(self.filename,  "a")
			file.write("\ns, base, "+str(self.arm.get_toff(base)))
			file.write("\ns, shoulder, "+str(self.arm.get_toff(shoulder)))
			file.write("\ns, elbow, "+str(self.arm.get_toff(elbow)))
			file.write("\ns, wrist, "+str(self.arm.get_toff(wrist)))
			file.write("\ns, wrench, "+str(self.arm.get_toff(wrench)))
			file.close()

class Arm:

	def __init__(self, 
	def_pos_base=Utils.get_middle_toff(base), 
	def_pos_shoulder=Utils.get_middle_toff(shoulder), 
	def_pos_elbow=Utils.get_middle_toff(elbow), 
	def_pos_wrist=Utils.get_middle_toff(wrist), 
	def_pos_wrench=Utils.get_middle_toff(wrench)):
		self.servo = Adafruit_PCA9685.PCA9685()
		self.servo.set_pwm_freq(frequency)
		self.base_pos = def_pos_base
		self.shoulder_pos = def_pos_shoulder
		self.elbow_pos = def_pos_elbow
		self.wrist_pos = def_pos_wrist
		self.wrench_pos = def_pos_wrench
		self.base_is_active = True
		self.shoulder_is_active = True
		self.elbow_is_active = True
		self.wrist_is_active = True
		self.wrench_is_active = True
		self.record_list = []
		self.record = False
		Arm.__set_toff__(self, base, def_pos_base, False)
		time.sleep(0.5)
		Arm.__set_toff__(self, shoulder, def_pos_shoulder, False)
		time.sleep(0.5)
		Arm.__set_toff__(self, elbow, def_pos_elbow, False)
		time.sleep(0.5)
		Arm.__set_toff__(self, wrist, def_pos_wrist, False)
		time.sleep(0.5)
		Arm.__set_toff__(self, wrench, def_pos_wrench, False)
		time.sleep(0.5)

	def __set_toff__(self, articulation, toff, sleep=True):
		if toff < articulation.min:
			toff = articulation.min
		if toff > articulation.max:
			toff = articulation.max
		if articulation.reverse:
			toff_middle = Utils.get_middle_toff(articulation)
			toff_end = toff_middle - (toff - toff_middle)
		else:
			toff_end = toff
		if articulation == shoulder:
			toff_middle = Utils.get_middle_toff(articulation)
			self.servo.set_pwm(articulation.rigth.port, 0, toff_end + articulation.rigth.adjust)
			self.servo.set_pwm(articulation.left.port, 0, (toff_middle - (toff_end - toff_middle)) + articulation.left.adjust)
		else:
			self.servo.set_pwm(articulation.port, 0, toff_end + articulation.adjust)
		if articulation == base:
			position = self.base_pos
			self.base_pos = toff
			self.base_is_active = True
		elif articulation == shoulder:
			position = self.shoulder_pos
			self.shoulder_pos = toff
			self.shoulder_is_active = True
		elif articulation == elbow:
			position = self.elbow_pos
			self.elbow_pos = toff
			self.elbow_is_active = True
		elif articulation == wrist:
			position = self.wrist_pos
			self.wrist_pos = toff
			self.wrist_is_active = True
		elif articulation == wrench:
			position = self.wrench_pos
			self.wrench_pos = toff
			self.wrench_is_active = True
		if sleep:
			if position > toff:
				increment = position - toff
			elif position < toff:
				increment = toff - position
			else:
				increment = 0
			time.sleep(1 / (articulation.max - articulation.min) * (increment))

	def __set_enable__(self, articulation):
		if articulation == base:
			toff = self.base_pos
			self.base_is_active = True
		elif articulation == shoulder:
			toff = self.shoulder_pos
			self.shoulder_is_active = True
		elif articulation == elbow:
			toff = self.elbow_pos
			self.elbow_is_active = True
		elif articulation == wrist:
			toff = self.wrist_pos
			self.wrist_is_active = True
		elif articulation == wrench:
			toff = self.wrench_pos
			self.wrench_is_active = True
		Arm.__set_toff__(self, articulation, toff, False)

	def __set_disable__(self, articulation):
		if articulation == base:
			self.base_is_active = False
		elif articulation == shoulder:
			self.shoulder_is_active = False
		elif articulation == elbow:
			self.elbow_is_active = False
		elif articulation == wrist:
			self.wrist_is_active = False
		elif articulation == wrench:
			self.wrench_is_active = False
		if articulation == shoulder:
			self.servo.set_pwm(articulation.rigth.port, 0, 0)
			self.servo.set_pwm(articulation.left.port, 0, 0)
		else:
			self.servo.set_pwm(articulation.port, 0, 0)

	def play_file(self, filename):
		file = open(filename,  "r")
		file_text = file.read().split("\n")
		for action in file_text:
			action_info = action.split(", ")
			if action_info[0] == 's':
				Arm.set_toff(self, eval(action_info[1]), int(action_info[2]))
			elif action_info[0] == 'ss':
				Arm.set_toff_speed(self, eval(action_info[1]), int(action_info[2]), int(action_info[3]))
			elif action_info[0] == 'st':
				Arm.set_toff_time(self, eval(action_info[1]), int(action_info[2]), int(action_info[3]))
			elif action_info[0] == 't':
				time.sleep(int(action_info[1]))
			elif action_info[0] == 'se':
				Arm.set_enable(self, eval(action_info[1]))
			elif action_info[0] == 'sd':
				Arm.set_disable(self, eval(action_info[1]))

	def set_enable(self, articulation):
		if self.record:
			self.record_list.append('se, '+articulation.name)
		if articulation == all:
			for object in articulation.list_articulations:
				Arm.__set_enable__(self, object)
		else:
			Arm.__set_enable__(self, articulation)

	def set_disable(self, articulation):
		if self.record:
			self.record_list.append('sd, '+articulation.name)
		if articulation == all:
			for obj in articulation.list_articulations:
				Arm.__set_disable__(self, obj)
		else:
			Arm.__set_disable__(self, articulation)

	def set_toff(self, articulation, toff):
		if self.record:
			self.record_list.append('s, '+articulation.name+', '+str(toff))
		Arm.__set_toff__(self, articulation, toff)

	def set_degrees(self, articulation, degrees):
		if articulation == wrench:
			print("The wrench can't be set in degrees. " + 'Try with "set_percent".')
		else:
			toff = Utils.degrees_to_toff(articulation, degrees)
			if self.record:
				self.record_list.append('s, '+articulation.name+', '+str(toff))
			Arm.__set_toff__(self, articulation, toff)

	def set_percent(self, articulation, percent):
		toff = Utils.percent_to_toff(articulation, percent)
		if self.record:
			self.record_list.append('s, '+articulation.name+', '+str(toff))
		Arm.__set_toff__(self, articulation, toff)

	def set_toff_speed(self, articulation, speed_percent, toff):
		pos = Arm.get_toff(self, articulation)
		if self.record:
			self.record_list.append('ss, '+articulation.name+', '+str(speed_percent)+', '+str(toff))
		if not toff == pos:
			time_interval = (100 - speed_percent) * 0.0001
			if pos > toff:
				difference = pos - toff
				add = -1
			elif toff > pos:
				difference = toff - pos
				add = 1
			while difference > 0:
				pos = pos + add
				Arm.__set_toff__(self, articulation, pos, False)
				difference = difference - 1
				time.sleep(time_interval)
		Arm.__set_toff__(self, articulation, toff)

	def set_degrees_speed(self, articulation, speed_percent, degrees):
		if articulation == wrench:
			print("The wrench can't be set in degrees. " + 'Try with "set_percent".')
		else:
			toff = Utils.degrees_to_toff(articulation, degrees)
			pos = Arm.get_toff(self, articulation)
			if self.record:
				self.record_list.append('ss, '+articulation.name+', '+str(speed_percent)+', '+str(toff))
			if not toff == pos:
				time_interval = (100 - speed_percent) * 0.0001
				if pos > toff:
					difference = pos - toff
					add = -1
				elif toff > pos:
					difference = toff - pos
					add = 1
				while difference > 0:
					pos = pos + add
					Arm.__set_toff__(self, articulation, pos, False)
					difference = difference - 1
					time.sleep(time_interval)
			Arm.__set_toff__(self, articulation, toff)

	def set_percent_speed(self, articulation, speed_percent, percent):
		toff = Utils.percent_to_toff(articulation, percent)
		pos = Arm.get_toff(self, articulation)
		if self.record:
			self.record_list.append('ss, '+articulation.name+', '+str(speed_percent)+', '+str(toff))
		if not toff == pos:
			time_interval = (100 - speed_percent) * 0.0001
			if pos > toff:
				difference = pos - toff
				add = -1
			elif toff > pos:
				difference = toff - pos
				add = 1
			while difference > 0:
				pos = pos + add
				Arm.__set_toff__(self, articulation, pos, False)
				difference = difference - 1
				time.sleep(time_interval)
		Arm.__set_toff__(self, articulation, toff)

	def set_toff_time(self, articulation, time_execution, toff):
		pos = Arm.get_toff(self, articulation)
		if self.record:
			self.record_list.append('st, '+articulation.name+', '+str(time_execution)+', '+str(toff))
		if not toff == pos:
			if pos > toff:
				difference = pos - toff
				add = -1
			elif toff > pos:
				difference = toff - pos
				add = 1
			time_interval = time_execution / difference
			while difference > 0:
				pos = pos + add
				Arm.__set_toff__(self, articulation, pos, False)
				difference = difference - 1
				time.sleep(time_interval)
		else:
			Arm.__set_toff__(self, articulation, toff, False)
			time.sleep(time_execution)
		Arm.__set_toff__(self, articulation, toff)

	def set_degrees_time(self, articulation, time_execution, degrees):
		if articulation == wrench:
			print("The wrench can't be set in degrees. " + 'Try with "set_percent".')
		else:
			toff = Utils.degrees_to_toff(articulation, degrees)
			pos = Arm.get_toff(self, articulation)
			if self.record:
				self.record_list.append('st, '+articulation.name+', '+str(time_execution)+', '+str(toff))
			if not toff == pos:
				if pos > toff:
					difference = pos - toff
					add = -1
				elif toff > pos:
					difference = toff - pos
					add = 1
				time_interval = time_execution / difference
				while difference > 0:
					pos = pos + add
					Arm.__set_toff__(self, articulation, pos, False)
					difference = difference - 1
					time.sleep(time_interval)
			else:
				Arm.__set_toff__(self, articulation, toff, False)
				time.sleep(time_execution)
			Arm.__set_toff__(self, articulation, toff)

	def set_percent_time(self, articulation, time_execution, percent):
		toff = Utils.percent_to_toff(articulation, percent)
		pos = Arm.get_toff(self, articulation)
		if self.record:
			self.record_list.append('st, '+articulation.name+', '+str(time_execution)+', '+str(toff))
		if not toff == pos:
			if pos > toff:
				difference = pos - toff
				add = -1
			elif toff > pos:
				difference = toff - pos
				add = 1
			time_interval = time_execution / difference
			while difference > 0:
				pos = pos + add
				Arm.__set_toff__(self, articulation, pos, False)
				difference = difference - 1
				time.sleep(time_interval)
		else:
			Arm.__set_toff__(self, articulation, toff, False)
			time.sleep(time_execution)
		Arm.__set_toff__(self, articulation, toff)

	def set_position_toff(self, position):
		if self.record:
			self.record_list.append('s, '+str(base)+', '+str(position[0]))
			self.record_list.append('s, '+str(shoulder)+', '+str(position[1]))
			self.record_list.append('s, '+str(elbow)+', '+str(position[2]))
			self.record_list.append('s, '+str(wrist)+', '+str(position[3]))
			self.record_list.append('s, '+str(wrench)+', '+str(position[4]))
		Arm.__set_toff__(self, base, position[0])
		Arm.__set_toff__(self, shoulder, position[1])
		Arm.__set_toff__(self, elbow, position[2])
		Arm.__set_toff__(self, wrist, position[3])
		Arm.__set_toff__(self, wrench, position[4])

	def get_is_active(self, articulation):
		if articulation == base:
			is_active = self.base_is_active
		elif articulation == shoulder:
			is_active = self.shoulder_is_active
		elif articulation == elbow:
			is_active = self.elbow_is_active
		elif articulation == wrist:
			is_active = self.wrist_is_active
		elif articulation == wrench:
			is_active = self.wrench_is_active
		return is_active

	def get_toff(self, articulation):
		if articulation == base:
			toff = self.base_pos
		elif articulation == shoulder:
			toff = self.shoulder_pos
		elif articulation == elbow:
			toff = self.elbow_pos
		elif articulation == wrist:
			toff = self.wrist_pos
		elif articulation == wrench:
			toff = self.wrench_pos
		return toff

	def get_degrees(self, articulation):
		if articulation == base:
			toff = self.base_pos
		elif articulation == shoulder:
			toff = self.shoulder_pos
		elif articulation == elbow:
			toff = self.elbow_pos
		elif articulation == wrist:
			toff = self.wrist_pos
		elif articulation == wrench:
			print("The wrench can't be get in degrees. " + 'Try with "get_percent".')
			return None
		return Utils.toff_to_degrees(articulation, toff)

	def get_percent(self, articulation):
		if articulation == base:
			toff = self.base_pos
		elif articulation == shoulder:
			toff = self.shoulder_pos
		elif articulation == elbow:
			toff = self.elbow_pos
		elif articulation == wrist:
			toff = self.wrist_pos
		elif articulation == wrench:
			toff = self.wrench_pos
		return Utils.toff_to_percent(articulation, toff)

	def get_position_toff(self):
		return [self.base_pos, self.shoulder_pos, self.elbow_pos, self.wrist_pos, self.wrench_pos]

def Vector_3D(x, y, z):

	def __calculate_length__(x, y, z):
		return math.sqrt((x)**2+(y)**2+(z)**2)

	def __calculate_base__(x, y):
		base_degrees = None
		if x > 0 and y > 0:
			base_degrees = math.degrees(math.atan(y/x))
		elif x < 0 and y > 0:
			base_degrees = 180 - math.degrees(math.atan(y/(x*-1)))
		elif x > 0 and y < 0:
			base_degrees = 180 - math.degrees(math.atan((y*-1)/x))
		elif x < 0 and y < 0:
			base_degrees = math.degrees(math.atan((y*-1)/(x*-1)))
		elif x == 0 and y > 0:
			base_degrees = 90
		elif x > 0 and y == 0:
			base_degrees = 0
		elif x == 0 and y < 0:
			base_degrees = 90
		elif x < 0 and y == 0:
			base_degrees = 180
		elif x == 0 and y == 0:
			base_degrees = 90
		return base_degrees
	print(__calculate_length__(x, y, z))
	print(__calculate_base__(x, y))
