# coding=utf-8
from __future__ import absolute_import
import sys


import octoprint.plugin
import flask
import threading
from hx711 import HX711
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)

class Filament_scalePlugin(octoprint.plugin.SettingsPlugin,
						   octoprint.plugin.AssetPlugin,
						   octoprint.plugin.TemplatePlugin,
						   octoprint.plugin.StartupPlugin):


	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=True)
		]
	
	def get_settings_defaults(self):
		return dict(
			tare = 8430152,
			reference_unit=-411,
			spool_weight=200,
			clockpin=21,
			datapin=20,
			lastknownweight=0
			
			# put your plugin's default settings here
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/filament_scale.js"],
			css=["css/filament_scale.css"],
			less=["less/filament_scale.less"]
		)

	
	def on_startup(self, host, port):
		try:
			self.hx = HX711(
        	    dout_pin=20,
        	    pd_sck_pin=21,
        	    channel='A',
        	    gain=128
        	)
			self.hx.reset()
			self.t = octoprint.util.RepeatedTimer(3.0, self.check_weight)
			self.t.start()
		finally:
			logging.debug("Scale Loaded!")
		
	def check_weight(self):
		self.hx.power_up()
		v = self.hx.get_raw_data()
		self._plugin_manager.send_plugin_message(self._identifier, v) 
		self.hx.power_down()
		
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			filament_scale=dict(
				displayName="Filament Scale Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="eliteSchwein",
				repo="OctoPrint-Filament-scale",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/eliteSchwein/Octoprint-Filament-Scale/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Filament Scale"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_version__ = "0.0.1b9"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Filament_scalePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin5.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

