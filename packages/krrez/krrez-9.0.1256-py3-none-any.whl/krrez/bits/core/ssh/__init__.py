#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import datetime
import time

import krrez.api


class Bit(krrez.api.Bit):

    _firewall: krrez.api.IfPicked["krrez.bits.net.firewall.Bit"] # TODO noh is reference to krrez_additionals
    __later: krrez.api.Later["krrez.bits.sys.config.Bit", "krrez.bits.core.ssh.LateBit"]

    def __apply__(self):
        self._packages.install("openssh-server")
        self._internals.session.context.config.set("core.ssh.available_since", datetime.datetime.now())

        port = self._internals.session.context.config.get("core.ssh.port", 22)

        self._fs.etc_dir("ssh/sshd_config.d/krrez.conf").set_data(f"Port {port}\n")

        self._services.restart_service("ssh")

        if self._firewall:
            self._firewall.accept_tcp(port, include_in_fallback_mode=True)


class LateBit(krrez.api.Bit):

    __more_deps: krrez.api.Beforehand[krrez.api.IfPicked["krrez.bits.seed.common.ConfirmationBit"],
                                      krrez.api.IfPicked["krrez.bits.core.data_partition.Bit"],
                                      krrez.api.IfPicked["krrez.bits.net.web.Bit"],
                                      krrez.api.IfPicked["krrez.bits.desktop.environment.Bit"]]

    def __apply__(self):
        available_since = self._internals.session.context.config.get("core.ssh.available_since")
        available_for = datetime.datetime.now() - available_since
        time.sleep(max(0.0, (datetime.timedelta(minutes=1.5) - available_for).total_seconds()))
