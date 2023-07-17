from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import Flask


class Pizza:
    DB = 'pizza_time_schema'
    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.qty = data['qty']
        # self.toppings = data['toppings']
        self.cheese = data['cheese']
        self.pepperoni = data['pepperoni']
        self.mushroom = data['mushroom']
        self.sausage = data['sausage']
        self.onion = data['onion']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        
    @classmethod
    def create_pizza(cls, data):
        query = """
        INSERT INTO pizzas(method, size, crust, qty, cheese, pepperoni, mushroom, sausage, onion, user_id)
        VALUES(%(method)s, %(size)s, %(crust)s, %(qty)s, %(cheese)s, %(pepperoni)s, %(mushroom)s, %(sausage)s, %(onion)s, %(user_id)s)
        """
        return MySQLConnection(cls.DB).query_db(query, data)