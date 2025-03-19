#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve


class Model(klovve.Model):

    method_name: t.Optional[str] = klovve.Property()

    args: list[object] = klovve.Property(default=lambda: [])

    kwargs: dict[str, object] = klovve.Property(default=lambda: {})

    answer = klovve.Property()


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        answer = dict(answer=props.answer)

        if self.model.method_name == "choose":
            return pieces.interact.triggers(message=self.model.args[0], triggers=self.model.kwargs["choices"], **answer)

        if self.model.method_name == "input":
            return pieces.interact.textline(message=self.model.args[0], **answer)
