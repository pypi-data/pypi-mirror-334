#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.api
import krrez.coding
import krrez.flow.bit_loader


class Model(krrez.apps.MainModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        @klovve.reaction(owner=self)
        def on_finish_was_confirmed():
            if self.finish_was_confirmed:
                with klovve.data.deps.no_dependency_tracking():
                    self.finish_was_confirmed = False
                self.installing_session = None

    selected_bit: t.Optional[type[krrez.api.Bit]] = klovve.Property()

    search_term: str = klovve.Property(default="")

    installing_session: t.Optional[krrez.flow.Session] = klovve.Property()

    finish_was_confirmed: bool = klovve.Property(default=False)

    show_installed_only: bool = klovve.Property(default=False)

    @klovve.ComputedProperty
    def all_normal_bits(self) -> list[type[krrez.api.Bit]]:
        return [bit for bit in self.all_bits
                if krrez.coding.Bits.is_bit_name_for_normal_bit(krrez.flow.bit_loader.bit_name(bit))]

    @klovve.ComputedProperty
    def visible_bits(self) -> list[type[krrez.api.Bit]]:
        return [bit for bit in self.all_normal_bits
                if all((part in krrez.flow.bit_loader.bit_name(bit)) for part in self.search_term.split(" "))
                and (not self.show_installed_only or self.context.is_bit_installed(bit))]


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def view_for_bit(self):
        pieces, props = self.make_view()

        if self.model.selected_bit:
            return pieces.krrez.apps.bits.bit(
                name=krrez.flow.bit_loader.bit_name(self.model.selected_bit),
                documentation=krrez.flow.bit_loader.bit_documentation(self.model.selected_bit),
                context=props.context,
                installing_session=props.installing_session
            )

        else:
            return pieces.label(text="Please choose one of the bits from the list on the left hand side.")

    def compose(self):
        pieces, props = self.make_view()

        if self.model.installing_session:
            return pieces.krrez.apps.session_with_finish_confirmation(
                session=props.installing_session,
                finish_was_confirmed=props.finish_was_confirmed,
            )

        else:
            return pieces.list_panel(
                items=props.visible_bits,
                selected_item=props.selected_bit,
                item_label_func=lambda bit: krrez.flow.bit_loader.bit_name(bit),
                body=props.view_for_bit,
                aux_controls=[
                    pieces.text_field(hint_text="search", text=props.search_term),
                    pieces.checkable(text="show installed only", is_checked=props.show_installed_only),
                ],
            )
