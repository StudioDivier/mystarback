from PIL import Image, ImageOps

mask = Image.open('media/avatars/1551512888_2.jpg').convert('L')
im = Image.open('image.png')

output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
output.putalpha(mask)

output.save('output.png')