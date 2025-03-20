import logging
import magpack.structures
from magpack.structures import *
from ThreeDViewer import image


def plot_skyrmion() -> None:
    """Plots a skyrmion using matplotlib."""
    v_field = magpack.structures.skyrmion(20, 20, 1)
    v_field = magpack.structures.stack_config(v_field, 10, -1)
    image.plot_3d(v_field)
    image.color_quiver_overlay(v_field[..., 5], skip=1)


def plot_meron() -> None:
    """Plots a meron-antimeron pair using matplotlib."""
    v_field = magpack.structures.meron_pair(20, 40)
    v_field = magpack.structures.stack_config(v_field, 10, -1)

    image.plot_3d(v_field)
    image.color_quiver_overlay(v_field[..., 5], skip=1)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    print("Choose a structure to plot: ")
    print("1. Skyrmion")
    print("2. Meron")

    choice = input()

    if choice == "1":
        plot_skyrmion()
    elif choice == "2":
        plot_meron()
    else:
        print("Invalid choice")
