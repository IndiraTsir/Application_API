import mysql.connector
from fastapi import FastAPI

# 1) run : uvicorn api:app --reload
# 2) change url : http://127.0.0.1:8000/data/

# Intisialisation de l'app Fast.
app = FastAPI()

# Fonction pour récupérer les données depuis la base de données MySQL
def get_data_from_database():
    conn = mysql.connector.connect(
        user="chemsdine",
        password="Ounissi69800",
        host="myserverchems.mysql.database.azure.com",
        port=3306,
        database="linkedin_bdd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table_b")
    data = cursor.fetchall()
    conn.close()
    return data

# Route pour récupérer les données via une requête.
@app.get("/data/")
async def get_data():
    data = get_data_from_database()
    return {"data": data}
