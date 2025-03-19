#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import enum
import threading
import time
import typing as t

import klovve
import klovve.pieces.busy_animation

import krrez.api
import krrez.apps.pieces.session
import krrez.flow
import krrez.flow.watch
import krrez.seeding.profile_loader


class Model(krrez.apps.MainModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__seed_thread = None

        @klovve.reaction(owner=self)
        def on_current_profile_changed():
            _ = self.selected_profile, self.selected_target_device
            with klovve.data.deps.no_dependency_tracking():
                self.__refresh_available_targets()
                self.__refresh_profile_open_parameters()
                self.__refresh_is_form_data_valid()

    class State(enum.Enum):
        FORM = enum.auto()
        AWAIT_SEEDING = enum.auto()
        SEEDING = enum.auto()
        AWAIT_FINISHING = enum.auto()
        FINISHING = enum.auto()

    state: State = klovve.Property(default=State.FORM)

    all_profiles = klovve.ListProperty()

    selected_profile = klovve.Property()

    seed_user = klovve.Property()

    after_seeding_summary_message: t.Optional[str] = klovve.Property()

    finish_was_confirmed: bool = klovve.Property(default=False)

    selected_profile_open_parameters = klovve.ListProperty()

    additional_seed_config: dict[str, str] = klovve.Property(default=lambda: {})  # TODO use/implement

    all_target_devices = klovve.ListProperty()

    selected_target_device = klovve.Property()

    is_form_data_valid: bool = klovve.Property(default=False)

    seed_session = klovve.Property()

    finish_from_here: t.Optional[bool] = klovve.Property()

    finish_from_here_session: t.Optional[krrez.flow.Session] = klovve.Property()

    def seed(self, context):
        profile = self.selected_profile.type.get(self.additional_seed_config)
        if self.__seed_thread:
            raise RuntimeError("seeding is already in progress")
        self.__seed_thread = threading.Thread(target=self.__seed, args=(profile, self.selected_target_device.path), daemon=True)
        self.__seed_thread.start()

    class _SeedAct(krrez.seeding.SeedAct):

        def __init__(self, main_app: "Model", *, profile: "krrez.api.Profile", target_device: "krrez.api.Path"):
            super().__init__(profile=profile, target_device=target_device)
            self.__main_app = main_app

        def _begin(self):
            self.__foo = self.__main_app.blocking_interrupts(
                f"You are currently seeding Krrez to '{self._target_device}'. If you close this app,"
                f" this process will continue to happen, but you will not be able to see when"
                f" it finishes.")
            self.__foo.__enter__()
            self.__main_app.after_seeding_summary_message = None
            self.__main_app.seed_session = self.__main_app.finish_from_here_session = None
            self.__main_app.finish_from_here = None
            self.__main_app.selected_target_device = self.__main_app.selected_profile = None
            self.__main_app.additional_seed_config = {}
            self.__main_app.state = Model.State.AWAIT_SEEDING

        def _start_creating_installation_medium(self, watch):
            self.__main_app.seed_session = watch.session
            self.__main_app.state = Model.State.SEEDING

        def _installation_medium_created(self, seed_user, seed_strategy):
            self.__main_app.seed_user = seed_user

            message = "Your installation medium is now ready to be used!\n"
            if seed_user:
                message += (f"Please write down the following credentials somewhere. They are only valid during"
                            f" installation.\n"
                            f"     User name: {seed_user.username}  /  Password: {seed_user.password}\n\n")
            message += seed_strategy.next_step_message + "\n\n"
            if seed_user:
                message += (
                    "There are two ways to finish the installation from there: You can either log in to that machine,"
                    " via ssh or locally, with the account from above, and follow the on-screen instructions."
                    " You are done here in that case."
                    " Another way is to finish the installation from here. That needs a network connection to the"
                    " target machine. In case of problems, or for any other reasons, you can just switch to the former"
                    " way whenever you want.")

            self.__foo.__exit__(None, None, None)
            self.__main_app.after_seeding_summary_message = message
            while self.__main_app.finish_from_here is None:
                time.sleep(1)
            return self.__main_app.finish_from_here

        def _start_finishing(self):
            self.__main_app.state = Model.State.AWAIT_FINISHING

        def _watch_finishing(self, watch):
            self.__main_app.finish_from_here_session = watch.session
            self.__main_app.state = Model.State.FINISHING

        def _done(self, *, finish_from_here, unknown):
            if finish_from_here:
                while not self.__main_app.finish_was_confirmed:
                    time.sleep(1)
            self.__main_app.state = Model.State.FORM
            self.__main_app.finish_was_confirmed = False

    def __seed(self, profile, target_device):
        Model._SeedAct(klovve.app.MainloopObjectProxy(self), profile=profile, target_device=target_device).seed()
        self.__seed_thread = None

    def __refresh_profile_open_parameters(self):
        self.selected_profile_open_parameters = self.selected_profile.type.open_parameters if self.selected_profile else []

    def __refresh_is_form_data_valid(self):
        self.is_form_data_valid = (self.selected_profile and self.selected_target_device
                                    and all([self.additional_seed_config.get(profile_open_parameter.name)
                                             for profile_open_parameter in self.selected_profile_open_parameters]))

    class Profile(klovve.Model):

        name = klovve.Property()

        type = klovve.Property()  # TODO

    class Target(klovve.Model):

        path = klovve.Property()

        description = klovve.Property()

        @klovve.ComputedProperty
        def label(self):
            return f"{self.description} ({self.path})"

    @staticmethod
    def __available_profiles__create_target_object(source_object):
        return Model.Profile(name=source_object.name, type=source_object)

    @staticmethod
    def __available_profiles__is_matching_target_object(target_object, source_object):
        return target_object.name == source_object.name

    @staticmethod
    def __available_targets__create_target_object(source_object):
        return Model.Target(path=source_object[0], description=source_object[1])

    @staticmethod
    def __available_targets__is_matching_target_object(target_object, source_object):
        return target_object.path == source_object[0]

    @krrez.apps.MainModel.refresher()
    def __refresh_available_profiles(self):
        self.all_profiles.update(krrez.seeding.profile_loader.browsable_profiles(),
                                 create_target_object_func=self.__available_profiles__create_target_object,
                                 is_matching_target_object_func=self.__available_profiles__is_matching_target_object)

    @krrez.apps.MainModel.refresher(every_counts=1)
    def __refresh_available_targets(self):
        self.all_target_devices.update(self.selected_profile.type.available_target_devices if self.selected_profile else [],
                                       create_target_object_func=self.__available_targets__create_target_object,
                                       is_matching_target_object_func=self.__available_targets__is_matching_target_object)


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()
        if self.model.state == Model.State.FORM:
            return pieces.krrez.apps.seeding.new_seeding(
                all_profiles=props.all_profiles,
                all_target_devices=props.all_target_devices,
                start_seed_func=props.seed,
                selected_profile_open_parameters=props.selected_profile_open_parameters,
                additional_seed_config=props.additional_seed_config,
                selected_profile=props.selected_profile,
                selected_target_device=props.selected_target_device
            )
        elif self.model.state == Model.State.AWAIT_SEEDING:
            return pieces.busy_animation(size=klovve.pieces.busy_animation.Model.Size.EXTRA_LARGE)
        elif self.model.state == Model.State.SEEDING:
            return pieces.krrez.apps.seeding.session(
                session=props.seed_session,
                after_seeding_summary_message=props.after_seeding_summary_message,
                do_finishing=props.finish_from_here
            )

        elif self.model.state == Model.State.AWAIT_FINISHING:
            return pieces.busy_animation(
                size=klovve.pieces.busy_animation.Model.Size.EXTRA_LARGE,
                text=f"Please start the target machine as described before. Things should then go on here a few minutes"
                     f" later.\n\nIf not, there might be a network issue.\n\nRemember that you can always log in to the"
                     f" target machine and finish the installation this way instead.\n\n"
                     f"     User name: {self.model.seed_user.username}  /  Password: {self.model.seed_user.password}")

        elif self.model.state == Model.State.FINISHING:
            return pieces.krrez.apps.seeding.finishing(session=props.finish_from_here_session,
                                                       finish_was_confirmed=props.finish_was_confirmed)
