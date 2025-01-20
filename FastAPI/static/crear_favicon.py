from PIL import Image

# Crear una imagen de 32x32 píxeles con color verde
img = Image.new('RGB', (32, 32), color='green')

# Guardar la imagen como favicon.ico
img.save('/favicon.ico')
