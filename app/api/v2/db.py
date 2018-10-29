"""This module initializes the db connection and run queries to set up tables"""
import sys

import psycopg2

def initialize_db(db_url=None):
    try:
        conn, cursor = query_db()
        queries = drop_table_if_it_exists() + create_db_tables()
        i = 0
        while i != len(queries):
            query = queries[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        conn.close()

    except Exception as error:
        print("\nThe queries have not been executed : {} \n".format(error))


def create_db_tables():
    """Setting up the database tables"""

    users_table = """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        email VARCHAR (100) NOT NULL UNIQUE,
        password VARCHAR (100) NOT NULL,
        role VARCHAR (10) NOT NULL
    )"""

    products_table = """
    CREATE TABLE products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR (24) NOT NULL,
        price INTEGER NOT NULL,
        category VARCHAR (50) NOT NULL
    )"""

    sales_table = """
    CREATE TABLE sales (
        sale_id SERIAL PRIMARY KEY,
        date_ordered TIMESTAMP DEFAULT NOW(),
        name VARCHAR (24) NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        totalamt INTEGER NOT NULL
    )"""

    return [users_table, products_table, sales_table]

def drop_table_if_it_exists():
    """Drops the tables if they already exist"""

    drop_users_table = """
    DROP TABLE IF EXISTS users"""

    drop_products_table = """
    DROP TABLE IF EXISTS products"""

    drop_sales_table = """
    DROP TABLE IF EXISTS sales"""

    return [drop_users_table, drop_products_table, drop_sales_table]


def query_db(query=None, db_url=None):
    """Creates a connection to the database and execute db queries"""

    conn = None
    if db_url is None:
        db_url = "dbname='store_manager' host='localhost' port='5432' user='postgres' password='Password2#'"
    try:
        # connecting to the db
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        if query:
            cursor.execute(query)
            conn.commit()

    except(Exception,
            psycopg2.DatabaseError,
            psycopg2.ProgrammingError) as error:
        print(error)
        return None

    return conn, cursor


def insert_to_db(query):
    """INSERT queries"""
        
    try:
        conn = query_db(query)[0]
        conn.close()
    except psycopg2.Error as error:
        print("Insertion error: {}".format(error))
        sys.exit(1)


def select_from_db(query):
    """SELECT queries"""
    
    fetched_data = None
    conn, cursor = query_db(query)
    if conn:
        fetched_data = cursor.fetchall()
        conn.close()

    return fetched_data


if __name__ == '__main__':
    initialize_db()
    query_db()