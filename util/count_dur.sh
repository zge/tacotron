#!/bin/bash
#
# Count the total duration of wav files in one filelist
#
# Zhenhao Ge, 2019-05-24

#flist=/mnt/rdspd/PSVR/xavier/For_LackSmith/ja-dra01_sn601-7.12-sdpl1-sdpl2_wav.lst
#flist=${HOME}/Work/Projects/ckws_internal/phoneme_recognition/lists/train-wav.lst
flist=/home/zge/Work/Projects/keithito-tacotron/LJSpeech-1.1/wavlist.txt

nlines=$(cat $flist | wc -l)

sum=0
cnt=0
blksize=1000
for f in $(cat $flist); do 
  dur=$(soxi -d $f)
  dur2=$(python -c "import sys; \
     hh, mm, ss = [float(e) for e in sys.argv[1].split(':')]; \
     print(hh*3600+mm*60+ss)" $dur)
  sum=$(echo $sum + $dur2 |bc)
  cnt=$((cnt+1))
  if [ $(($cnt%blksize)) == 0 ]; then
    pct=$(python -c "import sys; \
      print('%.2f' % (float(sys.argv[1])/float(sys.argv[2])*100))" \
      $cnt $nlines)
    echo "processed ${cnt}/${nlines} (${pct}%) files ..."
  fi
done

# sum is 691997.91 secs (192.22 hrs)
