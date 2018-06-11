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
    validate_arguments(parser)
    return parser.parse_args()


def validate_arguments(parser):
    params = parser.parse_args()
    if not params.path:
        parser.error(
            'ERROR: you need have to point out the path!'
        )
    if params.scale and (params.width or params.height):
        parser.error(
            'ERROR: you need have a scale or width and (or) height!'
        )
    if (params.scale <= 0 or params.width <= 0 or params.height <= 0):
        parser.error(
            'ERROR: a scale or a width or a height are positive numbers'
        )
    if params.width and params.height and params.scale:
        parser.error(
            'ERROR: if you have a width and height you can not have a scale'
        )
    if new_width:
        return True
    elif new_heigth:
        return True
    elif new_scale:
        return True
    elif new_width and new_scale:
        return True
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


def resize_picture(picture, new_width, new_height):
    new_picture = picture.resize((new_width, new_height), Image.ANTIALIAS)
    return new_picture


def save_resized_picture_to_output(path_to_image, output_path, new_picture):
    width, height = picture.size
    base, ext = splitext(path_to_image)
    picture_file_name = '{}__{}×{}{}'.format(base, width, height, ext)
    if output_path:
        path_to_save = os.path.join(output_path, picture_file_name)
    else:
        path_to_save = os.path.join(path_to_image, picture_file_name)
    return new_picture.save(path_to_save)


if __name__ == '__main__':
    argument = get_arguments()

    image = Image.open(argument.path)
    get_new_parametrs_picture(
        width,
        height,
        argument.width,
        argument.height,
        argument.scale
    )

    new_image = resize_picture(
        image,
        argument.width,
        argument.height,
    )
    save_resized_picture_to_output(
        argument.path, argument.output, new_image)
    print('Has the picture done')
