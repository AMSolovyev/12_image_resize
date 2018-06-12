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
    validated_args = validate_args(parser)
    return validated_args


def validate_args(parser):
    args = parser.parse_args()
    if not os.path.exists(args.path):
        parser.error(
            'ERROR: the specified file does not exist!'
        )
    if args.output and not os.path.isdir(args.output):
        parser.error(
            'ERROR: the specified output is not a directory'
        )
    if args.scale and (args.width or args.height):
        parser.error(
            'ERROR: you need have a scale or width and (or) height!'
        )
    if not any([args.scale, args.width, args.height]):
        parser.error(
            'ERROR: you have to have one argument at least'
        )
    # need check if args <= 0 and (args=None) <= 0
    if (
        args.scale and args.scale <= 0 or
        args.width and args.width <= 0 or
        args.height and args.height <= 0):
        parser.error(
            'ERROR: a scale or a width or a height are positive numbers'
        )
    return args


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
    # if it is a directory you need check it in def validate_args
        path_to_save = os.path.join(output_path, picture_file_name)
    else:
    # you can not join old_name_picture and join picture_file_name
    # because you have a mistake like this:  image.png/image__100x200.png
    # you need save as new_name_picture like this
        path_to_save = picture_file_name
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
