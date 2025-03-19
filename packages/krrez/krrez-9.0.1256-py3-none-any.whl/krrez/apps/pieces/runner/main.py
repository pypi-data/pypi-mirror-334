#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import typing as t

import klovve

import krrez.apps
import krrez.flow.runner
import krrez.flow.watch


class Model(krrez.apps.MainModel):

    @klovve.ComputedProperty
    def installing_session(self) -> t.Optional[krrez.flow.watch.Watch]:
        if self.bit_names is not None and self.context and self.engine:
            return self.engine.start(context=self.context, bit_names=self.bit_names).session

    engine: t.Optional[krrez.flow.runner.Engine] = klovve.Property()

    bit_names: t.Optional[list[str]] = klovve.Property()

    done: bool = klovve.Property(default=lambda: False)

    was_successful: t.Optional[bool] = klovve.Property()

    confirm_after_installation: bool = klovve.Property(default=lambda: False)


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        if self.model.installing_session:
            return pieces.krrez.apps.session_with_finish_confirmation(
                session=props.installing_session,
                with_finish_confirmation=props.confirm_after_installation,
                finish_was_confirmed=props.done,
                was_successful=props.was_successful,
            )
