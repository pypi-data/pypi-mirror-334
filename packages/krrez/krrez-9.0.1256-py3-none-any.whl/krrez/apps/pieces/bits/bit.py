#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve

import krrez.flow.runner


class Model(klovve.Model):

    name: str = klovve.Property(default="")

    documentation: str = klovve.Property(default="")

    context: t.Optional["krrez.flow.Context"] = klovve.Property()

    installing_session: t.Optional["krrez.flow.Session"] = klovve.Property()

    async def install(self):
        #TODO re
#        with self.blocking_interrupts("You are currently applying Bits. If you close this app now, this"
 #                                     " process with continue to happen in background. You will not be able to see"
  #                                    " questions that you have to answer. You also should not reboot the machine"
   #                                   " before this process is finished. In general, you should not close this app"
    #                                  " at the moment."):
            self.installing_session = krrez.flow.runner.Engine().start(
                context=self.context, bit_names=[self.name]).session


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.scrollable(
            item=pieces.form(
                items=[
                    pieces.header(text=props.name),
                    pieces.form.section(
                        item=pieces.label(text=props.documentation),
                    ),
                    pieces.form.section(
                        label="is installed?",
                        item=pieces.label(text="abc"),
                    ),
                    pieces.form.section(
                        label="version?",
                        item=pieces.label(text="def"),
                    ),
                    pieces.form.section(
                        label="bla bla",
                        item=pieces.label(text="ghi"),
                    ),
                    pieces.form.section(
                        item=pieces.button(text="Install", action=props.install),
                    ),
                ],
            )
        )
