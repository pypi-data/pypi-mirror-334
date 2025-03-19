#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import threading
import typing as t

import hallyd
import klovve.pieces.headered_panel
import klovve.pieces.log_pager.entry

import krrez.apps.pieces.session_interaction
import krrez.flow.dialog
import krrez.flow.logging
import krrez.flow.watch


class Model(klovve.Model):

    @staticmethod
    def datetime_to_str(d):
        return d.strftime("%X")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        @klovve.reaction(owner=self)
        def _sewa():
            self.headered_state = None
            if self.session:
                session = self.session
                self.__interaction_request_fetcher = session.context._interaction_request_fetcher_for_session(
                    session, _SessionViewConfigValuesProvider(self))
                self.__interaction_request_fetcher.__enter__()  # TODO __exit__ ?!

                self.__last_installed_bits_count = -1
                self.__block_nodes = {}
                self.__previous_state = None

                self._session_watch = krrez.flow.watch.Watch(
                    session, log_block_arrived_handler=self.__block_arrived,
                    log_block_changed_handler=self.__block_data_changed,
                    bit_graph_image_changed_handler=self.__bit_graph_image_changed,
                    status_changed_handler=self.__infos_changed)

                #TODO unregister?
                self.__infos_changed()
#                yy = self.session_watch.__exit__
 #               self.session_watch.__exit__ = lambda *a: (yy(*a), my_session_watch.__exit__(*a))
#                self.session_watch.__enter__()
                self._session_watch.__enter__()  # TODO

    interactions: list[krrez.apps.pieces.session_interaction.Model] = klovve.ListProperty()

    entries: list[klovve.pieces.log_pager.entry.Model] = klovve.ListProperty()

    bit_graph_image_svg: t.Optional[bytes] = klovve.Property()

    state_text: str = klovve.Property(default="")

    progress: float = klovve.Property(default=0)

    is_finished: bool = klovve.Property(default=False)

    was_successful: t.Optional[bool] = klovve.Property()

    session: t.Optional[krrez.flow.Session] = klovve.Property()

    headered_state: klovve.pieces.headered_panel.Model.State = klovve.Property(
        default=lambda: klovve.pieces.headered_panel.Model.State.BUSY)

    show_tree: bool = klovve.Property(default=False)

    verbose: bool = klovve.Property(default=False)

    actions: list[klovve.view.View] = klovve.ListProperty()

    _session_watch: t.Optional[krrez.flow.watch.Watch] = klovve.Property()

    @klovve.app.in_mainloop
    def __block_arrived(self, parent_block_id, block_id, message, began_at, only_single_time, severity):
        if not block_id:
            return
        parent_block_node = self.__block_nodes[parent_block_id] if parent_block_id else self
        new_block = klovve.pieces.log_pager.entry.Model()
        new_block.message = message
        new_block.began_at = began_at
        new_block.only_verbose = severity < krrez.flow.logging.Severity.INFO
        new_block.only_single_time = only_single_time
        parent_block_node.entries.append(new_block)
        self.__block_nodes[block_id] = new_block

    @klovve.app.in_mainloop
    def __block_data_changed(self, block_id, ended_at):
        self.__block_nodes[block_id].ended_at = ended_at

    @klovve.app.in_mainloop
    def __bit_graph_image_changed(self, bit_graph_image_svg):
        self.bit_graph_image_svg = bit_graph_image_svg

    @klovve.app.in_mainloop
    def __infos_changed(self):
        if len(self._session_watch.installed_bits) != self.__last_installed_bits_count:
            self.__last_installed_bits_count = len(self._session_watch.installed_bits)
            self.progress = self._session_watch.progress
        if self._session_watch.ended_at:
            self.was_successful = self._session_watch.was_successful
            self.is_finished = True
            if self._session_watch.was_successful:
                state_text = f"Succeeded on {self.__time_text(self._session_watch.ended_at)}."
                self.headered_state = klovve.pieces.headered_panel.Model.State.SUCCESSFUL
            else:
                state_text = f"Failed on {self.__time_text(self._session_watch.ended_at)}."
                self.headered_state = klovve.pieces.headered_panel.Model.State.FAILED
        else:
            state_text = f"Running since {self.__time_text(self._session_watch.began_at)}."
            self.headered_state = klovve.pieces.headered_panel.Model.State.BUSY
        state = (self._session_watch.began_at, self._session_watch.ended_at, self._session_watch.was_successful,
                 state_text)
        if state != self.__previous_state:
            self.__previous_state = state
            self.state_text = state_text
            # self.view.set_state(*state)

    @staticmethod
    def __time_text(atime):
        return atime.strftime("%c").strip()  # sometimes there is a space in the end; we don't want that


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def view_for_tree(self):
        pieces, props = self.make_view()

        if self.model.show_tree:
            return pieces.viewer.image(source=props.bit_graph_image_svg)

    @klovve.ComputedProperty
    def interactions(self):
        pieces, props = self.make_view()

        return [pieces.krrez.apps.session_interaction(x) for x in self.model.interactions]

    def compose(self):
        pieces, props = self.make_view()

        return pieces.headered_panel(
            title=props.state_text,
            title_secondary_items=[
                pieces.checkable(text="Show tree", is_checked=props.show_tree),
                pieces.checkable(text="Verbose", is_checked=props.verbose),
            ],
            state=props.headered_state,
            progress=props.progress,
            body=pieces.split(
                item1=pieces.vertical_box(
                    items=[
                        pieces.log_pager(
                            entries=props.entries,
                            show_verbose=props.verbose,
                        ),
                        pieces.vertical_box(items=props.interactions)
                    ]
                ),
                item2=props.view_for_tree,
            ),
            actions=props.actions,
        )


class _SessionViewConfigValuesProvider(krrez.flow.dialog.Provider,
                                       hallyd.lang.AllAbstractMethodsProvidedByTrick[krrez.flow.dialog.Provider]):

    def __init__(self, model: "Model"):
        self.__model = model
        self.__requests = {}

    def __interact(self, kind: str, *args, **kwargs):
        import klovve.drivers
        future = klovve.app.mainloop().create_future()

        def begin_ui_interaction():

            @klovve.app.in_mainloop
            def do():
                request = krrez.apps.pieces.session_interaction.Model(method_name=kind, args=args, kwargs=kwargs)
                self.__model.interactions.append(request)
                self.__requests[request] = request

                @klovve.app.in_mainloop
                def __set_request_answer(_):
                    request.answer = "TODO cancelled"

                future.add_done_callback(__set_request_answer)

                @klovve.reaction(owner=request)
                def __set_future_result():
                    if request.answer is not None and not future.done():
                        future.set_result(request.answer)
                        self.__requests.pop(request)
                        self.__model.interactions.remove(request)

            do()

        threading.Thread(target=begin_ui_interaction, daemon=True).start()
        return future

    def __getattribute__(self, item):
        if (not item.startswith("_")) and (item in dir(krrez.flow.dialog.Endpoint)):
            def method(*args, **kwargs):
                return self.__interact(item, *args, **kwargs)
            return method
        return super().__getattribute__(item)
