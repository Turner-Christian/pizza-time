from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app


class Pizza:
    DB = 'pizza_time_schema' 

    def price_calc(data):
        if data['size'] == 'small':
            return 7.00
        elif data['size'] == 'medium':
            return 9.00
        elif data['size'] == 'large':
            return 12.00
        elif data['size'] == 'xlarge':
            return 15.00
        else:
            return 0.00
        
    def topping_price(data):
        toppings_price = 0.00
        if data['cheese'] == 'on':
            toppings_price += 1.00
        if data['pepperoni'] == 'on':
            toppings_price += 1.00
        if data['mushroom'] == 'on':
            toppings_price += 1.00
        if data['sausage'] == 'on':
            toppings_price += 1.00
        if data['onion'] == 'on':
            toppings_price += 1.00
        return toppings_price
    
    def method_price(data):
        if data['method'] == 'delivery':
            return 7.99
        else:
            return 0.00

    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.qty = data['qty']
        self.cheese = data['cheese']
        self.pepperoni = data['pepperoni']
        self.mushroom = data['mushroom']
        self.sausage = data['sausage']
        self.onion = data['onion']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.price = None
        
    @classmethod
    def create_pizza(cls, data):
        query = """
        INSERT INTO pizzas(method, size, crust, qty, cheese, pepperoni, mushroom, sausage, onion, user_id)
        VALUES(%(method)s, %(size)s, %(crust)s, %(qty)s, %(cheese)s, %(pepperoni)s, %(mushroom)s, %(sausage)s, %(onion)s, %(user_id)s)
        """
        return MySQLConnection(cls.DB).query_db(query, data)
    
    @classmethod
    def get_one_pizza(cls, data):
        query = """
        Select * from pizzas
        Where id = %(id)s
        """
        result = MySQLConnection(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_all_pizzas(cls, data):
        query = """
        SELECT * FROM pizzas
        WHERE user_id = %(id)s;
        """
        result = MySQLConnection(cls.DB).query_db(query, data)
        print(result)
        all_pizzas = []
        for pizza in result:
            all_pizzas.append(cls(pizza))
        return all_pizzas
    
    @classmethod
    def get_ordered_pizzas(cls, data):
        query = """
        SELECT * FROM pizzas
        WHERE user_id = %(id)s
        ORDER BY created_at DESC
        LIMIT %(order_count)s;
        """
        result = MySQLConnection(cls.DB).query_db(query, data)
        if result == False:
            return 'No orders made by this user'
        all_ordered_pizzas = []
        for pizza in result:
            pizza_instance = cls(pizza)
            method_price = cls.method_price(pizza)
            size_price = cls.price_calc(pizza)
            topping_price = cls.topping_price(pizza) 
            price = format((((size_price + topping_price) * pizza['qty']) + method_price), '.2f')
            pizza_instance.price = price  # Set the price attribute
            all_ordered_pizzas.append(pizza_instance)
            # pizza['price'] = price
            # all_ordered_pizzas.append(pizza)
        return all_ordered_pizzas
    