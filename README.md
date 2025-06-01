# Lyrics-to-PNG
This program will read a text file called Lyrics.txt in the same folder as the program, and it will create png files with a transparent background plus text effects, based on the lyrics provided in the text file.
The title image will contain the text from the beginning of the file to the first blank line.
The text in the Lyrics.txt file will indicate a new image by a blank like between text.
This blank line will indicate that the following text will be in a new image, and each line of text will be on a new line in the image.
Each line of text will be centered horizontally in the image.
The png files will be saved in a folder called "output/" + the first line in the Lyrics.txt file, in the same directory as the program.
If the folder does not exist, it will be created.
If the folder exists, it will be cleared before creating new images.
Each PNG file will be 1920x1080 pixels in size, and the text will be centered in the image.
The title image will be saved as "title.png" and the rest of the images will be saved as "01.png", "02.png", etc.
The text will have a base color of ##F9EFD5 and a shadow color of ##000000, with a shadow offset of 5 pixels in both the x and y directions and a shadow blur of 10 pixels and opacity of 0.5.
The text will be rendered using the "Georgia" font at a size of 150 pixels.
The text on the image should be double-spaced, giving space between lines.
Increase the kerning between letters by 5.
The file, georgiab.ttf, is the font file in the program's folder.
The text should be in bold type.
The text will be rendered with a shadow effect.
A title image will be created with the first line of the lyrics, and the rest of the lyrics will be rendered in separate images.
The text will have a slight bevel effect applied to it, and the images will be saved in the output folder.
# Requirements
- Python 3.x
- Pillow library
# Installation
You can install the Pillow library using pip:
```bash
pip install Pillow
```
# Usage
1. Create a text file named `Lyrics.txt` in the same directory as the script.
2. Write the lyrics in the text file, with the first line being the title.
3. Run the script:
```bash
python lyrics_to_png.py
```
# Output
The output will be saved in a folder named after the first line of the lyrics, located in the same directory as the script. The images will be named as follows:
- `title.png` for the title image
- `01.png`, `02.png`, etc. for the subsequent lines of lyrics




