from glob import glob
import os
import csv
import sys
import numpy as np
import soundfile as sf
import noisereduce as nr
from tqdm import tqdm
import argparse


def nrsg(filename, border = [.5, .5], verbose = 0, save_path = ''):
  # Preberi posnetek govora
  data, rate = sf.read(filename)

  # Izoliraj pošumljeni del
  b0 = int(rate*border[0])
  b1 = -int(rate*border[1])
  noise = np.append(data[:b0], data[b1:])

  # Odstrani šum
  filtered = nr.reduce_noise(
    audio_clip=data,
    noise_clip=noise,
    verbose=bool(verbose))

  # Shrani razšumljeni signal
  if save_path:
    save_dir = os.path.dirname(os.path.abspath(save_path))
    if not os.path.exists(save_dir):
      os.makedirs(save_dir)
    sf.write(save_path, filtered, rate)


def main():

  if os.path.isdir(args.path):
    folders = []
    for depth in range(args.maxdepth):
      path_str = '*' + os.sep
      path_str = os.path.join(args.path, path_str*depth)
      folders += glob(path_str)

    root_folder = os.path.basename(os.path.dirname(os.path.join(args.path,'')))
    save_dir = args.out_path
    if not os.path.isdir(save_dir):
      os.makedirs(save_dir)

    for fld in tqdm(folders):
      files = sorted(glob(os.path.join(fld,'*.wav')))
      for fle in files:
        save_path = os.path.join(save_dir,
          fle[fle.find(root_folder)+len(root_folder)+1:])
        try:
          nrsg(fle, save_path=save_path)
          print('Razšumljen signal shranjen v %s'%save_path)
        except KeyboardInterrupt:
          sys.exit()
        except:
          print('Odstranitev šuma NRSG za ' + fle + ' ni mogoča.'
            ' Posnetek je verjetno prekratek ali napačnega formata.')

  elif os.path.isfile(args.path):
    nrsg(args.path, args.border, args.verbose, args.out_path)


if __name__ == '__main__':
  ap = argparse.ArgumentParser(
    description = '''Ta skripta izvede odstranitev šuma s postopkom 
     spektralnega razločevanja (ang. noise reduction using spectral gating, 
     NRSG).''')
  ap.add_argument('-p','--path',
    type = str,
    default = 'pot/do/dir/',
    help = '''Direktorij z datotekami WAV / pot do posamezne datoteke WAV.''')
  ap.add_argument('-m','--maxdepth',
    type = int,
    default = 3,
    help = 'Maksimalna globina poddirektorijev v katerih iščemo datoteke WAV.')
  ap.add_argument('-o','--out_path',
    type = str,
    default = './processed_audio/',
    help = 'Pot, kamor se bodo shranjevale WAV datoteke.')
  ap.add_argument('-b','--border',
    nargs=2,
    type = float,
    default = [.5, .5],
    help = 'Meje šuma v sekundah.')
  ap.add_argument('-v','--verbose',
    action='count',
    default=0)

  args = ap.parse_args()
  main()
