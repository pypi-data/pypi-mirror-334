import numpy as np
import pyvista as pv


def plot_vector_field(vector_field: np.ndarray):
    """Plot vector field using pyvista.

    :param: vector_field:   Vector field as a numpy array shaped (3, nx, ny, nz). First index corresponds to the
                            field's components
    :return:                None
    """
    # initialize mesh
    _, nx, ny, nz = vector_field.shape
    size = vector_field[0].size
    origin = (-(nx - 1) / 2, -(ny - 1) / 2, -(nz - 1) / 2)
    vector_mesh = pv.ImageData(dimensions=(nx, ny, nz), origin=origin)
    vector_mesh['mag'] = vector_field.T.reshape(size, 3)
    vector_mesh['mag_scalar'] = vector_mesh['mag'][:, 2]

    # remove some values for clarity
    num_arrows = vector_mesh['mag'].shape[0]
    n_remove = int(num_arrows - np.min([num_arrows / 2, 5000 * np.log(np.log(num_arrows))]))
    if n_remove > 0:
        rand_ints = np.random.choice(num_arrows - 1, size=n_remove, replace=False)
        vector_mesh['mag'][rand_ints] = np.array([0, 0, 0])
    arrows = vector_mesh.glyph('mag', factor=2 * np.log10(np.max([nx, ny, nz])))
    pv.set_plot_theme("document")
    p = pv.Plotter()
    p.add_mesh(arrows, scalars='mag_scalar', ambient=0.5, cmap='coolwarm')
    p.show_grid()
    p.add_bounding_box()

    p.show()


def plot_scalar_field(field: np.ndarray):
    """Plot contours of a scalar field using pyvista.

    :param: scalar:   Scalar field as a numpy array shaped (nx, ny, nz). 
    :return:          None
    """    # initialize mesh
    nx, ny, nz = field.shape
    origin = (-(nx - 1) / 2, -(ny - 1) / 2, -(nz - 1) / 2)
    scalar_mesh = pv.ImageData(dimensions=(nx, ny, nz), origin=origin)

    scalar_mesh['field'] = field.flatten('F')
    contours = scalar_mesh.contour(scalars='field')

    pv.set_plot_theme("document")
    p = pv.Plotter()
    p.add_mesh(contours, lighting=False, cmap='inferno', show_scalar_bar=True, opacity=0.5)
    p.show_grid()
    p.add_bounding_box()

    p.show()
