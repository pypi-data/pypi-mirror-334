#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import asyncio
import contextlib

import klovve

import krrez.api
import krrez.flow.bit_loader


class _ModelBase(klovve.Model):

    app: "AppModel" = klovve.Property()

    context: "krrez.flow.Context" = klovve.Property()

    all_bits: list[type["krrez.api.Bit"]] = klovve.ListProperty()


class _Model(_ModelBase):

    _REFRESHER_MARKER_NAME = "_krrez_apps_refresher"

    @staticmethod
    def refresher(*, every_counts=2.0):

        def decorator(func):
            setattr(func, _Model._REFRESHER_MARKER_NAME, every_counts)
            return func

        return decorator

    @contextlib.contextmanager
    def blocking_interrupts(self, message: str):
        def func():
            return message
        with   open("/dev/null","r"):#TODO self.interrupt_handler.check_function_applied(func):
            yield

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for item_name in dir(type(self)):
            try:
                item = getattr(self, item_name)
            except:
                continue  # TODO
            every_counts = getattr(item, _Model._REFRESHER_MARKER_NAME, None)
            if every_counts is not None:
                self.__add_refresher(item, every_counts)

    def __add_refresher(self, func, every_counts):  # TODO weakrefs?!

        def rfunc():
            asyncio.get_running_loop().call_later(0, func)  # TODO !!!!
            asyncio.get_running_loop().call_later(every_counts * 60, rfunc)

        klovve.app.in_mainloop(rfunc)()


class AppModel(_Model):

    @klovve.ComputedProperty
    def app(self):
        return self

    @_Model.refresher()
    def refresh_all_bits(self):
        self.all_bits = list(krrez.flow.bit_loader.all_bits())


class MainModel(_Model):
    pass


def common_properties(model: _ModelBase):
    return {key: getattr(model, key) for key in _ModelBase.__dict__.keys() if not key.startswith("__")}
