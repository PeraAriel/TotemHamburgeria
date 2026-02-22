import pymysql
from config import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseWrapper:
    """Wrapper per tutte le operazioni database"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connette al database MySQL"""
        try:
            self.connection = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                port=Config.DB_PORT,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            logger.info("Connected to database successfully")
        except pymysql.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def disconnect(self):
        """Chiude la connessione al database"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Disconnected from database")
    
    def execute_query(self, query, params=None):
        """Esegue una query e ritorna i risultati"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except pymysql.Error as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def execute_update(self, query, params=None):
        """Esegue un INSERT/UPDATE/DELETE e committa"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount
        except pymysql.Error as e:
            self.connection.rollback()
            logger.error(f"Update execution error: {e}")
            raise
    
    def execute_insert(self, query, params=None):
        """Esegue un INSERT e ritorna l'ID del nuovo record"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except pymysql.Error as e:
            self.connection.rollback()
            logger.error(f"Insert execution error: {e}")
            raise
    
    # === CATEGORIE ===
    def get_all_categories(self):
        """Recupera tutte le categorie"""
        query = "SELECT id, name, description FROM categories ORDER BY name"
        return self.execute_query(query)
    
    def get_category_by_id(self, category_id):
        """Recupera una categoria per ID"""
        query = "SELECT id, name, description FROM categories WHERE id = %s"
        result = self.execute_query(query, (category_id,))
        return result[0] if result else None
    
    def create_category(self, name, description=""):
        """Crea una nuova categoria"""
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        return self.execute_insert(query, (name, description))
    
    def update_category(self, category_id, name, description):
        """Aggiorna una categoria"""
        query = "UPDATE categories SET name = %s, description = %s WHERE id = %s"
        return self.execute_update(query, (name, description, category_id))
    
    def delete_category(self, category_id):
        """Elimina una categoria"""
        query = "DELETE FROM categories WHERE id = %s"
        return self.execute_update(query, (category_id,))
    
    # === PRODOTTI ===
    def get_all_products(self):
        """Recupera tutti i prodotti con le loro categorie"""
        query = """
            SELECT p.id, p.name, p.description, p.price, p.image_url, p.category_id, c.name as category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY c.name, p.name
        """
        return self.execute_query(query)
    
    def get_products_by_category(self, category_id):
        """Recupera i prodotti di una categoria specifica"""
        query = """
            SELECT id, name, description, price, image_url, category_id
            FROM products
            WHERE category_id = %s
            ORDER BY name
        """
        return self.execute_query(query, (category_id,))
    
    def get_product_by_id(self, product_id):
        """Recupera un prodotto per ID"""
        query = "SELECT id, name, description, price, image_url, category_id FROM products WHERE id = %s"
        result = self.execute_query(query, (product_id,))
        return result[0] if result else None
    
    def create_product(self, name, description, price, category_id, image_url=""):
        """Crea un nuovo prodotto"""
        query = """
            INSERT INTO products (name, description, price, category_id, image_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_insert(query, (name, description, price, category_id, image_url))
    
    def update_product(self, product_id, name, description, price, category_id, image_url):
        """Aggiorna un prodotto"""
        query = """
            UPDATE products
            SET name = %s, description = %s, price = %s, category_id = %s, image_url = %s
            WHERE id = %s
        """
        return self.execute_update(query, (name, description, price, category_id, image_url, product_id))
    
    def delete_product(self, product_id):
        """Elimina un prodotto"""
        query = "DELETE FROM products WHERE id = %s"
        return self.execute_update(query, (product_id,))
    
    # === ORDINI ===
    def get_all_orders(self):
        """Recupera tutti gli ordini"""
        query = """
            SELECT id, order_number, status, total_price, created_at, updated_at
            FROM orders
            ORDER BY created_at DESC
        """
        return self.execute_query(query)
    
    def get_order_by_id(self, order_id):
        """Recupera un ordine per ID"""
        query = "SELECT id, order_number, status, total_price, created_at, updated_at FROM orders WHERE id = %s"
        result = self.execute_query(query, (order_id,))
        return result[0] if result else None
    
    def get_order_items(self, order_id):
        """Recupera gli articoli di un ordine"""
        query = """
            SELECT oi.id, oi.product_id, oi.quantity, oi.unit_price, p.name, p.description
            FROM order_items oi
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
            ORDER BY oi.id
        """
        return self.execute_query(query, (order_id,))
    
    def create_order(self, total_price, items):
        """Crea un nuovo ordine con gli articoli"""
        try:
            # Generiamo il numero ordine
            query_order_num = "SELECT COALESCE(MAX(order_number), 0) + 1 as next_number FROM orders"
            result = self.execute_query(query_order_num)
            order_number = result[0]['next_number'] if result else 1
            
            # Creiamo l'ordine
            query_order = """
                INSERT INTO orders (order_number, status, total_price)
                VALUES (%s, %s, %s)
            """
            order_id = self.execute_insert(query_order, (order_number, 'pending', total_price))
            
            # Aggiungiamo gli articoli
            query_item = """
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
            """
            for item in items:
                self.execute_insert(query_item, (order_id, item['product_id'], item['quantity'], item['unit_price']))
            
            return order_id
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            raise
    
    def update_order_status(self, order_id, status):
        """Aggiorna lo stato di un ordine"""
        query = "UPDATE orders SET status = %s, updated_at = NOW() WHERE id = %s"
        return self.execute_update(query, (status, order_id))
    
    def delete_order(self, order_id):
        """Elimina un ordine e i suoi articoli"""
        try:
            # Eliminiamo gli articoli
            query_items = "DELETE FROM order_items WHERE order_id = %s"
            self.execute_update(query_items, (order_id,))
            
            # Eliminiamo l'ordine
            query_order = "DELETE FROM orders WHERE id = %s"
            return self.execute_update(query_order, (order_id,))
        except Exception as e:
            logger.error(f"Error deleting order: {e}")
            raise
