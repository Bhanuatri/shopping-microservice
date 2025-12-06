from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})
# ADD THESE LINES
@app.route("/products", methods=["GET"])
def get_products():
    # Return a dummy list of products as JSON
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Headphones", "price": 49.99},
        {"id": 3, "name": "Mouse", "price": 19.99},
    ]
    return jsonify(products)
# END OF ADDED LINES

@app.route("/pay", methods=["POST"])
def pay():
    data = request.get_json(force=True)

    name = data.get("name")
    card_number = data.get("card_number")
    amount = data.get("amount")

    if not (name and card_number and amount is not None):
        return jsonify({"status": "failed", "message": "Missing fields"}), 400

    # Dummy card validation:
    # Let's say if card number ends with an even digit, payment = success
    try:
        last_digit = int(str(card_number)[-1])
    except ValueError:
        return jsonify({"status": "failed", "message": "Invalid card number format"}), 400

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
