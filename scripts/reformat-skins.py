# Search in the skins folder and replace all the skin files with size 64x32 with the new format of size 64x64
import os
import cv2

skins_dir = './dataset/MCSNet/'
for file in os.listdir(skins_dir):
    if file.endswith('.png'):
      img = cv2.imread(skins_dir + file, cv2.IMREAD_UNCHANGED)
      if img.shape == (32, 64, 4):
        # Add padding to the image to fit the new size 64x64
        img = cv2.copyMakeBorder(img, 0, 32, 0, 0, cv2.BORDER_CONSTANT, value = 0)

        # Copy the region of pixels corresponding to the legs and arms of the skin and paste it in the new image
        legs = img[16:32, 0:16]
        arms = img[16:32, 40:56]
        img[48:64, 16:32] = legs
        img[48:64, 32:48] = arms

        print("Saving " + file)
        cv2.imwrite(skins_dir + file, img)

# Checking all files are now 64x64
for file in os.listdir(skins_dir):
  if file.endswith('.png'):
    img = cv2.imread(skins_dir + file, cv2.IMREAD_UNCHANGED)
    if img.shape != (64, 64, 4):
      print("Error: " + file + " is not 64x64")
      exit(1)

print("Success! All files are now 64x64")