
from flask import Flask, abort, request
from mock_data import catalog
import json
from about_me import me, test
import random
from flask_cors import CORS
from config import db
from bson import ObjectId

# create the server/app
app = Flask("server")
CORS(app)


@app.route("/myaddress")
def home_address():
    test()
    address = me["address"]
    # return address["street" + " " + address["city"]]
    return f"{address['street']} {address['city']}"


@app.route("/", methods=["get"])
def home_page():
    return "Under Construction!"


@app.route("/about")
def about_me():
    return "Brett Bryant"


@app.route("/test")
def test():
    return "I'm a simple test"


##################################################
############### API ENDPOINT #####################
##################################################


@app.route("/api/catalog")
def get_catalog():

    cursor = db.products.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()

    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "There should be a title. Title should be at least 5 chars long.")

    if not "price" in product:
        return abort(400, "Price is required.")

    if not "category" in product:
        return abort(400, "Must have a category.")

    if not isinstance(product["price"], int) and not isinstance(product["price"], float):
        return abort(400, "Price is a invalid.")

    if not (product["price"]) >= 0:
        return abort(400, "Price must be greater than free.")

    db.products.insert_one(product)

    product["_id"] = str(product["_id"])

    return json.dumps(product)


@app.route("/api/catalog/count")
def catalog_length():
    cursor = db.products.find({})
    count = 0
    for prod in cursor:
        count += 1

    json.dumps(count)


@app.route("/api/catalog/sum")
def price_sum():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    res = f"${total}"
    return json.dumps(res)


@app.route("/api/product/<id>")
def get_product(id):

    if not ObjectId.is_valid(id):
        return abort(400, "id is not a valid ObjectId")

    prod = db.products.find_one({"_id": ObjectId(id)})

    if not prod:
        return abort(404, "Product not found")

    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)

    # return abort(404)


@app.route("/api/product/most_expensive")
def most_expensive():
    pivot = cursor[0]
    cursor = db.products.find({})
    for prod in cursor:
        if prod["price"] > pivot["price"]:
            pivot = prod

    pivot["_id"] = str(pivot["_id"])
    return json.dumps(pivot)


@app.route("/api/categories")
def categories():

    cursor = db.products.find({})
    res = []
    for prod in cursor:
        category = prod["category"]

        if not category in res:
            res.append(category)

    return json.dumps(res)


@app.route("/api/catalog/<category>")
def products_by_category(category):

    res = []
    cursor = db.products.find({"category": category})
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        res.append(prod)

    return json.dumps(res)


##################################################
########## API METHOD FOR COUPON CODE ############
##################################################

coupons = []


@app.route("/api/coupons")
def get_coupons():
    cursor = db.coupons.find({})
    results = []
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)


@app.route("/api/coupons", methods=["POST"])
def save_coupons():
    coupon = request.get_json()

    db.coupons.insert_one(coupon)

    coupon["_id"] = str(coupon["_id"])

    return json.dumps(coupon)


@app.route("/api/coupons/<code>")
def get_coupon_by_code(code):
    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Coupon was not found for code: " + code)

    coupon["_id"] = str(coupon["_id"])
    return json.dumps(coupon)

##################################################
########## API METHOD FOR ORDERS #################
##################################################


@app.route("/api/orders", methods=["POST"])
def save_order():
    order = request.get_json()

    db.orders.insert_one(order)

    order["_id"] = str(order["_id"])

    return json.dumps(order)


@app.route("/api/orders")
def get_orders():
    cursor = db.orders.find({})
    results = []
    for order in cursor:
        order["_id"] = str(order["_id"])
        results.append(order)

    return json.dumps(results)


@app.route("/api/orders/<user_id>")
def get_order_by_user_id(user_id):
    cursor = db.orders.find({"user_id": int(user_id)})
    results = []
    for order in cursor:
        order["_id"] = str(order["_id"])
        results.append(order)

    return json.dumps(results)


# start the server
app.run(debug=True)
