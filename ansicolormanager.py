import colorsys
import random
from typing import List


class AnsiColorManager:
    """Class for managing colors in an ANSI terminal emulator."""

    class Color:
        """Class representing a color in the ANSI 256-color palette."""

        def __init__(self, r: int, g: int, b: int):
            """
            Initialize a color with RGB values.

            Args:
                r (int): Red component (0-5).
                g (int): Green component (0-5).
                b (int): Blue component (0-5).
            """
            if not (0 <= r <= 5 and 0 <= g <= 5 and 0 <= b <= 5):
                raise ValueError("RGB values must be in the range 0-5")
            self.r = r
            self.g = g
            self.b = b
            self.color_code = 16 + (r * 36) + (g * 6) + b

        def ansi(self) -> int:
            """
            Get the ANSI color code.

            Returns:
                int: The ANSI 256-color code.
            """
            return self.color_code

        def get_luminosity(self) -> float:
            """
            Calculate the luminosity of the color.

            Returns:
                float: The luminosity of the color.
            """
            return 0.2126 * self.r + 0.7152 * self.g + 0.0722 * self.b

        def get_contrasting_color(self, percentage: int = 100) -> 'AnsiColorManager.Color':
            """
            Generate a contrasting color.

            Args:
                percentage (int): The percentage of contrast.

            Returns:
                Color: The contrasting color.
            """
            luminosity = self.get_luminosity()
            if luminosity >= 2.5:
                new_r = max(0, self.r - self.r * (percentage / 100))
                new_g = max(0, self.g - self.g * (percentage / 100))
                new_b = max(0, self.b - self.b * (percentage / 100))
            else:
                new_r = min(5, self.r + (5 - self.r) * (percentage / 100))
                new_g = min(5, self.g + (5 - self.g) * (percentage / 100))
                new_b = min(5, self.b + (5 - self.b) * (percentage / 100))
            return AnsiColorManager.Color(int(new_r), int(new_g), int(new_b))

        def get_complementary_color(self) -> 'AnsiColorManager.Color':
            """
            Generate the complementary color.

            Returns:
                Color: The complementary color.
            """
            new_r = 5 - self.r
            new_g = 5 - self.g
            new_b = 5 - self.b
            return AnsiColorManager.Color(new_r, new_g, new_b)

        def __hash__(self):
            return hash((self.r, self.g, self.b))

        def __eq__(self, other) -> bool:
            if isinstance(other, AnsiColorManager.Color):
                return self.r == other.r and self.g == other.g and self.b == other.b
            return False

        def print(self, text: str, percentage: int = 100, **kwargs):
            """
            Print the text with the color as background and a contrasting foreground color.

            Args:
                text (str): The text to print.
                percentage (int): The percentage of contrast.
                **kwargs: Additional keyword arguments for the print function.
            """
            reset_escape = "\033[0m"
            contrast_color = self.get_contrasting_color(percentage)
            formatted_text = (
                f"\033[48;5;{self.ansi()}m\033[38;5;{contrast_color.ansi()}m"
                f"{text}{reset_escape}"
            )
            print(formatted_text, **kwargs)

    @staticmethod
    def generate_color_palette(
        base_color: 'AnsiColorManager.Color', palette_size: int = 16
    ) -> List['AnsiColorManager.Color']:
        """
        Generate a color palette based on a base color.

        Args:
            base_color (Color): The base color.
            palette_size (int): The number of colors in the palette.

        Returns:
            list: A list of Color objects representing the color palette.
        """
        def calculate_analogous(color: 'AnsiColorManager.Color') -> List['AnsiColorManager.Color']:
            r, g, b = color.r * 51, color.g * 51, color.b * 51
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            analogous1 = colorsys.hls_to_rgb((h + 1 / 12) % 1, l, s)
            analogous2 = colorsys.hls_to_rgb((h - 1 / 12) % 1, l, s)
            return [
                AnsiColorManager.Color(int(a * 5 / 51), int(b * 5 / 51), int(c * 5 / 51))
                for a, b, c in [analogous1, analogous2]
            ]

        def calculate_shades_and_tints(color: 'AnsiColorManager.Color') -> List['AnsiColorManager.Color']:
            r, g, b = color.r, color.g, color.b
            shades_and_tints = [
                AnsiColorManager.Color(max(0, r // 2), max(0, g // 2), max(0, b // 2)),
                AnsiColorManager.Color(min(5, r + (5 - r) // 2), min(5, g + (5 - g) // 2), min(5, b + (5 - b) // 2)),
                AnsiColorManager.Color(max(0, r // 3), max(0, g // 3), max(0, b // 3)),  # Additional shade
                AnsiColorManager.Color(min(5, r + (5 - r) // 3), min(5, g + (5 - g) // 3), min(5, b + (5 - b) // 3))  # Additional tint
            ]
            return shades_and_tints

        def add_neutral_colors() -> List['AnsiColorManager.Color']:
            return [
                AnsiColorManager.Color(5, 5, 5),
                AnsiColorManager.Color(1, 1, 1),
                AnsiColorManager.Color(3, 3, 3)
            ]  # Additional neutral color

        palette_set = {base_color}
        palette_set.add(base_color.get_complementary_color())
        palette_set.update(calculate_analogous(base_color))
        palette_set.update(add_neutral_colors())
        palette_set.update(calculate_shades_and_tints(base_color))

        # Add more variations to reach palette_size colors
        more_variations = [
            AnsiColorManager.Color(min(5, base_color.r + 1), base_color.g, base_color.b),
            AnsiColorManager.Color(base_color.r, min(5, base_color.g + 1), base_color.b),
            AnsiColorManager.Color(base_color.r, base_color.g, min(5, base_color.b + 1)),
            AnsiColorManager.Color(max(0, base_color.r - 1), base_color.g, base_color.b),
            AnsiColorManager.Color(base_color.r, max(0, base_color.g - 1), base_color.b),
            AnsiColorManager.Color(base_color.r, base_color.g, max(0, base_color.b - 1))
        ]
        palette_set.update(more_variations)

        # Ensure the palette has exactly palette_size colors with jitter
        while len(palette_set) < palette_size:
            jitter = random.choice([-1, 1])
            new_color = AnsiColorManager.Color(
                (base_color.r + jitter * random.randint(1, 2)) % 6,
                (base_color.g + jitter * random.randint(1, 2)) % 6,
                (base_color.b + jitter * random.randint(1, 2)) % 6
            )
            palette_set.add(new_color)

        return list(palette_set)[:palette_size]
