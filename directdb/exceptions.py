# LICENSE
# -----------------------------------------------------------------------
# directdb is distributed under the terms of the GNU Affero General Public License (AGPL).
# You can find a copy of the license in the LICENSE file included with this distribution.
# The AGPL is a copyleft license that ensures the freedom to use, modify, and distribute the library's code, even in the case of web-based services.
# By using directdb, you agree to comply with the terms and conditions of the AGPL.

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

