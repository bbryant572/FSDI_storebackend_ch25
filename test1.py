

def print_name():
    print("Brett Bryant")


def test_dict():
    print("-------- Dictionary---------")

    me = {
        "first": "Brett",
        "last": "Bryant",
        "age": 35,
        "hobbies": [],
        "address": {
            "street": "evergreen",
            "city": "springfield"
        }
    }

    print(me["first"] + " " + me["last"])

    address = me["address"]
    print(address["street"] + " " + address["city"])


def younger_person():
    ages = [12, 42, 32, 50, 56, 14, 78, 30, 51, 89, 12, 38, 67, 10]
    pivot = ages[0]
    for youngest in ages:
        if youngest < pivot:
            pivot = youngest
    print(f"The result is: {pivot}")


younger_person()
print_name()
test_dict()
