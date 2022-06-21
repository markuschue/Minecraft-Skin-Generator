# This script provides a simpler, encapsulated and custom way of generating DALLE
# images.

from pathlib import Path
from tqdm import tqdm

# torch
import torch
from einops import repeat

# vision imports
from PIL import Image
from torchvision.utils import make_grid, save_image

# dalle related classes and utils
from dalle_pytorch import DiscreteVAE, DALLE
from dalle_pytorch.tokenizer import tokenizer

# Defining constants
IMAGE_NUM = 64
OUTPUT_DIR = './outputs'
TOP_K_FILTER_THRESHOLD = 0.9
BATCH_SIZE = 4

def exists(val):
  """
  Helper function to check if a value exists.
  @param val: value to check
  """
  return val is not None

def generate(text, dalle_path):
  """
  Main function for image generation.
  @param text: text prompt
  @returns outputs_dir: directory of generated images
  """
  # Load DALL-E
  dalle_path = Path(dalle_path)
  assert dalle_path.exists(), 'trained DALL-E must exist'

  load_obj = torch.load(str(dalle_path))
  dalle_params, vae_params, weights, vae_class_name, version = load_obj.pop('hparams'), load_obj.pop('vae_params'), load_obj.pop('weights'), load_obj.pop('vae_class_name', None), load_obj.pop('version', None)

  if exists(version):
    print(f'Loading a model trained with DALLE-pytorch version {version}')
  else:
    print('You are loading a model trained on an older version of DALL-E pytorch - it may not be compatible with the most recent version')

  # Load VAE
  vae = DiscreteVAE(**vae_params)
  assert not (exists(vae_class_name) and vae.__class__.__name__ != vae_class_name), f'you trained DALL-E using {vae_class_name} but are trying to generate with {vae.__class__.__name__} - please make sure you are passing in the correct paths and settings for the VAE to use for generation'

  # Reconstitute DALL-E
  dalle = DALLE(vae = vae, **dalle_params).cuda()
  dalle.load_state_dict(weights)

  # Generate images
  image_size = vae.image_size

  text_tokens = tokenizer.tokenize([text], dalle.text_seq_len).cuda()
  text_tokens = repeat(text_tokens, '() n -> b n', b = IMAGE_NUM)

  outputs = []

  for text_chunk in tqdm(text_tokens.split(BATCH_SIZE), desc = f'Generating images for - {text}'):
    output = dalle.generate_images(text_chunk, filter_thres = TOP_K_FILTER_THRESHOLD)
    outputs.append(output)

  outputs = torch.cat(outputs)

  # Save all images
  file_name = text 
  outputs_dir = Path(OUTPUT_DIR) / file_name.replace(' ', '_')[:(100)]
  outputs_dir.mkdir(parents = True, exist_ok = True)

  for i, image in tqdm(enumerate(outputs), desc = 'saving images'):
    save_image(image, outputs_dir / f'{i}.png', normalize=True)
    with open(outputs_dir / 'caption.txt', 'w') as f:
      f.write(file_name)

  print(f'created {IMAGE_NUM} images at "{str(outputs_dir)}"')
  return './' + str(outputs_dir)