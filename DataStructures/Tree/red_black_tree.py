import rbt_node as rbt

def new_map():
    """
    Crea un árbol rojo-negro vacío.
    
    Returns:
        dict: Diccionario representando el árbol rojo-negro.
    """
    return {"root": None, "type": "RBT"}

def is_empty(my_rbt):
    """
    Verifica si el árbol está vacío.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
    
    Returns:
        bool: True si está vacío, False en caso contrario.
    """
    return my_rbt["root"] is None

def size(my_rbt):
    """
    Retorna el número de entradas en el árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
    
    Returns:
        int: Número de elementos en el árbol.
    """
    return size_tree(my_rbt["root"])

def size_tree(root):
    return root["size"] if root else 0

def put(my_rbt, key, value):
    """
    Inserta una pareja llave-valor en el árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
        key (any): La llave a insertar.
        value (any): El valor asociado.
    
    Returns:
        dict: El árbol actualizado.
    """
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    my_rbt["root"]["color"] = rbt.BLACK  # La raíz siempre debe ser negra
    return my_rbt

def insert_node(root, key, value):
    if root is None:
        return rbt.new_node(key, value, rbt.RED)

    cmp = default_compare(key, root["key"])
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value

    if rbt.is_red(root["right"]) and not rbt.is_red(root["left"]):
        root = rotate_left(root)
    if rbt.is_red(root["left"]) and rbt.is_red(root["left"].get("left")):
        root = rotate_right(root)
    if rbt.is_red(root["left"]) and rbt.is_red(root["right"]):
        flip_colors(root)

    root["size"] = size_tree(root["left"]) + size_tree(root["right"]) + 1
    return root

def get(my_rbt, key):
    """
    Obtiene el valor asociado a una llave en el árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
        key (any): La llave a buscar.
    
    Returns:
        any: El valor asociado, o None si no se encuentra.
    """
    return get_node(my_rbt["root"], key)

def get_node(root, key):
    while root:
        cmp = default_compare(key, root["key"])
        if cmp < 0:
            root = root["left"]
        elif cmp > 0:
            root = root["right"]
        else:
            return root["value"]
    return None

def remove(my_rbt, key):
    """
    Elimina una pareja llave-valor del árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
        key (any): La llave a eliminar.
    
    Returns:
        dict: El árbol actualizado.
    """
    if get(my_rbt, key) is not None:
        my_rbt["root"] = remove_key(my_rbt["root"], key)
        if my_rbt["root"]:
            my_rbt["root"]["color"] = rbt.BLACK
    return my_rbt

# Función recursiva para eliminar una llave
def remove_key(root, key):
    if default_compare(key, root["key"]) < 0:
        if not rbt.is_red(root["left"]) and not rbt.is_red(root["left"].get("left")):
            root = move_red_left(root)
        root["left"] = remove_key(root["left"], key)
    else:
        if rbt.is_red(root["left"]):
            root = rotate_right(root)
        if default_compare(key, root["key"]) == 0 and root["right"] is None:
            return None
        if not rbt.is_red(root["right"]) and not rbt.is_red(root["right"].get("left")):
            root = move_red_right(root)
        if default_compare(key, root["key"]) == 0:
            min_node = min_node_tree(root["right"])
            root["key"], root["value"] = min_node["key"], min_node["value"]
            root["right"] = delete_min(root["right"])
        else:
            root["right"] = remove_key(root["right"], key)

    return balance(root)

# Funciones auxiliares de rotación y balance
def rotate_left(h):
    x = h["right"]
    h["right"] = x["left"]
    x["left"] = h
    x["color"] = h["color"]
    h["color"] = rbt.RED
    x["size"] = h["size"]
    h["size"] = size_tree(h["left"]) + size_tree(h["right"]) + 1
    return x

def rotate_right(h):
    x = h["left"]
    h["left"] = x["right"]
    x["right"] = h
    x["color"] = h["color"]
    h["color"] = RED
    x["size"] = h["size"]
    h["size"] = size_tree(h["left"]) + size_tree(h["right"]) + 1
    return x

def flip_colors(h):
    h["color"] = RED
    h["left"]["color"] = BLACK
    h["right"]["color"] = BLACK

def move_red_left(h):
    flip_colors(h)
    if is_red(h["right"]["left"]):
        h["right"] = rotate_right(h["right"])
        h = rotate_left(h)
        flip_colors(h)
    return h

def move_red_right(h):
    flip_colors(h)
    if is_red(h["left"]["left"]):
        h = rotate_right(h)
        flip_colors(h)
    return h

def balance(h):
    if is_red(h["right"]):
        h = rotate_left(h)
    if is_red(h["left"]) and is_red(h["left"].get("left")):
        h = rotate_right(h)
    if is_red(h["left"]) and is_red(h["right"]):
        flip_colors(h)
    h["size"] = size_tree(h["left"]) + size_tree(h["right"]) + 1
    return h

# Función auxiliar de comparación
def default_compare(key, node_key):
    if key < node_key:
        return -1
    elif key > node_key:
        return 1
    else:
        return 0

from rbt_node import new_node, is_red, get_value, get_key, change_color, RED, BLACK

# Máscara para crear el árbol
def new_map():
    """
    Crea un árbol rojo-negro vacío.
    
    Returns:
        dict: Diccionario representando el árbol rojo-negro.
    """
    return {"root": None, "type": "RBT"}

# Máscara para verificar si el árbol está vacío
def is_empty(my_rbt):
    """
    Verifica si el árbol está vacío.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
    
    Returns:
        bool: True si está vacío, False en caso contrario.
    """
    return my_rbt["root"] is None

# Máscara para contar el tamaño
def size(my_rbt):
    """
    Retorna el número de entradas en el árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
    
    Returns:
        int: Número de elementos en el árbol.
    """
    return size_tree(my_rbt["root"])

# Función recursiva para contar el tamaño
def size_tree(root):
    return root["size"] if root else 0

# Máscara para insertar una llave-valor
def put(my_rbt, key, value):
    """
    Inserta una pareja llave-valor en el árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
        key (any): La llave a insertar.
        value (any): El valor asociado.
    
    Returns:
        dict: El árbol actualizado.
    """
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    my_rbt["root"]["color"] = BLACK  # La raíz siempre debe ser negra
    return my_rbt

# Función recursiva para insertar una llave-valor
def insert_node(root, key, value):
    if root is None:
        return new_node(key, value, RED)

    cmp = default_compare(key, root["key"])
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value

    # Ajuste de árbol rojo-negro
    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"].get("left")):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)

    root["size"] = size_tree(root["left"]) + size_tree(root["right"]) + 1
    return root

# Máscara para obtener un valor
def get(my_rbt, key):
    """
    Obtiene el valor asociado a una llave en el árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
        key (any): La llave a buscar.
    
    Returns:
        any: El valor asociado, o None si no se encuentra.
    """
    return get_node(my_rbt["root"], key)

# Función recursiva para obtener un valor
def get_node(root, key):
    while root:
        cmp = default_compare(key, root["key"])
        if cmp < 0:
            root = root["left"]
        elif cmp > 0:
            root = root["right"]
        else:
            return root["value"]
    return None

# Máscara para eliminar una llave
def remove(my_rbt, key):
    """
    Elimina una pareja llave-valor del árbol.
    
    Args:
        my_rbt (dict): El árbol rojo-negro.
        key (any): La llave a eliminar.
    
    Returns:
        dict: El árbol actualizado.
    """
    if get(my_rbt, key) is not None:
        my_rbt["root"] = remove_key(my_rbt["root"], key)
        if my_rbt["root"]:
            my_rbt["root"]["color"] = BLACK
    return my_rbt

# Función recursiva para eliminar una llave
def remove_key(root, key):
    if default_compare(key, root["key"]) < 0:
        if not is_red(root["left"]) and not is_red(root["left"].get("left")):
            root = move_red_left(root)
        root["left"] = remove_key(root["left"], key)
    else:
        if is_red(root["left"]):
            root = rotate_right(root)
        if default_compare(key, root["key"]) == 0 and root["right"] is None:
            return None
        if not is_red(root["right"]) and not is_red(root["right"].get("left")):
            root = move_red_right(root)
        if default_compare(key, root["key"]) == 0:
            min_node = min_node_tree(root["right"])
            root["key"], root["value"] = min_node["key"], min_node["value"]
            root["right"] = delete_min(root["right"])
        else:
            root["right"] = remove_key(root["right"], key)

    return balance(root)

# Funciones auxiliares de rotación y balance
def rotate_left(h):
    x = h["right"]
    h["right"] = x["left"]
    x["left"] = h
    x["color"] = h["color"]
    h["color"] = RED
    x["size"] = h["size"]
    h["size"] = size_tree(h["left"]) + size_tree(h["right"]) + 1
    return x

def rotate_right(h):
    x = h["left"]
    h["left"] = x["right"]
    x["right"] = h
    x["color"] = h["color"]
    h["color"] = RED
    x["size"] = h["size"]
    h["size"] = size_tree(h["left"]) + size_tree(h["right"]) + 1
    return x

def flip_colors(h):
    h["color"] = RED
    h["left"]["color"] = BLACK
    h["right"]["color"] = BLACK

def move_red_left(h):
    flip_colors(h)
    if is_red(h["right"]["left"]):
        h["right"] = rotate_right(h["right"])
        h = rotate_left(h)
        flip_colors(h)
    return h

def move_red_right(h):
    flip_colors(h)
    if is_red(h["left"]["left"]):
        h = rotate_right(h)
        flip_colors(h)
    return h

def balance(h):
    if is_red(h["right"]):
        h = rotate_left(h)
    if is_red(h["left"]) and is_red(h["left"].get("left")):
        h = rotate_right(h)
    if is_red(h["left"]) and is_red(h["right"]):
        flip_colors(h)
    h["size"] = size_tree(h["left"]) + size_tree(h["right"]) + 1
    return h

# Función auxiliar de comparación
def default_compare(key, node_key):
    if key < node_key:
        return -1
    elif key > node_key:
        return 1
    else:
        return 0

def min_node_tree(root):
    """
    Encuentra el nodo con la clave mínima en el subárbol dado.
    
    Args:
        root (dict): Nodo raíz del subárbol.
    
    Returns:
        dict: Nodo con la clave mínima.
    """
    while root["left"] is not None:
        root = root["left"]
    return root

# Función para eliminar el nodo con la clave mínima en un subárbol
def delete_min(root):
    """
    Elimina el nodo con la clave mínima en el subárbol dado.
    
    Args:
        root (dict): Nodo raíz del subárbol.
    
    Returns:
        dict: El subárbol sin el nodo de clave mínima.
    """
    if root["left"] is None:
        return None

    if not is_red(root["left"]) and not is_red(root["left"].get("left")):
        root = move_red_left(root)
    
    root["left"] = delete_min(root["left"])
    return balance(root)