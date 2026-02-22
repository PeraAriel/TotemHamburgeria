from flask import Flask, jsonify, request
from flask_cors import CORS
from database_wrapper_sqlite import DatabaseWrapper
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['DEBUG'] = True
CORS(app)

# Initialize database
db = DatabaseWrapper()

# ==================== CATEGORIE ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Recupera tutte le categorie"""
    try:
        db.connect()
        categories = db.get_all_categories()
        db.disconnect()
        return jsonify(categories)
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Recupera una categoria specifica"""
    try:
        db.connect()
        category = db.get_category_by_id(category_id)
        db.disconnect()
        if not category:
            return jsonify({"error": "Category not found"}), 404
        return jsonify(category)
    except Exception as e:
        logger.error(f"Error getting category: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Crea una nuova categoria"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing required field: name"}), 400
        
        db.connect()
        category_id = db.create_category(data['name'], data.get('description', ''))
        db.disconnect()
        return jsonify({"id": category_id, "message": "Category created successfully"}), 201
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Aggiorna una categoria"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing required field: name"}), 400
        
        db.connect()
        db.update_category(category_id, data['name'], data.get('description', ''))
        db.disconnect()
        return jsonify({"message": "Category updated successfully"})
    except Exception as e:
        logger.error(f"Error updating category: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Elimina una categoria"""
    try:
        db.connect()
        db.delete_category(category_id)
        db.disconnect()
        return jsonify({"message": "Category deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting category: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== PRODOTTI ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Recupera tutti i prodotti"""
    try:
        db.connect()
        products = db.get_all_products()
        db.disconnect()
        return jsonify(products)
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    """Recupera i prodotti di una categoria"""
    try:
        db.connect()
        products = db.get_products_by_category(category_id)
        db.disconnect()
        return jsonify(products)
    except Exception as e:
        logger.error(f"Error getting products by category: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Recupera un prodotto specifico"""
    try:
        db.connect()
        product = db.get_product_by_id(product_id)
        db.disconnect()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product)
    except Exception as e:
        logger.error(f"Error getting product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Crea un nuovo prodotto"""
    try:
        data = request.get_json()
        required_fields = ['name', 'price', 'category_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
        
        db.connect()
        product_id = db.create_product(
            data['name'],
            data.get('description', ''),
            data['price'],
            data['category_id'],
            data.get('image_url', '')
        )
        db.disconnect()
        return jsonify({"id": product_id, "message": "Product created successfully"}), 201
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Aggiorna un prodotto"""
    try:
        data = request.get_json()
        required_fields = ['name', 'price', 'category_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
        
        db.connect()
        db.update_product(
            product_id,
            data['name'],
            data.get('description', ''),
            data['price'],
            data['category_id'],
            data.get('image_url', '')
        )
        db.disconnect()
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un prodotto"""
    try:
        db.connect()
        db.delete_product(product_id)
        db.disconnect()
        return jsonify({"message": "Product deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== ORDINI ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Recupera tutti gli ordini"""
    try:
        db.connect()
        orders = db.get_all_orders()
        # Aggiungiamo gli articoli per ogni ordine
        for order in orders:
            order['items'] = db.get_order_items(order['id'])
        db.disconnect()
        return jsonify(orders)
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Recupera un ordine specifico"""
    try:
        db.connect()
        order = db.get_order_by_id(order_id)
        if not order:
            db.disconnect()
            return jsonify({"error": "Order not found"}), 404
        order['items'] = db.get_order_items(order_id)
        db.disconnect()
        return jsonify(order)
    except Exception as e:
        logger.error(f"Error getting order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Crea un nuovo ordine"""
    try:
        data = request.get_json()
        if not data or 'items' not in data or 'total_price' not in data:
            return jsonify({"error": "Missing required fields: items, total_price"}), 400
        
        db.connect()
        order_id = db.create_order(data['total_price'], data['items'])
        db.disconnect()
        return jsonify({"id": order_id, "message": "Order created successfully"}), 201
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Aggiorna lo stato di un ordine"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({"error": "Missing required field: status"}), 400
        
        db.connect()
        db.update_order_status(order_id, data['status'])
        db.disconnect()
        return jsonify({"message": "Order status updated successfully"})
    except Exception as e:
        logger.error(f"Error updating order status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Elimina un ordine"""
    try:
        db.connect()
        db.delete_order(order_id)
        db.disconnect()
        return jsonify({"message": "Order deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting order: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
