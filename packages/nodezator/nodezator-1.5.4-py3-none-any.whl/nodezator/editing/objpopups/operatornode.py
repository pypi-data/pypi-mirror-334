
### standard library imports

from functools import partial, partialmethod

from contextlib import suppress


### local imports

from ...config import APP_REFS

from ...menu.main import MenuManager

from ...our3rdlibs.behaviour import set_status_message

from ...loopman.exception import ContinueLoopException

from ...graphman.operatornode.constants import OPERATIONS_MAP

from .constants import (
    GeneralPopupCommands,
    get_node_info,
)



class OperatorNodePopupMenu(GeneralPopupCommands):

    get_node_info = get_node_info

    def __init__(self):

        super().__init__()

        menu_list = self.NODE_ONLY_SINGLE_COMMANDS.copy()

        node_replacing_submenu = []

        mode_switching_submenu = {
            "label": "Change mode to",
            "children": [
                {
                    "label": "Expanded signature",
                    "command": self.obj_to_expanded_signature,
                },
                {
                    "label": "Callable",
                    "command": self.obj_to_callable,
                },
            ],
        }

        for command in (
            {
                "label": "Replace operation",
                "icon": "operations",
                "children": node_replacing_submenu,
            },
            mode_switching_submenu,
            {
                "label": "Get source info",
                "key_text": "i",
                "icon": "python_viewing",
                "command": self.get_node_info,
            },
        ):
            menu_list.insert(1, command)

        for operation_id in OPERATIONS_MAP:

            node_replacing_submenu.append(
                {
                    "label": operation_id,
                    "command": partial(
                        self.replace_operation,
                        operation_id,
                    ),
                }
            )

        self.operator_node_only_popup = MenuManager(
            menu_list,
            is_menubar=False,
            use_outline=True,
            keep_focus_when_unhovered=True,
        )

        ###

        menu_list.extend(self.NODE_INCLUSIVE_COLLECTIVE_COMMANDS)

        self.operator_node_and_selected_popup = MenuManager(
            menu_list,
            is_menubar=False,
            use_outline=True,
            keep_focus_when_unhovered=True,
        )

    def show(self, operator_node, mouse_pos):

        self.obj_under_mouse = operator_node

        if operator_node in APP_REFS.ea.selected_objs:

            (
                self.operator_node_and_selected_popup.focus_if_within_boundaries(
                    mouse_pos
                )
            )

        else:

            (self.operator_node_only_popup.focus_if_within_boundaries(mouse_pos))

    def replace_operation(self, new_operation_id):
        """Replace node by one with new operation."""
        ### reference obj under mouse locally
        current_node = self.obj_under_mouse

        ### if new operation is equal to the current one,
        ### cancel switching by returning early

        if current_node.data["operation_id"] == new_operation_id:
            return

        ### list pre-existing nodes
        pre_existing_nodes = list(APP_REFS.gm.nodes)

        ### create new node at the same spot the current
        ### one is located

        APP_REFS.ea.insert_node(
            new_operation_id,
            absolute_midtop=(current_node.rect.midtop),
        )

        ### grab reference to newly created node

        new_node = next(
            node for node in APP_REFS.gm.nodes if node not in pre_existing_nodes
        )

        ### set same mode on new node
        new_node.set_mode(current_node.data['mode'], indicate_changes=False)

        ### transfer the connections of the current node
        ### to the new one

        ## reference graph manager locally
        gm = APP_REFS.gm

        ## transfer input sockets' connections

        for input_socket_a, input_socket_b in zip(
            current_node.input_sockets,
            new_node.input_sockets,
        ):

            try:
                parent = input_socket_a.parent
            except AttributeError:
                continue

            gm.socket_a = parent
            gm.socket_b = input_socket_b

            ## execute method, supressing exception it
            ## raises at the end

            with suppress(ContinueLoopException):
                gm.resume_defining_segment()

        ## transfer output node's connections if output
        ## socket of current node has children

        try:
            children = current_node.output_socket.children

        except AttributeError:
            pass

        else:

            parent = new_node.output_socket

            ## must iterate over children's copy since
            ## the list is altered during iteration

            for child in children.copy():

                gm.socket_a = parent
                gm.socket_b = child

                ## execute method, supressing exception it
                ## raises at the end

                with suppress(ContinueLoopException):
                    gm.resume_defining_segment()

        ### delete the current node
        self.delete_obj()

        ### XXX
        ### though there's no need to indicate the file was modified
        ### (is currently unsaved), since
        ### APP_REFS.gm.resume_defining_segment does it for us,
        ### relying on side effects like this is probably not healthy
        ### (for instance, the delete_obj() method call also does
        ### that indirectly, via the editing assistant's
        ### remove_selected() method);
        ###
        ### it will probably take time, but I'll leave this comment
        ### here so this can be scheduled/reviewed/improved in the
        ### future;

        ### report action to user via status bar
        set_status_message("Replaced node by one with new operation")

    def obj_to_mode(self, mode_name):
        self.obj_under_mouse.set_mode(mode_name)

    obj_to_expanded_signature = partialmethod(obj_to_mode, 'expanded_signature')
    obj_to_callable = partialmethod(obj_to_mode, 'callable')
