import appdaemon.plugins.hass.hassapi as hass
import time

class TradfriRemote(hass.Hass):

	def initialize(self):
		self.dictionary = self.args["groups"]
		self.count = len(self.dictionary)
		self.listen_state(self.button_pressed, self.args["remote"])
		self.last_action_was = False
		self.current_index = 0
		self.current_scene_index = 0
		self.reset_after = 0
		if "reset_after" in self.args:
			self.reset_after = self.args["reset_after"]
		self.right_arrow_mode = self.args["right_arrow_mode"]
		self.log("notherealmarco's TradfriRemote initialized!")
		self.fast_click = 0
		self.handle = None
		self.dimmer_speed = 0.2
		self.dimmer_step = 30
		self.zigbee_dimmer_speed = 80
		if "dimmer_speed" in self.args:
			self.dimmer_speed = self.args["dimmer_speed"]
		if "dimmer_step" in self.args:
			self.dimmer_step = self.args["dimmer_step"]
		if "zigbee_dimmer_speed" in self.args:
			self.zigbee_dimmer_speed = self.args["zigbee_dimmer_speed"]

	def button_pressed(self, entity, attribute, old, new, kwargs):
		if (new == "toggle" or new == "on") and old == "":
			if self.fast_click == 1:
				self.bright_up()
				return
			elif self.fast_click == 2:
				self.bright_down()
				return
			devices = self.dictionary[list(self.dictionary.keys())[self.current_index]]
			self.last_action_was = False
			for d in devices:
				if self.get_state(d) == "on":
					self.last_action_was = True
			for d in devices:
				if self.last_action_was:
					self.turn_off(d)
				else:
					self.turn_on(d)
		if (self.reset_after != 0 and self.handle is None):
			self.handle = self.run_in(self.reset_auto, self.reset_after)
		elif self.handle is not None:
			self.cancel_timer(self.handle)
			self.handle = self.run_in(self.reset_auto, self.reset_after)

		if new == "toggle_hold" and old == "":
			if self.last_action_was:
				self.turn_off(self.args["hold_group"])
			else:
				self.turn_on(self.args["hold_group"])

		if (new == "arrow_left_click" or new == "off") and old == "":
			self.current_index += 1
			if (self.current_index > self.count - 1):
				self.current_index = 0
			devices = self.dictionary[list(self.dictionary.keys())[self.current_index]]
			back_on = []
			back_off = []
			for d in devices:
				if self.get_state(d) == "on":
					self.turn_off(d)
					back_on.append(d)
				if self.get_state(d) == "off":
					self.turn_on(d)
					back_off.append(d)
			if len(back_on) > 0: self.run_in(self.turn_back_on, 1, devices = back_on)
			if len(back_off) > 0: self.run_in(self.turn_back_off, 1, devices = back_off)
			if (self.reset_after != 0 and self.handle is None):
				self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				self.cancel_timer(self.handle)
				self.handle = self.run_in(self.reset_auto, self.reset_after)

		if (new == "arrow_right_click" or new == "brightness_down") and old == "":
			back_off = []
			for x in range(self.count):
				devices = self.dictionary[list(self.dictionary.keys())[x]]
				for d in devices:
					if self.get_state(d) == "off":
						back_off.append(d)
			if self.right_arrow_mode == "input_select":
				self.call_service("input_select/select_next", entity_id = self.args["input_select"])
			else:
				scenes = self.args["scenes"]
				scenes_len = len(scenes)
				self.current_scene_index += 1
				if (self.current_scene_index > scenes_len - 1):
					self.current_scene_index = 0
				self.call_service("scene/turn_on", entity_id = scenes[self.current_scene_index])
			if len(back_off) > 0: self.run_in(self.turn_back_off, 1, devices = back_off)
			if (self.reset_after != 0 and self.handle is None):
				self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				self.cancel_timer(self.handle)
				self.handle = self.run_in(self.reset_auto, self.reset_after)
		
		if (new == "arrow_right_hold") and old == "":
			entity = self.args["right_hold_device"]
			if isinstance(entity, int):
				devices = self.dictionary[list(self.dictionary.keys())[entity]]
				self.current_index = entity
				self.last_action_was = False
				for d in devices:
					if self.get_state(d) == "on":
						self.last_action_was = True
				for d in devices:
					if self.last_action_was:
						self.turn_off(d)
					else:
						self.turn_on(d)
			else:
				self.toggle(entity)
			if (self.reset_after != 0 and self.handle is None):
				self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				self.cancel_timer(self.handle)
				self.handle = self.run_in(self.reset_auto, self.reset_after)

		if (new == "arrow_left_hold") and old == "":
			entity = self.args["left_hold_device"]
			if isinstance(entity, int):
				devices = self.dictionary[list(self.dictionary.keys())[entity]]
				self.current_index = entity
				self.last_action_was = False
				for d in devices:
					if self.get_state(d) == "on":
						self.last_action_was = True
				for d in devices:
					if self.last_action_was:
						self.turn_off(d)
					else:
						self.turn_on(d)
			else:
				self.toggle(entity)
			if (self.reset_after != 0 and self.handle is None):
				self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				self.cancel_timer(self.handle)
				self.handle = self.run_in(self.reset_auto, self.reset_after)

		if new == "brightness_up_click" and old == "":
			self.fast_click = 1
			self.run_in(self.fast_callback, 3)
			devices = self.dictionary[list(self.dictionary.keys())[self.current_index]]
			for d in devices:
				b = self.get_state(entity_id = d, attribute = "brightness")
				n = b + 50
				if n > 255:
					n = 255
				self.turn_on(d, brightness = n)
			if (self.reset_after != 0 and self.handle is None):
				self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				self.cancel_timer(self.handle)
				self.handle = self.run_in(self.reset_auto, self.reset_after)

		if (new == "brightness_down_click" or new == "brightness_up") and old == "":
			self.fast_click = 2
			self.run_in(self.fast_callback, 3)
			devices = self.dictionary[list(self.dictionary.keys())[self.current_index]]
			for d in devices:
				b = self.get_state(entity_id = d, attribute = "brightness")
				n = b - 50
				if n < 0:
					n = 1
				self.turn_on(d, brightness = n)
			if (self.reset_after != 0 and self.handle is None):
				self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				self.cancel_timer(self.handle)
				self.handle = self.run_in(self.reset_auto, self.reset_after)
		
		if new == "brightness_up_hold" and old == "":
			self.brightness_direction = True
			self.brightness_changing = True
			zigbee_key = list(self.dictionary.keys())[self.current_index]
			if ("zigbee_names" in self.args) and (zigbee_key in self.args['zigbee_names']):
				devices = self.args['zigbee_names'][zigbee_key]
				self.call_service("python_script/zigbee_dimmer", lights = devices, direction = "up", speed = self.zigbee_dimmer_speed)
			else: self.fire_event("REAL_DIMMER", entities = self.dictionary[list(self.dictionary.keys())[self.current_index]], speed = self.dimmer_speed, step = self.dimmer_step, direction = "up")

		if new == "brightness_down_hold" and old == "":
			self.brightness_direction = False
			self.brightness_changing = True
			zigbee_key = list(self.dictionary.keys())[self.current_index]
			self.log(self.args['zigbee_names'])
			self.log(zigbee_key)
			if ("zigbee_names" in self.args) and (zigbee_key in self.args['zigbee_names']):
				self.log('ya')
				devices = self.args['zigbee_names'][zigbee_key]
				self.call_service("python_script/zigbee_dimmer", lights = devices, direction = "down", speed = self.zigbee_dimmer_speed)
			else: self.fire_event("REAL_DIMMER", entities = self.dictionary[list(self.dictionary.keys())[self.current_index]], speed = self.dimmer_speed, step = self.dimmer_step, direction = "down")

		if (new == "brightness_stop" or new == "brightness_down_release" or new == "brightness_up_release") and old == "":
			if (self.reset_after != 0 and self.handle is None):
				zigbee_key = list(self.dictionary.keys())[self.current_index]
				if ("zigbee_names" in self.args) and (zigbee_key in self.args['zigbee_names']):
					devices = self.args['zigbee_names'][zigbee_key]
					self.call_service("python_script/zigbee_dimmer", lights = devices, direction = "stop")
				else:
					self.fire_event("REAL_DIMMER", entities = self.dictionary[list(self.dictionary.keys())[self.current_index]], speed = self.dimmer_speed, step = self.dimmer_step, direction = "stop")
					self.handle = self.run_in(self.reset_auto, self.reset_after)
			elif self.handle is not None:
				zigbee_key = list(self.dictionary.keys())[self.current_index]
				if ("zigbee_names" in self.args) and (zigbee_key in self.args['zigbee_names']):
					devices = self.args['zigbee_names'][zigbee_key]
					self.call_service("python_script/zigbee_dimmer", lights = devices, direction = "stop", speed = self.dimmer_speed)
				else:
					self.fire_event("REAL_DIMMER", entities = self.dictionary[list(self.dictionary.keys())[self.current_index]], speed = self.dimmer_speed, step = self.dimmer_step, direction = "stop")
					self.cancel_timer(self.handle)
					self.handle = self.run_in(self.reset_auto, self.reset_after)

	def bright_up(self):
		devices = self.dictionary[list(self.dictionary.keys())[self.current_index]]
		for d in devices:
			b = self.get_state(entity_id = d, attribute = "brightness")
			self.turn_on(d, brightness = 255)

	def bright_down(self):
		devices = self.dictionary[list(self.dictionary.keys())[self.current_index]]
		for d in devices:
			b = self.get_state(entity_id = d, attribute = "brightness")
			self.turn_on(d, brightness = 10)

	def fast_callback(self, b):
		self.fast_click = 0

	def turn_back_on(self, devices):
		devices_r = devices["devices"]
		for d in devices_r:
			self.turn_on(d)

	def turn_back_off(self, devices):
		devices_r = devices["devices"]
		for d in devices_r:
			self.turn_off(d)

	def reset_auto(self, b):
		self.current_index = 0