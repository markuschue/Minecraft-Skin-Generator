# Main file that generates the prompted skins, postprocesses them, and
# runs the viewer app.

from custom_generate import generate
from postprocess import postprocess
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Generate and postprocess skins.')