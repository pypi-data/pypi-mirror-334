class _MakeColors:

    """ ! developper area ! """

    def _makeansi(col: str, text: str) -> str:
        return f"\033[38;2;{col}m{text}\033[38;2;255;255;255m"

    def _rmansi(col: str) -> str:
        return col.replace('\033[38;2;', '').replace('m','').replace('50m', '').replace('\x1b[38', '')

    def _makergbcol(var1: list, var2: list) -> list:
        col = list(var1[:12])
        for _col in var2[:12]:
            col.append(_col)
        for _col in reversed(col):
            col.append(_col)
        return col

    def _start(color: str) -> str:
        return f"\033[38;2;{color}m"

    def _end() -> str:
        return "\033[38;2;255;255;255m"

    def _maketext(color: str, text: str, end: bool = False) -> str:
        end = _MakeColors._end() if end else ""
        return color+text+end

    def _getspaces(text: str) -> int:
        return len(text) - len(text.lstrip())

    def _makerainbow(*colors) -> list:
        colors = [color[:24] for color in colors]
        rainbow = []
        for color in colors:
            for col in color:
                rainbow.append(col)
        return rainbow
    
    def _reverse(colors: list) -> list:
        _colors = list(colors)
        for col in reversed(_colors):
            colors.append(col)
        return colors
    
    def _mixcolors(col1: str, col2: str, _reverse: bool = True) -> list:
        col1, col2 = _MakeColors._rmansi(col=col1), _MakeColors._rmansi(col=col2)
        fade1 = Colors.StaticMIX([col1, col2], _start=False)      
        fade2 = Colors.StaticMIX([fade1, col2], _start=False)
        fade3 = Colors.StaticMIX([fade1, col1], _start=False)
        fade4 = Colors.StaticMIX([fade2, col2], _start=False)
        fade5 = Colors.StaticMIX([fade1, fade3], _start=False)    
        fade6 = Colors.StaticMIX([fade3, col1], _start=False)
        fade7 = Colors.StaticMIX([fade1, fade2], _start=False)
        mixed = [col1, fade6, fade3, fade5, fade1, fade7, fade2, fade4, col2]
        return _MakeColors._reverse(colors=mixed) if _reverse else mixed 

class Colors:

    """
    54 variables (colors)
    
    3 lists:
        static_colors      |      colors that are static, ex: 'red' (can't be faded)
        dynamic_colors     |      colors that are dynamic, ex: 'blue_to_purple' (can be faded)
        all_colors         |      every color of static_colors and dynamic_colors
        
    3 functions:
        StaticRGB()        |      create your own fix/static color
        DynamicRGB()       |      create your own faded/dynamic color (soon...)
        StaticMIX()        |      mix two or more static colors
        DynamicMIX()       |      mix two or more dynamic colors
        Symbol()           |      create a colored symbol, ex: '[!]'
    """

    def StaticRGB(r: int, g: int, b: int) -> str:
        return _MakeColors._start(f"{r};{g};{b}")

    def DynamicRGB(r1: int, g1: int, b1: int, r2: int,
                   g2: int, b2: int) -> list: ...

    def StaticMIX(colors: list, _start: bool = True) -> str:
        rgb = []
        for col in colors:
            col = _MakeColors._rmansi(col=col)
            col = col.split(';')
            r = int(int(col[0]))
            g = int(int(col[1]))
            b = int(int(col[2]))
            rgb.append([r, g, b])
        r = round(sum(rgb[0] for rgb in rgb) / len(rgb))
        g = round(sum(rgb[1] for rgb in rgb) / len(rgb))
        b = round(sum(rgb[2] for rgb in rgb) / len(rgb))
        rgb = f'{r};{g};{b}'
        return _MakeColors._start(rgb) if _start else rgb

    def DynamicMIX(colors: list):
        _colors = []
        for color in colors:
            if colors.index(color) == len(colors) - 1:
                break
            _colors.append([color, colors[colors.index(color) + 1]])
        colors = [_MakeColors._mixcolors(col1=color[0], col2=color[1], _reverse=False) for color in _colors]

        final = []
        for col in colors:
            for col in col:
                final.append(col)
        return _MakeColors._reverse(colors=final)
            


    """ symbols """

    def Symbol(symbol: str, col: str, col_left_right: str, left: str = '[', right: str = ']') -> str:
        return f"{col_left_right}{left}{col}{symbol}{col_left_right}{right}{Col.reset}"


    """ dynamic colors """

    black_to_white = ["m;m;m"]
    black_to_red = ["m;0;0"]
    black_to_green = ["0;m;0"]
    black_to_blue = ["0;0;m"]

    white_to_black = ["n;n;n"]
    white_to_red = ["255;n;n"]
    white_to_green = ["n;255;n"]
    white_to_blue = ["n;n;255"]

    red_to_black = ["n;0;0"]
    red_to_white = ["255;m;m"]
    red_to_yellow = ["255;m;0"]
    red_to_purple = ["255;0;m"]

    green_to_black = ["0;n;0"]
    green_to_white = ["m;255;m"]
    green_to_yellow = ["m;255;0"]
    green_to_cyan = ["0;255;m"]

    blue_to_black = ["0;0;n"]
    blue_to_white = ["m;m;255"]
    blue_to_cyan = ["0;m;255"]
    blue_to_purple = ["m;0;255"]

    yellow_to_red = ["255;n;0"]
    yellow_to_green = ["n;255;0"]

    purple_to_red = ["255;0;n"]
    purple_to_blue = ["n;0;255"]

    cyan_to_green = ["0;255;n"]
    cyan_to_blue = ["0;n;255"]


    red_to_blue = ...
    red_to_green = ...

    green_to_blue = ...
    green_to_red = ...

    blue_to_red = ...
    blue_to_green = ...

    rainbow = ...

    """ static colors """

    red = _MakeColors._start('255;0;0')
    green = _MakeColors._start('0;255;0')
    blue = _MakeColors._start('0;0;255')

    white = _MakeColors._start('255;255;255')
    black = _MakeColors._start('0;0;0')
    gray = _MakeColors._start('150;150;150')

    yellow = _MakeColors._start('255;255;0')
    purple = _MakeColors._start('255;0;255')
    cyan = _MakeColors._start('0;255;255')

    orange = _MakeColors._start('255;150;0')
    pink = _MakeColors._start('255;0;150')
    turquoise = _MakeColors._start('0;150;255')

    light_gray = _MakeColors._start('200;200;200')
    dark_gray = _MakeColors._start('100;100;100')

    light_red = _MakeColors._start('255;100;100')
    light_green = _MakeColors._start('100;255;100')
    light_blue = _MakeColors._start('100;100;255')

    dark_red = _MakeColors._start('100;0;0')
    dark_green = _MakeColors._start('0;100;0')
    dark_blue = _MakeColors._start('0;0;100')

    reset = white

    """ ! developper area ! """

    col = (list, str)

    dynamic_colors = [
        black_to_white, black_to_red, black_to_green, black_to_blue,
        white_to_black, white_to_red, white_to_green, white_to_blue,

        red_to_black, red_to_white, red_to_yellow, red_to_purple,
        green_to_black, green_to_white, green_to_yellow, green_to_cyan,
        blue_to_black, blue_to_white, blue_to_cyan, blue_to_purple,

        yellow_to_red, yellow_to_green,
        purple_to_red, purple_to_blue,
        cyan_to_green, cyan_to_blue
    ]

    for color in dynamic_colors:
        _col = 20
        reversed_col = 220

        dbl_col = 20
        dbl_reversed_col = 220

        content = color[0]
        color.pop(0)

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(reversed_col))
                color.append(result)

            _col += 20
            reversed_col -= 20

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(dbl_reversed_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(dbl_col))
                color.append(result)

            dbl_col += 20
            dbl_reversed_col -= 20

    red_to_blue = _MakeColors._makergbcol(red_to_purple, purple_to_blue)
    red_to_green = _MakeColors._makergbcol(red_to_yellow, yellow_to_green)

    green_to_blue = _MakeColors._makergbcol(green_to_cyan, cyan_to_blue)
    green_to_red = _MakeColors._makergbcol(green_to_yellow, yellow_to_red)

    blue_to_red = _MakeColors._makergbcol(blue_to_purple, purple_to_red)
    blue_to_green = _MakeColors._makergbcol(blue_to_cyan, cyan_to_green)

    rainbow = _MakeColors._makerainbow(
        red_to_green, green_to_blue, blue_to_red)

    for _col in (
        red_to_blue, red_to_green,
        green_to_blue, green_to_red,
        blue_to_red, blue_to_green
    ): dynamic_colors.append(_col)

    dynamic_colors.append(rainbow)

    static_colors = [
        red, green, blue,
        white, black, gray,
        yellow, purple, cyan,
        orange, pink, turquoise,
        light_gray, dark_gray,
        light_red, light_green, light_blue,
        dark_red, dark_green, dark_blue,
        reset
    ]

    all_colors = [color for color in dynamic_colors]
    for color in static_colors:
        all_colors.append(color)
