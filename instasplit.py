from PIL import Image
import argparse
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="An addition program")
    parser.add_argument("f", nargs=1, metavar="str", type=str,
                        help="Input image.")
    parser.add_argument("n", nargs=1, metavar="num", type=int,
                        help="Number of images to be split into.")
    args = parser.parse_args()

    tile_width = 1080
    tile_max_height = 1080

    n_tiles = int(args.n[0])
    filename = args.f[0]
    im = Image.open(filename)
    width, height = im.size

    new_width = tile_width * n_tiles
    new_height = new_width / width * height
    print(new_width, new_height)

    if new_width > width:
        print("You're trying to enlarge the image, bad idea.")
        exit()

    if new_height > tile_max_height:
        print("Height is above its max value, strange.")
        exit()

    im_resized = im.resize((int(new_width), int(new_height)))

    tiles = []
    for i in range(n_tiles):
        left = i * tile_width
        up = 0
        right = left + tile_width
        bottom = new_height
        tile = im_resized.crop((left, up, right, bottom))
        tiles.append(tile)

    for i, tile in enumerate(tiles):
        tile_filename = os.path.splitext(filename)[0] + "_" + str(i) + ".jpg"
        tile.save(tile_filename)
