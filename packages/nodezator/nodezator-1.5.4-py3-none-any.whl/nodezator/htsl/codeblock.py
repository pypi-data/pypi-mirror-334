
### standard library imports

from os import linesep

from functools import partial


### third-party imports

from pygame import Surface

from pygame.draw import rect as draw_rect

try:
    from pygame.scrap import put_text
except ImportError:
    pass



### local imports

from ..our3rdlibs.button import Button

from ..classes2d.single import Object2D

from ..surfsman.render import combine_surfaces, render_rect

from ..surfsman.icon import render_layered_icon

from ..surfsman.draw import draw_border

from ..textman.render import render_text, get_text_size

from ..textman.text import (
    get_normal_lines,
    get_highlighted_lines,
)

from ..syntaxman.exception import SyntaxMappingError

from ..syntaxman.utils import get_ready_theme

from ..dialog import create_and_show_dialog

from ..colorsman.colors import BLACK, HTSL_GENERAL_TEXT_FG, HTSL_CANVAS_BG

from .constants import (
    GENERAL_CODE_TEXT_SETTINGS,
    NORMAL_TEXT_SETTINGS,
    PRE_TEXT_SETTINGS,
    PRE_TEXT_BORDER,
)

###

THEME_MAP = get_ready_theme(
    "python",
    GENERAL_CODE_TEXT_SETTINGS,
)

DIGIT_WIDTH, _ = get_text_size(
    "0",
    font_height=(GENERAL_CODE_TEXT_SETTINGS["font_height"]),
    font_path=GENERAL_CODE_TEXT_SETTINGS["font_path"],
)

###

def _get_clipboard_button_surf():
    """Create and return surface representing clipboard button."""

    ## text
    text_surf = render_text(text='Copy to clipboard', **NORMAL_TEXT_SETTINGS)

    ## icon

    icon_surf = Surface((20, 24)).convert()

    icon_surf.fill(HTSL_CANVAS_BG)

    _smaller_rect = icon_surf.get_rect().inflate(-8, -8)

    draw_rect(icon_surf, HTSL_CANVAS_BG, _smaller_rect)
    draw_rect(icon_surf, HTSL_GENERAL_TEXT_FG, _smaller_rect, 2)

    _smaller_rect.move_ip(4, 4)

    draw_rect(icon_surf, HTSL_CANVAS_BG, _smaller_rect)
    draw_rect(icon_surf, HTSL_GENERAL_TEXT_FG, _smaller_rect, 2)

    ## final combination

    surf = combine_surfaces(
        (text_surf, icon_surf),
        retrieve_pos_from="midright",
        assign_pos_to="midleft",
        offset_pos_by=(4, 0),
        padding=6,
        background_color=HTSL_CANVAS_BG,
    )

    draw_border(surf, color=HTSL_GENERAL_TEXT_FG, thickness=2)

    return surf

COPY_TO_CLIPBOARD_SURF =  _get_clipboard_button_surf()


def _get_save_button_surf():
    """Create and return surface representing save button."""

    ## text
    text_surf = render_text(text='Save on disk', **NORMAL_TEXT_SETTINGS)

    ## icon


    _arrow_down_icon = render_layered_icon(
        chars=[chr(ordinal) for ordinal in (50, 51)],
        dimension_name="height",
        dimension_value=12,
        rotation_degrees=180,
        colors=[
            BLACK,
            (30, 130, 70),
        ],
    )

    _ssd_icon = render_layered_icon(
        chars=[chr(ordinal) for ordinal in range(83, 87)],
        dimension_name="width",
        dimension_value=18,
        colors=[
            BLACK,
            (255, 0, 0),
            (0, 0, 255),
            (140, 140, 140),
        ],
        background_width=20,
        background_height=24,
        retrieve_pos_from="midbottom",
        assign_pos_to="midbottom",
        offset_pos_by=(0, -2),
    )

    icon_surf = combine_surfaces(
        [_ssd_icon, _arrow_down_icon],
        retrieve_pos_from="midbottom",
        assign_pos_to="midbottom",
        offset_pos_by=(0, -10),
    )


    ## final combination

    surf = combine_surfaces(
        (text_surf, icon_surf),
        retrieve_pos_from="midright",
        assign_pos_to="midleft",
        offset_pos_by=(4, 0),
        padding=6,
        background_color=HTSL_CANVAS_BG,
    )

    draw_border(surf, color=HTSL_GENERAL_TEXT_FG, thickness=2)

    return surf

SAVE_ON_DISK_SURF =  _get_save_button_surf()



### TODO ponder: should the code block surfaces be cached
### across different .htsl pages? they probably should.


def get_python_codeblock(python_code_element):

    text = python_code_element.childNodes[0].data

    ### by default, first line is stripped

    ## XXX maybe include <python> tag attribute "includefirst", to include
    ## first line, which is otherwise stripped by default;
    text = linesep.join(text.splitlines()[1:])

    ###

    try:

        lines = get_highlighted_lines(
            "python", text, syntax_settings_map=(THEME_MAP["text_settings"])
        )

    ## if a syntax mapping error occurs...

    except SyntaxMappingError:

        background_color = GENERAL_CODE_TEXT_SETTINGS["background_color"]

        lines = get_normal_lines(
            text,
            GENERAL_CODE_TEXT_SETTINGS,
        )

        lineno_settings = GENERAL_CODE_TEXT_SETTINGS

    else:

        background_color = THEME_MAP["background_color"]

        ##

        text_settings = THEME_MAP["text_settings"]

        try:
            lineno_settings = text_settings["line_number"]

        except KeyError:
            lineno_settings = text_settings["normal"]

    ### position text objects representing lines one below the other
    lines.rect.snap_rects_ip(retrieve_pos_from="bottomleft", assign_pos_to="topleft")

    ### if line numbers must be used, create surface with them

    uselineno = python_code_element.getAttribute("uselineno") or "false"

    if uselineno == 'true':

        first_lineno = int(python_code_element.getAttribute("linenofrom") or "1")

        ## calculate the number of digits needed to
        ## display the number of the last line
        max_chars = len(str((first_lineno - 1) + len(lines)))

        ## width of panel is total width occupied
        ## by max_chars plus 2 additional characters
        ## used as padding
        lineno_width = (max_chars + 2) * DIGIT_WIDTH

        ### areas

        code_area = lines.rect.copy()
        code_area.width += 10
        code_area.height += 10

        lineno_area = lines.rect.copy()
        lineno_area.width = lineno_width
        lineno_area.height += 10

        code_area.topleft = lineno_area.topright

        total_area = lineno_area.union(code_area)

        surf = render_rect(*total_area.size)

        for bg_color, area in (
            (
                lineno_settings["background_color"],
                lineno_area,
            ),
            (
                background_color,
                code_area,
            ),
        ):

            draw_rect(surf, bg_color, area)

        ###

        lines.rect.topleft = lineno_area.topright
        lines.rect.move_ip(5, 5)

        for lineno, line in enumerate(lines, first_lineno):

            surf.blit(line.image, line.rect)

            lineno_surf = render_text(
                str(lineno).rjust(max_chars, "0"),
                **lineno_settings,
            )

            surf.blit(lineno_surf, (DIGIT_WIDTH, line.rect.top))

    ### otherwise ignore them

    else:

        code_area = lines.rect.copy()
        code_area.width += 10
        code_area.height += 10

        surf = render_rect(*code_area.size, background_color)

        lines.rect.move_ip(5, 5)

        for line in lines:
            surf.blit(line.image, line.rect)


    ###

    obj = Object2D.from_surface(surf)
    obj.tag_name = 'python'
    obj.text = text

    ###

    return obj


def get_pre_textblock(pre_element):

    text = pre_element.childNodes[0].data

    ### by default, first line is stripped
    text = linesep.join(text.splitlines()[1:])

    ###
    background_color = PRE_TEXT_SETTINGS["background_color"]

    lines = get_normal_lines(
        text,
        PRE_TEXT_SETTINGS,
    )

    lineno_settings = PRE_TEXT_SETTINGS

    ### position text objects representing lines one
    ### below the other
    lines.rect.snap_rects_ip(retrieve_pos_from="bottomleft", assign_pos_to="topleft")

    ### lineno

    uselineno = pre_element.getAttribute("uselineno") or "false"

    if uselineno == "true":

        first_lineno = int(pre_element.getAttribute("linenofrom") or "1")

        ## calculate the number of digits needed to
        ## display the number of the last line
        max_chars = len(str((first_lineno - 1) + len(lines)))

        ## width of panel is total width occupied
        ## by max_chars plus 2 additional characters
        ## used as padding
        lineno_width = (max_chars + 2) * DIGIT_WIDTH

        ### areas

        text_area = lines.rect.copy()
        text_area.width += 15
        text_area.height += 10

        lineno_area = lines.rect.copy()
        lineno_area.width = lineno_width
        lineno_area.height += 10

        text_area.topleft = lineno_area.topright

        total_area = lineno_area.union(text_area)

        surf = render_rect(*total_area.size)

        for bg_color, area in (
            (
                lineno_settings["background_color"],
                lineno_area,
            ),
            (
                background_color,
                text_area,
            ),
        ):

            draw_rect(surf, bg_color, area)

        ###

        lines.rect.topleft = lineno_area.topright
        lines.rect.move_ip(5, 5)

        for lineno, line in enumerate(lines, first_lineno):

            surf.blit(line.image, line.rect)

            lineno_surf = render_text(
                str(lineno).rjust(max_chars, "0"),
                **lineno_settings,
            )

            surf.blit(lineno_surf, (DIGIT_WIDTH, line.rect.top))

    ###
    else:

        ### text area

        text_area = lines.rect.copy()
        text_area.width += 15
        text_area.height += 10

        surf = render_rect(*text_area.size)

        draw_rect(surf, background_color, text_area)

        ###

        lines.rect.move_ip(5, 5)

        for line in lines:
            surf.blit(line.image, line.rect)


    draw_border(surf, PRE_TEXT_BORDER)
    ###

    obj = Object2D.from_surface(surf)
    obj.tag_name = 'pre'
    obj.text = text

    return obj

def save_on_disk(text, extension):

    ### TODO the import below is performed inside this function
    ### temporariy, in order to avoid circular imports;
    ###
    ### however, given how often it is used throughout the package,
    ## it should probably be passed around as a reference rather than
    ### being imported, similarly to how the node manager, window manager
    ### and editing assistant are passed around as references;

    ### import select paths
    from ..fileman.main import select_paths

    ### prompt user to pick filepath from file manager

    paths = (
        select_paths(
            caption="Save code snippet on disk",
            path_name=f'snippet{extension}',
            expecting_files_only=True,
        )
    )

    ### if paths were given, it is a single one, we
    ### should assign it to 'filepath' variable

    if paths:
        filepath = paths[0]

    ### if the user didn't provide paths, though,
    ### return earlier

    else:

        create_and_show_dialog("Cancelled saving snippet on disk.")
        return

    ###

    try:
        filepath.write_text(text, encoding='utf-8')

    except Exception as err:

        error_message = "An error occurred while trying to save snippet on disk: "
        error_message += str(err)[:200]
        create_and_show_dialog(error_message)

def get_copy_button(text, bottomright):

    return Button(

        ## surf
        COPY_TO_CLIPBOARD_SURF,

        ## other arguments

        command = partial(put_text, text),
        coordinates_name='bottomright',
        coordinates_value=bottomright,

    )

def get_save_button(text, extension, bottomright):

    return Button(

        ## surf
        SAVE_ON_DISK_SURF,

        ## other arguments

        command = partial(save_on_disk, text, extension),
        coordinates_name='bottomright',
        coordinates_value=bottomright,

    )
