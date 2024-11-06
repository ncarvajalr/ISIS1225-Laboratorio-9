"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import os
import csv
import datetime

from DataStructures.List import array_list as al
from DataStructures.Map import map_linearprobing as lp
from DataStructures.Tree import red_black_tree as rbt

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def new_logic():
    """
    Inicializa el analizador.
    Crea una lista vacia para guardar todos los crimenes.
    Se crean indices (Maps) por los siguientes criterios:
    - Fechas
    - Areas
    """
    analyzer = {
        "crimes": al.new_list(),
        "dateIndex": rbt.new_map(),
        "areaIndex": rbt.new_map()  # Creación del índice ordenado por áreas reportadas
    }
    return analyzer

# Funciones para realizar la carga
def load_data(analyzer, crimesfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    crimesfile = data_dir + crimesfile
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"), delimiter=",")
    for crime in input_file:
        add_crime(analyzer, crime)
    return analyzer

# Funciones para agregar informacion al analizador
def add_crime(analyzer, crime):
    """
    Agrega un crimen al catalogo
    """
    al.add_last(analyzer['crimes'], crime)
    update_date_index(analyzer['dateIndex'], crime)
    update_area_index(analyzer['areaIndex'], crime)  # Actualizar el índice por áreas reportadas
    return analyzer

def update_area_index(map, crime):
    """
    Actualiza el índice de áreas reportadas con un nuevo crimen.
    """
    area = crime.get("REPORTING_AREA", "9999")  # Área desconocida = 9999
    if area in ["", " ", None]:
        area = "9999"
    area_crimes = rbt.get(map, area)
    if area_crimes is None:
        area_entry = al.new_list()
        al.add_last(area_entry, crime)
        rbt.put(map, area, area_entry)
    else:
        al.add_last(area_crimes, crime)
    return map

def update_date_index(map, crime):
    """
    Actualiza el índice por fechas.
    """
    occurreddate = crime['OCCURRED_ON_DATE']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = rbt.get(map, crimedate.date())
    if entry is None:
        datentry = new_data_entry(crime)
        rbt.put(map, crimedate.date(), datentry)
    else:
        datentry = entry
    add_date_index(datentry, crime)
    return map

def add_date_index(datentry, crime):
    """
    Actualiza el índice de tipos de crímenes.
    """
    lst = datentry["lstcrimes"]
    al.add_last(lst, crime)
    offenseIndex = datentry["offenseIndex"]
    offentry = lp.get(offenseIndex, crime["OFFENSE_CODE_GROUP"])
    if offentry is None:
        entry = new_offense_entry(crime["OFFENSE_CODE_GROUP"], crime)
        al.add_last(entry["lstoffenses"], crime)
        lp.put(offenseIndex, crime["OFFENSE_CODE_GROUP"], entry)
    else:
        al.add_last(offentry["lstoffenses"], crime)
    return datentry

def new_data_entry(crime):
    """
    Crea una entrada en el índice por fechas.
    """
    entry = {'offenseIndex': lp.new_map(num_elements=30, load_factor=0.5), 'lstcrimes': al.new_list()}
    return entry

def new_offense_entry(offensegrp, crime):
    """
    Crea una entrada en el índice por tipo de crimen.
    """
    ofentry = {'offense': offensegrp, 'lstoffenses': al.new_list()}
    return ofentry

# ==============================
# Funciones de consulta
# ==============================

def crimes_size(analyzer):
    """
    Número de crímenes
    """
    return al.size(analyzer['crimes'])

def index_height(analyzer):
    """
    Altura del árbol por fechas
    """
    return rbt.height(analyzer["dateIndex"])

def index_size(analyzer):
    """
    Número de elementos en el índice por fechas
    """
    return rbt.size(analyzer["dateIndex"])

def min_key(analyzer):
    """
    Llave más pequeña por fechas
    """
    return rbt.left_key(analyzer["dateIndex"])

def max_key(analyzer):
    """
    Llave más grande por fechas
    """
    return rbt.right_key(analyzer["dateIndex"])

# Funciones de consulta para el índice de áreas
def index_height_areas(analyzer):
    """
    Altura del árbol por áreas
    """
    return rbt.height(analyzer["areaIndex"])

def index_size_areas(analyzer):
    """
    Número de elementos en el índice por áreas
    """
    return rbt.size(analyzer["areaIndex"])

def min_key_areas(analyzer):
    """
    Llave más pequeña por áreas
    """
    return rbt.left_key(analyzer["areaIndex"])

def max_key_areas(analyzer):
    """
    Llave más grande por áreas
    """
    return rbt.right_key(analyzer["areaIndex"])

def get_crimes_by_range_area(analyzer, initialArea, finalArea):
    """
    Retorna el número de crímenes en un rango de áreas
    """
    areas = rbt.values(analyzer["areaIndex"], initialArea, finalArea)
    totalcrimes = sum(al.size(area["elements"]) for area in areas)
    return totalcrimes

def get_crimes_by_range(analyzer, initialDate, finalDate):
    """
    Retorna el número de crímenes en un rango de fechas.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    lst = rbt.values(analyzer["dateIndex"], initialDate.date(), finalDate.date())
    totalcrimes = sum(al.size(lstdate["lstcrimes"]) for lstdate in lst["elements"])
    return totalcrimes

def get_crimes_by_range_code(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el número de crímenes de un tipo específico.
    """
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    crimedate = rbt.get(analyzer["dateIndex"], initialDate.date())
    if crimedate is not None:
        offensemap = crimedate["offenseIndex"]
        numoffenses = lp.get(offensemap, offensecode)
        if numoffenses is not None:
            return al.size(numoffenses["lstoffenses"])
    return 0
