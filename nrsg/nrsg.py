import noisereduce as nr
import soundfile as sf
import argparse
import numpy as np
import os


def nrsg(filename, border = [.5, .5], verbose = 0, save_path = ''):

  # Read the recoreded speech
  data, rate = sf.read(filename)

  # Obtain noisy part
  b0 = int(rate*border[0])
  b1 = -int(rate*border[1])
  noise = np.append(data[:b0], data[b1:])

  # Remove noise  
  filtered = nr.reduce_noise(
    audio_clip=data,
    noise_clip=noise,
    verbose=bool(verbose))

  if save_path:
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
      os.makedirs(save_dir)
    sf.write(save_path, filtered, rate)

  return filtered


if __name__ == '__main__':

  ap = argparse.ArgumentParser(
    description = '''Noise reduction using spectral gating (NRSG).
    In order to run this code first install the repository
    noisereduce (https://github.com/timsainb/noisereduce).''')
  ap.add_argument('-f','--file',
    default = 'path/to/signal.vaw',
    type = str,
    help = 'String containig a path to the input file.')
  ap.add_argument('-b','--border',
    nargs=2,
    type = float,
    default = [.5, .5],
    help = 'Noise borders in seconds.')
  ap.add_argument('-s', '--save',
    default='',
    type=str,
    help='''A path where the denoised audio will be saved.
      If left empty (default) nothig is stored''')
  ap.add_argument('-v','--verbose',
    action='count',
    default=0)

  args = ap.parse_args()
  nrsg(args.file, args.border, args.verbose, args.save)
