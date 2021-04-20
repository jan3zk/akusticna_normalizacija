from glob import glob
import os
import csv
from tqdm import tqdm
from nrsg import nrsg
import argparse


def run_nrsg():

  folders = []
  for depth in range(args.maxdepth):
    path_str = '*' + os.sep
    path_str = os.path.join(args.dir, path_str*depth)
    folders += glob(path_str)

  root_folder = os.path.basename(os.path.dirname(os.path.join(args.dir,'')))
  save_dir = args.out_dir
  if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

  for fld in tqdm(folders):
    files = sorted(glob(os.path.join(fld,'*.wav')))
    for fle in files:
      save_path = os.path.join(save_dir,
        fle[fle.find(root_folder)+len(root_folder)+1:])
      try:
        #import ipdb; ipdb.set_trace()
        nrsg(fle, save_path=save_path)
        print('Denoised signal saved to %s'%save_path)
      except:
        print('Unable to compute the NRSG for ' + fle +
          '. The signal is probably too short or the audio format is wrong.')


if __name__ == '__main__':
  ap = argparse.ArgumentParser(
    description = '''This script performs the noise reduction using
     spectral gating (NRSG) on WAV files from the input directory and
     its subdirectories down to the level defined by maxdepth argument. 
     In order to run this code the repository noisereduce
     (https://github.com/timsainb/noisereduce) should be installed first.''')
  ap.add_argument('-d','--dir',
    type = str,
    default = 'path/to/dir/',
    help = 'String containig the directory with WAV files.')
  ap.add_argument('-m','--maxdepth',
    type = int,
    default = 3,
    help = 'Maximum depth of subdirectories in which to search for WAV files.')
  ap.add_argument('-o','--out_dir',
    type = str,
    default = './processed_audio/',
    help = 'Path where proceesed audio files will be stored.')

  args = ap.parse_args()
  run_nrsg()
