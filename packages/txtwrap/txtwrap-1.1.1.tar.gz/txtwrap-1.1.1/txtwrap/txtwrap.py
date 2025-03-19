from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union
from os import get_terminal_size
from re import compile

hyphenated_regex = compile(r'(?<=-)(?=(?!-).)')
version = '1.1.1'

LOREM_IPSUM_W = 'Lorem ipsum odor amet, consectetuer adipiscing elit.'
LOREM_IPSUM_S = ('Lorem ipsum odor amet, consectetuer adipiscing elit. In malesuada eros natoque '
                 'urna felis diam aptent donec. Cubilia libero morbi fusce tempus, luctus aenean '
                 'augue. Mus senectus rutrum phasellus fusce dictum platea. Eros a integer nec '
                 'fusce erat urna.')
LOREM_IPSUM_P = ('Lorem ipsum odor amet, consectetuer adipiscing elit. Nulla porta ex condimentum '
                 'velit facilisi; consequat congue. Tristique duis sociosqu aliquam semper sit id. '
                 'Nisi morbi purus, nascetur elit pellentesque venenatis. Velit commodo molestie '
                 'potenti placerat faucibus convallis. Himenaeos dapibus ipsum natoque nam dapibus '
                 'habitasse diam. Viverra ac porttitor cras tempor cras. Pharetra habitant nibh '
                 'dui ipsum scelerisque cras? Efficitur phasellus etiam congue taciti tortor quam. '
                 'Volutpat quam vulputate condimentum hendrerit justo congue iaculis nisl nullam.'
                 '\n\nInceptos tempus nostra fringilla arcu; tellus blandit facilisi risus. Platea '
                 'bibendum tristique lectus nunc placerat id aliquam. Eu arcu nisl mattis potenti '
                 'elementum. Dignissim vivamus montes volutpat litora felis fusce ultrices. '
                 'Vulputate magna nascetur bibendum inceptos scelerisque morbi posuere. Consequat '
                 'dolor netus augue augue tristique curabitur habitasse bibendum. Consectetur est '
                 'per eros semper, magnis interdum libero. Arcu adipiscing litora metus fringilla '
                 'varius gravida congue tellus adipiscing. Blandit nulla mauris nullam ante metus '
                 'curae scelerisque.\n\nSem varius sodales ut volutpat imperdiet turpis primis '
                 'nullam. At gravida tincidunt phasellus lacus duis integer eros penatibus. '
                 'Interdum mauris molestie posuere nascetur dignissim himenaeos; magna et quisque. '
                 'Dignissim malesuada etiam donec vehicula aliquet bibendum. Magna dapibus sapien '
                 'semper parturient id dis? Pretium orci ante leo, porta tincidunt molestie. '
                 'Malesuada dictumst commodo consequat interdum nisi fusce cras rhoncus feugiat.'
                 '\n\nHimenaeos mattis commodo suspendisse maecenas cras arcu. Habitasse id '
                 'facilisi praesent justo molestie felis luctus suspendisse. Imperdiet ipsum '
                 'praesent nunc mauris mattis curabitur. Et consectetur morbi auctor feugiat enim '
                 'ridiculus arcu. Ultricies magna blandit eget; vivamus sollicitudin nisl proin. '
                 'Sollicitudin sociosqu et finibus elit vestibulum sapien nec odio euismod. Turpis '
                 'eleifend amet quis auctor cursus. Vehicula pharetra sapien praesent amet purus '
                 'ante. Risus blandit cubilia lorem hendrerit penatibus in magnis.\n\nAmet posuere '
                 'nunc; maecenas consequat risus potenti. Volutpat leo lacinia sapien nulla '
                 'sagittis dignissim mauris ultrices aliquet. Nisi pretium interdum luctus donec '
                 'magna suscipit. Dapibus tristique felis natoque malesuada augue? Justo faucibus '
                 'tincidunt congue arcu sem; fusce aliquet proin. Commodo neque nibh; tempus ad '
                 'tortor netus. Mattis ultricies nec maximus porttitor non mauris?')

def mono(

    text: str,
    width: Union[int, float] = 70,
    lenfunc: Callable[[str], Union[int, float]] = len,

) -> List[str]:

    """
    Wraps the given text into lines of specified width.

    Parameters:
        text (str): The text to be wrapped.
        width (int | float, optional): The maximum width of each line. Defaults to 70.
        lenfunc (Callable[[str], int | float], optional): A function to calculate
                                                          the length of a string. Defaults to len.

    Returns:
        list[str]: A list of strings, where each string is a line of the wrapped text.
    """

    assert isinstance(text, str), "text must be a string"
    assert isinstance(width, (int, float)), "width must be an integer or float"
    assert callable(lenfunc), "lenfunc must be a callable function"

    assert width > 0, "width must be greater than 0"

    parts = []
    current_char = ''

    for char in text:
        if lenfunc(current_char + char) <= width:
            current_char += char
        else:
            parts.append(current_char)
            current_char = char

    if current_char:
        parts.append(current_char)

    return parts

def word(

    text: str,
    width: Union[int, float] = 70,
    lenfunc: Callable[[str], Union[int, float]] = len,

) -> List[str]:

    """
    Wraps the input text into lines of specified width.

    Parameters:
        text (str): The input text to be wrapped.
        width (int | float, optional): The maximum width of each line. Defaults to 70.
        lenfunc (Callable[[str], int | float], optional): A function to calculate
                                                          the length of a string. Defaults to len.

    Returns:
        list[str]: A list of strings, where each string is a line of wrapped text.
    """

    assert isinstance(text, str), "text must be a string"
    assert isinstance(width, (int, float)), "width must be an integer or float"
    assert callable(lenfunc), "lenfunc must be a callable function"

    assert width > 0, "width must be greater than 0"

    lines = []
    current_line = ''

    for word in text.split():
        test_line = current_line + ' ' + word if current_line else word

        if lenfunc(test_line) <= width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)

            current_line = ''

            for part in hyphenated_regex.split(word):
                for wrapped_part in mono(part, width, lenfunc):
                    if lenfunc(current_line + wrapped_part) <= width:
                        current_line += wrapped_part
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = wrapped_part

    if current_line:
        lines.append(current_line)

    return lines

def wrap(

    text: str,
    width: Union[int, float] = 70,
    lenfunc: Callable[[str], Union[int, float]] = len,
    method: Literal['mono', 'word'] = 'word',
    preserve_empty: bool = True

) -> List[str]:

    """
    Wraps the given text into lines of specified width.

    Parameters:
        text (str): The text to be wrapped.
        width (int | float, optional): The maximum width of each line. Defaults to 70.
        lenfunc (Callable[[str], int | float], optional): A function to calculate
                                                          the length of a string. Defaults to len.
        method (Literal['mono', 'word'], optional): The method to use for wrapping.
                                                    'mono' for character-based wrapping, 'word'
                                                    for word-based wrapping. Defaults to 'word'.
        preserve_empty (bool, optional): Whether to preserve empty lines. Defaults to True.

    Returns:
        list[str]: A list of wrapped lines.
    """

    assert isinstance(text, str), "text must be a string"
    assert isinstance(width, (int, float)), "width must be an integer or float"
    assert callable(lenfunc), "lenfunc must be a callable function"

    assert width > 0, "width must be greater than 0"

    wrapped_lines = []

    if method == 'mono':
        wrapfunc = mono
    elif method == 'word':
        wrapfunc = word
    else:
        raise ValueError(f"{method=} is invalid, must be 'mono' or 'word'")

    for line in text.splitlines():
        wrapped_line = wrapfunc(line, width, lenfunc)
        if wrapped_line:
            wrapped_lines.extend(wrapped_line)
        elif preserve_empty:
            wrapped_lines.append('')

    return wrapped_lines

def align(

    text: str,
    width: Union[int, float] = 70,
    linegap: Union[int, float] = 0,
    sizefunc: Callable[[str], Tuple[Union[int, float], Union[int, float]]] = lambda s : (len(s), 1),
    method: Literal['mono', 'word'] = 'word',
    alignment: Literal['left', 'center', 'right', 'fill'] = 'left',
    preserve_empty: bool = True,
    use_min_width: bool = True,
    return_details: bool = False

) -> List[Union[Tuple[Union[int, float], Union[int, float], str],
                Dict[Literal['aligned', 'wrapped', 'size'], Any]]]:

    """
    Wraps and aligns text within a specified width and yields the position and content of each line.

    Parameters:
        text (str): The text to be wrapped and aligned.
        width (int | float, optional): The maximum width of each line. Defaults to 70.
        linegap (int | float, optional): The vertical gap between lines. Defaults to 0.
        sizefunc (Callable[[str], tuple[int | float, int | float]], optional): A function that
                                                                               returns the width and
                                                                               height of a given
                                                                               string. Defaults to a
                                                                               lambda function that
                                                                               returns the length of
                                                                               the string and 1.
        method (Literal['mono', 'word'], optional): The method to use for wrapping.
                                                    'mono' for character-based wrapping, 'word'
                                                    for word-based wrapping. Defaults to 'word'.
        alignment (Literal['left', 'center', 'right', 'fill'], optional): The alignment of the text.
                                                                          'left', 'center', 'right',
                                                                          or 'fill'.
                                                                          Defaults to 'left'.
        preserve_empty (bool, optional): Whether to preserve empty lines. Defaults to True.
        use_min_width (bool, optional): Whether to use the manimum width of the wrapped text.
                                        Defaults to True.
        return_details (bool, optional): Whether to return the aligned text, wrapped text, and
                                         the size.
                                         Defaults to False.

    Returns:
        list[tuple[int | float, int | float, str] |
             dict[Literal['aligned', 'wrapped', 'size'], Any]]: A list of tuples containing the
                                                                position and content of each line.
                                                                If return_details, a dictionary
                                                                containing the wrapped text, and
                                                                the size is returned.
    """

    assert isinstance(linegap, (int, float)), "linegap must be an integer or float"
    assert callable(sizefunc), "sizefunc must be a callable function"

    assert linegap >= 0, "linegap must be equal to or greater than 0"

    wrapped = wrap(text, width, lambda s : sizefunc(s)[0], method, preserve_empty)
    size_wrapped = {i: sizefunc(line) for i, line in enumerate(wrapped)}
    aligned_positions = []
    offset_y = 0

    if use_min_width:
        max_width = max(size[0] for size in size_wrapped.values())
        use_width = max_width
    else:
        use_width = width

    if alignment == 'left':
        for i, line in enumerate(wrapped):
            height_line = size_wrapped[i][1]
            aligned_positions.append((0, offset_y, line))
            offset_y += height_line + linegap

    elif alignment == 'center':
        for i, line in enumerate(wrapped):
            width_line, height_line = size_wrapped[i]
            aligned_positions.append(((use_width - width_line) / 2, offset_y, line))
            offset_y += height_line + linegap

    elif alignment == 'right':
        for i, line in enumerate(wrapped):
            width_line, height_line = size_wrapped[i]
            aligned_positions.append((use_width - width_line, offset_y, line))
            offset_y += height_line + linegap

    elif alignment == 'fill':
        no_spaces = True
        for i, line in enumerate(wrapped):
            height_line = size_wrapped[i][1]
            words = line.split()
            total_words = len(words)
            word_widths = {i: sizefunc(w)[0] for i, w in enumerate(words)}
            extra_space = width - sum(word_widths.values())
            offset_x = 0

            if total_words > 1:
                space_between_words = extra_space / (total_words - 1)
                no_spaces = False
            else:
                space_between_words = extra_space

            for i, w in enumerate(words):
                aligned_positions.append((offset_x, offset_y, w))
                offset_x += word_widths[i] + space_between_words

            offset_y += height_line + linegap

    else:
        raise ValueError(f"{alignment=} is invalid, must be 'left', 'center', 'right', or 'fill'")

    if return_details:
        if use_min_width and alignment == 'fill':
            if no_spaces:
                size_width = max_width
            elif text:
                size_width = width
            else:
                size_width = 0
        else:
            size_width = use_width

        return {
            'aligned': aligned_positions,
            'wrapped': wrapped,
            'size': (size_width, offset_y - linegap)
        }

    return aligned_positions

def fillstr(

    text: str,
    width: Union[int, float] = 70,
    fill: str = ' ',
    lenfunc: Callable[[str], Union[int, float]] = len,
    method: Literal['mono', 'word'] = 'word',
    alignment: Union[Callable[[str], str], Literal['left', 'center', 'right', 'fill']] = 'left',
    preserve_empty: bool = True

) -> str:

    """
    String formats a given text to fit within a specified width, using various alignment methods.

    Parameters:
        text (str): The text to be formatted.
        width (Union[int, float], optional): The width of the formatted text. Defaults to 70.
        fill (str, optional): The character used to fill the space. Must be a single character.
                              Defaults to ' '.
        lenfunc (Callable[[str], Union[int, float]], optional): A function to calculate the
                                                                length of a string. Defaults to len.
        method (Literal['mono', 'word'], optional): The method to use for wrapping.
                                                    'mono' for character-based wrapping, 'word'
                                                    for word-based wrapping. Defaults to 'word'.
        alignment (Union[Callable[[str], str],
                   Literal['left', 'center', 'right', 'fill']], optional): The alignment of the
                                                                           text. 'left', 'center',
                                                                           'right', or 'fill'.
                                                                           Defaults to 'left'.
        preserve_empty (bool, optional): Whether to preserve empty lines. Defaults to True.

    Returns:
        str: The formatted text.
    """

    assert isinstance(fill, str), "fill must be a string"
    assert len(fill) == 1, "fill must be a single character"

    wrapped = wrap(text, width, lenfunc, method, preserve_empty)
    justified_lines = ''

    if callable(alignment):
        return '\n'.join(alignment(line) for line in wrapped)

    elif alignment == 'left':
        for line in wrapped:
            justified_lines += line + fill * (width - lenfunc(line)) + '\n'

    elif alignment == 'center':
        for line in wrapped:
            extra_space = width - lenfunc(line)
            left_space = extra_space // 2
            justified_lines += fill * left_space + line + fill * (extra_space - left_space) + '\n'

    elif alignment == 'right':
        for line in wrapped:
            justified_lines += fill * (width - lenfunc(line)) + line + '\n'

    elif alignment == 'fill':
        for line in wrapped:
            words = line.split()
            total_words = len(words)
            total_words_width = sum(lenfunc(w) for w in words)
            extra_space = width - total_words_width

            if total_words > 1:
                space_between_words = extra_space // (total_words - 1)
                extra_padding = extra_space % (total_words - 1)
            else:
                space_between_words = extra_space
                extra_padding = 0

            justified_line = ''
            for i, word in enumerate(words):
                justified_line += word
                if i < total_words - 1:
                    justified_line += fill * (space_between_words + (1 if i < extra_padding else 0))

            justified_lines += justified_line + '\n'

    else:
        raise ValueError(
            f"{alignment=} is invalid, must be 'left', 'center', 'right', 'fill' or "
            'a callable function'
        )

    return justified_lines[:-1]

def printwrap(

    *values: object,
    sep: Optional[str] = ' ',
    end: Optional[str] = '\n',
    fill: str = ' ',
    width: Optional[int] = None,
    lenfunc: Callable[[str], Union[int, float]] = len,
    method: Literal['word', 'mono'] = 'word',
    alignment: Union[Callable[[str], str], Literal['left', 'center', 'right', 'fill']] = 'left',
    file: Optional[object] = None,
    flush: bool = False,
    preserve_empty: bool = True

) -> None:

    """
    Print the given values with word wrapping and alignment.

    Parameters:
        *values (object): Values to be printed.
        sep (Optional[str]): Separator between values. Default to ' '.
        end (Optional[str]): String appended after the last value. Default to '\\n'.
        fill (str): Fill character for padding. Default to ' '.
        width (Optional[int]): Width of the output. If None, it tries to use the terminal width or
                               defaults to 70.
        lenfunc (Callable[[str], Union[int, float]]): Function to calculate the length of a string.
                                                      Default is len.
        method (Literal['word', 'mono']): The method to use for wrapping. 'mono' for character-based
                                          wrapping, 'word' for word-based wrapping.
                                          Defaults to 'word'.
        alignment (Union[Callable[[str], str],
                   Literal['left', 'center', 'right', 'fill']]): Alignment of the text.
                                                                 Default is 'left'.
        file (Optional[object]): A file-like object (stream) to write the output to.
                                 Default is None, which means sys.stdout.
        flush (bool): Whether to forcibly flush the stream. Default is False.
        preserve_empty (bool, optional): Whether to preserve empty lines. Defaults to True.
    """

    if width is None:
        try:
            width = get_terminal_size().columns
        except:
            width = 70

    print(
        fillstr(
            (' ' if sep is None else sep).join(map(str, values)),
            width,
            fill,
            lenfunc,
            method,
            alignment,
            preserve_empty
        ),
        end=end,
        file=file,
        flush=flush
    )

def shorten(

    text: str,
    width: Union[int, float] = 70,
    start: int = 0,
    lenfunc: Callable[[str], Union[int, float]] = len,
    placeholder: str = '...',
    strip_space: bool = True

) -> str:

    """
    Shortens the given text to fit within the specified width, optionally including a placeholder.

    Parameters:
        text (str): The text to be shortened.
        width (int | float, optional): The maximum width of the shortened text. Defaults to 70.
        start (int, optional): The starting index of the text to be shortened. Defaults to 0.
        lenfunc (Callable[[str], int | float], optional): A function to calculate
                                                          the length of a string. Defaults to len.
        placeholder (str, optional): The placeholder to append to the shortened text.
                                     Defaults to '...'.
        strip_space (bool, optional): Whether to strip extra spaces in the text. Defaults to True.

    Returns:
        str: The shortened text with the placeholder appended if necessary.
    """

    assert isinstance(text, str), "text must be a string"
    assert isinstance(width, (int, float)), "width must be an integer or float"
    assert isinstance(start, int), "start must be an integer"
    assert callable(lenfunc), "lenfunc must be a callable function"
    assert isinstance(placeholder, str), "placeholder must be a string"

    assert width >= lenfunc(placeholder), "width must be greater than length of the placeholder"
    assert start >= 0, "start must be equal to or greater than 0"

    if strip_space:
        text = ' '.join(text.split())

    if start == 0:
        current_char = ''
    elif start >= len(text):
        return ''
    else:
        current_char = placeholder

    for char in text[start:]:
        if lenfunc(current_char + char + placeholder) <= width:
            current_char += char
        else:
            current_char += placeholder
            if lenfunc(current_char) > width:
                return placeholder
            return current_char

    return current_char