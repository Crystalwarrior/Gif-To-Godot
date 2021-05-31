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
tracks/0/keys = {{
"""

anim_keys = '''{
"times": PoolRealArray( {0} ),
"transitions": PoolRealArray( {1} ),
"update": 1,
"values": [ {2} ]
}
'''

# Create .tres file.
with open(name + '.tres', 'w') as tres:
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

    tres.write(f'"times": PoolRealArray( {times} ),\n')
    tres.write(f'"transitions": PoolRealArray( {transitions} ),\n')
    tres.write('"update": 1,\n')
    tres.write(f'"values": [ {values} ]\n')
    tres.write('}')