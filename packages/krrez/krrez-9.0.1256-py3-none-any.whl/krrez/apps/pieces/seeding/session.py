#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.flow


class Model(klovve.Model):

    session: t.Optional[krrez.flow.Session] = klovve.Property()

    do_finishing: bool = klovve.Property(default=False)

    after_seeding_summary_message: t.Optional[str] = klovve.Property()

    after_seeding_summary_message_answer: t.Optional[int] = klovve.Property()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        @klovve.reaction(owner=self)
        def on_after_seeding_summary_message_answered():
            if self.after_seeding_summary_message_answer is not None:
                self.do_finishing = self.after_seeding_summary_message_answer == 0


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def view_for_summary(self):
        pieces, props = self.make_view()

        if self.model.after_seeding_summary_message:
            return pieces.interact.triggers(message=props.after_seeding_summary_message,
                                            triggers=["Finish the seeding from here", "I'm done here"],
                                            answer=props.after_seeding_summary_message_answer)

    def compose(self):
        pieces, props = self.make_view()

        return pieces.vertical_box(
            items=[
                pieces.krrez.apps.session(session=props.session),
                pieces.placeholder(item=props.view_for_summary),
            ],
        )
