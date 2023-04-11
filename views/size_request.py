SIZES = [
    { 
        "id": 1, 
        "carets": 0.5, 
        "price": 405 
    },
    {
        "id": 2, 
        "carets": 0.75, 
        "price": 782 
    },
    { 
        "id": 3, 
        "carets": 1, 
        "price": 1470 
    },
    { 
        "id": 4, 
        "carets": 1.5, 
        "price": 1997 
    },
    { 
        "id": 5, 
        "carets": 2, 
        "price": 3638 
    }
]

def get_all_sizes():
    """get all sizes"""
    return SIZES

def get_single_size(id):
    requested_size = None

    for size in SIZES:
        if size['id'] == id:
            requested_size = size
    return requested_size

def create_size(size):
    max_id = SIZES[-1]['id']
    new_id = max_id + 1
    size['id'] = new_id
    SIZES.append(size)
    return size

def delete_size(id):
    size_index = -1

    for index, size in enumerate(SIZES):
        if size['id'] == id:
            size_index = index
    if size_index >= 0:
        SIZES.pop(size_index)

def update_size(id, new_size):

    for index, size in enumerate(SIZES):
        if size['id'] == id:
            SIZES[index] = new_size
            break 