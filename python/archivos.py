import csv
from validaciones import validar_producto


# Lee archivos en formato tabla delimitados por punto y coma
def leer_tabla(ruta, columnas):

    filas = []

    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")

        if lector.fieldnames != columnas:
            raise ValueError("Columnas incorrectas. Deben ser: " + ";".join(columnas))

        for numero, fila in enumerate(lector, start=2):

            if None in fila or None in fila.values():
                raise ValueError("Fila " + str(numero) + ": faltan o sobran columnas.")

            for campo in columnas:
                fila[campo] = fila[campo].strip()

            fila["fila"] = numero

            filas.append(fila)

    if len(filas) == 0:
        raise ValueError("El archivo no tiene registros.")

    return filas




# Carga y valida todos los productos del catalogo TXT
def cargar_catalogo(ruta):

    filas = leer_tabla(ruta, ["codigo", "descripcion", "cantidad", "precio"])

    productos = []
    codigos = []

    for fila in filas:

        producto, error = validar_producto(fila)

        if error != "":
            raise ValueError("Catalogo, fila " + str(fila["fila"]) + ": " + error)

        if producto["codigo"] in codigos:
            raise ValueError("Codigo repetido en el catalogo: " + producto["codigo"])

        codigos.append(producto["codigo"])

        productos.append(producto)

    return productos




# Carga las modificaciones del archivo CSV
def cargar_cambios(ruta):

    return leer_tabla(ruta, ["codigo", "nueva_cantidad", "nuevo_precio"])




# Guarda el catalogo actualizado en un nuevo archivo TXT
def guardar_catalogo(ruta, productos):

    with open(ruta, "x", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo, delimiter=";")

        escritor.writerow(["codigo", "descripcion", "cantidad", "precio"])

        for producto in productos:

            escritor.writerow([producto["codigo"], producto["descripcion"],
                               producto["cantidad"], format(producto["precio"], ".2f")])
