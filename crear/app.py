from flask import Flask, request, jsonify
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

# Microservicio para crear aerolíneas
@app.route('/aerolineas', methods=['POST'])
def crear_aerolinea():
    data = request.get_json()
    if not data or 'nombre' not in data or 'numero_aviones' not in data:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    conn, error_response = get_db_connection()
    if conn is None:
        return error_response
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO aerolineas (nombre, numero_aviones) VALUES (%s, %s)",
                       (data['nombre'], data['numero_aviones']))
        conn.commit()
        return jsonify({"message": "Aerolínea creada exitosamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error en la base de datos: {str(err)}"}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("APP_PORT", 5000)))
