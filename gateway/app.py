from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests

app = Flask(__name__)
app.secret_key = "super-secret-key"  # for flash messages; change in real app

PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://products_service:5001")
PAYMENTS_SERVICE_URL = os.getenv("PAYMENTS_SERVICE_URL", "http://payments_service:5002")


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        products_response = requests.get(f"{PRODUCTS_SERVICE_URL}/products", timeout=3)
        products_response.raise_for_status()
        products = products_response.json()
    except Exception as e:
        products = []
        flash(f"Error fetching products: {e}", "error")

    if request.method == "POST":
        name = request.form.get("name")
        card_number = request.form.get("card_number")
        product_id = request.form.get("product_id")

        if not (name and card_number and product_id):
            flash("All fields are required.", "error")
            return render_template("index.html", products=products)

        # Find product price
        selected_product = next((p for p in products if str(p["id"]) == product_id), None)
        if not selected_product:
            flash("Invalid product selected.", "error")
            return render_template("index.html", products=products)

        amount = selected_product["price"]

        payment_payload = {
            "name": name,
            "card_number": card_number,
            "amount": amount
        }

        try:
            pay_response = requests.post(
                f"{PAYMENTS_SERVICE_URL}/pay",
                json=payment_payload,
                timeout=5
            )
            pay_response.raise_for_status()
            result = pay_response.json()
            if result.get("status") == "success":
                flash(f"Payment successful! Order placed for {selected_product['name']}.", "success")
            else:
                flash(f"Payment failed: {result.get('message', 'Unknown error')}", "error")
        except Exception as e:
            flash(f"Error processing payment: {e}", "error")

        return redirect(url_for("index"))

    return render_template("index.html", products=products)


if __name__ == "__main__":
    # When running inside Docker, it will bind on 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=True)
