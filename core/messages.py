
# Function message response a view
def message_response_list(data, count):
    return {"status": "OK", "count": count, "data": data}

def message_response_detail(data):
    return {"status": "OK", "data": data}

def message_response_created(object:str, data):
    return {"status": "Created", "data": data, "message": f"{object} se creo con exito"}

def message_response_bad_request(object:str, errors, method:str):

    if method == "PUT" or method == "PATCH":
        return {"status": "Bad Request", "errors": errors, "message": f"Error, {object} no se actualizo"}
    elif method == "POST":
        return {"status": "Bad Request", "errors": errors, "message": f"Error, {object} no se creo"}

def message_response_no_content(object:str):
    return {"status": "No Content", "message": f"No tenemos {object} registradas"}

def message_response_update(object:str, data):
    return {"status": "Reset Content", "data": data, "message": f"Se actualizo {object} con exito"}

def validator_errors_message(message):
    return {"status": "Bad Request", "message": message}
