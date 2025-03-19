#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.apps


class Model(krrez.apps.AppModel):

    start_with_test_plan: t.Optional[str] = klovve.Property()

    @klovve.ComputedProperty
    def window_title(self):
        return "Krrez Testing" + (f" - {self.start_with_test_plan}" if self.start_with_test_plan else "")


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.window(
            title=props.window_title,
            body=pieces.krrez.apps.testing.main(
                **krrez.apps.common_properties(props),
                start_with_test_plan=props.start_with_test_plan)
        )
