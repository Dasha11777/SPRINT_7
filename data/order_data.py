order_colors = [
    ['BLACK'],
    ['GREY'],
    ['BLACK', 'GRAY'],
    []
]

def generation_new_order_data(color):    
    data = {
        "firstName": "Daria",
        "lastName": "Pilyukova",
        "address": "Prospekt Lenina, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 144 44 35",
        "rentTime": 5,
        "deliveryDate": "2025-09-06",
        "color": color
    }

    return data
