import argparse
from PIL import Image
import os

from torchvision.utils import save_image
from torchvision.transforms.functional import to_tensor

from mag_models import CARN_V2, network_to_half
from Common import *

root = os.path.dirname(__file__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Waifu2x')
    
    parser.add_argument('-o', '--out', type=str, default='out.png')
    parser.add_argument('input', type=str)
    
    args = parser.parse_args()

    args.input = f'{root}/../static/portrait/{args.input}.png'
    args.out = f'{root}/../static/portrait/{args.out}.png'
    
    # load model
    model_cran_v2 = CARN_V2(color_channels=3, mid_channels=64, conv=nn.Conv2d,
                        single_conv_size=3, single_conv_group=1,
                        scale=2, activation=nn.LeakyReLU(0.1),
                        SEBlock=True, repeat_blocks=3, atrous=(1, 1, 1))
    model_cran_v2 = network_to_half(model_cran_v2)
    checkpoint = f"{root}/../core/checkpoint/CARN_model_checkpoint.pt"
    model_cran_v2.load_state_dict(torch.load(checkpoint, 'cpu'))
    model_cran_v2 = model_cran_v2.float() 

    img = args.input
    img = Image.open(img).convert("RGB")
    img = to_tensor(img).unsqueeze(0) 

    with torch.no_grad():

        out = model_cran_v2(img)

    save_image(out, args.out)
