#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve.pieces.tabbed.tab

import krrez.apps
import krrez.flow


class Model(krrez.apps.MainModel):
    pass


class View(klovve.ComposedView[Model]):

    class Tab:

        is_only_for_krrez_machines = False

        def piece(self, visible_tab_names: list[str]):
            pass

    @klovve.ComputedProperty
    def tabs(self):
        pieces, props = self.make_view()
        subview_kwargs = krrez.apps.common_properties(props)

        class Welcome(View.Tab):

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Welcome", item=pieces.krrez.apps.studio.welcome(
                    **subview_kwargs, visible_tab_names=visible_tab_names))

        class Bits(View.Tab):

            is_only_for_krrez_machines = True

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Bits", item=pieces.krrez.apps.bits.main(**subview_kwargs))

        class Logs(View.Tab):

            is_only_for_krrez_machines = True

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Logs", item=pieces.krrez.apps.log_browser.main(**subview_kwargs))

        class Seeding(View.Tab):

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Seeding", item=pieces.krrez.apps.seeding.main(**subview_kwargs))

        class Development(View.Tab):

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Development", item=pieces.krrez.apps.dev_lab.main(**subview_kwargs))

        class Testing(View.Tab):

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Testing", item=pieces.krrez.apps.testing.main(**subview_kwargs))

        class Help(View.Tab):

            def piece(self, visible_tab_names):
                return pieces.tabbed.tab(label="Help", item=pieces.krrez.apps.studio.help(**subview_kwargs))

        is_krrez_machine = krrez.flow.is_krrez_machine()
        visible_tabs = [tab_type() for tab_type in [Welcome, Bits, Logs, Seeding, Development, Testing, Help]
                        if is_krrez_machine or not tab_type.is_only_for_krrez_machines]
        visible_tab_names = [type(t).__name__ for t in visible_tabs]

        return [tab.piece(visible_tab_names) for tab in visible_tabs]

    def compose(self):
        pieces, props = self.make_view()

        return pieces.tabbed(items=props.tabs)
