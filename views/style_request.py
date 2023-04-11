STYLES = [
    {
        "id": 1, 
        "style": "Classic", 
        "price": 500 
    },
    {
        "id": 2, 
        "style": "Modern", 
        "price": 710 
    },
    {
        "id": 3, 
        "style": "Vintage", 
        "price": 965 
    }
    ]

def get_all_styles():
    """get all styles"""
    return STYLES

def get_single_style(id):
    requested_style = None
    for style in STYLES:
        if style['id'] == id:
            requested_style = style
    return requested_style

def create_style(style):
    max_id = STYLES[-1]['id']
    new_id = max_id + 1
    style['id'] = new_id
    STYLES.append(style)
    return style

def delete_style(id):

    style_index = -1

    for index, style in enumerate(STYLES):
        if style['id'] == id:
            style_index = index

    if style_index >= 0:
        STYLES.pop(style_index)

def update_style(id, new_style):

    for index, style in enumerate(STYLES):
        if style['id'] == id:
            STYLES[index] = new_style
            break
        