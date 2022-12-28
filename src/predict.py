import helpers
prominent_color_palette = {
    'red'   : (0, 0, 255),
    'orange': (0, 130, 255),
    'blue'  : (255, 0, 0),
    'green' : (0, 255, 0),
    'white' : (255, 255, 255),
    'yellow': (0, 255, 255)
}
        
def predicted_color(color):
    converted_color = helpers.bgr2lab(color)
    distances = []
    for color_name, color_bgr in prominent_color_palette.items():
        distances.append({
            'color_name': color_name,
            'color_bgr': color_bgr,
            'distance': helpers.ciede2000(converted_color, helpers.bgr2lab(color_bgr))
        })
    closest = min(distances, key=lambda item: item['distance'])['color_name']
    return closest