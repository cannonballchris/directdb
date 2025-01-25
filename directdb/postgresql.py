# LICENSE
# -----------------------------------------------------------------------
# Copyright (c) CannonBall Chris,  2024
# directdb is distributed under the terms of the GNU Affero General Public License (AGPL).
# You can find a copy of the license in the LICENSE file included with this distribution.
# The AGPL is a copyleft license that ensures the freedom to use, modify, and distribute the library's code, even in the case of web-based services.
# By using directdb, you agree to comply with the terms and conditions of the AGPL.

import asyncio
import asyncpg

from .exceptions import *

class Postgresql:

	""" A class to handle all database related tasks efficiently.
	
	Parameters
	----------
	host: str
		The host of the database.
	user: str
		The user of the database.
	password: str
		The password of the database.
	database: str
		The database name.
	port: int
		The port of the database.

	"""
	pool = None

	def __init__(self, host, user, password, database, port):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.port = port

	async def connect(self) -> asyncpg.Pool:
		""" Connects to the database. 
		
		Returns
		-------
		Class
			The custom database handler class.

		"""
		self.pool = await asyncpg.create_pool(
			host=self.host, user=self.user, password=self.password, database=self.database, port=self.port
		)
		return self.pool
	

	async def create_table(self, tables:list) -> None:
		""" Creates table(s) in the database.
		
		Parameters
		----------
		tables: list
			A list in format of [{'table_name': {'column_name:'datatype'}}]
		"""
		for table in tables:
			for name, columns in table.items():
				try:
					columns = ', '.join(['{} {}'.format(column, datatype) for column, datatype in columns.items()])
					query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(name, columns)
					await asyncio.sleep(0.2)
					await self.pool.execute(query)

				except Exception as e:
					raise DatabaseTableException(e)

	async def drop_table(self, table:str) -> None:
		""" Drops a table from the database.
		
		Parameters
		----------
		table: str
			The table to drop.

		"""
		try:
			query = 'DROP TABLE IF EXISTS {}'.format(table)
			await self.pool.execute(query)
		except Exception as e:
			raise DatabaseTableException(e)

	async def insert(self, table: str, **data) -> None:

		""" Inserts data into the database.
		
		Parameters
		----------
		table: str
			The table to insert data into.
		data: **kwargs dict
			The data to insert into the table in format column_name = data.

		"""
		try:
			columns = ', '.join(data.keys())
			values = ', '.join(['${}'.format(i + 1) for i in range(len(data))])
			query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, values)
			await self.pool.execute(query, *data.values())
		except Exception as e:
			raise DatabaseInsertionException(e)
		

	async def fetch(self, table:str, *, query_string:str = None, data_filter:dict = None, **sorting, ) -> list:
		""" Fetches data from the database.
		
		Parameters
		----------
		table: str
			The table to fetch data from.
		data_filter: dict [Optional]
			The data_filter to use in format {'column name':data}.
		sort_by : str [Optional]
			The column to sort the data by.The data which will be sorted will be always in descending order.
		sort : str [Optional]
			The order to sort the data by. Can be either 'ASC' or 'DESC'.

		Returns
		-------
		list
			A list of data fetched from the database.

		"""
		try:
			if query:
				return await self.pool.fetch(query_string)
			else:
				if not data_filter:
					query = 'SELECT * FROM {}'.format(table)
					if sorting:
						sort_by = sorting.get('sort_by', None)
						sort = sorting.get('sort', None)
						if sort_by and sort:
							query += ' ORDER BY {} {}'.format(sort_by, sort)
					return await self.pool.fetch(query)
				else:
					data_filters = ' AND '.join(['{} = ${}'.format(column, i + 1) for i, column in enumerate(data_filter)])
					query = 'SELECT * FROM {} WHERE {}'.format(table, data_filters)
					if sorting:
						sort_by = sorting.get('sort_by')
						sort = sorting.get('sort')
						if sort_by and sort:
							query += ' ORDER BY {} {}'.format(sort_by, sort)
					return await self.pool.fetch(query, *data_filter.values())

		except Exception as e:
			raise DatabaseFetchException(e)
		
	async def update(self, table:str,data_filter:dict,  **data ) -> None:
		""" Updates data in the database.
		
		Parameters
		----------
		table: str
			The table to update data in.
		data: dict
			The data to update in format {'column name':data}.
		data_filter: kwags dict
			The data_filter to use in format column_name = data.

		"""
		try:
			#Since $1, $2 etc are used in update data, we need to continue from there for data_filter data to avoid errors.
			columns = ', '.join(['{} = ${}'.format(column, i + 1) for i, column in enumerate(data)])
			data_filters = ' AND '.join(['{} = ${}'.format(column, i + len(data) + 1) for i, column in enumerate(data_filter)])
			query = 'UPDATE {} SET {} WHERE {}'.format(table, columns, data_filters)
			await self.pool.execute(query, *data.values(), *data_filter.values())
		except Exception as e:
			raise DatabaseUpdateException(e)
		
	async def delete(self, table:str, **data_filter) -> None:
		""" Deletes data from the database.
		
		Parameters
		----------
		table: str
			The table to delete data from.
		data_filter: dict
			The data_filter to use in format `column_name = data`.

		"""
		try:
			data_filters = ' AND '.join(['{} = ${}'.format(column, i + 1) for i, column in enumerate(data_filter)])
			query = 'DELETE FROM {} WHERE {}'.format(table, data_filters)
			await self.pool.execute(query, *data_filter.values())
		except Exception as e:
			raise DatabaseDeleteException(e)