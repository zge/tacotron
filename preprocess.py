import argparse
import os
from multiprocessing import cpu_count
from tqdm import tqdm
from datasets import blizzard, ljspeech
from hparams import hparams


def preprocess_blizzard(args):
  in_dir = os.path.join(args.base_dir, 'Blizzard2012')
  out_dir = os.path.join(args.base_dir, args.output)
  os.makedirs(out_dir, exist_ok=True)
  metadata = blizzard.build_from_path(in_dir, out_dir, args.num_workers, tqdm=tqdm)
  write_metadata(metadata, out_dir)


def preprocess_ljspeech(args):
  in_dir = os.path.join(args.base_dir, 'LJSpeech-1.1')
  out_dir = os.path.join(args.base_dir, args.output)
  os.makedirs(out_dir, exist_ok=True)
  metadata = ljspeech.build_from_path(in_dir, out_dir, args.num_workers, tqdm=tqdm)
  write_metadata(metadata, out_dir)


def write_metadata(metadata, out_dir):
  with open(os.path.join(out_dir, 'train.txt'), 'w', encoding='utf-8') as f:
    for m in metadata:
      f.write('|'.join([str(x) for x in m]) + '\n')
  frames = sum([m[2] for m in metadata])
  hours = frames * hparams.frame_shift_ms / (3600 * 1000)
  print('Wrote %d utterances, %d frames (%.2f hours)' % (len(metadata), frames, hours))
  print('Max input length (#words in normalized text):  %d' %
        max(len(m[3]) for m in metadata))
  print('Max output length: %d (#frames in spectrogram)' % max(m[2] for m in metadata))

# # Parser for debug use
# class Parser(object):
#   def __init__(self):
#     self.base_dir = ''
#     self.output = ''
#     self.dataset = ''
#     self.num_workers = cpu_count()

def main():

  parser = argparse.ArgumentParser()

  # runtime
  parser.add_argument('--base_dir', default=os.path.expanduser('~/tacotron'))
  parser.add_argument('--output', default='training')
  parser.add_argument('--dataset', required=True, choices=['blizzard', 'ljspeech'])
  parser.add_argument('--num_workers', type=int, default=cpu_count())
  args = parser.parse_args()

  # # debug (with ljspeech as example)
  # # args = parser.parse_args()
  # args = Parser()
  # args.base_dir = os.path.expanduser('~/Work/Projects/keithito-tacotron')
  # args.output = 'training'
  # args.dataset = 'ljspeech'
  # args.num_workers = cpu_count()

  if args.dataset == 'blizzard':
    preprocess_blizzard(args)
  elif args.dataset == 'ljspeech':
    preprocess_ljspeech(args)


if __name__ == "__main__":
  main()
