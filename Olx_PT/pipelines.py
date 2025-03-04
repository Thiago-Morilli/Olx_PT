from Olx_DataBase.Mysql_connection import Mysql_Connector
from Olx_PT.items import OlxPtItem


class OlxPtPipeline:
    def process_item(self, item, spider):
        #print(item)
        

        self.save_mysql(item)

    def save_mysql(self, item):
        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]

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
