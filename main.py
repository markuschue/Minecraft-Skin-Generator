# Main file that generates the prompted skins, postprocesses them, and
# runs the viewer app.

from custom_generate import generate
from postprocess import postprocess
from libs.viewer.app import run
import argparse, webbrowser, os, shutil


# Parse arguments
parser = argparse.ArgumentParser(description = 'Generate and postprocess skins.')
parser.add_argument('--dalle', type = str, required = False, help='The path to dalle.pt', default = './models/dalle.pt')
parser.add_argument('--no_viewer', action = 'store_true', help = 'Doesn\'t open the viewer app.')
parser.add_argument('--text', type = str, required = True, help='The text prompt')
args = parser.parse_args()

# Generation and postprocessing
output_dir = generate(args.text, args.dalle)
postprocess(output_dir)

# Copying images to the viewer and open viewer app
if not args.no_viewer:
  viewSkinPath = './libs/viewer/skins/'
  for file in os.listdir(viewSkinPath):
    os.remove(viewSkinPath + file)
  for file in os.listdir(output_dir):
    shutil.copy(output_dir + '/' + file, viewSkinPath)

  webbrowser.open('http://localhost:8080/libs/viewer/source/', new = 2)
  run()