import praw
import re
from collections import deque 

USERNAME  = "hypebot"
PASSWORD  = "PASSWORD"
USERAGENT = "A bot that looks to see how hype a thread is. hypebot v1"

hypePattern = re.compile("[Hh][Yy][Pp][Ee]")

class Thread:
	def __init__(self, thread):
		self.threadId = 
		self.timeCreated = 0

class HypeThread(Thread):
	def __init__(self, thread):
		super.__init__(thread)
		self.firstHype = ""
		self.totalHype = 0
		self.totalComments = 0
		self.lastHype = 0

	def countHype(self, reddit):

reddit = praw.Reddit(USERAGENT)
reddit.login(USERNAME,PASSWORD) # necessary if your bot will talk to people



def main():
	pass

if __name__ == '__main__':
	main()