# -*- coding: utf-8 -*-
import sys
sys.path.insert(1,'/media/sda1/janezk/projects/acoustic_norm/quality_measures/speechmetrics')
import os
from glob import glob
import csv
from tqdm import tqdm
import speechmetrics
import pandas as pd
import argparse


def run_speechmetrics(in_dir, ref_dir, maxdepth, out_file):
  
  folders = []
  for depth in range(maxdepth):
    path_str = '*' + os.sep
    path_str = os.path.join(in_dir, path_str*depth)
    folders += glob(path_str)

  in_folder = os.path.basename(os.path.dirname(os.path.join(in_dir,'')))
  fields = ['mosnet', 'srmr', 'wav_file']
  window_length = None
  abs_metrics = speechmetrics.load('absolute', window_length)
  if ref_dir:
    fields = ['mosnet', 'srmr',
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
          if ref_dir:
            ref = os.path.join(ref_dir,fle_clip)
            rel_scores = rel_metrics(fle, ref)
        except KeyboardInterrupt:
          sys.exit()
        except:
          print('Unable to compute quality scores for ' + fle +'.')
          if ref_dir:
            csvwriter.writerow(['','','','','','','','',fle_clip])
          else:
            csvwriter.writerow(['','',fle_clip])
        else:
          if ref_dir:
            csvwriter.writerow([abs_scores['mosnet'][0][0], abs_scores['srmr'],
              rel_scores['sdr'][0][0], rel_scores['isr'][0][0],
              rel_scores['sar'][0][0], rel_scores['pesq'],
              rel_scores['sisdr'], rel_scores['stoi'],
                                fle_clip])
          else:
            csvwriter.writerow([abs_scores['mosnet'][0][0], abs_scores['srmr'],
                                fle_clip])


if __name__ == '__main__':
  ap = argparse.ArgumentParser(
    description = '''Skripta za izračun abolutnih in relativnih metrik 
      kakovosti govornih posnetkov.''')
  ap._action_groups.pop()
  required = ap.add_argument_group('Obvezni argumenti')
  optional = ap.add_argument_group('Opcijski argumenti')
  required.add_argument('-i','--in_dir',
    type = str,
    required = True,
    metavar = 'INPUT_DIR',
    help = 'String containig the directory with WAV files.')
  required.add_argument('-o','--out_file',
    type = str,
    required = True,
    metavar = 'OUT_FILE',
    help = 'Izhodna datoteka z izračunanimi metrikami vhodnih posnetkov.')   
  optional.add_argument('-r','--ref_dir',
    default = '',
    type = str,
    help = '''Direktorij z referenčnimi daatotekami WAV. Nanaša se le na 
      relativne metrike. Ob predpostavljeni prazni vrednost se izračunajo le 
      absolutne metrike.''')
  optional.add_argument('-m','--maxdepth',
    default = 3,
    type = int,
    help = 'Maksimalna globina poddirektorijev v katerih iščemo datoteke WAV.')
   

  args = ap.parse_args()
  run_speechmetrics(args.in_dir, args.ref_dir, args.maxdepth, args.out_file)
