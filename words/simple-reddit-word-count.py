import praw
import re
from collections import deque 
 
USERNAME  = "USERNAME"
PASSWORD  = "PASSWORD"
USERAGENT = "simple words occurance count bot v.1 by mrpenguinman"
RESULTS_FILE_PATH = "results.txt"

reddit = praw.Reddit(USERAGENT)
reddit.login(USERNAME,PASSWORD) # necessary if your bot will talk to people
 
cache = deque(maxlen=200) # To make sure we don't duplicate effort
wordPattern = re.compile("[\w']+")

#Data Structure to store all of the words and the number of their appearances.
class TrieNode(object):
	def __init__(self, parent, value):
		self.parent = parent
		self.endNode = False
		self.value = value
		self.children = []
		self.count = 0

	def addWord(self, word):
		currentWord = word
		if self.value != "":
			if len(word) > 1:
				currentWord = word[1:]
			else:
				currentWord = ""

		if currentWord == "":
			self.incrementCount()
			self.endNode = True
		else:
			firstLetter = currentWord[0]
			nextNode = None
			for node in self.children: 
				if node.value == currentWord[0]:
					nextNode = node

			if nextNode == None:
				nextNode = TrieNode(self, currentWord[0])
				self.children.append(nextNode)
			nextNode.addWord(currentWord)

	def findEndNodes(self, endNodesList):
		if self.endNode == True:
			endNodesList.append(self)
		for node in self.children:
			node.findEndNodes(endNodesList)

	def incrementCount(self):
		self.count += 1

	def findWord(self):
		word = self.value;
		parent = self.parent
		while parent != None : 
			word = parent.value + word
			parent = parent.parent
		return word
	
def saveToFile(rootTrieNode, filePath):
	#Find the list of words and occurances into the trie 
	endNodes = []
	rootTrieNode.findEndNodes(endNodes)
	countList = sorted(endNodes, key=lambda node: node.count, reverse=True)
	#Save the list to a file so another program can parse it
	resultsFile = open(filePath, 'w')
	for node in countList :
		word = node.findWord()
		resultsFile.write("{}, {}\n".format(word, node.count))
	resultsFile.close()

#The actual bot 
theTrie = TrieNode(None, "")
running = True;
commentsCount = 0
whileCount = 0
while whileCount < 100:
	#Go through all of the comments and add them into the trie data structure
	comments =  reddit.get_comments('all', limit=None)
	for comment in comments:
		if comment.id in cache:
			break
		cache.append(comment.id)
		commentsCount += 1
		words = set(re.findall(wordPattern, comment.body))
		for word in words:
			if len(word) < 100:
				theTrie.addWord(word)

	#Save to the results to a file if we have read in 10,000 comments
	if commentsCount > 10000:
		saveToFile(theTrie, RESULTS_FILE_PATH)
		commentsCount = 0
	whileCount += 1
saveToFile(theTrie, RESULTS_FILE_PATH) #do a final save