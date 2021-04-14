import argparse
import os
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fake Generator')

    parser.add_argument('--labels', type=str, default=None)
    parser.add_argument('--truncation', type=float, default=1)
    parser.add_argument('--truncation_mean', type=int, default=4096)
    parser.add_argument('--output', type=str, default='0')

    args = parser.parse_args()

    print(f'[INFO] labels: {args.labels}, truncation: {args.truncation}, truncation mean: {args.truncation_mean}')

    root = os.path.dirname(__file__)
    src = f'{root}/../static/portrait/example.png'
    dst = f'{root}/../static/portrait/{args.output}.png'
    shutil.copy(src, dst)
