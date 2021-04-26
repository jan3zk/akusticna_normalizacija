# -*- coding: utf-8 -*-
import sys
sys.path.insert(1,'/path/to/speechmetrics')
import os
from glob import glob
import csv
from tqdm import tqdm
import speechmetrics
import pandas as pd
import argparse
import numpy as np
import soundfile as sf


def snr(filename, border=[.5, .5], method='rms', verbose=0):
  
  # Read the input signal
  data, rate = sf.read(filename)

  # Split noisy part from the speech part.
  b0 = int(rate*border[0])
  b1 = -int(rate*border[1])
  speech = data[b0 : b1]
  noise = np.append(data[:b0], data[b1:])

  if speech.any(): 
    if method.lower() == 'fft':
    # https://stackoverflow.com/a/58464434
    
      # Power spectrum (averaged spectral density)
      speechPS = np.sum(np.abs(np.fft.fft(speech)/len(speech))**2)
      noisePS = np.sum(np.abs(np.fft.fft(noise)/len(noise))**2)

      SNR = 10*np.log10(speechPS/noisePS)
      if verbose:
        print('SNR_fft: '+str(SNR))
      
    elif method.lower() == 'rms':
    # https://medium.com/analytics-vidhya/adding-noise-to-audio-clips-5d8cee24ccb8
    
      # Root mean square (RMS) amplitude
      speechRMS = np.sqrt(np.mean(speech**2))
      noiseRMS = np.sqrt(np.mean(noise**2))

      SNR = 20*np.log10(speechRMS/noiseRMS)
      if verbose:
        print('SNR_rms: '+str(SNR))
    
    return SNR

def speech_quality_metrics(in_dir, ref_dir, maxdepth, out_file):

  folders = []
  for depth in range(maxdepth):
    path_str = '*' + os.sep
    path_str = os.path.join(in_dir, path_str*depth)
    folders += glob(path_str)

  in_folder = os.path.basename(os.path.dirname(os.path.join(in_dir,'')))
  fields = ['snr', 'mosnet', 'srmr', 'wav_file']
  window_length = None
  abs_metrics = speechmetrics.load('absolute', window_length)
  if ref_dir:
    fields = ['snr', 'mosnet', 'srmr',
      'sdr', 'isr', 'sar', 'pesq', 'sisdr', 'stoi',
      'wav_file']
    rel_metrics = speechmetrics.load('relative', window_length)
  csv_file = args.out_file
  
  with open(csv_file, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for fld in tqdm(folders):
      files = sorted(glob(os.path.join(fld,'*.wav')))
      for fle in files:
        fle_clip = fle[fle.find(in_folder)+len(in_folder)+1:]
        try:
          print('Computing metrics for %s.'%fle)
          abs_scores = abs_metrics(fle)
          snr_score = snr(fle, method='rms')
          if ref_dir:
            ref = os.path.join(ref_dir,fle_clip)
            rel_scores = rel_metrics(fle, ref)
        except KeyboardInterrupt:
          sys.exit()
        except:
          print('Unable to compute quality scores for ' + fle +'.')
          if ref_dir:
            csvwriter.writerow(['','','','','','','','','',fle_clip])
          else:
            csvwriter.writerow(['','','',fle_clip])
        else:
          if ref_dir:
            csvwriter.writerow([snr_score,
              abs_scores['mosnet'][0][0], abs_scores['srmr'],
              rel_scores['sdr'][0][0], rel_scores['isr'][0][0],
              rel_scores['sar'][0][0], rel_scores['pesq'],
              rel_scores['sisdr'], rel_scores['stoi'],
                                fle_clip])
          else:
            csvwriter.writerow([snr_score, abs_scores['mosnet'][0][0], 
                                abs_scores['srmr'], fle_clip])


if __name__ == '__main__':
  ap = argparse.ArgumentParser(
    description = '''Skripta za izračun absolutnih in relativnih metrik 
      kakovosti govornih posnetkov.''')
  ap._action_groups.pop()
  required = ap.add_argument_group('Obvezni argumenti')
  optional = ap.add_argument_group('Opcijski argumenti')
  required.add_argument('-i','--in_dir',
    type = str,
    required = True,
    metavar = 'INPUT_DIR',
    help = 'Vhodni direktorij z datotekami WAV.')
  required.add_argument('-o','--out_file',
    type = str,
    required = True,
    metavar = 'OUT_FILE',
    help = 'Izhodna datoteka CSV izračunanimi metrikami vhodnih posnetkov.')   
  optional.add_argument('-r','--ref_dir',
    default = '',
    type = str,
    help = '''Direktorij z referenčnimi datotekami WAV. Nanaša se le na 
      relativne metrike. Ob predpostavljeni prazni vrednost se izračunajo le 
      absolutne metrike.''')
  optional.add_argument('-m','--maxdepth',
    default = 3,
    type = int,
    help = 'Maksimalna globina poddirektorijev v katerih iščemo datoteke WAV.')
   

  args = ap.parse_args()
  speech_quality_metrics(args.in_dir, args.ref_dir, args.maxdepth, args.out_file)
