# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
import sqlite3


class ImdbPipeline:
    collection_name = 'best_movies'

    def open_spider(self, spider):
        logging.warn("open spider from pipeline")
        # self.client = pymongo.MongoClient(
        #     host="mongodb://localhost",
        #     port=27017
        # )

        self.client = pymongo.MongoClient(
            'mongodb+srv://ravi:<password>@cluster0.drw1m.mongodb.net/<dbname>?retryWrites=true&w=majority')
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        logging.warn("close spider from pipeline")
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item


class SQLitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.Connection('imdb.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE best_movies (
                title TEXT,
                year TEXT,
                duration TEXT,
                genre TEXT,
                rating TEXT,
                movie_url TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
                INSERT INTO best_movies (title, year, duration, genre, rating, movie_url) VALUES(?,?,?,?,?,?)
            
            ''', (
            item.get('title'),
            item.get('year'),
            item.get('duration'),
            item.get('genre'),
            item.get('rating'),
            item.get('movie_url')
        ))
        self.connection.commit()
        return item
