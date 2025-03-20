"""Facility for third party behaviour related tools."""

### standard library imports

from functools import partial

from contextlib import contextmanager


### third-party imports
from pygame.display import get_caption, set_caption


### local imports

from ..config import APP_REFS

from ..pygamesetup.constants import get_fps

from ..loopman.exception import QuitAppException, CloseFileException

from ..translation import STATUS_MESSAGES_MAP



### utility functions

set_status_message = partial(setattr, APP_REFS, "status_message")


def set_status_message_from_key(key):
    set_status_message(STATUS_MESSAGES_MAP[key])


def quit_app():
    """Raise a quit app exception."""
    raise QuitAppException

def close_loaded_file():
    """Raise a close file exception."""
    raise CloseFileException

def are_changes_saved():
    """Return True if there are no unsaved changes."""
    ### retrieve the title in the window
    title, _ = get_caption()

    ### the absence of a '*' character at the beginning
    ### of the window title marks the absence of unsaved
    ### changes
    if not title.startswith("*"):
        return True


def toggle_caption(indicate_saved):
    """Toggle caption to indicate saved/unsaved state.

    That is, to indicate whether there are changes in the
    positions which aren't saved on file.

    indicate_saved (boolean)
        hints to whether or not we should indicate that
        changes made are saved.
    """
    title, icontitle = get_caption()

    ### remove asterisk

    if indicate_saved:

        if not are_changes_saved():

            title = title[1:]
            icontitle = icontitle[1:]

    ### add asterisk

    else:

        if are_changes_saved():

            title = "*" + title
            icontitle = "*" + icontitle

    ### set the caption using the resulting
    ### title and icontitle
    set_caption(title, icontitle)


indicate_saved = partial(toggle_caption, True)
indicate_unsaved = partial(toggle_caption, False)


@contextmanager
def saved_or_unsaved_state_kept():
    """Restore saved/unsaved state at the end, if needed.

    That is, this context manager makes sure that, once we
    leave the context, the saved/unsaved state is kept the
    same it was at the beginning.
    """
    ### store state before entering context
    changes_were_saved = are_changes_saved()

    ### enter context
    try:
        yield

    ### now that we left the context, restore the state
    ### if it is different from when it was at the
    ### beginning

    finally:

        changes_are_saved = are_changes_saved()

        if changes_were_saved and not changes_are_saved:
            indicate_saved()

        elif not changes_were_saved and changes_are_saved:
            indicate_unsaved()


def get_current_fps():
    """Return current fps custom formatted.

    Gets the fps from the clock object then round it and
    turn it into a string like this:

     9.18484242 -> '09'
    29.18484242 -> '29'
    """
    return str(round(get_fps())).rjust(2, "0")
