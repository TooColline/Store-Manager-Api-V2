"""This module initializes the db connection and run queries to set up tables"""
import os
import psycopg2
import psycopg2.extras
import sys

from instance.config import config
from werkzeug.security import generate_password_hash

def initialize_db(db_url=None):
    try:
        if os.getenv('FLASK_ENV') == 'testing':
            conn, cursor = query_db()
            queries = drop_table_if_it_exists() + create_db_tables()

        else:

            conn, cursor = query_db()
            queries = create_db_tables()

        i = 0
        while i != len(queries):
            query = queries[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        conn.close()
        create_admin_user()
    except Exception as error:
        print("\nThe queries have not been executed : {} \n".format(error))


def create_db_tables():
    """Setting up the database tables"""

    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        email VARCHAR (100) NOT NULL UNIQUE,
        password VARCHAR (100) NOT NULL,
        role VARCHAR (10) NOT NULL
    )"""

    products_table = """
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR (24) NOT NULL,
        price INTEGER NOT NULL,
        min_quantity INTEGER NOT NULL,
        inventory INTEGER NOT NULL,
        category VARCHAR (30) NOT NULL
    )"""

    sales_table = """
    CREATE TABLE IF NOT EXISTS sales (
        sale_id SERIAL PRIMARY KEY,
        date_ordered TIMESTAMP DEFAULT NOW(),
        amount INTEGER NOT NULL,
        sold_by VARCHAR (30) NOT NULL REFERENCES users(email) ON DELETE CASCADE
    )"""

    sold_items = """
    CREATE TABLE IF NOT EXISTS solditems (
        sale_id INTEGER NOT NULL REFERENCES sales(sale_id) ON DELETE CASCADE,
        product INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
        quantity INTEGER NOT NULL
    )"""

    blacklist_table = """
    CREATE TABLE IF NOT EXISTS blacklist (
        token VARCHAR (300) NOT NULL
    )
    """

    

    return [users_table, products_table, sales_table, sold_items, blacklist_table]

def create_admin_user():

    hashed = generate_password_hash('123456')
    admin_query = """
    INSERT INTO users (email, password, role) 
    SELECT 'defaultadmin@gmail.com', '%s', 'Admin'
    WHERE 'defaultadmin@gmail.com' NOT IN
    (
        SELECT email FROM users
    );
    """ % hashed

    conn, cursor = query_db()
    cursor.execute(admin_query)
    conn.commit()

def drop_table_if_it_exists():
    """Drops the tables if they already exist"""

    drop_users_table = """
    DROP TABLE IF EXISTS users CASCADE"""

    drop_products_table = """
    DROP TABLE IF EXISTS products CASCADE"""

    drop_sales_table = """
    DROP TABLE IF EXISTS sales CASCADE"""

    drop_solditems_table = """
    DROP TABLE IF EXISTS solditems CASCADE"""

    drop_blacklist_table = """
    DROP TABLE IF EXISTS blacklist CASCADE"""

    return [drop_users_table, drop_products_table, drop_sales_table, drop_solditems_table, drop_blacklist_table]


def query_db(query=None, db_url=None):
    """Creates a connection to the database and execute db queries"""

    conn = None
    if db_url is None:
        db_url = config[os.getenv('FLASK_ENV')].DB_URL
    try:
        # connecting to the db
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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