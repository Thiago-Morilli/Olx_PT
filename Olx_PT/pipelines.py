import mysql.connector
from Olx_PT.items import OlxPtItem


class OlxPtPipeline:
    def process_item(self, item, spider):

        self.save_mysql(item)

    def save_mysql(self, item):

        db_connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="998674629Th.",
        database="Scrapy_Olx"
        )

        cursor = db_connection.cursor()

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Cars(
            Title VARCHAR(100),
            Model VARCHAR (40),
            Price INT,
            Brand VARCHAR (50),
            production_data INT,
            City VARCHAR (150),
            Description LONGTEXT
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Cars(Title, Model, Price, Brand, production_data, City, Description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, (
            item["Title"],
            item["Model"],
            item["Price"],
            item["Brand"],
            item["production_data"],
            item["City"],
            item["Description"]
        ))

        db_connection.commit()
    
        cursor.close()
        db_connection.close()
