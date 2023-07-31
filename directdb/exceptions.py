import datetime

class DatabaseInsertionException(Exception):
	"""Class for exceptions when insertion into database fails.
	
	Parameters
	----------
	message: str
		The error message.
	"""

	def __init__(self, message):
		with open("./log.txt", "a") as f:
			f.write(f"- ERROR {datetime.datetime.now()} | {self.__class__.__name__} | {message} \n")
		super().__init__(message)

class DatabaseTableException(Exception):
	"""Class for exceptions when table creation fails.
	
	Parameters
	----------
	message: str
		The error message.
	"""

	def __init__(self, message):
		with open("./log.txt", "a") as f:
			f.write(f"- ERROR {datetime.datetime.now()} | {self.__class__.__name__} | {message} \n")
		super().__init__(message)

class DatabaseFetchException(Exception):
	"""Class for exceptions when table fetching fails.
	
	Parameters
	----------
	message: str
		The error message.
	"""

	def __init__(self, message):
		with open("./log.txt", "a") as f:
			f.write(f"- ERROR {datetime.datetime.now()} | {self.__class__.__name__} | {message} \n")
		super().__init__(message)

class DatabaseUpdateException(Exception):
	"""Class for exceptions when table fetching fails.
	
	Parameters
	----------
	message: str
		The error message.
	"""

	def __init__(self, message):
		with open("./log.txt", "a") as f:
			f.write(f"- ERROR {datetime.datetime.now()} | {self.__class__.__name__} | {message} \n")
		super().__init__(message)

class DatabaseDeleteException(Exception):
	"""Class for exceptions when table fetching fails.
	
	Parameters
	----------
	message: str
		The error message.
	"""

	def __init__(self, message):
		self.message = message
		with open("./log.txt", "a") as f:
			f.write(f"- ERROR {datetime.datetime.now()} | {self.__class__.__name__} | {message} \n")
		super().__init__(message)

