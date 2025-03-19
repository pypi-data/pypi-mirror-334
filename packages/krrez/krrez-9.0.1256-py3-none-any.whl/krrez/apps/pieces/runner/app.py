#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.apps
import krrez.flow


class Model(krrez.apps.AppModel):

    bit_names = klovve.Property()

    engine = klovve.Property()

    confirm_after_installation: bool = klovve.Property(default=False)

    installing_session: t.Optional[krrez.flow.Session] = klovve.Property()

    done: bool = klovve.Property(default=False)

    was_successful: t.Optional[bool] = klovve.Property(default=None)


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.window(
            title="Krrez",
            body=pieces.krrez.apps.runner.main(
                bit_names=props.bit_names,
                engine=props.engine,
                confirm_after_installation=props.confirm_after_installation,
                installing_session=props.installing_session,
                done=props.done,
                was_successful=props.was_successful,
                **krrez.apps.common_properties(props)
            ),
            is_closed=props.done
        )
