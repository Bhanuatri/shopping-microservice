from flask import Flask, jsonify

app = Flask(__name__)

# Dummy in-memory products list
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 799.99},
    {"id": 2, "name": "Headphones", "price": 49.99},
    {"id": 3, "name": "Mouse", "price": 19.99},
    {"id": 4, "name": "Keyboard", "price": 39.99}
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(PRODUCTS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
