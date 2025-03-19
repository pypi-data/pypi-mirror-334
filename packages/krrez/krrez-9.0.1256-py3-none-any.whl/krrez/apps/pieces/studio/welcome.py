#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import klovve


class Model(klovve.Model):

    _TABS = {
        "Welcome": ("Welcome", "This text."),
        "Bits": ("Bits", "Check which bits are available and installed, and install further ones."),
        "Logs": ("Logs", "Inspect details from former Bit installations, usually for problem analysis."),
        "Seeding": ("Seeding", "Prepare an installation medium that deploys a Krrez system to a fresh machine."),
        "Development": ("Development", "Create your automation logic."),
        "Testing": ("Testing", "Verify that your automation logic works as expected before seeding to a real machine."),
        "Help": ("Help", "Read the Krrez documentation."),
    }

    visible_tab_names = klovve.Property()

    @klovve.ComputedProperty
    def text_html(self):
        result = ("<h1>Welcome to Krrez!</h1>"
                  "There is a bar of tabs at the top that allow you to accomplish various tasks. If you are new to"
                  " Krrez, start with 'Help'.")
        result += "<ul>"
        for tab_name, (tab_title, tab_description) in Model._TABS.items():
            if tab_name in self.visible_tab_names:
                result += f"<li><foo>{tab_title}: </foo>{tab_description}</li>"
        result += "</ul>"
        return result


class View(klovve.ComposedView[Model]):

    def compose(self):
        pieces, props = self.make_view()

        return pieces.formatted_text(text=props.text_html)
