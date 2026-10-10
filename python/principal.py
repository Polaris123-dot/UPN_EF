from pathlib import Path
from decimal import InvalidOperation
from archivos import cargar_catalogo, cargar_cambios, guardar_catalogo
from procesamiento import preparar_cambios
from reportes import escribir_reporte

BASE = Path(__file__).resolve().parent.parent




# Solicita al usuario un archivo existente dentro de una carpeta
def pedir_archivo(carpeta, extension, mensaje):

    print("\n" + mensaje)
    print("Carpeta: " + str(carpeta))

    for ruta in sorted(carpeta.glob("*" + extension)):
        print("  " + ruta.name)

    while True:

        nombre = input("Escribe el nombre del archivo, o SALIR: ").strip()

        if nombre.upper() == "SALIR":
            return None

        ruta = carpeta / nombre

        if ruta.parent != carpeta or ruta.suffix.lower() != extension:
            print("Escribe solo un nombre de archivo con extension " + extension + ".")

        elif not ruta.is_file():
            print("No se encontro el archivo. Revisa el nombre e intenta otra vez.")
        else:
            return ruta




# Busca el siguiente correlativo libre para no sobreescribir archivos
def elegir_version():

    numero = 1

    while True:

        etiqueta = "v" + str(numero).zfill(3)

        catalogo = BASE / "txt" / ("catalogo_" + etiqueta + ".txt")
        reporte = BASE / "reportes" / ("reporte_" + etiqueta + ".txt")

        if not catalogo.exists() and not reporte.exists():
            return catalogo, reporte

        numero = numero + 1




# Funcion principal que controla el flujo de la aplicacion
def main():

    print("ACTUALIZACION DEL CATALOGO DE PRODUCTOS")
    print("El catalogo original se conserva. Los cambios se guardan al confirmar.")

    try:

        origen = pedir_archivo(BASE / "txt", ".txt", "PASO 1: Carga el catalogo actual.")

        if origen is None:
            print("Operacion cancelada. No se guardaron cambios.")
            return

        productos = cargar_catalogo(origen)
        print(str(len(productos)) + " productos cargados correctamente.")


        cambios = pedir_archivo(BASE / "excels", ".csv", "PASO 2: Carga el CSV exportado desde Excel.")

        if cambios is None:
            print("Operacion cancelada. No se guardaron cambios.")
            return

        filas = cargar_cambios(cambios)

        nuevos, aceptados, errores, sin_cambios = preparar_cambios(productos, filas)


        print("\nPASO 3: Revisa el resultado antes de guardar.")
        print("Filas revisadas: " + str(len(filas)))
        print("Productos con cambios validos: " + str(len(aceptados)))
        print("Filas rechazadas: " + str(len(errores)))
        print("Filas sin cambios: " + str(len(sin_cambios)))

        for cambio in aceptados:
            antes = cambio["anterior"]
            despues = cambio["nuevo"]
            print(antes["codigo"] + " | " + antes["descripcion"])
            print("  Cantidad: " + str(antes["cantidad"]) + " -> " + str(despues["cantidad"]))
            print("  Precio: " + format(antes["precio"], ".2f") + " -> " + format(despues["precio"], ".2f"))

        for error in errores:
            print("ERROR fila " + str(error["fila"]) + ": " + error["codigo"] + " - " + error["motivo"])


        while True:
            respuesta = input("Guardar los cambios validos y el reporte? SI / NO: ").strip().upper()
            if respuesta in ["SI", "NO"]:
                break
            print("Responde SI para guardar o NO para cancelar.")

        if respuesta == "NO":
            print("Operacion cancelada. No se guardaron cambios ni reportes.")
            return


        destino, reporte = elegir_version()

        guardar_catalogo(destino, nuevos)
        escribir_reporte(reporte, origen, cambios, destino, len(productos), aceptados, errores, sin_cambios)

        print("\nPASO 4: Proceso finalizado correctamente.")
        print("Catalogo actualizado: " + str(destino))
        print("Reporte de cambios: " + str(reporte))
        print("Carga este nuevo TXT en la proxima sesion.")

    except (OSError, ValueError, UnicodeError, InvalidOperation) as error:
        print("No se pudo completar el proceso: " + str(error))
        print("El archivo original se conserva. Revisa si se genero una salida parcial.")
    except (KeyboardInterrupt, EOFError):
        print("\nSesion interrumpida. Los cambios sin guardar se pierden.")


if __name__ == "__main__":
    main()
