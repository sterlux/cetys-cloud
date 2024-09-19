from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.json
    product_id = order['product_id']
    quantity = order['quantity']

    # Get product details from the Product service
    response = requests.get('http://product-service:5000/products')
    products = response.json()

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    total_price = product['price'] * quantity
    new_order = {
        "id": len(orders) + 1,
        "product_id": product_id,
        "product_name": product['name'],
        "quantity": quantity,
        "total_price": total_price
    }
    orders.append(new_order)
    return jsonify(new_order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
