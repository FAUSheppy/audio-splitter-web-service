#!/usr/bin/python3

import sys
import argparse
import os
import pydub
import pydub.playback


def playTagAndSave(chunk, origname, outputDir, count):
    chunk.export("{}-chunk-{}.ogg".format(origname,count))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='None',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('FILE', help='file to analyse')
    parser.add_argument('--skip', type=int, default=0, help="skipchunks")
    parser.add_argument('--silence-vol', type=int, default=-60, help="silence threshold")
    parser.add_argument('--target-dir', default=".", help="target directory")
    parser.add_argument('--min-silence-dur', type=int, default=1000, help="min silence duration")
    parser.add_argument('--silence-padding', type=int, default=200, help="min silence duration")
    args = parser.parse_args()

    if not os.path.isdir(args.target_dir):
        os.mkdir(args.target_dir)

    filename = args.FILE
    audio = pydub.AudioSegment.from_ogg(filename)

    print("Average Volume: {}".format(audio.dBFS))

    chunks = pydub.silence.split_on_silence(audio, min_silence_len=args.min_silence_dur, 
                                                silence_thresh=args.silence_vol,
                                                keep_silence=args.silence_padding)

    print("Chunk-Count: {}".format(len(chunks)))
    
    skip = args.skip
    count = 0
    for c in chunks:
        count += 1
        if skip > 0:
            skip -= 1
            continue
        playTagAndSave(c, filename.split(".")[0], args.target_dir, count)
