"Turn all your gifs into HTML documents!"

"Never waste time loading lengthy gif resources again!"

TranCSScoding is a project designed to convert all of your gif files into CSS so that the browser can more efficiently load and render them. You won't have to load gifs at all. In fact, as soon as your page is loaded, your gifs are good to go! That's because TranCSScoding stores the gif data as specially crafted CSS in a style tag.

Using box-shadow and keyframe animation, the gif's pixels are mapped to no-blur box-shadows of a 1x1 div, and each frame of the gif becomes a box-shadow property to animate between!

Disclaimer: only works in webkit browsers thus far, will add more support later


Usage:

python tranCSScode.py gifname scale


e.g.:
python tranCSScode.py example_gifs/colbert 0.5

Note: example_gifs/colbert.gif must exist relative to the current directory, and example_gifs/colbert.html will be created as output
