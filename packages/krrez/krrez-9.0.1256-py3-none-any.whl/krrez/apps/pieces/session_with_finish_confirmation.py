#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve

import krrez.apps.pieces.session


class Model(krrez.apps.pieces.session.Model):

    with_finish_confirmation: bool = klovve.Property(default=True)

    finish_was_confirmed: bool = klovve.Property(default=False)


class View(krrez.apps.pieces.session.View):

    @klovve.ComputedProperty
    def confirmation_bar(self):
        pieces, props = self.make_view()

        if self.model.is_finished:
            if self.model.with_finish_confirmation and not self.model.finish_was_confirmed:
                return pieces.interact.message(message="The installation has been finished.",
                                               answer=props.finish_was_confirmed)
            elif not self.model.with_finish_confirmation:
                self.model.finish_was_confirmed = True

    def compose(self):
        pieces, props = self.make_view()

        return pieces.vertical_box(
            items=[
                pieces.krrez.apps.session(self.model),
                pieces.placeholder(item=props.confirmation_bar),
            ]
        )
