#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.button

import krrez.coding
import krrez.flow.bit_loader


class Model(klovve.Model):

    test = klovve.Property()

    main = klovve.Property()

    selected_profile_name = klovve.Property()

    @klovve.ComputedProperty
    def current_test_profiles(self):
        return self.main.get_profile_names_from_test(self.test) if (self.test and self.main) else []

    @klovve.ComputedProperty
    def current_test_short_name(self):
        return krrez.coding.Tests.bit_name_to_test_name(self.test.name) if (self.test and self.main) else None

    async def remove(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(message=f"Do you really want to delete the"
                                                              f" Test '{self.current_test_short_name}'?")):
            self.main.remove_test(self.test)

    async def add_a_profile(self, context):
        pieces, props = self.make_view()

        profile_idx = await context.dialog(pieces.interact.triggers(message="Please pick the Profile you want to add.",
                                                                    triggers=self.main.all_profile_tests))
        if profile_idx is not None:
            profile = self.main.all_profile_tests[profile_idx]
            self.main.add_profile_to_test(profile, self.test)
            self.__refresh()

    async def remove_selected_profile(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(
                message=f"Do you really want to remove the Profile '{self.selected_profile_name}' from"
                        f" Test Plan '{self.current_test_short_name}'?")):
            self.main.remove_profile_from_test(self.selected_profile_name, self.test)
            self.__refresh()

    def __refresh(self):
        goof = self.main; self.main = None; self.main = goof  # TODO


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def header_text(self):
        return f"Test '{self.model.current_test_short_name}'"

    def compose(self):
        pieces, props = self.make_view()

        if self.model.test:
            return pieces.scrollable(
                item=pieces.form(
                    items=[
                        pieces.header(text=props.header_text),
                        pieces.form.section(
                            label="This Test is associated to the following Profiles:",
                            item=pieces.list(
                                items=props.current_test_profiles,
                                list_actions=[
                                    klovve.pieces.button.Model(text="Add a Profile", action=props.add_a_profile)
                                ],
                                item_actions=[
                                    klovve.pieces.button.Model(text="Remove from Test",
                                                               action=props.remove_selected_profile)
                                ],
                                selected_item=props.selected_profile_name,
                            ),
                        ),
                        pieces.form.section(
                            label="If you want to make any changes to this Test, modify its code in this file:",
                            item=pieces.label(text=str(krrez.flow.bit_loader.bit_module_path(self.model.test))),
                        ),
                        pieces.form.section(
                            item=pieces.button(text="Remove this Test", action=props.remove),
                        ),
                    ]
                )
            )
