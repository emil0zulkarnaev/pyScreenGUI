#!/usr/bin/python3
#-*- coding:utf-8 -*-


# created on python -V 3.6.8

import os, sys, keyboard, threading

EXIT = False

class GUI:
	def __init__(self):
		self.make_input = False
		self.input_element = None
		self.screens = []
		self.current = 0 
		self.select_view = False
		self.hooks()

	def run(self):
		if len(self.screens) == 0:
			print("You have not any screens")
			return;

		while True:
			# вывод скрина
			if not self.screens[self.current].showed:
				os.system('cls' if os.name == 'nt' else 'clear')
				print(self.screens[self.current])
				self.screens[self.current].showed = True
			# ввод данных в поле
			if self.make_input:
				if self.input_element:
					value = input("Value: ").strip()
					self.input_element.value = value
					self.screens[self.current].showed = False
					self.make_input = False
			if EXIT:
				break

	def new_screen(self, name, description, elements):
		self.screens.append(self.Screen(name=name, description=description, elements=elements))

	def hooks(self):
		keyboard.add_hotkey("space", self.space_hotkey)
		keyboard.add_hotkey("down", self.move_hotkey, args=(False,))
		keyboard.add_hotkey("up", self.move_hotkey, args=(True,))

	def space_hotkey(self):
		element = self.screens[self.current].elements[self.screens[self.current].current]

		if type(element) == self.Screen.Checkbox:
			element.value = not element.value 
		elif type(element) == self.Screen.Input:
			self.make_input = True
			self.input_element = element
			return;
		elif type(element) == self.Screen.Button:
			element.call()
			return;
		elif type(element) == self.Screen.Select:
			if self.select_view:
				self.select_view = False
				element.show_variants = False
			else:
				element.show_variants = True
				element.value = 0
				self.input_element = element
				self.select_view = True
		self.screens[self.current].showed = False

	def move_hotkey(self, direction):
		if direction:
			if self.select_view:
				if self.input_element.value == 0:
					self.input_element.value = len(self.input_element.variants) - 1
				else:
					self.input_element.value -= 1
			else:
				if self.screens[self.current].current == 0:
					self.screens[self.current].current = len(self.screens[self.current].elements) - 1
				else:
					self.screens[self.current].current -= 1
		else:
			if self.select_view:
				if self.input_element.value == len(self.input_element.variants) - 1:
					self.input_element.value = 0 
				else:
					self.input_element.value += 1
			else:
				if self.screens[self.current].current == len(self.screens[self.current].elements) - 1:
					self.screens[self.current].current = 0 
				else:
					self.screens[self.current].current += 1
		self.screens[self.current].showed = False

	class Screen:
		def __init__(self, name, description, elements):
			self.name = name
			self.elements = []
			self.description = description
			self.current = 0 
			self.showed  = False

			self.create_elements(elements)

		def exit(self, obj):
			global EXIT
			EXIT = True 

		def create_elements(self, elements):
			for element in elements:
				if element['type'] == "check":
					self.elements.append(self.Checkbox(name=element['name']))
				elif element['type'] == "select":
					self.elements.append(self.Select(name=element['name'], variants=element['variants']))
				elif element['type'] == "input":
					self.elements.append(self.Input(name=element['name']))
				elif element['type'] == "button":
					self.elements.append(self.Button(name=element['name'], callback=element['callback']))
			self.elements.append(self.Button(name="exit", callback=self.exit))


		def __str__(self):
			screen_str = ' ' + self.description + "\n\n" + \
						 "\n".join("%s%s" % ('→ ' if ind == self.current else '  ', x) for ind, x in enumerate(self.elements))
			return screen_str

		class Element:
			def __init__(self, name="element"):
				self.name = name

		class Checkbox(Element):
			def __init__(self, name):
				super().__init__(name)

				self.value = False

			def __str__(self):
				return "[%s] %s" % ('x' if self.value else ' ', self.name)

		class Select(Element):
			def __init__(self, name, variants):
				super().__init__(name)

				self.value = None 
				self.variants = ["close"] + [x for x in variants]
				self.show_variants = False

			def __str__(self):
				if self.show_variants:
					string = ""
					str_ = " "*2+" "*len(self.name) + "  "
					string = "%s > %s\n"%(self.name, self.variants[self.value]) + str_ + ("\n" + str_).join("%s%s"%('→' if ind == self.value else ' ', x) for ind, x in enumerate(self.variants))
					return string
				elif not self.value:
					return "%s > %s" % (self.name, "----")
				else:
					return "%s > %s" % (self.name, self.variants[self.value])

		class Input(Element):
			def __init__(self, name):
				super().__init__(name)

				self.value = ""

			def __str__(self):
				return "%s : %s" % (self.name, self.value)

		class Button(Element):
			def __init__(self, name, callback):
				super().__init__(name)
				self.callback = callback

			def call(self):
				self.callback(self)

			def __str__(self):
				return "[ %s ]" % (self.name)

def main():
	gui = GUI()

	# необходимо упростить всё так, чтобы экран можно было реализовать в одну строку
	# с помощью dict

	options = [
		{
			"name": "Use uppercase",
			"type": "check",
			"value": False,
		},
		{
			"name": "Select what to say",
			"type": "select",
			"variants": ["first option", "second option", "some option"],
			"value": 0,
		},
		{
			"name": "What is the name?",
			"type": "input",
			"value": "",
		},
		{
			"name": "Say it",
			"type": "button",
			"callback": lambda obj: print("hello", obj)
		}
	]

	gui.new_screen(name="test", description="just select somethink", elements=options)
	#gui.set_callbask(screen_name="test", option_ind=0, callback=print_callback)

	gui.run()

if __name__ == 	"__main__":
	main()