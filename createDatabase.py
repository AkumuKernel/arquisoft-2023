import psycopg2
from psycopg2 import sql

class DatabaseServer:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None

    def create_connection(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname='postgres',
                user=self.user,
                password=self.password
            )
            self.conn.autocommit = True
            cursor = self.conn.cursor()

            # Verificar si la base de datos ya existe
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (self.dbname,))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.dbname)))
                print(f"Database '{self.dbname}' created successfully.")
            else:
                print(f"La base de datos '{self.dbname}' ya existe.")

            cursor.close()
            self.conn.close()

            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")


    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if cursor.description is not None:
                result = cursor.fetchall()
                self.conn.commit()
                return result
            else:
                self.conn.commit()
                return None
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()

    def create_tables(self):
        try:
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                telefono VARCHAR(20),
                localizacion TEXT,
                logged_in BOOLEAN NOT NULL DEFAULT FALSE,
                admin BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
            create_noticias_table = """
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            CREATE TABLE IF NOT EXISTS noticias (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                titulo VARCHAR(255),
                rss VARCHAR(255),
                visitas INTEGER,
                link VARCHAR(255),
                tags JSONB,
                positivo INTEGER,
                neutro INTEGER,
                negativo INTEGER
            )
            """
            create_votos_table = """
            CREATE TABLE IF NOT EXISTS votos (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                id_noticia UUID NOT NULL REFERENCES noticias(id) ON DELETE CASCADE,
                id_user INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                localizacion VARCHAR(255),
                tipo_voto TEXT,
                CONSTRAINT unique_tupla_votos UNIQUE (id_noticia, id_user)
            )
            """            
            self.execute_query(create_users_table)
            self.execute_query(create_noticias_table)
            self.execute_query(create_votos_table)
            print("Tablas creadas con éxito.")
        except Exception as e:
            print(f"Error al crear las tablas: {e}")


# Reemplaza los valores con la información de tu base de datos
server = DatabaseServer(host='localhost', port='5432', dbname='ArquiSoft', user='postgres', password='')

server.create_connection()
server.create_tables()
