import sqlite3
import os
from typing import List, Dict, Any

class DatabaseWrapper:
    """SQLite Wrapper - Versione di sviluppo locale"""
    
    def __init__(self, db_file="hamburgeria.db"):
        self.db_file = db_file
        self.connection = None
        self.cursor = None
        self._init_db()
    
    def _init_db(self):
        """Inizializza il database con schema e dati di esempio"""
        self.connect()
        
        # Creiamo le tabelle
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                category_id INTEGER NOT NULL,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number INTEGER UNIQUE NOT NULL,
                status TEXT DEFAULT 'pending',
                total_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                unit_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        ''')
        
        # Inseriamo dati di esempio
        try:
            self.cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)',
                               ('Panini', 'Panini freschi e gustosi'))
            self.cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)',
                               ('Bevande', 'Bevande fredde e calde'))
            self.cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)',
                               ('Menu', 'Menu completi'))
            self.cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)',
                               ('Dolci', 'Dolci e dessert'))
            
            # Panini
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Hamburger Classico', 'Pane, carne, pomodoro, lattuga, cipolla', 7.50, 1))
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Cheeseburger', 'Con formaggio cheddar premium', 8.50, 1))
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Veggie Burger', 'Panino vegetariano con verdure grigliate', 7.00, 1))
            
            # Bevande
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Coca Cola', 'Lattina 33cl', 2.50, 2))
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Acqua Naturale', 'Bottiglia 50cl', 1.50, 2))
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Birra', 'Birra artigianale 33cl', 4.00, 2))
            
            # Menu
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Menu Combo', 'Hamburger + Patatine + Bevanda', 12.00, 3))
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Menu Deluxe', 'Cheeseburger + Patatine + Bevanda + Dolce', 15.00, 3))
            
            # Dolci
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Tiramisù', 'Dolce tradizionale italiano', 4.50, 4))
            self.cursor.execute('INSERT INTO products (name, description, price, category_id) VALUES (?, ?, ?, ?)',
                               ('Gelato', 'Gelato assortito', 3.50, 4))
            
            self.connection.commit()
        except sqlite3.IntegrityError:
            # Dati già inseriti
            pass
        
        self.disconnect()
    
    def connect(self):
        """Connette al database"""
        self.connection = sqlite3.connect(self.db_file)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def disconnect(self):
        """Chiude la connessione"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Esegue una query e ritorna i risultati"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return [dict(row) for row in self.cursor.fetchall()]
    
    def execute_update(self, query, params=None):
        """Esegue un INSERT/UPDATE/DELETE"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.rowcount
    
    def execute_insert(self, query, params=None):
        """Esegue un INSERT e ritorna l'ID"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid
    
    # === CATEGORIE ===
    def get_all_categories(self):
        return self.execute_query("SELECT id, name, description FROM categories ORDER BY name")
    
    def get_category_by_id(self, category_id):
        result = self.execute_query("SELECT id, name, description FROM categories WHERE id = ?", (category_id,))
        return result[0] if result else None
    
    def create_category(self, name, description=""):
        return self.execute_insert("INSERT INTO categories (name, description) VALUES (?, ?)", (name, description))
    
    def update_category(self, category_id, name, description):
        return self.execute_update("UPDATE categories SET name = ?, description = ? WHERE id = ?", (name, description, category_id))
    
    def delete_category(self, category_id):
        return self.execute_update("DELETE FROM categories WHERE id = ?", (category_id,))
    
    # === PRODOTTI ===
    def get_all_products(self):
        query = """
            SELECT p.id, p.name, p.description, p.price, p.image_url, p.category_id, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY c.name, p.name
        """
        return self.execute_query(query)
    
    def get_products_by_category(self, category_id):
        query = """
            SELECT id, name, description, price, image_url, category_id
            FROM products
            WHERE category_id = ?
            ORDER BY name
        """
        return self.execute_query(query, (category_id,))
    
    def get_product_by_id(self, product_id):
        result = self.execute_query("SELECT id, name, description, price, image_url, category_id FROM products WHERE id = ?", (product_id,))
        return result[0] if result else None
    
    def create_product(self, name, description, price, category_id, image_url=""):
        query = "INSERT INTO products (name, description, price, category_id, image_url) VALUES (?, ?, ?, ?, ?)"
        return self.execute_insert(query, (name, description, price, category_id, image_url))
    
    def update_product(self, product_id, name, description, price, category_id, image_url):
        query = "UPDATE products SET name = ?, description = ?, price = ?, category_id = ?, image_url = ? WHERE id = ?"
        return self.execute_update(query, (name, description, price, category_id, image_url, product_id))
    
    def delete_product(self, product_id):
        return self.execute_update("DELETE FROM products WHERE id = ?", (product_id,))
    
    # === ORDINI ===
    def get_all_orders(self):
        query = "SELECT id, order_number, status, total_price, created_at, updated_at FROM orders ORDER BY created_at DESC"
        return self.execute_query(query)
    
    def get_order_by_id(self, order_id):
        query = "SELECT id, order_number, status, total_price, created_at, updated_at FROM orders WHERE id = ?"
        result = self.execute_query(query, (order_id,))
        return result[0] if result else None
    
    def get_order_items(self, order_id):
        query = """
            SELECT oi.id, oi.product_id, oi.quantity, oi.unit_price, p.name, p.description
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
            ORDER BY oi.id
        """
        return self.execute_query(query, (order_id,))
    
    def create_order(self, total_price, items):
        try:
            # Generiamo il numero ordine
            result = self.execute_query("SELECT MAX(order_number) as max_order FROM orders")
            order_number = (result[0]['max_order'] or 0) + 1 if result else 1
            
            # Creiamo l'ordine
            order_id = self.execute_insert(
                "INSERT INTO orders (order_number, status, total_price) VALUES (?, ?, ?)",
                (order_number, 'pending', total_price)
            )
            
            # Aggiungiamo gli articoli
            for item in items:
                self.execute_insert(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, item['product_id'], item['quantity'], item['unit_price'])
                )
            
            return order_id
        except Exception as e:
            raise e
    
    def update_order_status(self, order_id, status):
        query = "UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        return self.execute_update(query, (status, order_id))
    
    def delete_order(self, order_id):
        try:
            self.execute_update("DELETE FROM order_items WHERE order_id = ?", (order_id,))
            return self.execute_update("DELETE FROM orders WHERE id = ?", (order_id,))
        except Exception as e:
            raise e
