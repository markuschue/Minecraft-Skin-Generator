# Simple script to format the VizWiz dataset into the format required by the
# dalle-pytorch library. Takes the annotations from the VizWiz .json file and
# creates a folder structure with the annotations in the following format:
#  - dataset
#  |   - image1.jpg
#  |   - image1.txt
#  |   - image2.jpg
#  |   - image2.txt
#  |   - ...

import json

PATH = "./dataset/train/"

with open('./dataset/train.json') as json_file:
  data = json.load(json_file)

for img in data["images"]:
  currentImgName = img["file_name"]
  currentID = img["id"]
  currentCaptions = []
  for cap in data["annotations"]:
    if cap["image_id"] == currentID:
      currentCaptions.append(cap["caption"] + "\n")
    elif cap["image_id"] > currentID:
      break
  outputName = currentImgName[:-3] + "txt"
  ouputFile = open(PATH + outputName, "w")
  ouputFile.writelines(currentCaptions)
  ouputFile.close()
