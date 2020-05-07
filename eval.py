import argparse
import os
import re
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer


def get_output_base_path(checkpoint_path):
  base_dir = os.path.dirname(checkpoint_path)
  m = re.compile(r'.*?\.ckpt\-([0-9]+)').match(checkpoint_path)
  name = 'eval-%d' % int(m.group(1)) if m else 'eval'
  return os.path.join(base_dir, name)


def run_eval(args, sentences):
  print(hparams_debug_string())
  synth = Synthesizer()
  synth.load(args.checkpoint)
  base_path = get_output_base_path(args.checkpoint)
  for i, text in enumerate(sentences):
    path = '%s-%d.wav' % (base_path, i)
    txtpath = path.replace('.wav', '.txt')
    print('Synthesizing: %s' % path)
    with open(path, 'wb') as f:
      f.write(synth.synthesize(text))
    with open(txtpath, 'w') as f:
      f.write('{}\n'.format(text))

def get_sentences(textfile):
  sentences = open(textfile, 'r').readlines()
  sentences = [sent.rstrip() for sent in sentences]
  return sentences

def main():

  sentences = [
    # From July 8, 2017 New York Times:
    'Scientists at the CERN laboratory say they have discovered a new particle.',
    'There’s a way to measure the acute emotional intelligence that has never gone out of style.',
    'President Trump met with other leaders at the Group of 20 conference.',
    'The Senate\'s bill to repeal and replace the Affordable Care Act is now imperiled.',
    # From Google's Tacotron example page:
    'Generative adversarial network or variational auto-encoder.',
    'The buses aren\'t the problem, they actually provide a solution.',
    'Does the quick brown fox jump over the lazy dog?',
    'Talib Kweli confirmed to AllHipHop that he will be releasing an album in the next year.',
  ]

  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', required=True, help='Path to model checkpoint')
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  parser.add_argument('--textfile', default='', help='File with sentences')
  args = parser.parse_args()

  # read in sentences if specified
  if args.textfile:
    sentences = get_sentences(args.textfile)

  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  hparams.parse(args.hparams)
  print('sentences to be synthesized:')
  print('\n'.join(sentences))
  run_eval(args, sentences)


if __name__ == '__main__':
  main()
