import logging
import magpack.vectorop
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Union, Tuple, Any
from matplotlib.widgets import Slider
from matplotlib.axes import Axes


def axial_align(x: np.ndarray, y: np.ndarray, z: np.ndarray, index: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Aligns the components of an orientation field such that a singular direction (index) is always positive.

    :param x:       The x component of the orientation field.
    :param y:       The y component of the orientation field.
    :param z:       The z component of the orientation field.
    :param index:   The axis to align towards 'x', 'y' or 'z'.
    """
    mask = locals()[index] < 0 if index in ('x', 'y', 'z') else None
    if mask is not None:
        x[mask], y[mask], z[mask] = -x[mask], -y[mask], -z[mask]
    else:
        raise ValueError('Index not recognised.')
    return x, y, z


def plot_3d(data: np.ndarray, fig: plt.Figure = None, extent: list[float] = None, init_take=1, axial=False,
            save: Optional[str] = None, vmin: Optional[float] = None, vmax: Optional[float] = None, **kwargs) -> \
        Optional[tuple[Slider, Slider]]:
    """Plots a 3D scalar or vector field, with the possibility to slice along different axes.

    :param data:        The 3D scalar or vector field to plot.
    :param fig:         Matplotlib figure to use (by default a new figure will be created).
    :param extent:      The extent of the 3D scalar or vector field.
    :param init_take:   Initial slicing direction (0, 1, 2) corresponding to the (x, y, z) spatial dimensions.
    :param axial:       True for orientation field coloring, False for vector field coloring.
    :param save:        Filename to save a snapshot of the figure.
    :param vmin:        Lower bound for the colorbar.
    :param vmax:        Upper bound for the colorbar.
    :param kwargs:      Additional keyword arguments for matplotlib (e.g. cmap).
    """
    all_data = None
    if data.ndim == 4 and data.shape[-1] != 3 and data.shape[0] == 3:
        all_data = np.stack([vector_color(data, axial=axial, oop=ii) for ii in range(3)])
        data = all_data[init_take]

    elif data.ndim != 3:
        print("Data not 3D and cannot be plotted.")
        return None

    if fig is None:
        fig = plt.figure()

    # globals
    take_axis = [init_take]
    slice_index = [0]
    extents = _get_extents(data)
    extents[2] = extent if extent is not None else extents[2]

    # plot space
    ax = fig.add_axes((0.15, 0.2, 0.7, 0.7))
    first_img = np.take(data, slice_index[0], axis=take_axis[0]).swapaxes(0, 1)
    image = ax.imshow(first_img, origin='lower', extent=extents[take_axis[0]], **kwargs)

    # adjust the main plot to make room for the sliders
    if data.ndim == 3:
        if vmin is None:
            vmin = np.nanmin(data)
        if vmax is None:
            vmax = np.nanmax(data)
        fig.colorbar(image, ax=ax)
        image.set_clim((vmin, vmax))

    ax_slice = fig.add_axes((0.15, 0.1, 0.5, 0.03))
    slice_slider = Slider(ax=ax_slice, label='slice', valmin=0, valmax=np.max(data.shape) - 1, valstep=1, valinit=0)

    ax_slice_axis = fig.add_axes((0.05, 0.25, 0.03, 0.5))
    ax_slice_slider = Slider(ax=ax_slice_axis, label='slice axis', valmin=0, valmax=2, valinit=init_take, valstep=1,
                             orientation="vertical")

    def draw():
        if all_data is not None:
            img = np.take(all_data[int(take_axis[0])], int(slice_index[0]), axis=take_axis[0]).swapaxes(0, 1)
        else:
            img = np.take(data, int(slice_index[0]), axis=take_axis[0]).swapaxes(0, 1)
        image.set_data(img)
        fig.canvas.draw_idle()

    def slice_update(val):
        slice_index[0] = val
        if data.shape[take_axis[0]] < slice_index[0]:
            slice_index[0] = 0
        slice_slider.valmax = data.shape[take_axis[0]] - 1  # doesn't work visually but keeps the slider in the limits
        draw()

    def slice_axis_update(val):
        take_axis[0] = val
        if data.shape[take_axis[0]] < slice_index[0]:
            slice_index[0] = 0
        image.set_extent(extents[take_axis[0]])
        draw()

    # register the update function with each slider
    slice_slider.on_changed(slice_update)
    ax_slice_slider.on_changed(slice_axis_update)

    if save:
        fig.savefig(save, dpi=fig.dpi)
        plt.close()
    plt.show()

    return slice_slider, ax_slice_slider


def vector_color(data: np.ndarray, saturation: float = 1, mode: int = 1, axial=False, oop=1) -> np.ndarray:
    """Converts a 3D or 2D array of 3 components into a complex number, which can then be plotted using complex domain
    coloring.

    The input should be an array with [x, y, z] vector components. Each component can have 2 or 3 spatial dimensions
    thus the input array should have the shape (3, nx, ny).
    The components x, z are considered to be in-plane and the y component out of plane by default.

    The mapping of the out of plane component can be done linearly or with some other function to improve contrast.
    The available modes are:

    1) Linear:          l = y
    2) Root:            l = sqrt(y)
    3) Tangential:      l = 2/pi tan(y)
    4) Cubic:           l = y^3

    :param data:        Input vector field numpy array shaped (3, x, y) or (3, x, y, z).
    :param saturation:  0...1 for color saturation or 0 to colour according to magnitude.
    :param mode:        Choice (0 - 4) for lightness maps described above.
    :param axial:       Degenerate coloring for orientation fields.
    :param oop:         Index of out-of-plane direction.
    :return:            RBG array (x, y, z, 3) for plotting.
    """
    # convention here is that y is out of plane
    x, y, z = data

    if oop == 1:
        if axial:
            x, y, z = axial_align(x, y, z, 'y')
    elif oop == 2:
        if axial:
            x, y, z = axial_align(x, y, z, 'z')
        x, y, z = x, z, y
    elif oop == 0:
        if axial:
            x, y, z = axial_align(x, y, z, 'x')
        x, y, z = y, x, z
    else:
        raise ValueError("Out-of-plane parameter has to be an integer from 0 to 2.")

    hue = np.arctan2(z, x)
    if axial:
        if np.count_nonzero(np.sqrt(x ** 2 + z ** 2) > np.abs(y)):
            hue *= 2
            logging.info("Vector primarily in-plane, using degenerate map.")

    if mode not in [1, 2, 3, 4]:
        print("Warning: Invalid lightness function, using default.")
        mode = 1

    y_max = np.max(magpack.vectorop.magnitude(data))  # y_max = np.max(np.abs(y))
    y_max = 1 if y_max < 1 else y_max
    y_norm = y / y_max

    if mode == 2:
        y_norm = np.sign(y_norm) * np.sqrt(np.abs(y_norm))
    elif mode == 3:
        y_norm = 2 * np.tan(y_norm) / np.pi
    elif mode == 4:
        y_norm = y_norm ** 3

    lightness = (y_norm + 1) / 2
    mag = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    lightness = np.where(mag == 0, 1, lightness)

    if not 0 <= saturation <= 1:
        saturation = 1
    elif saturation == 0:
        saturation = mag / np.max(mag)
    return hls2rgb(hue, lightness, saturation)


def complex_color(z: np.ndarray, saturation=0.6, log=False) -> np.ndarray:
    """Applies complex domain coloring to a 3D vector field.

    :param z:           Input complex number.
    :param saturation:  0...1 for color saturation.
    :param log:         Logarithmic coloring according to the magnitude.
    :return:            RBG array with shape (input_shape, 3) for plotting."""
    radial = np.log(np.abs(z) + 1) if log else np.abs(z)
    hue = np.angle(z) + np.pi
    lightness = radial / np.max(radial)
    return hls2rgb(hue, lightness, saturation)


def rgb2gray(rgb: np.ndarray) -> np.ndarray:
    """Converts RGB/RGBA data of shape (x, y, ..., 3) to grayscale.

    The output is in the same range as the input, so either [0,1] or [0,255] ranges work.
    Only 3 indices from the last dimension are used, the rest are discarded.

    :param rgb:     Numpy array of shape (x, y, ..., 3) to be converted
    :return:        Numpy array of shape (x, y, ...) grayscale data
    """
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def hls2rgb(hue: np.ndarray, lightness: np.ndarray, saturation: Union[np.ndarray, float]) -> np.ndarray:
    """Convert HLS values (Hue, Lightness, Saturation) to RGB values (Red, Green, Blue) for image plotting.

    :param hue:         Hue [0, 2pi].
    :param lightness:   Lightness [0, 1].
    :param saturation:  Saturation [0, 1].

    :returns:           Numpy array of size input.shape + (3,) with (r, g, b) values in the [0,255] range
    """
    hue = hue % (2 * np.pi)
    section = np.pi / 3
    c = (1 - np.abs(2 * lightness - 1)) * saturation
    x = c * (1 - np.abs((hue / section) % 2 - 1))
    m = lightness - c / 2

    c, x = c + m, x + m

    sextant = hue // section % 6
    result = np.where(sextant == 0, [c, x, m], 0) + np.where(sextant == 1, [x, c, m], 0) + \
             np.where(sextant == 2, [m, c, x], 0) + np.where(sextant == 3, [m, x, c], 0) + \
             np.where(sextant == 4, [x, m, c], 0) + np.where(sextant == 5, [c, m, x], 0)

    result *= 255
    return np.moveaxis(result, 0, -1).astype(np.uint8)


def rgb2lab(r, g, b) -> np.ndarray:
    """Converts RGB of shape (..., 3) to LAB.

    :param r:         red value [0, 1].
    :param g:         green value [0, 1].
    :param b:         blue value [0, 1].
    :return:          Inpout arrays in Lab coordinates.
    """
    m1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                   [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]])
    temp = np.einsum('ij,j...->i...', m1, np.stack([r, g, b]))
    m2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                   [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    return np.einsum('ij,j...->i...', m2, np.cbrt(temp))


def lab2rgb(lum, a, b) -> np.ndarray:
    """Converts LAB of shape (..., 3) to RGB.

    :param lum:     Lab lum value.
    :param a:       Lab a value.
    :param b:       Lab b value.
    :return:        Corresponding RGB array.
    """
    m1 = np.array([[1, +0.3963377774, 0.2158037573],
                   [1, -0.1055613458, -0.0638541728],
                   [1, -0.0894841775, -1.2914855]])
    temp = np.einsum('ij,j...->i...', m1, np.stack([lum, a, b]))
    m2 = np.array([[+4.0767416621, -3.3077115913, +0.2309699292],
                   [-1.2684380046, +2.6097574011, -0.3413193965],
                   [-0.0041960863, -0.7034186147, 1.7076147010]])
    return np.einsum('ij,j...->i...', m2, np.power(temp, 3))


def color_quiver_overlay(data: np.ndarray, slice_axis=2, axial: bool = False, skip: int = 4,
                         save: Optional[str] = None, saturation=1) -> None:
    """Plots vectors using complex color and adds a quiver overlay for clarity.

    :param data:        Vector or orientation array with shape (3, nx, ny).
    :param slice_axis:  Index from which the slice was taken (so that out-of-plane component can be determined).
    :param axial:       True for orientations, False for vector fields.
    :param skip:        Number of arrows to skip for visual clarity.
    :param save:        Filename to which the figure will be saved.
    :param saturation:  Color saturation, None for magnitude-based
    :return:            None
    """

    sizes = data.shape
    components, spatial_dims = sizes[0], sizes[1:]
    logging.info(f"{components=},{spatial_dims=}")
    if not (components in [2, 3]):
        raise ValueError("Quiver plot vector field must have 2 or 3 components.")
    if len(spatial_dims) != 2:
        raise ValueError("Quiver plot vector field must have 2 spatial dimensions.")
    if components == 2:
        data = np.concatenate([data, np.zeros((1,) + spatial_dims)], axis=0)
    if axial:
        arrow_kwarg = dict(headwidth=1, headaxislength=0, headlength=0)
    else:
        arrow_kwarg = {}
    x_idx, y_idx = np.delete(np.arange(3), slice_axis)
    logging.info(f"{x_idx=},{y_idx=}")

    xx, yy = np.meshgrid(np.linspace(0, spatial_dims[0] - 1, spatial_dims[0]),
                         np.linspace(0, spatial_dims[1] - 1, spatial_dims[1]), indexing='ij')
    logging.info(f"{xx.shape=},{yy.shape=}")
    skips = (slice(None, None, skip), slice(None, None, skip))
    arrow_x = data[x_idx][skips]
    arrow_y = data[y_idx][skips]

    plt.quiver(xx[skips], yy[skips], arrow_x, arrow_y, color=(0, 0, 0, 1),
               pivot='mid', scale=1 / skip, scale_units='xy', angles='xy', minlength=0, **arrow_kwarg)
    color = vector_color(data, axial=axial, oop=slice_axis, saturation=saturation)
    logging.info(f"{color.shape=}")
    plt.imshow(color.transpose((1, 0, 2)), origin='lower')
    if save:
        plt.axis('off')
        plt.savefig(save, dpi=330)
    plt.show()


def _get_extents(data: np.ndarray) -> list[tuple[float, float, float, float]]:
    """Gets extents of vector field data.

    :param data:    Array for creating a list of extents for plotting.
    :return:        List of tuples containing extents for each of the slicing options.
    """
    extents = [(0, data.shape[1], 0, data.shape[2]),
               (0, data.shape[0], 0, data.shape[2]),
               (0, data.shape[0], 0, data.shape[1])]
    return extents
