import psycopg2
from psycopg2 import sql
import json
import re

class databaseServer:
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
   
   if "SELECT" in query:
    result = cursor.fetchall()
   else:
    result = None

   self.conn.commit()
   return result
  except psycopg2.Error as e:
   self.conn.rollback()
   print(f"Error al ejecutar la consulta: {e}")
  finally:
   cursor.close()

 def register(self, nombre, email, password, telefono, localizacion):
  try:
   query = f"SELECT * FROM users WHERE email = '{email}'"
   user_exist = self.execute_query(query)

   if user_exist:
    print ("Correo ya registrado!")
    return 'Mail'

   else:
    query = f"""
            INSERT INTO users (nombre, email, password, telefono, localizacion)
            VALUES ('{nombre}', '{email}', '{password}', '{telefono}', '{localizacion}')
            """
    self.execute_query(query)
    print("Usuario registrado con éxito")
    return 'True'
  except Exception as e:
   print(f"Error al registrar usuario: {e}")
   return 'False'

 def login(self, email, password):
  try:
   query = f"SELECT * FROM users WHERE email = '{email}' and password = '{password}'"
   auth = self.execute_query(query)
   if auth:
    query2 = f"UPDATE users SET logged_in = TRUE WHERE email = '{email}' AND password = '{password}'"
    self.execute_query(query2)
    return 'True'
   else:
    return 'Wrong'
  except Exception as e:
   return 'False'

 def viewLogged(self):
  try:
   cursor = self.conn.cursor()
   query = f"SELECT id FROM users WHERE logged_in = TRUE"
   cursor.execute(query)
   result = str(cursor.fetchone())
   auth = re.sub(r'\(([^)]+),\)', r'(\1)', result)
   print(auth)
   if auth:
    return auth
  except Exception as e:
    return 'False'

 def logOut(self):
  try:
   query = f"UPDATE users SET logged_in = FALSE WHERE logged_in = TRUE"
   result = self.execute_query(query)
   return result
  except Exception as e:
   return 'False' 

 def insertNoticia(self, titulo, rss, visitas, link, tags=[]):
  try:
   datos_json = {
    "tags": tags
   }
   datos_json_str = json.dumps(datos_json)
   query = f"""
          INSERT INTO noticias (titulo, rss, visitas, link, tags, positivo, neutro, negativo) 
          VALUES ('{titulo}', '{rss}', '{visitas}', '{link}', '{datos_json_str}'::json, 0, 0, 0)
          """
   self.execute_query(query)
   return 'True'
  except Exception as e:
   print(f"Error al ingresar la noticia: {e}")
   return 'False'

 def valorarNoticia(self, id_noticia, id_user , value, localizacion):
  try:
   if value not in ('positivo', 'neutro', 'negativo'):
    print("No válido")
    return
   query = f"""
           UPDATE noticias
           SET {value} = {value} + 1
           WHERE id = '{id_noticia}'
           """
   query2 = f"INSERT INTO votos (id_noticia, id_user , tipo_voto, localizacion) VALUES ('{id_noticia}', '{id_user}', '{localizacion}', '{value}')"
   self.execute_query(query)
   self.execute_query(query2)
   return 'True'
  except Exception as e:
   print(f"Error al valorar noticia: {e}")
   return 'False'
 
 def load_data(self):
  cursor = self.conn.cursor()
  cursor.execute("SELECT * FROM noticias")
  data = cursor.fetchall()
  datos = []
  column_names = [desc[0] for desc in cursor.description]
  for fila in data:
   fila_json = dict(zip(column_names, fila))
   datos.append(fila_json)

  return json.dumps(datos, indent=2)

 def search(self, keyword):
  cursor = self.conn.cursor()
  cursor.execute(f"SELECT * FROM noticias WHERE titulo LIKE '%{keyword}%'")
  data = cursor.fetchall()
  datos = []
  column_names = [desc[0] for desc in cursor.description]
  for fila in data:
   fila_json = dict(zip(column_names, fila))
   datos.append(fila_json)

  return json.dumps(datos, indent=2)

 def obtainGraphics(self):
  try:
   query = f"SELECT u.localizacion, COUNT(n.positivo) AS positivo, COUNT(n.neutro) AS neutro, COUNT(n.negativo) AS negativo FROM users u LEFT JOIN votos v ON u.id = v.id_user LEFT JOIN noticias n ON v.id_noticia = n.id GROUP BY u.localizacion;"
   resultados = self.execute_query(query)
   
   porcentajes = []

   for resultado in resultados:
    total = sum(resultado[1:])
    p_positivo = (resultado[1]/total)*100 if total > 0 else 0
    p_neutro = (resultado[2]/total)*100 if total > 0 else 0
    p_negativo = (resultado[3]/total)*100 if total > 0 else 0

    porcentajes.append({
     'localizacion': resultado[0],
     'positivo': p_positivo,
     'neutro': p_neutro,
     'negativo': p_negativo
    })
   return json.dumps(porcentajes, indent=2)
  except Exception as e:
   print(f"Error: {e}")