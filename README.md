# Gif-To-Godot
Scripts to convert gifs to Godot-supported formats, such as AnimatedTexture or Animation files.

# Usage
Simply drag & drop your .gif onto one of the scripts. Before launching, make sure to use [Python 3](https://www.python.org/downloads/) and to [install Pillow](https://pillow.readthedocs.io/en/stable/installation.html#basic-installation) for Python.
Both of the files will split up your gif

## gif_animatedtexture.py
 - Exports an AnimatedTexture resource that can be used for Sprites, Tilesets, etc.
 - Great for animations of decorations and other 'passive' game elements, like tiles, trees, bushes, etc.
 - Not as great for when you actually need to know when the animation ends, how long it it is, when it loops - such as character sprites, enemies, etc. In this use case, use `gif_animation.py` instead

## gif_animation.py 
 - Exports an Animation file that can be imported into an AnimationPlayer.
 - Note that there must be a Sprite node next to the AnimationPlayer for the initial set-up. Later on you can move things around after import.
