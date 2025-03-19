#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.button

import krrez.flow.bit_loader
import krrez.seeding.profile_loader


class Model(klovve.Model):

    profile = klovve.Property()

    main = klovve.Property()

    selected_bit_name = klovve.Property()

    @klovve.ComputedProperty
    def current_profile_bits(self):
        return self.main.get_bit_names_from_profile(self.profile[0]) if (self.profile and self.main) else []

    async def remove(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(message=f"Do you really want to delete the"
                                                              f" Profile '{self.profile[0].name}'?")):
            self.main.remove_profile(self.profile[0], self.profile[1])

    async def add_a_bit(self, context):
        pieces, props = self.make_view()

        bit_idx = await context.dialog(pieces.interact.triggers(message="Please pick the Bit you want to add.",
                                                                triggers=[x.name for x in self.main.all_normal_bits]))
        if bit_idx is not None:
            bit = self.main.all_normal_bits[bit_idx]
            self.main.add_bit_to_profile(bit.name, self.profile[0])
            self.__refresh()

    async def remove_selected_bit(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(
                message=f"Do you really want to remove the Bit '{self.selected_bit_name}' from"
                        f" Profile '{self.profile[0].name}'?")):
            self.main.remove_bit_from_profile(self.selected_bit_name, self.profile[0])
            self.__refresh()

    def __refresh(self):
        goof = self.main; self.main = None; self.main = goof  # TODO


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def header_text(self):
        return f"Profile '{self.model.profile[0].name}'"

    def compose(self):
        pieces, props = self.make_view()

        if self.model.profile:
            return pieces.scrollable(
                item=pieces.form(
                    items=[
                        pieces.header(text=props.header_text),
                        *([
                              pieces.form.section(
                                  label="This profile will install the following Bits:",
                                  item=pieces.list(
                                      items=props.current_profile_bits,
                                      list_actions=[
                                          klovve.pieces.button.Model(text="Add a Bit", action=props.add_a_bit)
                                      ],
                                      item_actions=[
                                          klovve.pieces.button.Model(text="Remove from Profile",
                                                                     action=props.remove_selected_bit)
                                      ],
                                      selected_item=props.selected_bit_name,
                                  ),
                              ),
                        ] if (self.model.current_profile_bits is not None) else []),
                        pieces.form.section(
                            label="If you want to make any changes to this Profile, modify its code in this file:",
                            item=pieces.label(text=str(krrez.seeding.profile_loader.profile_module_path(self.model.profile[0]))),
                        ),
                        *([
                            pieces.form.section(
                                label="There is also another file, which is relevant for testing, especially when you"
                                      " want to customize testing related things:",
                                item=pieces.label(text=str(krrez.flow.bit_loader.bit_module_path(self.model.profile[1]))),
                            ),
                        ] if self.model.profile[1] else []),
                        pieces.form.section(
                            item=pieces.button(text="Remove this Profile", action=props.remove),
                        ),
                    ]
                )
            )
