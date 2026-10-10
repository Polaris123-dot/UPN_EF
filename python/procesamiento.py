from validaciones import validar_cantidad, validar_precio


# Busca un producto por codigo mediante busqueda secuencial
def buscar_producto(productos, codigo):

    for posicion in range(len(productos)):
        if productos[posicion]["codigo"] == codigo:
            return posicion

    return -1




# Procesa y clasifica las modificaciones del catalogo
def preparar_cambios(productos, filas):

    nuevos = []
    for producto in productos:
        nuevos.append(producto.copy())

    aceptados = []
    errores = []
    sin_cambios = []

    conteo = {}

    for fila in filas:
        codigo = fila["codigo"]

        if codigo not in conteo:
            conteo[codigo] = 0
        conteo[codigo] = conteo[codigo] + 1


    for fila in filas:
        codigo = fila["codigo"]
        error = ""

        posicion = buscar_producto(productos, codigo)

        if codigo == "":
            error = "Falta el codigo."

        elif conteo[codigo] > 1:
            error = "Codigo repetido en el CSV. Se rechazan todas sus filas."

        elif posicion == -1:
            error = "El codigo no existe en el catalogo."

        if error == "":
            anterior = productos[posicion]

            cantidad = anterior["cantidad"]
            precio = anterior["precio"]

            if fila["nueva_cantidad"] != "":
                cantidad, error = validar_cantidad(fila["nueva_cantidad"])

            if error == "" and fila["nuevo_precio"] != "":
                precio, error = validar_precio(fila["nuevo_precio"])

            if error == "":
                if cantidad == anterior["cantidad"] and precio == anterior["precio"]:
                    sin_cambios.append(fila)
                else:

                    nuevos[posicion]["cantidad"] = cantidad
                    nuevos[posicion]["precio"] = precio

                    aceptados.append({"fila": fila["fila"], "anterior": anterior.copy(),
                                      "nuevo": nuevos[posicion].copy()})

        if error != "":
            errores.append({"fila": fila["fila"], "codigo": codigo, "motivo": error})

    return nuevos, aceptados, errores, sin_cambios
