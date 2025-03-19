#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve

import krrez.apps


class Model(krrez.apps.AppModel):
    pass


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.window(
            title="Krrez Bits",
            body=pieces.krrez.apps.bits.main(**krrez.apps.common_properties(props))
        )
