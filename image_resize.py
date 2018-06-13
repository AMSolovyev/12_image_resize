from PIL import Image
import os
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='a path to the file')
    parser.add_argument('-w', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-s', '--scale', type=float)
    parser.add_argument('-o', '--output', help='path to put the picture')
    return parser


def validate_args(argument_parser):
    args = argument_parser.parse_args()
    if not args.path:
        argument_parser.error(
            'ERROR: the path to image was not presented!'
        )
    if not os.path.isfile(args.path):
        argument_parser.error(
            'ERROR: the present file does not exist!'
        )
    if args.output and not os.path.isdir(args.output):
        argument_parser.error(
            'ERROR: the specified output is not a directory'
        )

    if args.scale and (args.width or args.height):
        argument_parser.error(
            'ERROR: you need have a scale or width and (or) height!'
        )
    if (
        args.scale and args.scale <= 0 or
        args.width and args.width <= 0 or
        args.height and args.height <= 0
    ):
            argument_parser.error(
                'ERROR: a scale or a width or a height are positive numbers'
            )
    if not (args.width or args.height or args.scale):
        argument_parser.error(
            'A width or a heigth or a scale does not exist'
        )
    return args


def open_image(path):
    source_img = Image.open(path)
    return source_img


def compute_result_size(
        source_width,
        source_height,
        width=None,
        height=None,
        scale=None
):
    if scale:
        return int(source_width * scale), int(source_height * scale)
    if width and height:
        return width, height
    if width:
        height = int((width / source_width) * source_height)
        return width, height
    if height:
        width = int((height / source_height) * source_width)
        return width, height


def resize_image(source_img, output_size_tuple):
    return source_img.resize(output_size_tuple)


def get_output_path(args, output_size_tuple):
    source_img_dir, source_img_name = os.path.split(args.path)
    source_img_name_part, source_img_ext_part = os.path.splitext(
        source_img_name
    )
    output_img_name = '{}__{}x{}{}'.format(
        source_img_name_part,
        output_size_tuple[0],
        output_size_tuple[1],
        source_img_ext_part)
    if not args.output:
        output_path = os.path.join(
            source_img_dir, output_img_name)
    else:
        output_path = os.path.join(
            args.output, output_img_name)
    return output_path


def is_preserve_aspect_ratio(
        source_width,
        source_height,
        args_width,
        args_height
     ):
    return int(source_width/args_width) == int(source_height/args_height)


if __name__ == '__main__':
    size_params = {}

    argument_parser = get_parser()

    valid_args = validate_args(argument_parser)
    source_image = open_image(valid_args.path)
    source_width, source_height = source_image.size

    if valid_args.width and valid_args.height and not is_preserve_aspect_ratio(
        source_width,
        source_height,
        valid_args.width,
        valid_args.height
    ):
        print('The image source scale will not be saved')

    output_size_tuple = compute_result_size(
        source_width,
        source_height,
        valid_args.width,
        valid_args.height,
        valid_args.scale)

    resized_img = resize_image(source_image, output_size_tuple)
    output_path = get_output_path(valid_args, output_size_tuple)
    resized_img.save(output_path)
    print('The new file is saved as {}'.format(output_path))
