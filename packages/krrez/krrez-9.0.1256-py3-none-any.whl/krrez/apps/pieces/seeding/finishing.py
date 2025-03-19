#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.flow


class Model(klovve.Model):

    session: t.Optional[krrez.flow.Session] = klovve.Property()

    finish_was_confirmed: bool = klovve.Property(default=False)


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.krrez.apps.session_with_finish_confirmation(session=props.session,
                                                                  finish_was_confirmed=props.finish_was_confirmed)
