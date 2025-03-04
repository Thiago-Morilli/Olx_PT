from flask import Flask, jsonify
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Olx_DataBase.Mysql_connection import Mysql_Connector

app = Flask(__name__)

@app.route('/')
def index():
    cnn =  Mysql_Connector.Connection()
    cursor = cnn[0]

    cursor.execute("USE Scrapy_Olx")
    cursor.execute("SELECT * FROM Cars")
    resultados = cursor.fetchall()

    carros = list()

    for cars in resultados:
        carros.append(
            {
                "Title": cars[0],
                "Model": cars[1],
                "Price": cars[2],
                "Brand": cars[3],
                "production_data": cars[4],
                "City": cars[5],
                "Description": cars[6]

            }
        )

    return jsonify(carros)

if __name__ == '__main__':
    app.run(debug=True)
