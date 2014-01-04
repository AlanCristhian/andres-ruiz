import os
import sys
import unittest


# change directroy for import my libraries
os.chdir('../..')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)
sys.path.append(currentDirectory + '/framework')


from framework.templates.helpers import set_responsive_image


url = '/project-folder/image.jpg'
htmlForImageSmall = set_responsive_image(url, 'thumbnail', 'small')
# htmlForImageMedium = set_responsive_image(url, 'image', 'medium')
# htmlForImageLarge = set_responsive_image(url, 'image', 'large')
# htmlForImageSizeNumber = set_responsive_image(url, 'image', '500')

# htmlForThumbnailSmall = set_responsive_image(url, 'thumbnail', 'small')
# htmlForThumbnailMedium = set_responsive_image(url, 'thumbnail', 'medium')
# htmlForThumbnailLarge = set_responsive_image(url, 'thumbnail', 'large')
# htmlForThumbnailSizeNumber = set_responsive_image(url, 'thumbnail', '1000')

print(htmlForImageSmall)
# print(htmlForImageMedium)
# print(htmlForImageLarge)
# print(htmlForImageSizeNumber)

# print(htmlForThumbnailSmall)
# print(htmlForThumbnailMedium)
# print(htmlForThumbnailLarge)
# print(htmlForThumbnailSizeNumber)