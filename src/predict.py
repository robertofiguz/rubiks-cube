import helpers

        
def predicted_color(color,colors):
    converted_color = helpers.bgr2lab(color)
    distances = []
    for color_name, color_bgr in colors.prominent_color_palette.items():
        distances.append({
            'color_name': color_name,
            'color_bgr': color_bgr,
            'distance': helpers.ciede2000(converted_color, helpers.bgr2lab(color_bgr))
        })
    closest = min(distances, key=lambda item: item['distance'])['color_name']
    return closest