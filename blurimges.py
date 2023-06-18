from skimage import io, util
#import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from pathlib import Path
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2

images = Path(IDD)
negative = Path("C:\\Users\\Security\\documents\\josephsy\\github\\dat\\negative")
blur = Path("C:\\Users\\Security\\documents\\josephsy\\github\\dat\\blur")
noise = Path("C:\\Users\\Security\\documents\\josephsy\\github\\dat\\noise2")
colors = Path("./stuff")


newNoise = colors / 'blank.jpg'
print (newNoise)
#     # Generate a single random RGB value
random_color = np.random.randint(0, 256, 3, dtype=np.uint8)

#     # Create a 512x512 array filled with the random RGB value
random_array = np.full((512, 512, 3), random_color, dtype=np.uint8)

#     # Create an image from the array
img = Image.fromarray(random_array)
img.save(newNoise)







    #random_array = np.random.randint(0, 256, (540, 800, 3), dtype=np.uint8)

    # Create an image from the array
    #img = Image.fromarray(random_array)
    #img.save(newNoise)


if False:
    for image in blur.iterdir():
        newNoise = noise / (image.stem + '.jpg')
        print (newNoise)
    # Read the image using skimage.io
        image = io.imread(image)

        # Add noise to the image
        noisy_image = util.random_noise(image)

        # The noisy image is in float format ranging from 0 to 1, so we have to convert it to uint8 format
        noisy_image = (255*noisy_image).astype('uint8')

        # Save the noisy image
        io.imsave(newNoise, noisy_image)    




if False:
    for image in images.iterdir():
        newNegative = negative / (image.stem + '.jpg')
        newBlur = blur / (image.stem + '.jpg')
        print (newNegative, newBlur)

            # if not newfile.exists():
            #     print (image)
        img = Image.open(image)
        negative_img = ImageOps.invert(img)
        negative_img.save(newNegative)
        blurred_img = negative_img.filter(ImageFilter.BLUR)
        blurred_img.save(newBlur)




# # Open the image file
# img = Image.open('image.jpg')

# # Convert the image to a negative image
# negative_img = ImageOps.invert(img)

# # Save the negative image
# negative_img.save('negative_image.jpg')
