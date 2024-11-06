from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as lt
import random

_EMPTY_ = "_EMPTY_"

def new_map(num_elements, load_factor, prime=109345121):
    """Crea un nuevo map con probing lineal"""
    capacity = mf.next_prime(int(num_elements / load_factor))
    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)
    table = [None] * capacity
    return {
        'prime': prime,
        'capacity': capacity,
        'scale': scale,
        'shift': shift,
        'table': table,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0,
        'type': 'PROBING'
    }

def put(my_map, key, value):
    """Agrega o reemplaza una pareja llave-valor en el map"""
    if my_map['current_factor'] >= my_map['limit_factor']:
        rehash(my_map)
    
    hash_value = mf.hash_value(my_map, key)
    occupied, slot = find_slot(my_map, key, hash_value)
    
    if occupied:
        my_map['table'][slot] = me.set_value(my_map['table'][slot], value)
    else:
        entry = me.new_map_entry(key, value)
        my_map['table'][slot] = entry
        my_map['size'] += 1
        my_map['current_factor'] = my_map['size'] / my_map['capacity']
    
    return my_map

def contains(my_map, key):
    """Verifica si el map contiene una llave"""
    hash_value = mf.hash_value(my_map, key)
    occupied, slot = find_slot(my_map, key, hash_value)
    return occupied

def get(my_map, key):
    """Obtiene el valor asociado a una llave"""
    hash_value = mf.hash_value(my_map, key)
    occupied, slot = find_slot(my_map, key, hash_value)
    
    if occupied:
        return me.get_value(my_map['table'][slot])
    else:
        return None

def remove(my_map, key):
    """Elimina una pareja llave-valor del map"""
    hash_value = mf.hash_value(my_map, key)
    occupied, slot = find_slot(my_map, key, hash_value)
    
    if occupied:
        my_map['table'][slot] = _EMPTY_
        my_map['size'] -= 1
        my_map['current_factor'] = my_map['size'] / my_map['capacity']
    
    return my_map

def size(my_map):
    """Devuelve el número de elementos en el map"""
    return my_map['size']

def is_empty(my_map):
    """Verifica si el map está vacío"""
    return my_map['size'] == 0

def key_set(my_map):
    """Devuelve todas las llaves en el map"""
    keys = lt.new_list()
    for entry in my_map['table']:
        if entry and entry != _EMPTY_:
            lt.add_last(keys, me.get_key(entry))
    return keys

def value_set(my_map):
    """Devuelve todos los valores en el map"""
    values = lt.new_list()
    for entry in my_map['table']:
        if entry and entry != _EMPTY_:
            lt.add_last(values, me.get_value(entry))
    return values

def find_slot(my_map, key, hash_value):
    """Encuentra un slot disponible o la llave en el map"""
    position = hash_value
    while not is_available(my_map['table'], position):
        if mf.default_compare(key, me.get_key(my_map['table'][position])) == 0:
            return True, position
        position = (position + 1) % my_map['capacity']
    
    return False, position

def is_available(table, pos):
    """Verifica si una posición está disponible"""
    return table[pos] is None or table[pos] == _EMPTY_

def rehash(my_map):
    """Rehash de todos los elementos en el map"""
    old_table = my_map['table']
    new_capacity = mf.next_prime(2 * my_map['capacity'])
    my_map['table'] = [None] * new_capacity
    my_map['capacity'] = new_capacity
    my_map['size'] = 0
    my_map['current_factor'] = 0
    
    for entry in old_table:
        if entry and entry != _EMPTY_:
            put(my_map, me.get_key(entry), me.get_value(entry))

def default_compare(key, element):
    """Comparación por defecto"""
    entry_key = me.get_key(element)
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    else:
        return-1