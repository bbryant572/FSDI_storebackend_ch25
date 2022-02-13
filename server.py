from calendar import c
from flask import Flask, abort
from mock_data import catalog
import json
from about_me import me, test

# create the server/app
app = Flask("server")


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
    return json.dumps(catalog)


@app.route("/api/catalog/count")
def catalog_length():
    count = len(catalog)
    return json.dumps(count)


@app.route("/api/catalog/sum")
def price_sum():
    total = 0
    for prod in catalog:
        total += prod["price"]

    res = f"${total}"
    return json.dumps(res)


@app.route("/api/product/<id>")
def get_product(id):
    for prod in catalog:
        if id == prod["_id"]:
            return json.dumps(prod)

    return abort(404)


@app.route("/api/product/most_expensive")
def most_expensive():
    pivot = catalog[0]
    for prod in catalog:
        if prod["price"] > pivot["price"]:
            pivot = prod

    return json.dumps(pivot)


# start the server
app.run(debug=True)
