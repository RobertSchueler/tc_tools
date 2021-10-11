import numpy as np

from PIL import Image


def array_map(fun):
    """
    Decorator function aimed to decorate functions which manipulate
    rgb or rgba pixel map arrays.
    The resulting function takes the arguments infile and outfile as well
    as the additional arguments of the original function.
    The resulting function then loads an array from an image file infile manipulates it by the
    given function and saves it in another file.
    """
    def inner_fun(infile, outfile=None, *args, **kwargs):
        if not outfile:
            outfile = f"out_{infile}"
        in_img = Image.open(infile)
        a = np.asarray(in_img)
        b = fun(a, *args, **kwargs)
        out_img = Image.fromarray(b)
        out_img.save(outfile)
        return outfile

    return inner_fun
