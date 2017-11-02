import os
import sys
import datetime
(DEBUG, INFO, WARNING, ERROR, FATAL) = (0, 1, 2, 3, 4)

def strToLevel(elvl):
	if elvl == "DEBUG":
		return DEBUG
	if elvl == "INFO":
		return INFO
	if elvl == "WARNING":
		return WARNING
	if elvl == "ERROR":
		return ERROR
	if elvl == "FATAL":
		return FATAL
	else:
		return None

def levelToStr(lvl):
	if lvl == DEBUG:
		return "DEBUG"
	if lvl == INFO:
		return "INFO"
	if lvl == WARNING:
		return "WARNING"
	if lvl == ERROR:
		return "ERROR"
	if lvl == FATAL:
		return "FATAL"
	return None


def levelToShortStr(lvl):
	if lvl == DEBUG:
		return "DBUG"
	if lvl == INFO:
		return "INFO"
	if lvl == WARNING:
		return "WARN"
	if lvl == ERROR:
		return "ERROR"
	if lvl == FATAL:
		return "FATAL"
	return None

class Logger:
	def __init__(self, modulename, level, crashlevel):
		self.__modulename = modulename
		self.__level = level
		self.__crashlevel = crashlevel

	def debug(self, mainstr, *args, **kwargs):
		self.log(DEBUG, mainstr, *args, **kwargs)
	def info(self, mainstr, *args, **kwargs):
		self.log(INFO, mainstr, *args, **kwargs)
	def warning(self, mainstr, *args, **kwargs):
		self.log(WARNING, mainstr, *args, **kwargs)
	def error(self, mainstr, *args, **kwargs):
		self.log(ERROR, mainstr, *args, **kwargs)
	def fatal(self, mainstr, *args, **kwargs):
		self.log(FATAL, mainstr, *args, **kwargs)

	def log(self, level, mainstr, *args, **kwargs):
		if level >= self.__level:
			sys.stdout.write(self.formatmsg(level,str(mainstr).format(*args, **kwargs)))

		if level >= self.__crashlevel:
			exit(1)

	def setLevel(self, level):
		self.__level = level

	def formatmsg(self, level, mainstr):
		class bcolors:
			HEADER = '\033[95m'
			OKBLUE = '\033[94m'
			OKGREEN = '\033[92m'
			WARNING = '\033[93m'
			FAIL = '\033[91m'
			ENDC = '\033[0m'
	

		col = bcolors.OKGREEN
		if level >= WARNING:
			col = bcolors.WARNING
		if level >= ERROR:
			col = bcolors.FAIL

		return "{startcol}[{now:%H:%M:%S.%f} {module} {lvl}] {mainstr}{endcol}\n".format(
				lvl=levelToShortStr(level),
				module=self.__modulename,
				now=datetime.datetime.today(),
				mainstr=mainstr,
				startcol=col,
				endcol=bcolors.ENDC);

defaultLogLevel = INFO
defaultCrashLevel = FATAL

def getAbstractLogLevel(env, default):
	elvl = os.environ[env] if env in os.environ else ''

	lvl = strToLevel(elvl)
	if lvl:
		return lvl
	else:
		return default

def getLogLevel():
	return getAbstractLogLevel('NAIVE_LOGLEVEL', defaultLogLevel)

def getCrashLevel():
	return getAbstractLogLevel('NAIVE_CRASHLEVEL', defaultCrashLevel)

def getLogger(modulename):
	return Logger(modulename, getLogLevel(), getCrashLevel())

if __name__ == "__main__":
	l = getLogger('testmodule')
	l.info("bla");
	l.info("test nummer {}{}", 2, " is good")
	l.info("test {hier} is ook ok", hier=3, daar=4)
	l.info("should not see this")


	l2 = getLogger('testmodule.m2')
	l2.info("More info")
	l2.info("and even more")
