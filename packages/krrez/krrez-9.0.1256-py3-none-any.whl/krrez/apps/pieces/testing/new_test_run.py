#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve


class Model(klovve.Model):

    all_test_plans: list[str] = klovve.ListProperty()

    selected_test_plan: t.Optional[str] = klovve.Property()

    start_test_func: klovve.app.TAction = klovve.Property(default=lambda: (lambda *_: None))

    @klovve.ComputedProperty
    def is_form_invalid(self):
        return not self.selected_test_plan


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.scrollable(
            item=pieces.form(
                items=[
                    pieces.header(text="Start a new test run."),
                    pieces.form.section(
                        label="Please choose the test to run.",
                        item=pieces.dropdown(items=props.all_test_plans, selected_item=props.selected_test_plan),
                    ),
                    pieces.disableable(
                        item=pieces.form.section(
                            item=pieces.button(text="Start test", action=self.model.start_test_func),
                        ),
                        is_disabled=props.is_form_invalid,
                    ),
                ],
            )
        )
