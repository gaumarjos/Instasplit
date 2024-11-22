from PIL import Image
import argparse
import os
from glob import glob

def scale(im, tile_size = 1080):
    width, height = im.size
    if width >= height:
        height = int(height / width * tile_size)
        width = tile_size
    else:
        width = int(width / height * tile_size)
        height = tile_size
    im = im.resize((width, height), Image.LANCZOS)
    return im

def make_square(im, colour='white', tile_size = 1080):
    colours = {'white': 255, 'black': 0}
    fill = colours[colour]
    x, y = im.size
    if x == y:
        sq_im = im
    else:
        sq_im = Image.new('RGB', (tile_size, tile_size), (fill, fill, fill))
        sq_im.paste(im, (int((tile_size - x) / 2), int((tile_size - y) / 2)))
    return sq_im

def process_image(filename, n_tiles, tile_size=1080):
    im = Image.open(filename)
    width, height = im.size

    if n_tiles == 1:
        # Make square
        make_square(scale(im)).save(os.path.splitext(filename)[0] + "_sq" + ".jpg")

    else:
        # Split it in tiles
        # E' importante che il numero di tessere in orizzontale sia intero, e poi le squadriamo
        new_width = int(tile_size * n_tiles)
        new_height = int(new_width / width * height)
        re_im = im.resize((new_width, new_height), Image.LANCZOS)

        if new_height > tile_size:
            print("Images in tiles should still be wider than higher!")
            exit()

        tiles = []
        for i in range(n_tiles):
            left = i * tile_size
            up = 0
            right = left + tile_size
            bottom = new_height
            tile = re_im.crop((left, up, right, bottom))
            tiles.append(tile)

        for i, tile in enumerate(tiles):
            sq_tile = make_square(tile)
            sq_tile.save(os.path.splitext(filename)[0] + "_sq" + str(i) + ".jpg")


def main():
    parser = argparse.ArgumentParser(description="A program to split panorama images in multiple horizontal tiles to post on Instagram.")
    parser.add_argument("f", nargs=1, metavar="file", type=str,
                        help="Input image.")
    parser.add_argument("n", nargs=1, metavar="n_tiles", type=int,
                        help="Number of images to be split into.")
    args = parser.parse_args()
    filelist = glob(args.f[0])
    n_tiles = int(args.n[0])

    for filename in filelist:
        process_image(filename, n_tiles)

if __name__ == '__main__':
    main()