from PIL import Image, ImageTk
from colorsys import rgb_to_hls

textures = [
    Image.open("./assets/wall.png").convert("RGBA"), 
    Image.open("./assets/cracked_wall.png").convert("RGBA"),
    Image.open("./assets/suspicious_wall.png").convert("RGBA"),
    Image.open("./assets/door.png").convert("RGBA"),
    Image.open("./assets/door.png").convert("RGBA"),
]

spriteTextures = [
    Image.open("./assets/unstamped_assignments.png").convert("RGBA"), 
    Image.open("./assets/stamper_assignment.png").convert("RGBA"), 
    Image.open("./assets/stamp.png").convert("RGBA"), 
]

stamper = ImageTk.PhotoImage(image=Image.open("./assets/stamper.png").resize((256, 256)))

def deconstructImage(image):
    columns = []
    hlsColumns = []
    pixels = list(image.getdata())
    length = texture.size[0]
    
    for i in range(length):
        columns.append([])
        hlsColumns.append([])
        
    for i, v in enumerate(pixels):
        columns[i % length].append(v)
        hlsColumns[i % length].append(rgb_to_hls(*v[:3]))

    return (columns, hlsColumns, length)
    
textureMap = [()]
for texture in textures:
    textureMap.append(deconstructImage(texture))


spriteTextureMap = [()]
for texture in spriteTextures:
    spriteTextureMap.append(deconstructImage(texture))