#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.button

import krrez.coding
import krrez.flow.bit_loader


class Model(klovve.Model):

    test_plan = klovve.Property()

    main = klovve.Property()

    selected_test_name = klovve.Property()

    selected_test_plan_name = klovve.Property()

    selected_profile_name = klovve.Property()

    @klovve.ComputedProperty
    def current_test_plan_short_name(self):
        return krrez.coding.TestPlans.bit_name_to_test_plan_name(self.test_plan.name) if (self.test_plan and self.main) else None

    @klovve.ComputedProperty
    def current_test_plan_tests(self):
        return self.main.get_test_names_from_test_plan(self.test_plan) if (self.test_plan and self.main) else []

    @klovve.ComputedProperty
    def current_test_plan_test_plans(self):
        return self.main.get_test_plan_names_from_test_plan(self.test_plan) if (self.test_plan and self.main) else []

    @klovve.ComputedProperty
    def current_test_plan_profiles(self):
        return self.main.get_profile_test_names_from_test_plan(self.test_plan) if (self.test_plan and self.main) else []

    async def remove(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(message=f"Do you really want to delete the"
                                                              f" Test Plan '{self.current_test_plan_short_name}'?")):
            self.main.remove_test_plan(self.test_plan)

    async def add_a_test(self, context):
        pieces, props = self.make_view()

        test_idx = await context.dialog(pieces.interact.triggers(message="Please pick the Test you want to add.",
                                                                 triggers=self.main.all_test_names))
        if test_idx is not None:
            test = self.main.all_test_names[test_idx]
            self.main.add_test_to_test_plan(test, self.test_plan)
            self.__refresh()

    async def remove_selected_test(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(message=f"Do you really want to remove the"
                                                              f" Test '{self.selected_test_name}' from"
                                                              f" Test Plan '{self.current_test_plan_short_name}'?")):
            self.main.remove_test_from_test_plan(self.selected_test_name, self.test_plan)
            self.__refresh()

    async def add_a_test_plan(self, context):
        pieces, props = self.make_view()

        test_plan_idx = await context.dialog(pieces.interact.triggers(message="Please pick the Test Plan you want to add.",
                                                                      triggers=self.main.all_test_plan_names))
        if test_plan_idx is not None:
            test_plan = self.main.all_test_plan_names[test_plan_idx]
            self.main.add_test_plan_to_test_plan(test_plan, self.test_plan)
            self.__refresh()

    async def remove_selected_test_plan(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(message=f"Do you really want to remove the"
                                                              f" Test Plan '{self.selected_test_plan_name}' from"
                                                              f" Test Plan '{self.current_test_plan_short_name}'?")):
            self.main.remove_test_plan_from_test_plan(self.selected_test_plan_name, self.test_plan)
            self.__refresh()

    async def add_a_test_profile(self, context):
        pieces, props = self.make_view()

        profile_idx = await context.dialog(pieces.interact.triggers(message="Please pick the Profile you want to add.",
                                                                    triggers=self.main.all_profile_test_names))
        if profile_idx is not None:
            profile = self.main.all_profile_test_names[profile_idx]
            self.main.add_profile_test_to_test_plan(profile, self.test_plan)
            self.__refresh()

    async def remove_selected_profile(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(
                message=f"Do you really want to remove the Profile '{self.selected_profile_name}' from"
                        f" Test Plan '{self.current_test_plan_short_name}'?")):
            self.main.remove_profile_test_from_test_plan(self.selected_profile_name, self.test_plan)
            self.__refresh()

    def __refresh(self):
        goof = self.main; self.main = None; self.main = goof  # TODO


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def header_text(self):
        return f"Test Plan '{self.model.current_test_plan_short_name}'"

    def compose(self):
        pieces, props = self.make_view()

        if self.model.test_plan:
            return pieces.scrollable(
                item=pieces.form(
                    items=[
                        pieces.header(text=props.header_text),
                        pieces.form.section(
                            label="This test plan includes the following Tests:",
                            item=pieces.list(
                                items=props.current_test_plan_tests,
                                list_actions=[
                                    klovve.pieces.button.Model(text="Add a Test", action=props.add_a_test)
                                ],
                                item_actions=[
                                    klovve.pieces.button.Model(text="Remove from Test Plan",
                                                               action=props.remove_selected_test)
                                ],
                                selected_item=props.selected_test_name,
                            ),
                        ),

                        pieces.form.section(
                            label="This Test Plan inherits from the following Test Plans:",
                            item=pieces.list(
                                items=props.current_test_plan_test_plans,
                                list_actions=[
                                    klovve.pieces.button.Model(text="Add a Test Plan",
                                                               action=props.add_a_test_plan)
                                ],
                                item_actions=[
                                    klovve.pieces.button.Model(text="Remove from Test Plan",
                                                               action=props.remove_selected_test_plan)
                                ],
                                selected_item=props.selected_test_plan_name,
                            ),
                        ),

                        pieces.form.section(
                            label="This Test Plan uses machines for the following Test Profiles:",
                            item=pieces.list(
                                items=props.current_test_plan_profiles,
                                list_actions=[
                                    klovve.pieces.button.Model(text="Add a Test Profile",
                                                               action=props.add_a_test_profile)
                                ],
                                item_actions=[
                                    klovve.pieces.button.Model(text="Remove from Test Plan",
                                                               action=props.remove_selected_profile)
                                ],
                                selected_item=props.selected_profile_name,
                            ),
                        ),
                        pieces.form.section(
                            label="If you want to make any changes to this Test Plan, modify its code in this file:",
                            item=pieces.label(text=str(krrez.flow.bit_loader.bit_module_path(self.model.test_plan))),
                        ),
                        pieces.form.section(
                            item=pieces.button(text="Remove this Test Plan", action=props.remove),
                        ),
                    ]
                )
            )
