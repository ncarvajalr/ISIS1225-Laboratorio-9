def new_list():
    """
    Crea una lista implementada con un Array List vacío.
    Returns: Lista creada
    """
    return {'size': 0, 'elements': []}

def add_first(my_list, element):
    """
    Agrega un elemento al ArrayList en la primera posición.
    """
    my_list['elements'].insert(0, element)
    my_list['size'] += 1
    return my_list

def add_last(my_list, element):
    """
    Agrega un elemento en la última posición de la lista.
    """
    my_list['elements'].append(element)
    my_list['size'] += 1
    return my_list

def is_empty(my_list):
    """
    Indica si la lista está vacía
    """
    return my_list['size'] == 0

def size(my_list):
    """
    Retorna el número de elementos de la lista.
    """
    return my_list['size']

def first_element(my_list):
    """
    Retorna el primer elemento de una lista no vacía.
    """
    if not is_empty(my_list):
        return my_list['elements'][0]
    return None

def last_element(my_list):
    """
    Retorna el último elemento de una lista no vacía.
    """
    if not is_empty(my_list):
        return my_list['elements'][-1]
    return None

def get_element(my_list, pos):
    """
    Retorna el elemento en la posición pos de la lista.
    """
    if 0 <= pos < size(my_list):
        return my_list['elements'][pos]
    return None

def delete_element(my_list, pos):
    """
    Elimina el elemento en la posición pos de la lista.
    """
    if 0 <= pos < size(my_list):
        my_list['elements'].pop(pos)
        my_list['size'] -= 1
    return my_list

def remove_first(my_list):
    """
    Remueve el primer elemento de la lista.
    """
    if not is_empty(my_list):
        element = my_list['elements'].pop(0)
        my_list['size'] -= 1
        return element
    return None

def remove_last(my_list):
    """
    Remueve el último elemento de la lista.
    """
    if not is_empty(my_list):
        element = my_list['elements'].pop()
        my_list['size'] -= 1
        return element
    return None

def insert_element(my_list, element, pos):
    """
    Inserta el elemento element en la posición pos de la lista.
    """
    if 0 <= pos <= size(my_list):
        my_list['elements'].insert(pos, element)
        my_list['size'] += 1
    return my_list

def is_present(my_list, element, cmp_function=None):
    """
    Informa si el elemento element esta presente en la lista.
    """
    if cmp_function is None:
        cmp_function = default_function
    
    for i in range(size(my_list)):
        if cmp_function(my_list['elements'][i], element) == 0:
            return i
    return -1

def change_info(my_list, pos, new_info):
    """
    Cambia la información contenida en el nodo de la lista.
    """
    if 0 <= pos < size(my_list):
        my_list['elements'][pos] = new_info
    return my_list

def exchange(my_list, pos1, pos2):
    """
    Intercambia la información en las posiciones pos1 y pos2 de la lista.
    """
    if 0 <= pos1 < size(my_list) and 0 <= pos2 < size(my_list):
        my_list['elements'][pos1], my_list['elements'][pos2] = \
            my_list['elements'][pos2], my_list['elements'][pos1]
    return my_list

def sub_list(my_list, pos, num_elem):
    """
    Retorna una sub-lista de la lista recibida.
    """
    new_list_dict = new_list()
    if 0 <= pos < size(my_list):
        end = min(pos + num_elem, size(my_list))
        new_list_dict['elements'] = my_list['elements'][pos:end][:]
        new_list_dict['size'] = end - pos
    return new_list_dict

def compare_elements(my_list, element, info, cmp_function=None):
    """
    Compara el elemento element con el elemento info.
    """
    if cmp_function is None:
        return default_function(element, info)
    return cmp_function(element, info)

def default_function(id1, id2):
    """
    Función de comparación por defecto
    """
    if id1 > id2:
        return 1
    elif id1 < id2:
        return -1
    return 0

def selection_sort(my_list, sort_crit):
    """
    Implementación del algoritmo Selection Sort
    """
    if size(my_list) <= 1:
        return my_list
    
    for i in range(size(my_list)):
        min_idx = i
        for j in range(i + 1, size(my_list)):
            if sort_crit(my_list['elements'][j], my_list['elements'][min_idx]):
                min_idx = j
        if min_idx != i:
            exchange(my_list, i, min_idx)
    
    return my_list

def insertion_sort(my_list, sort_crit):
    """
    Implementación del algoritmo Insertion Sort
    """
    if size(my_list) <= 1:
        return my_list
    
    for i in range(1, size(my_list)):
        key = my_list['elements'][i]
        j = i - 1
        while j >= 0 and sort_crit(key, my_list['elements'][j]):
            my_list['elements'][j + 1] = my_list['elements'][j]
            j -= 1
        my_list['elements'][j + 1] = key
    
    return my_list

def shell_sort(my_list, sort_crit):
    """
    Implementación del algoritmo Shell Sort
    """
    if size(my_list) <= 1:
        return my_list
    
    n = size(my_list)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = my_list['elements'][i]
            j = i
            while j >= gap and sort_crit(temp, my_list['elements'][j - gap]):
                my_list['elements'][j] = my_list['elements'][j - gap]
                j -= gap
            my_list['elements'][j] = temp
        gap //= 2
    
    return my_list

def merge_sort(my_list, sort_crit):
    """
    Implementación del algoritmo Merge Sort
    """
    if size(my_list) <= 1:
        return my_list
    
    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if sort_crit(left[i], right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    middle = size(my_list) // 2
    left = my_list['elements'][:middle]
    right = my_list['elements'][middle:]
    
    left = merge_sort({'elements': left, 'size': len(left)}, sort_crit)['elements']
    right = merge_sort({'elements': right, 'size': len(right)}, sort_crit)['elements']
    
    my_list['elements'] = merge(left, right)
    return my_list

def quick_sort(my_list, sort_crit):
    """
    Función principal de Quick Sort
    """
    if size(my_list) <= 1:
        return my_list
    
    quick_sort_recursive(my_list, 0, size(my_list) - 1, sort_crit)
    return my_list

def quick_sort_recursive(my_list, lo, hi, sort_crit):
    """
    Implementación recursiva del algoritmo Quick Sort
    """
    if lo < hi:
        pivot = partition(my_list, lo, hi, sort_crit)
        quick_sort_recursive(my_list, lo, pivot - 1, sort_crit)
        quick_sort_recursive(my_list, pivot + 1, hi, sort_crit)

def partition(my_list, lo, hi, sort_crit):
    """
    Función de partición para Quick Sort
    """
    pivot = my_list['elements'][hi]
    i = lo - 1
    
    for j in range(lo, hi):
        if sort_crit(my_list['elements'][j], pivot):
            i += 1
            my_list['elements'][i], my_list['elements'][j] = \
                my_list['elements'][j], my_list['elements'][i]
    
    my_list['elements'][i + 1], my_list['elements'][hi] = \
        my_list['elements'][hi], my_list['elements'][i + 1]
    
    return i + 1

def default_sort_criteria(element1, element2):
    """
    Criterio de ordenamiento por defecto (orden ascendente)
    """
    return element1 < element2