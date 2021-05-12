import argparse
import json
import random
import os

import torch
from torchvision import utils
from gen_model import Generator

root = os.path.dirname(__file__)

with open(f'{root}/../core/tags.json', 'r') as f:
    tags = json.load(f)
tag_ind = {tag: ind for ind, tag in enumerate(tags)}


def one_hot(sample, lb, device):
    labels = [0] * len(tags)
    for tag in lb:
        labels[tag_ind[tag]] = 1
    labels = torch.Tensor(labels).float()
    labels = labels.unsqueeze(0)
    labels = labels.repeat(sample, 1)
    return labels.to(device)


with open(f'{root}/../core/sample_labels.json', 'r') as f:
    sample_labels = json.load(f)
total_samples = len(sample_labels)


def get_random_labels(batch, device):
    labels = []
    for i in range(batch):
        labels.append(sample_labels[random.randint(0, total_samples - 1)])
    return torch.Tensor(labels).float().to(device)


def generate(args, g_ema, device, mean_latent):
    with torch.no_grad():
        g_ema.eval()
        for i in range(args.pics):
            sample_z = torch.randn(args.sample, args.latent, device=device)
            if len(args.labels) == 0:
                sample_l = get_random_labels(args.sample, device=device)
            else:
                sample_l = one_hot(args.sample, args.labels, device=device)

            sample, _ = g_ema(
                [sample_z], sample_l, truncation=args.truncation, truncation_latent=mean_latent
            )

            rows = int(args.sample ** 0.5)
            rows = args.sample // rows
            utils.save_image(
                sample,
                f"{root}/../static/portrait/{args.output}.png",
                nrow=rows,
                normalize=True,
                range=(-1, 1),
            )


if __name__ == '__main__':
    device = 'cpu'

    parser = argparse.ArgumentParser(description='Generate samples from the generator')

    parser.add_argument('--size', type=int, default=128)
    parser.add_argument('--sample', type=int, default=1)
    parser.add_argument('--pics', type=int, default=1)
    parser.add_argument('--truncation', type=float, default=1)
    parser.add_argument('--truncation_mean', type=int, default=4096)
    parser.add_argument('--ckpt', type=str, default=f'{root}/../core/checkpoint/600000.pt')
    parser.add_argument('--channel_multiplier', type=int, default=2)
    parser.add_argument('--labels', type=str, default=None)
    parser.add_argument('--output', type=str, default='example')

    args = parser.parse_args()

    args.latent = 256
    args.n_mlp = 8

    if args.labels is None:
        args.labels = []
    else:
        args.labels = args.labels.split(",")

    g_ema = Generator(
        args.size, 23, args.latent, args.n_mlp, channel_multiplier=args.channel_multiplier
    ).to(device)

    if args.ckpt is not None:
        checkpoint = torch.load(args.ckpt)

        g_ema.load_state_dict(checkpoint["g_ema"])

    if args.truncation < 1:
        labels = one_hot(args.truncation_mean, args.labels, device=device)
        with torch.no_grad():
            mean_latent = g_ema.mean_latent(args.truncation_mean, labels)
    else:
        mean_latent = None

    generate(args, g_ema, device, mean_latent)
