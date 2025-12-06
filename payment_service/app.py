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

# ADD THESE LINES
@app.route("/pay", methods=["POST"])
def pay():
    data = request.get_json(force=True)

    name = data.get("name")
    card_number = data.get("card_number")
    amount = data.get("amount")

    # Dummy card validation based on last digit being even/odd
    try:
        last_digit = int(str(card_number)[-1])
    except (ValueError, TypeError):
        return jsonify({"status": "failed", "message": "Invalid card number"}), 400

    if last_digit % 2 == 0:
        return jsonify({
            "status": "success",
            "message": f"Payment of ${amount} approved for {name}"
        })
    else:
        return jsonify({
            "status": "failed",
            "message": "Card declined by dummy processor"
        }), 402
# END OF ADDED LINES

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
