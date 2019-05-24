#!/usr/bin/env python
import time
import atexit
from threading import Thread
import gunicorn.app.base
from gunicorn.six import iteritems

import app
import control

class StandaloneApplication(gunicorn.app.base.BaseApplication):
	def __init__(self, app, options=None):
		self.options = options or {}
		self.application = app
		super(StandaloneApplication, self).__init__()

	def load_config(self):
		config = dict([(key, value) for key, value in iteritems(self.options)
					   if key in self.cfg.settings and value is not None])
		for key, value in iteritems(config):
			self.cfg.set(key.lower(), value)

	def load(self):
		return self.application

def gunicorn_exit(arg):
	control.exit_loop = True


if __name__ == '__main__':

	options = {
		'on_exit': gunicorn_exit,
	}

	control_thread = Thread(target=control.MainLoop)
	control_thread.start()

	StandaloneApplication(app.app, options).run()
