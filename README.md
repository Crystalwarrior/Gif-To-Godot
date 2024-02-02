# Gif-To-Godot
Scripts to convert gif, apng, webp etc. to Godot-supported formats. It even generates a scene file for you and supports batching!

# Usage
Simply drag & drop your files onto the script. Before launching, make sure to use [Python 3](https://www.python.org/downloads/) and to [install Pillow](https://pillow.readthedocs.io/en/stable/installation.html#basic-installation) for Python.

Once you drag and drop the file, the script will create a new folder for you that will split it up into frames and create all the necessary resources and scene for you to easily import into Godot 4.

## gif_animation.py 
 - Exports Animation resources, AnimationLibrary resource and the Scene file with a basic setup to get you started.
 - You can choose a path to nest this scene in! Note that you should put this folder as-is into Godot, and if you want to rearrange the file structure in post you should do so from within the Godot editor.

Here's a gif how you can use this:

![usage_example](https://github.com/Crystalwarrior/Gif-To-Godot/assets/3470436/b17a5299-ce7d-43ec-aa4a-04613eccc429)
