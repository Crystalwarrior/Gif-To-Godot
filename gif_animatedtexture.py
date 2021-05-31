import argparse
import os

from PIL import Image

parser = argparse.ArgumentParser(
        description='Convert GIF into frames and then create '
                    'AnimatedTexture .tres')
parser.add_argument('gif', help='GIF to process')
args = parser.parse_args()

name = os.path.basename(os.path.splitext(args.gif)[0])
frames = []

# Break GIF into PNG frames.
with Image.open(args.gif) as im:
    fps = 0.0
    n_frames = im.n_frames
    for i in range(n_frames):
        im.seek(i)
        fn = f'{name}/{i}.png'
        if not os.path.exists(name):
            os.makedirs(name)
        im.save(fn)
        frames.append({'name': fn, 'duration': im.info['duration'] / 1000.})

# Create .tres file.
with open(name + '.tres', 'w') as tres:
    tres.write(f'[gd_resource type="AnimatedTexture" load_steps={n_frames + 1} format=2]\n\n')

    for i, frame in enumerate(frames, 1):
        name = frame['name']
        tres.write(f'[ext_resource path="res://{name}" type="Texture" id={i}]\n')
    tres.write('\n')

    tres.write(f'[resource]\nframes = {n_frames}\nfps = {fps}\n')

    frame_data = ('frame_{0}/texture = ExtResource( {1} )\n'
                  'frame_{0}/delay_sec = {2}\n')

    for i, frame in enumerate(frames):
        tres.write(frame_data.format(i, i+1, frame['duration']))
