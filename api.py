import mysql.connector
from fastapi import FastAPI
import random

# 1) run : uvicorn api:app --reload
# 2) change url : http://127.0.0.1:8000/data/

# ======================================================================================================================>

# Initialisation de l'app FastAPI.
app = FastAPI()

# Paramètre de connexion.
conn = mysql.connector.connect(
    user="chemsdine",
    password="Ounissi69800",
    host="myserverchems.mysql.database.azure.com",
    port=3306,
    database="linkedin_bdd"
)

# ======================================================================================================================>

# Fonction pour récupérer les données depuis la base de données MySQL.
def get_data_from_database(conn=conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_b")
    data = cursor.fetchall()
    conn.close()
    return data

# Route pour récupérer les données via une requête GET.
@app.get("/data/get")
async def get_data():
    data = get_data_from_database()
    print("Message : Données récupérées avec succès")
    return {"data": data}

# ======================================================================================================================>

# Fonction pour insérer des données dans la base de données MySQL.
def insert_data_to_database(table_1: str, table_2: str, data: dict, conn=conn):
    try:
        cursor = conn.cursor()

        # Création des tables si elles n'existent pas
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_1} (
            id VARCHAR(5) PRIMARY KEY, 
            feature_0 VARCHAR(255), 
            feature_1 VARCHAR(255), 
            feature_2 VARCHAR(255))""")

        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_2} (
                        id_fk VARCHAR(5) NOT NULL DEFAULT '0', 
                    y_pred TEXT, FOREIGN KEY (id_fk) REFERENCES {table_1}(id))""")

        # Génération d'un code ID aléatoire
        code_id = "".join([str(random.randint(0, 10)) for _ in range(5)])

        # Insertion des données dans la table 1
        table1_sql = f"INSERT INTO {table_1} (id, feature_0, feature_1, feature_2) VALUES (%s, %s, %s, %s)"
        table1_values = (code_id, data.get("feature_0"), data.get("feature_1"), data.get("feature_2"))
        cursor.execute(table1_sql, table1_values)

        # Insertion des données dans la table 2
        table2_sql = f"INSERT INTO {table_2} (id_fk, y_pred) VALUES (%s, %s)"
        table2_values = (code_id, data.get("y_pred"))
        cursor.execute(table2_sql, table2_values)

        conn.commit()
        print("Données insérées avec succès.")
    except:
        print(cursor._executed)

# Route pour envoyer des données via une requête POST.
@app.post("/data/post")
async def send_data(data: dict):
    table_1 = "table_a"
    table_2 = "table_b"
    insert_data_to_database(table_1, table_2, data)
    return {"message": "Données insérées avec succès"}

# ======================================================================================================================>


