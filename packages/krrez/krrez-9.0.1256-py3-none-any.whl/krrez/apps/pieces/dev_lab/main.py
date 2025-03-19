#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import hallyd
import klovve.pieces.button

import krrez.api
import krrez.coding
import krrez.apps.pieces.dev_lab.bit
import krrez.apps.pieces.dev_lab.profile
import krrez.apps.pieces.dev_lab.test
import krrez.apps.pieces.dev_lab.test_plan
import krrez.apps.pieces.session
import krrez.flow.bit_loader
import krrez.seeding.profile_loader


class Model(krrez.apps.MainModel):

    selected_custom_bit = klovve.Property()

    selected_custom_profile = klovve.Property()

    selected_custom_test = klovve.Property()

    selected_custom_test_plan = klovve.Property()

    @klovve.ComputedProperty
    def all_custom_bits(self) -> list[krrez.apps.pieces.dev_lab.bit.Model]:  # TODO
        return [krrez.apps.pieces.dev_lab.bit.Model(name=krrez.flow.bit_loader.bit_name(bit), bit=bit, main=self,
                                                    module_path=krrez.flow.bit_loader.bit_module_path(bit))
                for bit in self.all_bits if krrez.coding.Bits.is_bit_name_for_normal_bit(krrez.flow.bit_loader.bit_name(bit))
                and self.__is_custom_module(krrez.flow.bit_loader.bit_module_path(bit))]

    @klovve.ComputedProperty
    def all_custom_profiles(self):
        available_custom_profiles = []
        for profile in krrez.seeding.profile_loader.all_profiles():
            if self.__is_custom_module(krrez.seeding.profile_loader.profile_module_path(profile)):
                profile_test_bit_name = krrez.coding.ProfileTests.profile_test_name_to_bit_name(profile.name)
                for bit in self.all_bits:
                    if krrez.flow.bit_loader.bit_name(bit) == profile_test_bit_name:
                        profile_test_bit = bit()
                        break
                else:
                    profile_test_bit = None
                available_custom_profiles.append((profile, profile_test_bit))
        available_custom_profiles.sort(key=lambda profile_tuple: profile_tuple[0].name)
        return available_custom_profiles

    @klovve.ComputedProperty
    def all_custom_tests(self):
        return [bit for bit in self.all_bits if krrez.coding.Tests.is_bit_name_for_test(krrez.flow.bit_loader.bit_name(bit))
                and self.__is_custom_module(krrez.flow.bit_loader.bit_module_path(bit))]

    @klovve.ComputedProperty
    def all_custom_test_plans(self):
        return [bit for bit in self.all_bits if krrez.coding.TestPlans.is_bit_name_for_test_plan(krrez.flow.bit_loader.bit_name(bit))
                and self.__is_custom_module(krrez.flow.bit_loader.bit_module_path(bit))]

    @klovve.ComputedProperty
    def all_normal_bits(self):
        return [bit for bit in self.all_bits if krrez.coding.Bits.is_bit_name_for_normal_bit(krrez.flow.bit_loader.bit_name(bit))]

    @klovve.ComputedProperty
    def all_test_names(self):
        return [krrez.coding.Tests.bit_name_to_test_name(krrez.flow.bit_loader.bit_name(bit)) for bit in self.all_bits
                if krrez.coding.Tests.is_bit_name_for_test(krrez.flow.bit_loader.bit_name(bit))]

    @klovve.ComputedProperty
    def all_test_plan_names(self):
        return [krrez.coding.TestPlans.bit_name_to_test_plan_name(krrez.flow.bit_loader.bit_name(bit)) for bit in self.all_bits
                if krrez.coding.TestPlans.is_bit_name_for_test_plan(krrez.flow.bit_loader.bit_name(bit))]

    @klovve.ComputedProperty
    def all_profile_test_names(self):
        return [krrez.coding.ProfileTests.bit_name_to_profile_test_seed_name(krrez.flow.bit_loader.bit_name(bit)) for bit in self.all_bits
                if krrez.coding.ProfileTests.is_bit_name_for_profile_test_seed(krrez.flow.bit_loader.bit_name(bit))]

    def create_bit(self, module_base_directory: krrez.api.Path, bit_name: str) -> None:
        with krrez.coding.Bits.editor_for_new_bit(bit_name, module_base_directory) as bit_code:
            bit_code.create()
        self.app.refresh_all_bits()

    def create_profile(self, module_base_directory: krrez.api.Path, profile_name: str) -> None:
        with krrez.coding.Profiles.editor_for_new_profile(profile_name, module_base_directory) as profile_code:
            profile_code.create()
        with krrez.coding.ProfileTests.editor_for_new_profile_test(profile_name, module_base_directory) as profiletest_code:
            profiletest_code.create()
        self.app.refresh_all_bits()

    def create_test(self, module_base_directory: krrez.api.Path, test_name: str) -> None:
        with krrez.coding.Tests.editor_for_new_test(test_name, module_base_directory) as test_code:
            test_code.create()
        self.app.refresh_all_bits()

    def create_test_plan(self, module_base_directory: krrez.api.Path, test_plan_name: str) -> None:
        with krrez.coding.TestPlans.editor_for_new_test_plan(test_plan_name, module_base_directory) as test_plan_code:
            test_plan_code.create()
        self.app.refresh_all_bits()

    def remove_bit(self, bit):
        self.__remove_for_editor(krrez.coding.Bits.editor_for_bit(bit))
        self.app.refresh_all_bits()

    def remove_profile(self, profile, profile_test):
        self.__remove_for_editor(krrez.coding.Profiles.editor_for_profile(profile))
        if profile_test:
            self.__remove_for_editor(krrez.coding.ProfileTests.editor_for_profile_test(profile_test))
        self.app.refresh_all_bits()

    def remove_test(self, test):
        self.__remove_for_editor(krrez.coding.Tests.editor_for_test(test))
        self.app.refresh_all_bits()

    def remove_test_plan(self, test_plan):
        self.__remove_for_editor(krrez.coding.TestPlans.editor_for_test_plan(test_plan))
        self.app.refresh_all_bits()

    def __remove_for_editor(self, editor: hallyd.coding.Editor) -> None:
        editor.path.remove()

    def get_bit_names_from_profile(self, profile: krrez.api.Profile) -> t.Optional[list[str]]:
        with krrez.coding.Profiles.editor_for_profile(profile) as profile_code:
            return profile_code.krrez_bits

    def get_test_names_from_test_plan(self, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            return test_plan_code.tests

    def get_test_plan_names_from_test_plan(self, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            return test_plan_code.test_plans

    def get_profile_test_names_from_test_plan(self, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            return test_plan_code.profile_tests

    def get_profile_names_from_test(self, test: krrez.api.Bit):
        with krrez.coding.Tests.editor_for_test(test) as test_code:
            return test_code.profile_names

    def add_bit_to_profile(self, bit_name: str, profile: krrez.api.Profile):
        with krrez.coding.Profiles.editor_for_profile(profile) as profile_code:
            profile_code.add_krrez_bit(bit_name)

    def remove_bit_from_profile(self, bit_name: str, profile: krrez.api.Profile):
        with krrez.coding.Profiles.editor_for_profile(profile) as profile_code:
            profile_code.remove_krrez_bit(bit_name)

    def add_test_to_test_plan(self, test_name: str, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            test_plan_code.add_test(test_name)

    def remove_test_from_test_plan(self, test_name: str, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            test_plan_code.remove_test(test_name)

    def add_test_plan_to_test_plan(self, test_plan_name: str, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            test_plan_code.add_test_plan(test_plan_name)

    def remove_test_plan_from_test_plan(self, test_plan_name: str, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            test_plan_code.remove_test_plan(test_plan_name)

    def add_profile_test_to_test_plan(self, profile_test_name: str, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            test_plan_code.add_profile_test(profile_test_name)

    def remove_profile_test_from_test_plan(self, profile_test_name: str, test_plan: krrez.api.Bit):
        with krrez.coding.TestPlans.editor_for_test_plan(test_plan) as test_plan_code:
            test_plan_code.remove_profile_test(profile_test_name)

    def add_profile_to_test(self, profile_name: str, test: krrez.api.Bit):
        with krrez.coding.Tests.editor_for_test(test) as test_code:
            test_code.add_profile(profile_name)

    def remove_profile_from_test(self, profile_name: str, test: krrez.api.Bit):
        with krrez.coding.Tests.editor_for_test(test) as test_code:
            test_code.remove_profile(profile_name)

    def get_profile_by_name(self, profile_name):
        for profile, _ in self.all_custom_profiles:
            if profile.name == profile_name:
                return profile

    def get_test_plan_by_name(self, test_plan_name):
        test_plan_bit_name = krrez.coding.TestPlans.test_plan_name_to_bit_name(test_plan_name)
        for test_plan in self.all_custom_test_plans:
            if krrez.flow.bit_loader.bit_name(test_plan) == test_plan_bit_name:
                return test_plan

    def get_test_by_name(self, test_name):
        test_bit_name = krrez.coding.Tests.test_name_to_bit_name(test_name)
        for test in self.all_custom_tests:
            if krrez.flow.bit_loader.bit_name(test) == test_bit_name:
                return test

    # TODO noh use more List.update()

    @staticmethod
    def __is_custom_module(path):
        return any(path.is_relative_to(module_dir_path) for module_dir_path
                   in krrez.flow.bit_loader.krrez_module_directories(with_builtin=False))

    async def __target_directory(self, context, message) -> t.Optional[krrez.api.Path]:
        pieces, props = self.make_view()

        krrez_module_directories = krrez.flow.bit_loader.krrez_module_directories(with_builtin=False)
        if len(krrez_module_directories) == 0:
            TODO
        elif len(krrez_module_directories) == 1:
            return krrez_module_directories[0]
        else:
            idx = await context.dialog(pieces.interact.triggers(message=message,
                                                                triggers=[str(x) for x in krrez_module_directories]))
            if idx is not None:
                return krrez_module_directories[idx]

    async def create_new_bit(self, context):
        pieces, props = self.make_view()

        krrez_module_directory = await self.__target_directory(context, "Where do you want to create the new Bit?")
        if not krrez_module_directory:
            return
        new_name = await context.dialog(pieces.interact.textline(message="Please enter a name for the new Bit."))
        if not new_name:
            return
        async with context.error_message_for_exceptions(Exception):
            self.create_bit(krrez_module_directory, new_name)

    async def create_new_profile(self, context):
        pieces, props = self.make_view()

        krrez_module_directory = await self.__target_directory(context, "Where do you want to create the new Profile?")
        if not krrez_module_directory:
            return
        new_name = await context.dialog(pieces.interact.textline(message="Please enter a name for the new Profile."))
        if not new_name:
            return
        async with context.error_message_for_exceptions(Exception):
            self.create_profile(krrez_module_directory, new_name)

    async def create_new_test_plan(self, context):
        pieces, props = self.make_view()

        krrez_module_directory = await self.__target_directory(context, "Where do you want to create the new Test"
                                                                        " Plan?")
        if not krrez_module_directory:
            return
        new_name = await context.dialog(pieces.interact.textline(message="Please enter a name for the new Test Plan."))
        if not new_name:
            return
        async with context.error_message_for_exceptions(Exception):
            self.create_test_plan(krrez_module_directory, new_name)

    async def create_new_test(self, context):
        pieces, props = self.make_view()

        krrez_module_directory = await self.__target_directory(context, "Where do you want to create the new Test?")
        if not krrez_module_directory:
            return
        new_name = await context.dialog(pieces.interact.textline(message="Please enter a name for the new Test."))
        if not new_name:
            return
        async with context.error_message_for_exceptions(Exception):
            self.create_test(krrez_module_directory, new_name)


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def view_for_bit_panel(self):
        pieces, props = self.make_view()

        if not self.model.selected_custom_bit:
            return pieces.label(text="Create a new Bit or choose an existing one in order to see more details.")
        return pieces.krrez.apps.dev_lab.bit(self.model.selected_custom_bit)

    @klovve.ComputedProperty
    def view_for_profile_panel(self):
        pieces, props = self.make_view()

        if not self.model.selected_custom_profile:
            return pieces.label(text="Create a new Profile or choose an existing one in order to see more details.")
        return pieces.krrez.apps.dev_lab.profile(profile=props.selected_custom_profile, main=self.model)

    @klovve.ComputedProperty
    def view_for_test_panel(self):
        pieces, props = self.make_view()

        if not self.model.selected_custom_test:
            return pieces.label(text="Create a new Test or choose an existing one in order to see more details.")
        return pieces.krrez.apps.dev_lab.test(test=props.selected_custom_test, main=self.model)

    @klovve.ComputedProperty
    def view_for_test_plan_panel(self):
        pieces, props = self.make_view()

        if not self.model.selected_custom_test_plan:
            return pieces.label(text="Create a new Test Plan or choose an existing one in order to see more details.")
        return pieces.krrez.apps.dev_lab.test_plan(test_plan=props.selected_custom_test_plan, main=self.model)

    def compose(self):
        pieces, props = self.make_view()

        return pieces.tabbed(
            items=[
                pieces.tabbed.tab(
                    label="Bits",
                    item=pieces.list_panel(
                        items=props.all_custom_bits,
                        selected_item=props.selected_custom_bit,
                        body=props.view_for_bit_panel,
                        item_label_func=lambda bit: bit.name,
                        list_actions=[
                            klovve.pieces.button.Model(text="Create new Bit", action=props.create_new_bit)
                        ],
                    ),
                ),
                pieces.tabbed.tab(
                    label="Profiles",
                    item=pieces.list_panel(
                        items=props.all_custom_profiles,
                        selected_item=props.selected_custom_profile,
                        body=props.view_for_profile_panel,
                        item_label_func=lambda profile_tuple: profile_tuple[0].name,
                        list_actions=[
                            klovve.pieces.button.Model(text="Create new Profile", action=props.create_new_profile)
                        ],
                    ),
                ),
                pieces.tabbed.tab(
                    label="Tests",
                    item=pieces.list_panel(
                        items=props.all_custom_tests,
                        selected_item=props.selected_custom_test,
                        body=props.view_for_test_panel,
                        item_label_func=lambda test_bit: krrez.coding.Tests.bit_name_to_test_name(
                            krrez.flow.bit_loader.bit_name(test_bit)),
                        list_actions=[
                            klovve.pieces.button.Model(text="Create new Test", action=props.create_new_test)
                        ],
                    ),
                ),
                pieces.tabbed.tab(
                    label="Test Plans",
                    item=pieces.list_panel(
                        items=props.all_custom_test_plans,
                        selected_item=props.selected_custom_test_plan,
                        body=props.view_for_test_plan_panel,
                        item_label_func=lambda test_plan_bit: krrez.coding.TestPlans.bit_name_to_test_plan_name(
                            krrez.flow.bit_loader.bit_name(test_plan_bit)),
                        list_actions=[
                            klovve.pieces.button.Model(text="Create new Test Plan", action=props.create_new_test_plan)
                        ],
                    ),
                ),
            ]
        )
