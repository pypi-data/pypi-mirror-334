#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import enum
import typing as t

import hallyd
import klovve

import krrez.apps.pieces.session
import krrez.coding
import krrez.flow.watch
import krrez.testing.landmark


class Model(krrez.apps.MainModel):

    @klovve.ComputedProperty
    def __foo(self):
        if self.start_with_test_plan:
            self.selected_test_plan = self.start_with_test_plan
            with klovve.data.deps.no_dependency_tracking():
                self.start_test_plan(None)

    all_sessions = klovve.ListProperty()

    selected_session: t.Optional[krrez.flow.Session] = klovve.Property()

    all_test_plans = klovve.ListProperty()

    selected_test_plan: t.Optional[str] = klovve.Property()

    start_with_test_plan: t.Optional[str] = klovve.Property()

    foox = klovve.Property(default=1)#TODO

    @klovve.ComputedProperty
    def selected_session_landmark_size(self) -> t.Optional[int]:
        if self.selected_session:
            try:
                if krrez.testing.landmark.has_resumable_landmark(self.selected_session):
                    return krrez.testing.landmark.landmark_size_on_disk(self.selected_session)
            except IOError:
                pass

    @klovve.ComputedProperty
    def selected_session_has_landmark(self) -> bool:
        str(self.foox)

        if self.selected_session:
            try:
                return krrez.testing.landmark.has_resumable_landmark(self.selected_session)
            except IOError:
                pass

    @klovve.ComputedProperty
    def selected_session_can_be_aborted(self) -> bool:
        str(self.foox)

        if self.selected_session:
            return krrez.flow.watch.Watch(self.selected_session).ended_at is None
        return False

    @staticmethod
    def __sessions__is_matching_target_object(target_object, source_object):
        if (not target_object) and (not source_object):
            return True
        return target_object.name == source_object.name

    @krrez.apps.MainModel.refresher(every_counts=1)
    def __refresh_sessions(self):
        self.all_sessions.update([None, *reversed(krrez.testing.all_test_sessions(self.context))],
                                 is_matching_target_object_func=self.__sessions__is_matching_target_object)

    @krrez.apps.MainModel.refresher()
    def __refresh_available_test_plans(self):
        self.all_test_plans = krrez.testing.all_available_test_plans()

    @krrez.apps.MainModel.refresher(every_counts=1)
    def __refresh_landmark_foo(self):
        self.foox += 1

    def start_test_plan(self, context) -> None:
        watch = krrez.testing.start_tests([krrez.coding.TestPlans.test_plan_name_to_bit_name(self.selected_test_plan)],
                                          context=self.context)
        self.__refresh_sessions()
        new_session_ = [session for session in self.all_sessions if session and session.name == watch.session.name]
        if new_session_:
            self.selected_session = new_session_[0]


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def panel_body_actions(self):
        pieces, props = self.make_view()

        async def landmark_foo(context):
            landmark_size_str = hallyd.fs.byte_size_to_human_readable(self.model.selected_session_landmark_size)
            idx = await context.dialog(pieces.interact.triggers(
                message=f"This test run has been stopped immaturely, e.g. due to a system shutdown.\n\n"
                        f"There is a landmark (taking {landmark_size_str}) that you can resume from.\n\n"
                        f"Please choose what you want to do with this landmark.",
                triggers=["Resume from here", "Delete"]))
            if idx == 0:
                reader = krrez.testing.landmark.start_resume_tests_from_landmark(self.model.selected_session)
                self.model._Model__refresh_sessions()  # TODO
                new_session_ = [s for s in self.model.all_sessions if s and s.name == reader.session.name]
                if new_session_:
                    self.model.selected_session = new_session_[0]
            elif idx == 1:
                idx = await context.dialog(
                    pieces.interact.triggers(message="Do you really want to remove this landmark?",
                                             triggers=["Yes", "No"]))
                if idx == 0:
                    krrez.testing.landmark.forget_landmark(self.model.selected_session)
                    self.model.selected_session, fuh = None, self.model.selected_session
                    self.model.selected_session = fuh

        async def abort(context):
            idx = await context.dialog(
                pieces.interact.triggers(message="Do you really want to abort this test run?",
                                         triggers=["Yes", "No"]))
            if idx == 0:
                krrez.flow.watch.Watch(self.model.selected_session).abort()
                self.model.selected_session, fuh = None, self.model.selected_session
                self.model.selected_session = fuh

        actions = []

        if self.model.selected_session_can_be_aborted:
            actions.append(pieces.button(text="Abort", action=abort))

        if self.model.selected_session_has_landmark:
            actions.append(pieces.button(text="Landmark", action=landmark_foo))

        return actions

    @klovve.ComputedProperty
    def panel_body(self):
        pieces, props = self.make_view()

        # TODO at the moment there is no way to refresh the body action buttons due to some klovve bug?!

        if self.model.selected_session:
            return pieces.krrez.apps.session(session=props.selected_session,
                                             actions=props.panel_body_actions)

        else:
            return pieces.krrez.apps.testing.new_test_run(all_test_plans=props.all_test_plans,
                                                          selected_test_plan=props.selected_test_plan,
                                                          start_test_func=props.start_test_plan)

    def compose(self):
        pieces, props = self.make_view()

        if self.model.start_with_test_plan:
            return self.panel_body

        else:
            return pieces.list_panel(
                items=props.all_sessions,
                item_label_func=lambda item: item.name if item else "New test run",
                selected_item=props.selected_session,
                body=props.panel_body)
