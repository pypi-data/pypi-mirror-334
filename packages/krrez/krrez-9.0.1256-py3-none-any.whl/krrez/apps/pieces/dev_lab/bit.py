#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    main = klovve.Property()

    name = klovve.Property()

    module_path = klovve.Property()

    async def remove(self, context):
        pieces, props = self.make_view()

        if await context.dialog(pieces.interact.yesno(message=f"Do you really want to delete the"
                                                              f" Bit '{self.name}'?")):
            self.main.remove_bit(self.bit)


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def header_text(self):
        return f"Bit '{self.model.name}'"

    @klovve.ComputedProperty
    def module_path_text(self):
        return str(self.model.module_path)

    def compose(self):
        pieces, props = self.make_view()

        return pieces.scrollable(
            item=pieces.form(
                items=[
                    pieces.header(text=props.header_text),
                    pieces.form.section(
                        label="If you want to make any changes to this Bit, modify its code in this file:",
                        item=pieces.label(text=props.module_path_text),
                    ),
                    pieces.form.section(
                        item=pieces.button(text="Remove this Bit", action=props.remove),
                    ),
                ]
            )
        )
