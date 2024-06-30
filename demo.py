#!/usr/bin/env python3

from ansicolormanager import AnsiColorManager


def print_system_colors():
    """Print the first 16 system colors (0-15) in a 4x4 grid."""
    for row in range(4):
        for col in range(4):
            color_code = row * 4 + col
            color = AnsiColorManager.Color(0, 0, 0)
            color.color_code = color_code
            color.print(f" {color_code:2} ", end='')
        print()
    print()


def print_grayscale_colors():
    """Print the grayscale colors (232-255) in a 4x4 grid."""
    for row in range(4):
        for col in range(4):
            color_code = 232 + row * 4 + col
            color = AnsiColorManager.Color(0, 0, 0)
            color.color_code = color_code
            color.print(f" {color_code:3} ", end='')
        print()
    print()


def visualize_palette_in_terminal(palette):
    """
    Visualize the color palette in the terminal.

    Args:
        palette (list): A list of Color objects representing the color palette.
    """
    for color in palette:
        color.print(f" {color.ansi():3} ", end='')
    print()


def print_6x6x6_color_cube():
    """Print the 6x6x6 color cube in the terminal in two rows with three grids each."""
    for grid_row in range(2):
        for row in range(6):
            for grid_col in range(3):
                for col in range(6):
                    r = grid_row * 3 + grid_col
                    g = row
                    b = col
                    color = AnsiColorManager.Color(r, g, b)
                    color.print(f" {color.ansi():3} ", end='')
                print("  ", end='')
            print()
        print()


def demonstrate_palettes():
    """
    Demonstrate generating and printing 8 different color palettes in the terminal.
    """
    base_colors = [
        AnsiColorManager.Color(0, 2, 2),  # Teal
        AnsiColorManager.Color(2, 0, 2),  # Purple
        AnsiColorManager.Color(2, 2, 0),  # Olive
        AnsiColorManager.Color(5, 0, 0),  # Bright Red
        AnsiColorManager.Color(0, 5, 0),  # Bright Green
        AnsiColorManager.Color(0, 0, 5),  # Bright Blue
        AnsiColorManager.Color(5, 5, 0),  # Yellow
        AnsiColorManager.Color(5, 0, 5),  # Magenta
    ]

    for i, base_color in enumerate(base_colors, start=1):
        base_color.print(f" Palette {i}: ", end='')
        print(' ', end='')
        palette = AnsiColorManager.generate_color_palette(base_color)
        visualize_palette_in_terminal(palette)


if __name__ == "__main__":
    print_system_colors()
    print_6x6x6_color_cube()
    print_grayscale_colors()
    demonstrate_palettes()
