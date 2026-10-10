from datetime import datetime




# Genera el archivo de reporte con el resumen de la actualizacion
def escribir_reporte(ruta, origen, cambios, destino, total, aceptados, errores, sin_cambios):

    with open(ruta, "x", encoding="utf-8") as archivo:

        archivo.write("REPORTE DE ACTUALIZACION DEL CATALOGO\n")
        archivo.write("=" * 60 + "\n")

        archivo.write("Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " (hora del equipo)\n")
        archivo.write("Catalogo original: " + origen.name + "\n")
        archivo.write("Archivo de cambios: " + cambios.name + "\n")
        archivo.write("Catalogo generado: " + destino.name + "\n\n")

        archivo.write("Productos cargados: " + str(total) + "\n")
        archivo.write("Productos actualizados: " + str(len(aceptados)) + "\n")
        archivo.write("Filas rechazadas: " + str(len(errores)) + "\n")
        archivo.write("Filas sin cambios: " + str(len(sin_cambios)) + "\n\n")

        archivo.write("CAMBIOS APLICADOS\n" + "-" * 60 + "\n")

        for cambio in aceptados:
            antes = cambio["anterior"]
            despues = cambio["nuevo"]

            archivo.write("Producto: " + antes["codigo"] + " - " + antes["descripcion"] + "\n")
            archivo.write("Fila del CSV: " + str(cambio["fila"]) + "\n")
            archivo.write("Cantidad: " + str(antes["cantidad"]) + " -> " + str(despues["cantidad"]) + "\n")
            archivo.write("Precio S/: " + format(antes["precio"], ".2f") + " -> " + format(despues["precio"], ".2f") + "\n\n")

        archivo.write("REGISTROS RECHAZADOS\n" + "-" * 60 + "\n")

        for error in errores:
            archivo.write("Fila " + str(error["fila"]) + " | Codigo: " + error["codigo"] + "\n")
            archivo.write("Motivo: " + error["motivo"] + "\n\n")

        archivo.write("REGISTROS SIN CAMBIOS\n" + "-" * 60 + "\n")

        for fila in sin_cambios:
            archivo.write("Fila " + str(fila["fila"]) + " | Codigo: " + fila["codigo"] + "\n")
