from prelimZSim import controlled_run

class Wrapper(object):

	def __init__(self):
		# Start the game
		controlled_run(self, 0)

	def control(self, values):
		dist,dir = values['avg_z']

	def gameover(self, score):
		# The game has completed. Do cleanup stuff here