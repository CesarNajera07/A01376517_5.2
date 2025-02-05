"""
computeSales.py Calcula el costo total de las ventas basado en un catálogo.
Lee archivos JSON, procesa guarda los resultados en un archivo .txt.
"""

import json
import sys
import time
import os


def load_json(file_path):
    """Carga un archivo JSON y maneja posibles errores."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Archivo JSON inválido {file_path}")
        sys.exit(1)


def compute_total_cost(sales, price_catalogue):
    """Calcula el costo total de las ventas."""
    total_cost = 0
    for sale in sales:
        product_name = sale.get('Product')
        quantity = sale.get('Quantity', 0)

        # Buscar el producto en el catálogo por el nombre
        product = next(
            (item for item in price_catalogue
                if item.get('title') == product_name), None
        )
        if product:
            price = product.get('price', 0)
            total_cost += price * quantity
        else:
            print(f"Advertencia: '{product_name}' no encontrado en catálogo.")
    return total_cost


def process_sales(price_catalogue_file, sales_file):
    """Procesa un archivo de ventas y calcula el costo total."""
    price_catalogue = load_json(price_catalogue_file)
    sales_records = load_json(sales_file)

    start_time = time.time()
    total_cost = compute_total_cost(sales_records, price_catalogue)
    end_time = time.time()

    elapsed_time = end_time - start_time

    return total_cost, elapsed_time


def main():
    """Función principal que coordina la ejecución del programa."""
    if len(sys.argv) != 5:
        print("Uso incorrecto. El formato correcto es:")
        print("python computeSales.py priceCatalogue.json "
              "salesRecord1.json salesRecord2.json salesRecord3.json")
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_files = sys.argv[2:]  # Los tres archivos de ventas

    # Abrir el archivo de resultados para escribir
    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        # Escribir "TOTAL" en la segunda columna
        result_file.write(f"{'':<8}TOTAL\n")
        # Variable para guardar los resultados a imprimir más tarde
        result_lines = []

        for sales_file in sales_files:
            print(f"Procesando {sales_file}...")

            total_cost, elapsed_time = process_sales(
                price_catalogue_file, sales_file
            )

            # Extraer el nombre del archivo sin la extensión
            sales_file_name = os.path.splitext(os.path.basename(sales_file))[0]

            # Mostrar resultados en pantalla
            print(f"Total de ventas en {sales_file_name}: {total_cost:.2f}")
            print(f"T ejecución {sales_file_name}: {elapsed_time:.4f} s")

            # Agregar los resultados a las líneas para el archivo
            result_lines.append(f"{sales_file_name:<8}\t{total_cost:.2f}")

        # Escribir los resultados en el archivo después de la cabecera
        for line in result_lines:
            result_file.write(f"{line}\n")


if __name__ == "__main__":
    main()
