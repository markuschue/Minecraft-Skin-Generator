# Simple script that reads the captions for each category and applies them to
# the corresponding images from that category in the dataset.
import os

data_dir = './dataset/MCSNetVAE/full_body/'
for cat in os.listdir(data_dir):
  category_path = data_dir + cat
  category_caption = ''
  if cat.endswith('.txt'):
    with open(category_path, 'r') as f:
      category_caption = f.read()
    category_path = category_path[:-4]
    for subcat in os.listdir(category_path):
      subcategory_path = category_path + '/' + subcat
      subcategory_caption = ''
      if subcat.endswith('.txt'):
        with open(subcategory_path , 'r') as f:
          subcategory_caption = f.read()
        subcategory_path = subcategory_path[:-4]
        for skin in os.listdir(subcategory_path):
          skin = skin[:-4] + '.txt'
          skin_dalle_path = './dataset/MCSNet/' + skin
          print('Adding from ' + subcategory_path + ': ' + category_caption + '\n' + subcategory_caption + '\n')
          with open(skin_dalle_path, 'a') as f:
            f.write('\n' + category_caption + '\n' + subcategory_caption + '\n')