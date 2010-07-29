# Copyright (C) 2008-2009 Konstantin Lepa <konstantin.lepa@gmail.com>.
# Copyright (C) 2010 Przemyslaw Iskra <sparky@pld-linux.org>.
#
# This file used to be part of termcolor.
#
# termcolor is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# termcolor is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License
# along with termcolor.  If not, see <http://www.gnu.org/licenses/>.

"""mIRC Color formatting for output in IRC messages."""

import os


__ALL__ = [ 'colored' ]


ATTRIBUTES = dict(
        zip([
            'bold',
            'dark',
            '',
            'underline',
            'blink',
            '',
            'reverse',
            'concealed'
            ],
            range(1, 9)
            )
        )
del ATTRIBUTES['']


HIGHLIGHTS = dict(
        zip([
            'on_white',
            '',
            'on_blue',
            'on_green',
            '',
            'on_red',
            'on_magenta',
            'on_yellow',
            '',
            '',
            'on_cyan'
            '',
            '',
            '',
            'on_grey',
            '',
            ],
            range(0, 15)
            )
        )


COLORS = dict(
        zip([
            'white',
            '',
            'blue',
            'green',
            '',
            'red',
            'magenta',
            'yellow',
            '',
            '',
            'cyan'
            '',
            '',
            '',
            'grey',
            '',
            ],
            range(0, 15)
            )
        )


RESET = '\017'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if os.getenv('MIRC_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if attrs is not None:
            for attr in attrs:
                if attr == 'bold':
                    text = '\002' + text

        if color is not None:
            if on_color is not None:
                text = '\003%.2d,%.2d%s' % (COLORS[color], HIGHLIGHTS[on_color], text)
            else:
                text = '\003%.2d%s' % (COLORS[color], text)
        else:
            if on_color is not None:
                text = '\00301,%.2d%s' % (HIGHLIGHTS[on_color], text)

        text += RESET
    return text

def test():
    test=[[
        colored('Grey color', 'grey'),
        colored('Red color', 'red'),
        colored('Green color', 'green'),
        colored('Yellow color', 'yellow'),
        colored('Blue color', 'blue'),
        colored('Magenta color', 'magenta'),
        colored('Cyan color', 'cyan'),
        colored('White color', 'white')
    ]]

    test+=[[
        colored('On grey color', on_color='on_grey'),
        colored('On red color', on_color='on_red'),
        colored('On green color', on_color='on_green'),
        colored('On yellow color', on_color='on_yellow'),
        colored('On blue color', on_color='on_blue'),
        colored('On magenta color', on_color='on_magenta'),
        colored('On cyan color', on_color='on_cyan'),
        colored('On white color', color='grey', on_color='on_white')
    ]]

    test+=[[
        colored('Bold grey color', 'grey', attrs=['bold']),
        colored('Dark red color', 'red', attrs=['dark']),
        colored('Underline green color', 'green', attrs=['underline']),
        colored('Blink yellow color', 'yellow', attrs=['blink']),
        colored('Reversed blue color', 'blue', attrs=['reverse']),
        colored('Concealed Magenta color', 'magenta', attrs=['concealed']),
        colored('Bold underline reverse cyan color', 'cyan', attrs=['bold', 'underline', 'reverse']),
        colored('Dark blink concealed white color', 'white', attrs=['dark', 'blink', 'concealed'])
    ]]

    test+=[[
        colored('Underline red on grey color', 'red', 'on_grey', ['underline']),
        colored('Reversed green on red color', 'green', 'on_red', ['reverse'])
    ]]

    return [' '.join(x) for x in test]
