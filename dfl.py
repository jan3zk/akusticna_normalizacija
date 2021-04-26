# -*- coding: utf-8 -*-
import sys
sys.path.insert(1,'/path/to/SpeechDenoisingWithDeepFeatureLosses/')
from model import *
from data_import import *
import getopt
from glob import glob
import argparse

def run_senet():

  valfolder = args.in_dir
  modfolder = args.model_dir

  # SPEECH ENHANCEMENT NETWORK
  SE_LAYERS = 13 # NUMBER OF INTERNAL LAYERS
  SE_CHANNELS = 64 # NUMBER OF FEATURE CHANNELS PER LAYER
  SE_LOSS_LAYERS = 6 # NUMBER OF FEATURE LOSS LAYERS
  SE_NORM = "NM" # TYPE OF LAYER NORMALIZATION (NM, SBN or None)

  fs = 16000

  # SET LOSS FUNCTIONS AND PLACEHOLDERS
  with tf.variable_scope(tf.get_variable_scope()):
    input=tf.placeholder(tf.float32,shape=[None,1,None,1])
    clean=tf.placeholder(tf.float32,shape=[None,1,None,1])
        
    enhanced=senet(input, n_layers=SE_LAYERS, norm_type=SE_NORM, n_channels=SE_CHANNELS)

  # LOAD DATA
  folders = []
  for depth in range(args.maxdepth):
    path_str = '*' + os.sep
    path_str = os.path.join(args.in_dir, path_str*depth)
    folders += glob(path_str)

  valset = {}
  valset['innames'] = []
  valset['shortnames'] = []
  for fld in folders:
    tmp = load_noisy_data_list(valfolder = fld)
    valset['innames'].extend(tmp['innames'])
    valset['shortnames'].extend(tmp['shortnames'])
  valset = load_noisy_data(valset)

  # BEGIN SCRIPT #########################################################################################################

  # INITIALIZE GPU CONFIG
  config=tf.ConfigProto()
  config.gpu_options.allow_growth=True
  sess=tf.Session(config=config)

  print "Config ready"

  sess.run(tf.global_variables_initializer())

  print "Session initialized"

  saver = tf.train.Saver([var for var in tf.trainable_variables() if var.name.startswith("se_")])
  saver.restore(sess, "./%s/se_model.ckpt" % modfolder)

  #####################################################################################

  for id in tqdm(range(0, len(valset["innames"]))):

    i = id # NON-RANDOMIZED ITERATION INDEX
    inputData = valset["inaudio"][i] # LOAD DEGRADED INPUT

    # VALIDATION ITERATION
    output = sess.run([enhanced],
                        feed_dict={input: inputData})
    output = np.reshape(output, -1)
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    wavfile.write("%s/%s" % (args.out_dir,valset["shortnames"][i]), fs, output)


if __name__ == '__main__':
  ap = argparse.ArgumentParser(
    description = '''Ta skripta izvede odstranitev šuma s postopkom 
     DFL (ang. Deep Feature Losses).''')
  ap._action_groups.pop()
  required = ap.add_argument_group('Obvezni argumenti')
  optional = ap.add_argument_group('Opcijski argumenti')
  required.add_argument('-i','--in_dir',
    type = str,
    required = True,
    metavar = 'INPUT_DIR',
    help = 'Direktorij z vhodnimi datotekami WAV .')
  required.add_argument('-o','--out_dir',
    type = str,
    required = True,
    metavar = 'OUTPUT_DIR',
    help = 'Direktorij kamor se bodo shranjevale razšumljene datoteke WAV.')
  required.add_argument('-m','--model_dir',
    type = str,
    required = True,
    metavar = 'MODEL_DIR',
    help = 'Direktorij s SEnet modelom.')
  optional.add_argument('-x','--maxdepth',
    type = int,
    default = 1,
    help = 'Maksimalna globina poddirektorijev v katerih iščemo datoteke WAV.')
  

  args = ap.parse_args()
  run_senet()
