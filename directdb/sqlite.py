# LICENSE
# -----------------------------------------------------------------------
# Copyright (c) CannonBall Chris,  2024
# directdb is distributed under the terms of the GNU Affero General Public License (AGPL).
# You can find a copy of the license in the LICENSE file included with this distribution.
# The AGPL is a copyleft license that ensures the freedom to use, modify, and distribute the library's code, even in the case of web-based services.
# By using directdb, you agree to comply with the terms and conditions of the AGPL.


import aiosqlite

from .exceptions import *


class SQLite:
	
	def __init__(self, database_file:str):
		"""A class that handles all sqlite database operations efficiently.

		Parameters
		----------
		database_file : str
			The name of the database file.
		"""
		self.database = database_file
		self.conn = None

	async def connect(self):
		"""Connects to the database.
		
		Returns
		-------
		connection obj
			The connection object of the database.
		"""
		self.conn = await aiosqlite.connect(self.database)
		return self.conn
	
	async def create_tables(self, table_list:list) -> None:
		"""Creates a table in the database.

		Parameters
		----------
		table_list : list
			The list of tables to be created
			Format: [{'table_name': {'column_name':'datatype'}}]
		"""

		try:
			for table in table_list:
				for name, columns in table.items():
					query = f"CREATE TABLE IF NOT EXISTS {name} ("
					for column, datatype in columns.items():
						query += f"{column} {datatype},"
					query = query[:-1] + ")"
					async with self.conn.cursor() as cur:
						await cur.execute(query)

		except Exception as e:
			raise DatabaseTableException(e)
		

	async def drop_table(self, table:str) -> None:
		"""Drops a table from the database.

		Parameters
		----------
		table : str
			The name of the table to drop.
		"""

		try:
			query = f"DROP TABLE IF EXISTS {table}"
			async with self.conn.cursor() as cur:
				await cur.execute(query)
		
		except Exception as e:
			raise DatabaseTableException(e)
		

	async def insert(self, table:str, **data) -> bool:
		"""Inserts data to the tables in the database.

		Parameters
		----------
		table : str
			The name of the table to insert data into.
		data : dict
			The data to insert into the table in format {'column name':data}.

		Returns
		-------
		None
			Whether the data was inserted successfully or not.
		"""

		try:
			query = f"INSERT INTO {table} ("
			for column, value in data.items():
				query += f"{column},"
			query = query[:-1] + ") VALUES ("
			#Question marks for the values
			for i in range(len(data)):
				query += "?,"
			query = query[:-1] + ")"
			async with self.conn.cursor() as cur:
				await cur.execute(query, tuple(data.values()))
				await self.conn.commit()
				return True

		except Exception as e:
			raise DatabaseInsertionException(e)
		
	async def fetch(self, table:str, *, data_filter:dict = None, **sorting) -> list:
		""" Fetches data from the database.
		
		Parameters
		----------
		table: str
			The table to fetch data from.
		data_filter: dict [Optional]
			The data_filter to use in format {'column name':data}.
		sorting: dict [Optional]
			The sorting to use in format {'sort_by':'column name', 'sort':'ASC/DESC'}.

		Returns
		-------
		list
			A list of data in tuple format fetched from the database.

		"""

		try:
			query = f"SELECT * FROM {table}"
			if data_filter:
				query += " WHERE "
				for column, value in data_filter.items():
					query += f"{column} = ? AND "
				query = query[:-5]

			if sorting:
				sort_by = sorting.get('sort_by', None)
				sort = sorting.get('sort', None)
				if sort_by and sort:
					query += f" ORDER BY {sort_by} {sort}"

			async with self.conn.cursor() as cur:
				if data_filter:
					await cur.execute(query, tuple(data_filter.values()))
				else:
					await cur.execute(query)
				return await cur.fetchall()
		
		except Exception as e:
			raise DatabaseFetchException(e)
		
	async def fetch_element(self, table:str, element:str, column:str) -> list:
		"""Fetches a single element from the database in given column.

		Parameters
		----------
		table : str
			The table to fetch data from.
		element : str
			The element to fetch.
		column : str
			The column to fetch the element from.

		Returns
		-------
		list
			A list of data in tuple format fetched from the database.
		"""
		try:
			query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
			async with self.conn.cursor() as cur:
				await cur.execute(query, (f'%{element}%',))
				return await cur.fetchall()
		except Exception as e:
			raise DatabaseFetchException(e)
		
	async def update(self, table:str, data_filter:dict = None, **data) -> bool:
		"""Updates data in the database.

		Parameters
		----------
		table : str
			The table to update data in.
		data : dict
			The data to update in format {'column name':data}.
		data_filter : dict [Optional]
			The data_filter to use in format {'column name':data}.

		Returns
		-------
		bool
			Whether the data was updated successfully or not.
		"""

		try:
			query = f"UPDATE {table} SET "
			for column, value in data.items():
				query += f"{column} = ?,"
			query = query[:-1]
			query += " WHERE "
			for column, value in data_filter.items():
				query += f"{column} = ? AND "
			query = query[:-5]
			async with self.conn.cursor() as cur:
				await cur.execute(query, tuple(data.values()) + tuple(data_filter.values()))
				await self.conn.commit()
				return True
		
		except Exception as e:
			raise DatabaseUpdateException(e)
		
	async def delete(self, table:str, **data_filter) -> bool:
		"""Deletes data from the database.

		Parameters
		----------
		table : str
			The table to delete data from.
		data_filter : dict
			The data_filter to use in format {'column name':data}.

		Returns
		-------
		bool
			Whether the data was deleted successfully or not.
		"""

		try:
			query = f"DELETE FROM {table} WHERE "
			for column, value in data_filter.items():
				query += f"{column} = ? AND "
			query = query[:-5]
			async with self.conn.cursor() as cur:
				await cur.execute(query, tuple(data_filter.values()))
				await self.conn.commit()
				return True
		
		except Exception as e:
			raise DatabaseDeleteException(e)
		

	async def close(self):
		"""Close the connection"""
		if self.conn:
			await self.conn.close()