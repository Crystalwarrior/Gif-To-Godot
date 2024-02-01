import argparse
import os

from glob import glob  
from PIL import Image, ImageSequence

parser = argparse.ArgumentParser(
        description='Convert any animated image(s) into frames and then create an '
                    'Animation File you can import into an AnimationLibrary')
parser.add_argument('images', nargs='*', help='Image(s) to process')
args = parser.parse_args()
# use glob to find files matching wildcards
#if a string does not contain a wildcard, glob will return it as is.
images = []
for arg in args.images:  
    images += glob(arg)


anims_dir = input("Put these where? (Leave blank if current dir) ")

anim_data = """
[resource]
resource_name = "{0}"
length = {1}
loop = {2}
tracks/0/type = "value"
tracks/0/path = NodePath("Sprite:texture")
tracks/0/interp = 1
tracks/0/loop_wrap = true
tracks/0/imported = false
tracks/0/enabled = true
tracks/0/keys = 
"""

anim_keys = """{{
"times": PoolRealArray( {0} ),
"transitions": PoolRealArray( {1} ),
"update": 1,
"values": [ {2} ]
}}
"""

def parse_image(image):
    name = os.path.basename(os.path.splitext(image)[0])
    frames = []

    with Image.open(image) as im:
        index = 0
        n_frames = im.n_frames
        for frame in ImageSequence.Iterator(im):
            directory = f'{anims_dir}/{name}'
            fn = f'{directory}/{index}.png'
            if not os.path.exists(directory):
                os.makedirs(directory)
            frame.convert(mode='RGBA')
            frame.save(fn)
            frames.append({'name': fn, 'duration': im.info['duration'] / 1000.})
            index += 1

    fn = f'{anims_dir}/{name}.tres'
    if not os.path.exists(anims_dir):
        os.makedirs(anims_dir)
    # Create .tres file.
    with open(fn, 'w') as tres:
        tres.write(f'[gd_resource type="Animation" load_steps={n_frames + 1} format=2]\n\n')

        length = 0.0
        loop = 'true'

        for i, frame in enumerate(frames, 1):
            frame_name = frame['name']
            length += frame['duration']
            tres.write(f'[ext_resource path="res://{frame_name}" type="Texture" id={i}]\n')

        tres.write(anim_data.format(name, length, loop))

        times = ['0']

        curr_time = 0.0
        for frame in frames:
            curr_time += frame['duration']
            times.append(format(curr_time, '.2f'))
        
        times = ', '.join(times[:len(frames)])
        transitions = ', '.join(['1'] * len(frames))
        values = ', '.join([f'ExtResource( {i+1} )' for i in range(len(frames))])

        tres.write(anim_keys.format(times, transitions, values))


for image in images:
    print(f"Parsing {image}...")
    parse_image(image)

input("Done! (Press any key to close this window.)")