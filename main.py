# 1. python -m pip install pymongo
# 2. python -m pip install --upgrade pymongo
# 3. MongoDB Container: docker run --name container_name -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=tupw -d mongo
# 4. NOTA: Como sugerencia conectarse al mismo tiempo mediante un cliente GUI al connection string para visualizar cambios (Compass)
# 5. Ejecutar el archivo -> python main.py
# 6. Se puede hacer el connection_string con una URI de MongoDB ATLAS, modificando argumentos como username, password,etc (<argumento>)

from pymongo import MongoClient

# Estableciendo el connection string (Subir docker container y copiar connection string)
connection_string = 'mongodb://mongoadmin:UnaClav3@localhost:27017/?authMechanism=SCRAM-SHA-256'

# Instanciando un cliente de la clase MongoClient y conectandose a dicha instancia
try:
    cliente = MongoClient(connection_string)
except Exception:
    print('Error: ', Exception)

# Definicion de la base de datos -> si está creada se conecta, de lo contrario la crea -> CREATE DATABASE
base_datos = cliente['gestion_utilizacion_buses_cargadores']

# Listar las bases de datos
databases_array = cliente.list_database_names()
print('Las bases de datos existentes actualmente son: ', databases_array)
# La base de datos creada llamada gestion_utilizacion_buses_cargadores, no aparece debido a que no hay documentos dentro de dicha DB

# Accediendo a una coleccion en específico -> si no exite, el motor de mongodb la crea - CREANDO LA COLECCION 'buses'
coleccion = base_datos['buses']

# Creacion de documentos -> Formato BSON <=> JSON
documento = {
    "id": 1,
    "placa": "ADG135",
    "estado": "Parqueado",
    "marca": "Renault"
}

documento_2 = {
    "id": 2,
    "placa": "ZCB246",
    "estado": "Cargando",
    "marca": "BMW"
}

documento_3 = {
    "id": 3,
    "placa": "GKH084",
    "estado": "En Operacion",
    "marca": "Chevrolet"
}

documento_4 = {
    "id": 4,
    "placa": "THO345",
    "estado": "Parqueado",
    "marca": "BMW"
}

docs_array = [documento_2, documento_3, documento_4] # Array de Diccionarios (JSON)

# --- Insertar documentos dentro de Colecciones ---
coleccion.insert_one(documento)
coleccion.insert_many(docs_array, ordered=False)
# Recomendacion: comentar la insercion, debido a que cada ejecución del programa insertará los mismo valores y no estamos en un mundo Relacional

# --- Leer el _id asignado automaticamente por el motor de mongodb
# --- resp = coleccion.insert_one(documento)
# --- print(resp.inserted_id)

# --- Leer las bases de datos existentes
print('Las bases de datos existentes actualmente son: ', databases_array)

# --- Leer un solo documento (Leerá el primer documento de dicha coleccion si no se le asigna un filtro)
print(coleccion.find_one())

# --- Leer (READ) los documentos que contiene una coleccion
for doc_i in coleccion.find():
    print(doc_i)


# --- Actualizar (UPDATE) un documento
consulta = {
    "placa": "THO345"
}

nuevo_valor = {
    "$set": {
        "placa": "SBS531"
    }
}

coleccion.update_one(consulta, nuevo_valor)

# --- Leyendo el documento actualizado
print(coleccion.find_one({"placa":"SBS531"})) # Se utiliza un filtro -> se puede evaluar en un cliente de GUI para Mongo


# --- Eliminar registros (DELETE)
# --- En el ciclo for, se encontró que hay 5 documentos con la misma informacion, por tanto, se eliminarán
delete_consulta = {
    'id':1
}

coleccion.delete_many(delete_consulta)

print('--- --- LEYENDO TODA LA COLECCION LUEGO DEL BORRADO DE DOCUMENTOS --- --- ---')

for doc_i in coleccion.find():
    print(doc_i)
