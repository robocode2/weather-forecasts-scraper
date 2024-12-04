# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from scrapy.exceptions import DropItem

from collections import defaultdict

class PostgreSQLPipeline:
    def open_spider(self, spider):
        try:
            """ self.connection = psycopg2.connect(
                host='127.0.0.1',
                database='testforecastsdb',
                user='postgres',
                password='IDnowLOV123!',
                port='5434'
            ) """
            self.connection = psycopg2.connect(
                database='defaultdb',
                user='doadmin',
                password='AVNS_CtP8-riN5ITOU4EoaFS',
                host='dbaas-db-1559411-do-user-16960082-0.c.db.ondigitalocean.com',  # Host URL
                port='25060'
            )
            self.cursor = self.connection.cursor()
            self.city_cache = {}
            self.country_cache = {}
            self.source_cache = {}
        except psycopg2.Error as e:
            spider.logger.error(f"Error connecting to PostgreSQL: {e}")
            raise

    def close_spider(self, spider):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def get_or_create_id(self, table, name, cache):
        if name in cache:
            return cache[name]
        
        self.cursor.execute(f"""
            INSERT INTO {table} (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
        """, (name,))
        result = self.cursor.fetchone()
        if result:
            cache[name] = result[0]
        else:
            self.cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (name,))
            cache[name] = self.cursor.fetchone()[0]
        
        return cache[name]

    def process_item(self, item, spider):
        try:
            city_id = self.get_or_create_id('City', item['city'], self.city_cache)
            country_id = self.get_or_create_id('Country', item['country'], self.country_cache)
            source_id = self.get_or_create_id('Source', item['source'], self.source_cache)

            self.cursor.execute("""
                INSERT INTO Forecast (
                    source_id, city_id, country_id, state, collection_date,
                    forecasted_day, precipitation_chance, precipitation_amount,
                    temp_high, temp_low, wind_speed, humidity, weather_condition
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                source_id,
                city_id,
                country_id,
                item['state'],
                item['collection_date'],
                item['forecasted_day'],
                item['precipitation_chance'],
                item['precipitation_amount'],
                item['temp_high'],
                item['temp_low'],
                item['wind_speed'],
                item['humidity'],
                item['weather_condition']
            ))
            self.connection.commit()
        except psycopg2.Error as e:
            self.connection.rollback()
            raise DropItem(f"Error processing item: {e}")
        return item

            

    

    