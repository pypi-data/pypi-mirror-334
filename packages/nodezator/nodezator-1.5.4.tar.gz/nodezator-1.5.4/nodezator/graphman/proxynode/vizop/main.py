"""Facility for visuals related node class extension."""

### standard library import
from functools import partialmethod


### third-party import
from pygame.draw import rect as draw_rect


### local imports

from ....config import APP_REFS

from ....pygamesetup import SCREEN

## function for injection
from .reposition import reposition_elements


class VisualRelatedOperations:
    """Manages operations on visual node object."""

    reposition_elements = reposition_elements

    def on_mouse_action(self, method_name, event):
        """Check whether any object was targeted by mouse.

        if not, act as though the node itself was the
        target of the mouse action.

        Parameters
        ==========

        event (pygame.event.Event of
            pygame.MOUSEBUTTONDOWN/MOUSEBUTTONUP type)

            required in order to comply with protocol
            used; needed here so we can retrieve the
            position of the mouse click in order to
            know over which object the mouse button was
            clicked/released.

            Check pygame.event module documentation on
            pygame website for more info about this event
            object.
        """
        ### retrieve mouse position
        mouse_pos = event.pos

        ### check whether any of the objects collided with
        ### the mouse position when it was clicked,
        ### calling the appropriate mouse method of the
        ### object if available

        for obj in self.mouse_aware_objects:

            if obj.rect.collidepoint(mouse_pos):

                ### if the mouse release method exists,
                ### we store it and execute it, otherwise
                ### we just pass

                try:
                    method = getattr(obj, method_name)
                except AttributeError:
                    pass
                else:
                    method(event)

                ### we then break out of the loop, since
                ### at this moment there will be no point
                ### in looking whether the other objects
                ### collided (we assume none of the
                ### objects' rects intersect)
                break

        ### if we don't collide with any object though, we
        ### consider as though the node itself was the
        ### target of the mouse method;
        ###
        ### if such method is 'on_mouse_click' or
        ### 'on_mouse_release', set on or off the
        ### 'mouse_click_target' flag according to the
        ### method name; the flag is used to support the
        ### "move by dragging" feature; if the event
        ### is 'on_mouse_release' we also change the
        ### selection state of this node;
        ###
        ### if we are dealing with a right mouse release
        ### method, we show the popup menu

        else:

            if method_name == "on_mouse_click":
                self.mouse_click_target = True

            elif method_name == "on_mouse_release":

                self.mouse_click_target = False
                APP_REFS.ea.change_selection_state(self)

            elif method_name == "on_right_mouse_release":

                (APP_REFS.ea.proxy_node_popup_menu.show(self, event.pos))

    on_mouse_click = partialmethod(on_mouse_action, "on_mouse_click")

    on_mouse_release = partialmethod(
        on_mouse_action,
        "on_mouse_release",
    )

    on_right_mouse_release = partialmethod(
        on_mouse_action,
        "on_right_mouse_release",
    )

    def draw(self):
        """Draw node visual elements on screen."""
        for obj in self.visual_objects:
            obj.draw()

    def draw_selection_outline(self, color):
        """Draw outline around to indicate it is selected."""
        draw_rect(SCREEN, color, self.rect.inflate(-8, 4), 4)
