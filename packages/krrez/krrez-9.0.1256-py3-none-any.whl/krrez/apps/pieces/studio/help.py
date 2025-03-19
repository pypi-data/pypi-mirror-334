#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve

import krrez.aux.data


class Model(klovve.Model):
    pass


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.viewer.pdf(path=krrez.aux.data.readme_pdf_path)
