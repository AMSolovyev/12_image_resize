from PIL import Image
from os.path import exists, join, splitext, sys
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='a path to the file')
    parser.add_argument('-w', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-s', '--scale', type=float)
    parser.add_argument('-o', '--output', help='path to put the picture')
    return parser.parse_args()


def validate_args(arguments):
    if not exists(arguments.path):
        parser.error(
            'ERROR: You need have a scale or width and (or) height!'
        )
        return False
    if not (arguments.scale and (arguments.width or arguments.height)):
        parser.error(
            'ERROR: you need have a scale or width and (or) height!'
        )
        return False
    return True


def get_new_parametrs_picture(width, height, new_width, new_height, scale):
    if new_width:
        scale = new_width/width
        return new_width, int(height*scale)
    if new_height:
        scale = new_height/height
        return int(width*scale), new_height
    if scale:
        return int(width*scale), int(height*scale)
    return new_width, new_height


def resize_picture(picture, new_width, new_height, scale):
    new_picture = picture.resize((new_width, new_height), Image.ANTIALIAS)
    return new_picture


def save_resized_picture_to_output(path_to_image, output_path, new_picture):
    width, height = picture.size
    base, ext = splitext(path_to_image)
    picture_file_name = '{}__{}×{}{}'.format(base, width, height, ext)
    if output_path is None:
        new_picture.save(picture_file_name)
    elif output_path is None:
        new_picture.save(join(output_path, picture_file_name))


if __name__ == '__main__':
    arguments = get_arguments()

    if not validate_args(arguments):
        exit('Exit. There isn\'t any arguments valid')

    image = Image.open(arguments.path)
    get_new_parametrs_picture(
        width,
        height,
        arguments.width,
        arguments.height,
        arguments.scale
    )

    new_image = resize_picture(
        image,
        arguments.width,
        arguments.height,
        arguments.scale
    )
    save_resized_picture_to_output(
        arguments.path, arguments.output, new_image)
    print('Has the picture done')
