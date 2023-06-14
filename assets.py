from PIL import Image

textures = [
    Image.open("./assets/wall.png").convert("RGBA"), 
    Image.open("./assets/cracked_wall.png").convert("RGBA"),
    Image.open("./assets/suspicious_wall.png").convert("RGBA"),
    Image.open("./assets/door.png").convert("RGBA"),
    Image.open("./assets/door.png").convert("RGBA"),
]

spriteTextures = [
    Image.open("./assets/unstamped_assignments.png").convert("RGBA"), 
    Image.open("./assets/stamp.png").convert("RGBA"), 
]

def deconstructImage(image):
    columns = []
    pixels = list(image.getdata())
    length = texture.size[0]
    
    for i in range(length):
        columns.append([])
        
    for i, v in enumerate(pixels):
        columns[i % length].append(v)

    return (columns, length)
    
textureMap = [()]
for texture in textures:
    textureMap.append(deconstructImage(texture))


spriteTextureMap = [()]
for texture in spriteTextures:
    spriteTextureMap.append(deconstructImage(texture))