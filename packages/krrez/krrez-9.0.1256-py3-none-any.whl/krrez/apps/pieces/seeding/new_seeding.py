#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import typing as t

import klovve.pieces.property_panel.entry

import krrez.api.internal
import krrez.apps.pieces.seeding.main


class Model(klovve.Model):

    all_profiles: list[krrez.api.Profile] = klovve.ListProperty()

    selected_profile: t.Optional[krrez.api.Profile] = klovve.Property()

    all_target_devices: list[krrez.apps.pieces.seeding.main.Model.Target] = klovve.ListProperty()

    selected_target_device: t.Optional[krrez.apps.pieces.seeding.main.Model.Target] = klovve.Property()

    selected_profile_open_parameters: list[krrez.api.internal.ProfileMeta._ProfileParameter] = klovve.ListProperty()

    additional_seed_config: dict[str, str] = klovve.Property(default=lambda: {})

    start_seed_func: klovve.app.TAction = klovve.Property(default=lambda: (lambda *_: None))

    @klovve.ComputedProperty
    def is_form_invalid(self) -> bool:
        return not (self.selected_profile and self.selected_target_device)  #  TODO additional_seed_config


class View(klovve.ComposedView[Model]):

    @klovve.ComputedProperty
    def view_for_open_parameters(self):
        pieces, props = self.make_view()

        if self.model.selected_profile_open_parameters:
            return pieces.form.section(
                label="Please specify the following infos.",
                item=pieces.property_panel(
                    entries=[klovve.pieces.property_panel.entry.Model(name=x.name) for x in
                             self.model.selected_profile_open_parameters],
                    values=props.additional_seed_config),
            )

    def compose(self):
        pieces, props = self.make_view()

        return pieces.scrollable(
            item=pieces.form(
                items=[
                    pieces.header(
                        text="Create Krrez installation media here, like USB sticks or SD cards, with a profile that is"
                             " customized for a particular use case."
                    ),
                    pieces.label(
                        text="Note that its primary purpose is to set up real production machines, while there is also"
                             " the virtual machine based Testing feature for development."
                    ),
                    pieces.form.section(
                        label="Please choose the profile that you want to create an installation medium for.",
                        item=pieces.dropdown(
                            items=props.all_profiles,
                            selected_item=props.selected_profile,
                            item_label_func=lambda profile: profile.name
                        ),
                    ),
                    pieces.placeholder(item=props.view_for_open_parameters),
                    pieces.form.section(
                        label="Please choose the destination device. Everything on this device will be overwritten!",
                        item=pieces.dropdown(items=props.all_target_devices,
                                             selected_item=props.selected_target_device,
                                             item_label_func=lambda target: target.label),
                    ),
                    pieces.disableable(
                        item=pieces.form.section(item=pieces.button(text="Seed", action=props.start_seed_func)),
                        is_disabled=props.is_form_invalid,
                    ),
                ],
            )
        )


# TODO "store settings as profile for later" button
