"""File Manager class extension with operations."""

### standard-library imports

from os import pathsep

from functools import partialmethod


### third-party imports

from pygame.locals import (
    QUIT,
    KEYDOWN,
    KEYUP,
    K_UP,
    K_DOWN,
    K_RETURN,
    K_KP_ENTER,
    K_a,
    KMOD_ALT,
    KMOD_CTRL,
    KMOD_SHIFT,
    K_HOME,
    K_END,
    K_PAGEUP,
    K_PAGEDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)


### local imports

from ..pygamesetup import SERVICES_NS, SCREEN_RECT, blit_on_screen

from ..translation import TRANSLATION_HOLDER as t

from ..dialog import create_and_show_dialog

from ..ourstdlibs.behaviour import (
    empty_function,
    get_oblivious_callable,
)

from ..loopman.exception import (
    SwitchLoopException,
    QuitAppException,
)

from ..surfsman.cache import UNHIGHLIGHT_SURF_MAP

from ..classes2d.single import Object2D



class FileManagerOperations(Object2D):
    """Operations for file manager class."""

    def select_paths(
        self,
        *,
        caption="",
        path_name="",
        expecting_files_only=False,
    ):
        """Return selected paths.

        This method shows the user the file manager
        interface, allowing the user to browse the
        filesystem visually while selecting paths
        to be returned or providing the name for new
        path(s) to be created.

        Parameters
        ==========

        caption (string)
            represents a caption for the widget.
        path_name (string)
            It is used as a path name to be included in the
            selected paths entry. It can actually represent
            multiple path names, as long as you separate each
            path with the path separator character (os.pathsep).
        expecting_files_only (bool)
            When set to True, clicking folders won't cause their
            names to appear in the selection entry. Default is
            False.
        """
        ### blit screen sized semi transparent object

        blit_on_screen(UNHIGHLIGHT_SURF_MAP[SCREEN_RECT.size], (0, 0))

        ### update widget caption label

        self.caption_label.set(

            caption
            if caption
            else t.file_manager.select_paths

        )

        ### store flag
        self.expecting_files_only = expecting_files_only

        ### load paths from the current directory so they
        ### are displayed in the directory panel
        self.dir_panel.load_current_dir_contents()

        ### check whether the current bookmarks still exists
        self.bkm_panel.check_live_bookmarks()

        ### set entry contents
        self.selection_entry.set(path_name)

        ### alias self as the loop holder
        loop_holder = self

        ### set an attribute to keep track of when the user cancelled
        ### selecting paths
        self.cancelled = False

        ### keep looping the execution of methods
        ### "handle_input", "update" and "drawing" of the
        ### loop holder until running is set to False

        self.running = True

        while True:

            try:

                while self.running:

                    ### perform various checkups for this frame;
                    ###
                    ### stuff like maintaing a constant framerate and more
                    SERVICES_NS.frame_checkups()

                    ### run the GUD methods (check the glossary
                    ### for loop holder/loop/methods)

                    loop_holder.handle_input()
                    loop_holder.update()
                    loop_holder.draw()

                ## if we leave the inner loop, also exit the outer loop
                break

            ### if a SwitchLoopException occur, set a new
            ### object to become the loop holder

            except SwitchLoopException as err:

                ## use the loop holder in the err
                ## attribute of same name
                loop_holder = err.loop_holder

        ### blit smaller semi transparent object
        self.rect_size_semitransp_obj.draw()

        ### if the user didn't cancel and only files are expected to be
        ### selected, we must update the selection according to the entry,
        ### since they might be out of sync

        ### XXX review behaviour of this expecting_files_only flag.
        ### For instance, what if the person selected folders as well?
        ### When you do that, update docstrings and related comments
        ### accordingly

        if not self.cancelled and self.expecting_files_only:
            self.update_selection_from_entry()

        ### return a copy of the path selection
        return tuple(self.path_selection)

    def handle_input(self):
        """Handle event queue."""
        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                raise QuitAppException

            ### KEYDOWN

            elif event.type == KEYDOWN:

                if event.key == K_UP:

                    ## if alt key is pressed as well, load
                    ## the parent folder

                    if event.mod & KMOD_ALT:
                        self.load_parent()

                    ## otherwise just go to the previous
                    ## item
                    else:
                        self.go_to_previous()

                elif event.key == K_DOWN:
                    self.go_to_next()

            ### KEYUP

            elif event.type == KEYUP:

                if event.key in (K_RETURN, K_KP_ENTER):
                    self.load_selected()

                ## de/select all

                elif event.key == K_a and event.mod & KMOD_CTRL:

                    if event.mod & KMOD_SHIFT:
                        self.deselect_all()

                    else:
                        self.select_all()

                ## jump to first/last item

                elif event.key == K_HOME:

                    # if alt key is pressed as well, load
                    # the parent folder

                    if event.mod & KMOD_ALT:
                        self.load_home()

                    ## otherwise just go to the previous
                    ## item
                    else:
                        self.go_to_first()

                elif event.key == K_END:
                    self.go_to_last()

                ## jump the number of items showing

                elif event.key == K_PAGEUP:
                    self.jump_many_up()

                elif event.key == K_PAGEDOWN:
                    self.jump_many_down()

            ### MOUSEBUTTONDOWN

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:
                    self.on_mouse_click(event)

            ### MOUSEBUTTONUP

            elif event.type == MOUSEBUTTONUP:

                if event.button == 1:
                    self.on_mouse_release(event)

                elif event.button == 4:
                    self.scroll_contents(event.pos, "up")

                elif event.button == 5:
                    self.scroll_contents(event.pos, "down")

    def on_mouse_action(self, method_name, event):
        """Check whether mouse action occurred inside widget.

        Parameters
        ==========
        method_name (string)
            either 'on_mouse_click' or 'on_mouse_release',
            actions which we track in this method.
        event (custom instance)
            pygame.event.Event of type
            pygame.MOUSEBUTTONDOWN or MOUSEBUTTONUP;
            check pygame.event module documentation on
            pygame website for more info about these event
            objects.

        If inside the file manager boundaries, determine
        if it was inside one of the panels or buttons,
        triggering the appropriate action. If outside,
        get out of the file manager loop using the
        'cancel' method.
        """
        mouse_pos = event.pos

        ### if mouse was released inside file manager

        if self.rect.collidepoint(mouse_pos):

            ## see if one of the panels collides

            for panel in self.panels:

                if panel.rect.collidepoint(mouse_pos):

                    try:
                        method = getattr(panel, method_name)

                    except AttributeError:
                        pass

                    else:

                        method(event)
                        return

            ## see if buttons were pressed (mouse released)

            for button in self.buttons:

                if button.rect.collidepoint(mouse_pos):

                    try:
                        method = getattr(button, method_name)
                    except AttributeError:
                        pass

                    else:

                        method(event)
                        return

        ### otherwise trigger the exit of the file manager
        ### loop by cancelling
        else:
            self.cancel()

    on_mouse_click = partialmethod(on_mouse_action, "on_mouse_click")

    on_mouse_release = partialmethod(on_mouse_action, "on_mouse_release")

    def scroll_contents(self, mouse_pos, orientation):
        """Verify if scrolling contents and scroll if so.

        Parameters
        ==========
        mouse_pos (2-tuple of integers)
            represents the point on screen where the object
            was 'scrolled'.
        orientation (string)
            represents a hint indicating the direction of
            the scrolling. If it equals 'up' we perform
            scrolling up, otherwise, whatever the value,
            we perform the scrolling down.
        """
        ### if inside directory panel, scroll it

        if self.dir_panel.rect.collidepoint(mouse_pos):

            if orientation == "up":
                self.dir_panel.scroll_up()

            else:
                self.dir_panel.scroll_down()

        ### if inside bookmark panel, scroll it

        elif self.bkm_panel.rect.collidepoint(mouse_pos):

            if orientation == "up":
                self.bkm_panel.scroll_up()

            else:
                self.bkm_panel.scroll_down()

    def draw(self):
        """Draw different objects/groups and update screen."""
        super().draw()

        self.labels.draw()

        self.panels.call_draw()

        self.buttons.draw()

        SERVICES_NS.update_screen()

    def store_current_selection(self):
        """Retrieve path info and store it."""
        ### store a list of selected paths in the
        ### path_selection attribute
        self.path_selection = self.dir_panel.get_selection()

    def get_selection_text(self):
        """Return custom text according to selected paths."""
        ### reference the path selection in a local variable
        path_selection = self.path_selection

        ### if its has more than one items, the text
        ### is all the names of the paths joined by ', '

        if len(path_selection) > 1:
            text = pathsep.join(path.name for path in path_selection)

        ### otherwise...

        else:

            ### try assigning the name of the first path
            ### as the text
            try:
                text = path_selection[0].name

            ### if it fails, though, then use an empty
            ### string as the text
            except IndexError:
                text = ''

        return text

    def update_entry_with_selected(self):
        """If a file was selected, copy its name to entry."""
        ps = self.path_selection

        ps.clear()

        ps.extend(self.dir_panel.get_selection())

        if (
            self.expecting_files_only
            and len(ps) == 1
            and ps[0].is_dir()
        ):
            pass

        else:

            name = pathsep.join(
                path.name
                for path in self.path_selection
            )

            self.selection_entry.set(name, False)

    def update_selection_from_entry(self):

        entry_contents = self.selection_entry.get()

        self.path_selection.clear()

        if entry_contents:

            current_dir = self.dir_panel.current_dir

            self.path_selection.extend(

                current_dir / path_name.strip()

                for path_name
                in entry_contents.split(pathsep)

            )

        self.dir_panel.update_data_from_path_selection()

    def submit(self):
        """Trigger exit of file browser, if there's a selection."""
        ### if we are only interested in selecting files, then the
        ### selection shown in the directory panel and the selection entry
        ### might be out of sync, so we make sure they are the same,
        ### based on the entry's content

        if self.expecting_files_only:
            self.update_selection_from_entry()

        ### if there's a selection, we can trigger the exit of the
        ### local loop by setting the 'running' flag off
        if self.path_selection:
            self.running = False

        ### otherwise, we display a proper message
        ### explaining that we can't exit the loop yet
        ### because no path was typed in the entry or
        ### selected
        else:
            create_and_show_dialog(
                (
                    "You must either type name(s) for new path(s) in"
                    " the entry at the bottom or select existing ones"
                ),
            )

    def cancel(self):
        """Cancel selecting/creating path.

        Works by clearing the path selection, which causes no
        path to be returned.

        The 'cancelled' attribute is also set to True, to indicate the
        user cancelled providing path(s).

        The 'running' attribute is also set to False, which
        triggers the exit of the file manager loop which
        you can find on the select_paths method.
        """
        self.path_selection.clear()
        self.cancelled = True
        self.running = False
