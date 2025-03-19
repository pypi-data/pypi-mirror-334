#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.apps.pieces.session
import krrez.flow.watch


class Model(krrez.apps.MainModel):

    all_sessions: list[krrez.flow.Session] = klovve.ListProperty()

    selected_session: t.Optional[krrez.flow.Session] = klovve.Property()

    @staticmethod
    def __all_sessions__is_matching_target_object(target_object, source_object):
        return target_object.name == source_object.name

    @krrez.apps.MainModel.refresher(every_counts=1)
    def __refresh_sessions(self):
        self.all_sessions.update(reversed(self.context.get_sessions()),
                                 is_matching_target_object_func=self.__all_sessions__is_matching_target_object)


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def view_for_panel(self):
        pieces, props = self.make_view()

        if self.model.selected_session:
            return pieces.krrez.apps.session(krrez.apps.pieces.session.Model(session=props.selected_session))

        else:
            return pieces.label(text="There is a list of all sessions from the past on the left hand side."
                                     "\n\nChoose one of them in order to see more details about it.")

    def compose(self):
        pieces, props = self.make_view()

        if len(self.model.all_sessions) == 0:
            return pieces.label(text="You have not installed any Krrez bits yet.")

        else:
            return pieces.list_panel(
                items=props.all_sessions,
                item_label_func=(lambda item: item.name),
                selected_item=props.selected_session,
                body=props.view_for_panel
            )
