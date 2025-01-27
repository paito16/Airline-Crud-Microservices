from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "db_aerolinea"),
            port=int(os.getenv("DB_PORT", 3306))
        )
    except mysql.connector.Error as err:
        return None, jsonify({"error": f"Error en la base de datos: {str(err)}"}), 500

# Microservicio para leer aerolíneas
@app.route('/aerolineas/<int:id>', methods=['GET'])
def leer_aerolinea(id):
    conn, error_response = get_db_connection()
    if conn is None:
        return error_response
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM aerolineas WHERE ID = %s", (id,))
        aerolinea = cursor.fetchone()
        if not aerolinea:
            return jsonify({"error": "Aerolínea no encontrada"}), 404
        return jsonify(aerolinea)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("APP_PORT", 5001)))
