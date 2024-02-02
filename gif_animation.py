import argparse
import os
import numpy as np

from glob import glob  
from PIL import Image, ImageSequence, ImageChops

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


anims = []

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

anim_library = """
[resource]
_data = {{
{0}
}}
"""


anim_scene = """
[gd_scene load_steps=2 format=2]

[ext_resource type="AnimationLibrary" path="{0}" id=1]

[node name="ImportedAnimation" type="Node2D"]

[node name="Sprite" type="Sprite2D" parent="."]
centered = false

[node name="AnimationPlayer" type="AnimationPlayer" parent="."]
libraries = {{
"": ExtResource( 1 )
}}
"""

def calcdiff(im1, im2):
    dif = ImageChops.difference(im1, im2)
    return np.mean(np.array(dif))

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
            for compare in frames:
                cmp_img = compare['image']
                cmp_name = compare['name']
                if calcdiff(frame, cmp_img) <= 0.0001:
                    print(f"{fn} is too similar to {cmp_name}, reusing the latter!")
                    fn = cmp_name
                    frame = cmp_img
                    break
            frame.save(fn, optimize=True)
            frames.append({'name': fn, 'duration': im.info['duration'] / 1000.0, 'image': frame.copy()})
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
            frame_name = frame['name'].replace('\\', '/')
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
        anims.append(fn)

def animation_library():
    fn = f'{anims_dir}/animation_library.tres'
    # Create animation library file.
    with open(fn, 'w') as lib:
        lib.write(f'[gd_resource type="AnimationLibrary" load_steps={len(anims)+1} format=2]\n\n')

        data = []
        for i, anim in enumerate(anims, 1):
            anim_name = anim.replace('\\', '/')
            lib.write(f'[ext_resource path="res://{anim_name}" type="Texture" id={i}]\n')
            name = os.path.basename(os.path.splitext(anim_name)[0])
            data.append(f'"{name}": ExtResource( {i} )')
                
        lib.write(anim_library.format(',\n'.join(data)))

def scene():
    fn = f'{anims_dir}/imported_animation.tscn'
    # Create a scene file.
    with open(fn, 'w') as tscn:                
        tscn.write(anim_scene.format(f'res://{anims_dir}/animation_library.tres'))


for image in images:
    print(f"Parsing {image}...")
    parse_image(image)

print(f"Creating animation library file...")
animation_library()

print(f"Creating a scene file...")
scene()

input("Done! (Press any key to close this window.)")