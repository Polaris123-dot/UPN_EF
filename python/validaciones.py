from decimal import Decimal, InvalidOperation


# Valida que la cantidad sea un entero mayor o igual a cero
def validar_cantidad(texto):

    if not texto.isascii() or not texto.isdigit():
        return None, "La cantidad debe ser un entero mayor o igual a cero."

    return int(texto), ""




# Valida que el precio sea un numero no negativo con hasta dos decimales
def validar_precio(texto):

    try:
        precio = Decimal(texto.replace(",", "."))
    except InvalidOperation:
        return None, "El precio debe ser un numero."

    if not precio.is_finite() or precio < 0:
        return None, "El precio debe ser finito y mayor o igual a cero."

    try:
        precio_redondeado = precio.quantize(Decimal("0.01"))
    except InvalidOperation:
        return None, "El precio es demasiado grande para procesarlo."

    if precio != precio_redondeado:
        return None, "El precio debe tener como maximo dos decimales."

    return precio, ""




# Valida los datos obligatorios del producto en el catalogo
def validar_producto(fila):

    if fila["codigo"] == "" or fila["descripcion"] == "":
        return None, "El codigo y la descripcion son obligatorios."

    cantidad, error = validar_cantidad(fila["cantidad"])

    if error != "":
        return None, error

    precio, error = validar_precio(fila["precio"])
    if error != "":
        return None, error

    producto = {"codigo": fila["codigo"], "descripcion": fila["descripcion"],
                "cantidad": cantidad, "precio": precio}

    return producto, ""
