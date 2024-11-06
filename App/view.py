"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import sys
import App.logic as logic

def new_logic():
    """
    Se crea una instancia del controlador
    """
    control = logic.new_logic()
    return control

def print_menu():
    """
    Menú de usuario
    """
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de crímenes")
    print("3- Consultar crímenes en un rango de fechas")
    print("4- Consultar crímenes por código y fecha")
    print("5- Consultar crímenes en un rango de áreas")  
    print("0- Salir")
    print("*******************************************")

# main del ejercicio
def main():
    working = True
    crimefile = 'Boston Crimes//crime-utf8.csv'

    while working:
        print_menu()
        inputs = input("Seleccione una opción para continuar\n")
            
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            control = new_logic()
        elif int(inputs[0]) == 2:
            print("\nCargando información de crímenes ....")
            logic.load_data(control, crimefile)
            print('Crímenes cargados: ' + str(logic.crimes_size(control)))
            print('Altura del árbol: ' + str(logic.index_height(control)))
            print('Elementos en el árbol: ' + str(logic.index_size(control)))
            print('Menor Llave: ' + str(logic.min_key(control)))
            print('Mayor Llave: ' + str(logic.max_key(control)))
        elif int(inputs[0]) == 3:
            print("\nBuscando crímenes en un rango de fechas: ")
            initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
            finalDate = input("Fecha Final (YYYY-MM-DD): ")
            total = logic.get_crimes_by_range(control, initialDate, finalDate)
            print("\nTotal de crímenes en el rango de fechas: " + str(total))
        elif int(inputs[0]) == 4:
            print("\nBuscando crímenes por grupo de ofensa en una fecha: ")
            initialDate = input("Fecha (YYYY-MM-DD): ")
            offensecode = input("Ofensa: ")
            numoffenses = logic.get_crimes_by_range_code(control, initialDate, offensecode)
            print("\nTotal de ofensas tipo: " + offensecode + " en esa fecha:  " + str(numoffenses))
        elif int(inputs[0]) == 5:
            print("\nBuscando crímenes en un rango de áreas: ")
            initialArea = input("Área Inicial: ")
            finalArea = input("Área Final: ")
            total = logic.get_crimes_by_range_area(control, initialArea, finalArea)
            print("\nTotal de crímenes en el rango de áreas: " + str(total))
        else:
            sys.exit(0)
    sys.exit(0)