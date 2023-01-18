import numpy
from elasticdeform import deform_random_grid
import matplotlib.pyplot as plt
import numpy as np
import phantominator
from phantominator import ct_shepp_logan_params_2d
from phantominator import shepp_logan
import imgaug.augmenters as iaa
from random import randrange
import random

#dispays the image
def showImage(image):
    plt.title('Image')
    plt.imshow(image, cmap='gray',vmin=0,vmax=1)
    plt.show()

#return a vertically flipped image using the original image
def verticalRotation(image):
    vflip_obj = iaa.Flipud(p=1)
    vertical_flipped_image  = vflip_obj.augment_image(image)
    return vertical_flipped_image

#return a horizontally flipped image using the original image
def horizontalRotation(image):
    hflip_obj = iaa.Fliplr(p=1)
    horizontal_flipped_image = hflip_obj.augment_image(image)
    return horizontal_flipped_image

#return a image that has been flipped with specified degree user requests
def imageRotation(degree,image):
    rotation_object =iaa.Affine(rotate=(degree))
    rotated_image = rotation_object.augment_image(image)
    return rotated_image

#returns a image with deformations applied to it
def elasticDeformation(image):
    deformed_img = deform_random_grid(image, sigma=25, points=3, order=3, prefilter=True)
    return deformed_img

#returns a random ellipse
def createRandomEllipse():
    E = np.zeros((1, 6))
    E[0, :] = [random.random(),random.random(),random.random(),
            randrange(-1,1),random.random() * randrange(-1,1),randrange(-360,360)]
    return E

#performs the augmentation on all ellipses
def performAugmentation(degreeRotation,augment_list,image):
    final_image = image
    for x in augment_list:
        if x == 'elasticdeformation':
            final_image = elasticDeformation(final_image)
        elif x == 'rotation':
            final_image = imageRotation(degreeRotation,final_image)
        elif x == 'horizontalrotation':
            final_image = horizontalRotation(final_image)
        elif x == 'verticalrotation':
            final_image = verticalRotation(final_image)
    return final_image

def main():
    #creates the random ellipses to user amount specified
    degree = 0
    ellipse_list = []
    ellipse_images = []
    converted_ellipse_images = []
    number_of_ellipses = int(input("Please enter the amount of ellipses you would like to create\n"))
    for i in range(number_of_ellipses):
        ellipse_list.append(createRandomEllipse())
        ellipse_images.append(shepp_logan((256, 256), MR=False, E=ellipse_list[i], ret_E=False, zlims=(-.25, 25)))
        #used to show how it looks delete line of code below later
        numpy.save(f"original ellipse#{i+1}",ellipse_images[i])
        showImage(ellipse_images[i])
    '''try:
      augment = input('Enter desired image augmentations seperated by a space: ').split()
      augment_list = list(map(str,augment))
    except ValueError:
      print('empty or invalid input')
      exit(0)'''
    while True:
      try:
          augment = input('Enter desired image augmentations seperated by a space: ').split()
          augment_list = list(map(str,augment))
          break
      except ValueError:
          if len(augment)==0:
              print("you entered nothing")
          else:
              print("That was not a valid input, try again")

    
    for x in augment_list:
            print("x value",x)
    if x !='elasticdeformation' and x != 'rotation' and x != 'horizontalrotation' and x != 'verticalrotation':
            print('This is not an image augmentation, exiting the program')
            exit(0)
    if "rotation" in augment_list:
            degree = int(input('Enter desired rotation degree: '))
    for images in ellipse_images:
            new_image =performAugmentation(degree,augment_list,images)
            converted_ellipse_images.append(new_image)
    for j in range(len(converted_ellipse_images)):
            showImage(converted_ellipse_images[j])
            numpy.save(f"converted ellipse#{j+1}",ellipse_images[j])


    # merge the images and display it
    final_array = np.ndarray(shape=(256, 256), dtype=float, order='F')
    index_counter = 0
    total_sum = 0
    while index_counter < 256:
        for i in range(len(converted_ellipse_images)):
            total_sum += converted_ellipse_images[i][index_counter]
        final_array[index_counter] = total_sum / number_of_ellipses
        index_counter += 1
        total_sum = 0
    showImage(final_array)
    numpy.save(f"finalphantom",final_array)


if __name__ == "__main__":
    main()
