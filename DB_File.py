import sqlite3
from sqlite3 import Error

'''
	We are creating 3 tables 
	file_paths(to maintain (file name,path) (file extension,path))
	word_paths(to maintain (words,path))
	file_time_stamps(to maintian(file name,path,timestamp))
	We are indexing on the "file name" in file_paths and words in word_paths
'''

# Establishing the connection with sqlite DB
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

# Creating the tables 
def create_table(conn, create_table_sql,index):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        if index != None:
        	c.execute(index)
    except Error as e:
        print(e)

def insert_into_file_paths_table(conn, values):

	sql = ''' INSERT INTO file_paths(f_name,f_path)
              VALUES(?,?) '''
	try:
		cur = conn.cursor()
		cur.execute(sql, values)
		conn.commit()
		return cur.lastrowid
	except Error as e:
		return
	

def insert_into_word_paths_table(conn, values):
	sql = ''' INSERT INTO word_paths(words,f_path)
              VALUES(?,?) '''
	try:
		cur = conn.cursor()
		cur.execute(sql, values)
		conn.commit()
		return cur.lastrowid
	except Error as e:
		return

def insert_values_into_file_time_stamps_table (conn, values):
	sql = ''' INSERT INTO file_time_stamps (f_name,f_path,f_time)
              VALUES(?,?,?) '''
	try:
		cur = conn.cursor()
		cur.execute(sql, values)
		conn.commit()
		return cur.lastrowid
	except Error as e:
		return

def file_retrival_exec(conn,value,sql):
	
	try:
		cur = conn.cursor()
		value = '%'+value+'%'
		cur.execute(sql, (value,))
		rows = cur.fetchall()
		return rows
	except Error as e:
		return []

def file_retrival_timestamp_exec(conn,value,sql):
	try:
		cur = conn.cursor()
		value = '%'+value+'%'
		cur.execute(sql, (value,))
		rows = cur.fetchall()
		return rows
	except Error as e:
		return []

# Creates DB
def create_db():
	database = "desktopsearch.db"
	file_paths_table = """ CREATE TABLE IF NOT EXISTS file_paths (
                                        f_name text NOT NULL,
                                        f_path text,
                   						PRIMARY KEY(f_name,f_path)
                                    ); """

	words_path_table = """ CREATE TABLE IF NOT EXISTS word_paths (
                                    words text NOT NULL,
                                    f_path text,
                                    PRIMARY KEY(words,f_path)
                                );"""
	file_time_stamps_table = """ CREATE TABLE IF NOT EXISTS file_time_stamps (
										f_name text NOT NULL,
   										f_path text,
   										f_time real,
   										PRIMARY KEY(f_name,f_path)
                                	); """
    # Creating indices on the file name and words. Internally indices will create b-trees.
	file_paths_table_index = """ CREATE INDEX file_paths_index ON file_paths(f_name) """
	words_path_table_index = """ CREATE INDEX word_paths_index ON word_paths(words) """


	conn = create_connection(database)

	if conn is not None:
		create_table(conn, file_paths_table, file_paths_table_index)

		create_table(conn, words_path_table,words_path_table_index)

		create_table(conn, file_time_stamps_table,None)

	else:

			print("Error! cannot create the database connection.")



def insert_values_into_files_path(values):
	database = "desktopsearch.db"

	conn = create_connection(database)

	if conn is not None:
		insert_into_file_paths_table(conn, values)
	else:
		print("Error! cannot create the database connection.")

def insert_values_into_word_path(values):
	database = "desktopsearch.db"

	conn = create_connection(database)

	if conn is not None:
		insert_into_word_paths_table(conn, values)
	else:
		print("Error! cannot create the database connection.")

def insert_values_into_file_time_stamps(values):
	database = "desktopsearch.db"

	conn = create_connection(database)

	if conn is not None:
		insert_values_into_file_time_stamps_table(conn, values)
	else:
		print("Error! cannot create the database connection.")

def file_retrival(values):

	database = "desktopsearch.db"

	conn = create_connection(database)

	if conn is not None:
		sql = ''' SELECT f_path from file_paths where f_name LIKE ? '''
		rows = file_retrival_exec(conn, values,sql)
		return rows
	else:
		print("Error! cannot create the database connection.")

def file_time_stamps_retrival(value):

	database = "desktopsearch.db"

	conn = create_connection(database)

	if conn is not None:
		sql = ''' SELECT * from file_time_stamps where f_path LIKE ? '''

		rows = file_retrival_timestamp_exec(conn, value, sql)
		return rows
	else:
		print("Error! cannot create the database connection.")

def word_retrival(value):

	database = "desktopsearch.db"

	conn = create_connection(database)

	if conn is not None:
		sql = ''' SELECT * from word_paths where words = ? '''
		try:
			cur = conn.cursor()
			cur.execute(sql, (value,))
			rows = cur.fetchall()
			return rows
		except Error as e:
			return []
	else:
		print("Error! cannot create the database connection.")



