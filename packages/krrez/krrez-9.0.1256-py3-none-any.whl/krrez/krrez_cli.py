#!/usr/bin/env python3
#  SPDX-FileCopyrightText: © 2021 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import abc
import argparse
import contextlib
import json
import logging
import os
import sys
import time
import traceback
import typing as t

try:  # weird, but useful in some cases ;)
    if "__main__" == __name__:
        import krrez.api
except ModuleNotFoundError:
    sys.path.append(os.path.abspath(os.path.realpath(__file__)+"/../.."))

import hallyd
import klovve

import krrez.aux.data
import krrez.flow.bit_loader
import krrez.flow.runner
import krrez.seeding.profile_loader
import krrez.testing.landmark


_logger = logging.getLogger("krrez.krrez_cli")


# noinspection PyUnusedLocal
def get_parser(only_relevant: bool = False) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"Welcome to Krrez {krrez.aux.project_info.version}!"
                                                 f" For more information, read '{krrez.aux.data.readme_pdf_path}'"
                                                 f" and visit '{krrez.aux.project_info.homepage_url}'.")
    parser.add_argument("--context-path", help=argparse.SUPPRESS)
    p_cmd = parser.add_subparsers(help="What to do?", required=False, dest="command", metavar="[command]")

    if (not only_relevant) or krrez.flow.is_krrez_machine():

        p_cmd_bits = p_cmd.add_parser("bits", help="Manage Krrez bits.")
        p_cmd_bits_cmd = p_cmd_bits.add_subparsers(help="What to do with bits?", required=False, dest="subcommand",
                                                   metavar="[subcommand]")
        p_cmd_bits_cmd_list = p_cmd_bits_cmd.add_parser("list", help="List all bits.")
        p_cmd_bits_cmd_status = p_cmd_bits_cmd.add_parser("status", help="Show the status for some bits.")
        p_cmd_bits_cmd_status.add_argument("bits", type=str, help="The bits to show.", nargs="*")
        p_cmd_bits_cmd_install = p_cmd_bits_cmd.add_parser("apply", help="Apply one or more bits.")
        p_cmd_bits_cmd_install.add_argument("bits", type=str, help="The bits to install.", nargs="*")
        p_cmd_bits_cmd_install.add_argument("--no-confirm-after-installation", action="store_true",
                                            help="Skip the final message that must be confirmed by the user.")

        p_cmd_logs = p_cmd.add_parser("logs", help="Read logs.")
        p_cmd_logs_cmd = p_cmd_logs.add_subparsers(help="What to do with logs?", required=False, dest="subcommand",
                                                   metavar="[subcommand]")
        p_cmd_logs_cmd_list = p_cmd_logs_cmd.add_parser("list", help="List all existing sessions.")
        p_cmd_logs_cmd_show = p_cmd_logs_cmd.add_parser("show", help="Show the log for a particular session.")
        p_cmd_logs_cmd_show.add_argument("session", type=str, help="The session to show.")
        p_cmd_logs_cmd_show.add_argument("--verbose", help="Show debug output as well.", action="store_true")

    p_cmd_seeding = p_cmd.add_parser("seeding", help="Seed Krrez to a machine.")
    p_cmd_seeding_cmd = p_cmd_seeding.add_subparsers(help="What to do with seeding?", required=False, dest="subcommand",
                                                     metavar="[subcommand]")
    p_cmd_seeding_cmd_sow = p_cmd_seeding_cmd.add_parser("sow", help="Sow a seed. This will purge all existing data on"
                                                                     " the target device!")
    p_cmd_seeding_cmd_sow.add_argument("profile", type=str, help="Seed profile.")
    p_cmd_seeding_cmd_sow.add_argument("arguments", type=str, help="Arguments for this profile, as json string.")
    p_cmd_seeding_cmd_sow.add_argument("target-device", type=str, help="Path to target device.")
    p_cmd_seeding_cmd_profiles = p_cmd_seeding_cmd.add_parser("profiles", help="Manage profiles.")
    p_cmd_seeding_cmd_profiles_cmd = p_cmd_seeding_cmd_profiles.add_subparsers(help="What to do with profiles?",
                                                                               dest="subsubcommand", required=True,
                                                                               metavar="<subsubcommand>")
    p_cmd_seeding_cmd_profiles_cmd_list = p_cmd_seeding_cmd_profiles_cmd.add_parser(
        "list", help="List all available profiles.")
    p_cmd_seeding_cmd_profiles_cmd_info = p_cmd_seeding_cmd_profiles_cmd.add_parser(
        "info", help="Show further details for a profile.")
    p_cmd_seeding_cmd_profiles_cmd_info.add_argument("profile", type=str, help="The profile to show.")

    p_cmd_dev_lab = p_cmd.add_parser("dev-lab", help="Krrez development tool.")

    p_cmd_testing = p_cmd.add_parser("testing", help="Krrez testing.")
    p_cmd_testing_cmd = p_cmd_testing.add_subparsers(help="What to do with testing?", required=False, dest="subcommand",
                                                     metavar="[subcommand]")
    p_cmd_testing_cmd_run = p_cmd_testing_cmd.add_parser("run", help="Run a test plan.")
    p_cmd_testing_cmd_run.add_argument("plan", type=str, help="Test plan name.")
    p_cmd_testing_cmd_plans = p_cmd_testing_cmd.add_parser("plans", help="Manage test plans.")
    p_cmd_testing_cmd_plans_cmd = p_cmd_testing_cmd_plans.add_subparsers(help="What to do with test plans?",
                                                                       dest="subsubcommand", required=True,
                                                                       metavar="<subsubcommand>")
    p_cmd_testing_cmd_run_plans_cmd_list = p_cmd_testing_cmd_plans_cmd.add_parser(
        "list", help="List all available test plans.")
    p_cmd_testing_cmd_logs = p_cmd_testing_cmd.add_parser("logs", help="Manage test logs.")
    p_cmd_testing_cmd_logs_cmd = p_cmd_testing_cmd_logs.add_subparsers(help="What to do with test logs?",
                                                                       dest="subsubcommand", required=True,
                                                                       metavar="<subsubcommand>")
    p_cmd_testing_cmd_logs_cmd_list = p_cmd_testing_cmd_logs_cmd.add_parser(
        "list", help="List all existing test sessions.")
    p_cmd_testing_cmd_logs_cmd_show = p_cmd_testing_cmd_logs_cmd.add_parser("show", help="Show the log for a particular"
                                                                                         " test session.")
    p_cmd_testing_cmd_logs_cmd_show.add_argument("session", type=str, help="The session to show.")
    p_cmd_testing_cmd_logs_cmd_show.add_argument("--verbose", help="Show debug output as well.", action="store_true")
    p_cmd_testing_cmd_landmarks = p_cmd_testing_cmd.add_parser("landmarks", help="Manage test landmarks.")
    p_cmd_testing_cmd_landmarks_cmd = p_cmd_testing_cmd_landmarks.add_subparsers(help="What to do with test landmarks?",
                                                                                 dest="subsubcommand", required=True,
                                                                                 metavar="<subsubcommand>")
    p_cmd_testing_cmd_run_landmarks_cmd_list = p_cmd_testing_cmd_landmarks_cmd.add_parser(
        "list", help="List all available test landmarks.")
    p_cmd_testing_cmd_run_landmarks_cmd_resume = p_cmd_testing_cmd_landmarks_cmd.add_parser(
        "resume", help="Resume a test landmark.")
    p_cmd_testing_cmd_run_landmarks_cmd_resume.add_argument("session", type=str, help="The session to resume.")
    p_cmd_testing_cmd_run_landmarks_cmd_remove = p_cmd_testing_cmd_landmarks_cmd.add_parser(
        "remove", help="Remove a test landmark.")
    p_cmd_testing_cmd_run_landmarks_cmd_remove.add_argument("session", type=str, help="The session to remove the"
                                                                                      " landmark for.")

    return parser


class _Command(abc.ABC):

    def __init__(self, *, context_path, **_):
        self.__context = krrez.flow.Context(hallyd.fs.Path(context_path) if context_path else None)

    @property
    def context(self):
        return self.__context

    @contextlib.contextmanager
    def ui_app(self, app_name: str, unavailable_message: t.Optional[str] = None, **kwargs):
        unavailable_message = unavailable_message or ("This command is not available in an interactive way on your"
                                                      " system.")
        try:
            app = klovve.create_app(
                lambda pieces: getattr(pieces.krrez.apps, app_name).app(context=self.context, **kwargs)
                # TODO window here or window in the .app ?! -> streamline
            )
        except klovve.app.ApplicationUnavailableError as ex:
            raise Commands.AppUnavailableError(f"{unavailable_message} Please add '--help' to your command line and"
                                               f" use one of the listed sub-commands instead.") from ex

        yield app

    def __getattr__(self, item):
        if item.startswith("sub_"):
            item = item[4:]
            command_name = f"Command_{item}"
            if hasattr(self, command_name):
                subcommand_type = getattr(self, command_name, None)
                subcommand = subcommand_type(context_path=self.context.path)
                def foo(**kwargs):
                    kwwargs = {}
                    for k, v in kwargs.items():
                        if k.endswith("subcommand"):
                            k = k[3:]
                        kwwargs[k] = v
                    return subcommand(**kwwargs)
                return foo
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __call__(self, *, subcommand: t.Optional[str] = None, **kwargs):
        if subcommand:
            subcommand_fct = getattr(self, f"sub_{subcommand}", None)
            if not subcommand_fct:
                raise RuntimeError(f"the command '{subcommand}' is not valid")
            return subcommand_fct(**kwargs)
        self.main()

    def main(self):
        pass


def _list_logs(sessions):
    for session in sessions:
        print(session.name)


def _apply_bits(bits, *, context_path=None, confirm_after_installation=True, engine=None):  # TODO  move?!
    with _Command(context_path=context_path).ui_app("runner", bit_names=bits,
                                                    engine=engine or krrez.flow.runner.Engine(),
                                                    confirm_after_installation=confirm_after_installation) as app:
        app.run()
        if not app._view._model.was_successful:
            raise RuntimeError("applying of bits failed")


def _dump_session(session_name, verbose, context):
    print("TODO logs_show", verbose)
    for log in krrez.flow.log.get_all_install_logs(context=context):
        if log.log_name == session_name:
            print(f"{succctxt} installation for '{log.bit_name}' at {log.time}:\n\n{log.output}")
            return
    raise Exception("log not found")


class Commands:

    class AppUnavailableError(RuntimeError):
        pass

    # noinspection PyPep8Naming
    class Command_bits(_Command):

        def main(self):
            with self.ui_app("bits") as app:
                app.run()

        def sub_list(self, **_):
            for bit in krrez.flow.bit_loader.all_normal_bits():
                print(bit.bit_name)

        def sub_status(self, *, bits: list[str], **_):
            for bit_name in bits:
                try:
                    bit = krrez.flow.bit_loader.bit_by_name(bit_name)()
                    print(f"{bit_name}: {'not ' if self.context.is_bit_installed(bit) else ''}installed")
                except krrez.flow.bit_loader.BitNotFoundError:
                    print(f"{bit_name}: not found")
            print(f"bits_status {bits}")

        def sub_apply(self, *, bits: list[str], no_confirm_after_installation: bool, **_):
            with self.ui_app("runner", bit_names=bits,
                             engine=krrez.flow.runner.Engine(),
                             confirm_after_installation=not no_confirm_after_installation) as app:
                app.run()
                if not app._view._model.was_successful:
                    raise RuntimeError("applying of bits failed")

    # noinspection PyPep8Naming
    class Command_logs(_Command):

        def main(self):
            with self.ui_app("log_browser") as app:
                app.run()

        def sub_list(self, **_):
            _list_logs(krrez.flow.log.get_all_install_logs(context=self.context))

        def sub_show(self, *, session: str, verbose: bool, **_):
            _dump_session(session, verbose, self.context)

    # noinspection PyPep8Naming
    class Command_seeding(_Command):

        # noinspection PyPep8Naming
        class Command_profiles(_Command):

            def sub_list(self, **_):
                for profile in krrez.seeding.profile_loader.browsable_profiles():
                    print(profile.name)

            def sub_info(self, profile, **_):
                for profile_ in krrez.seeding.profile_loader.all_profiles():
                    if profile_.name == profile:
                        print("Parameters:")
                        for open_parameter in profile_.open_parameters:
                            print(f" {open_parameter.name}\n  (type: {open_parameter.type})")
                        print("Possible target devices (insert your empty medium in order to show it here):")
                        for target_device, target_device_description in profile_.available_target_devices:
                            print(f" {target_device}\n  ({target_device_description})")
                        break
                else:
                    raise RuntimeError(f"the profile '{profile}' does not exist")

        def main(self):
            with self.ui_app("seeding") as app:
                app.run()

        def sub_sow(self, *, profile: str, arguments: str, target_device: str, **_):
            with self.ui_app("seeding") as app:
                app._view._model.body.selected_profile = profile
                app._view._model.body.selected_target_device = target_device
                for arg_key, arg_value in json.loads(arguments).items():
                    app._view._model.body.additional_seed_config[arg_key] = arg_value
                app._view._model.body.seed()
                app.run()

    # noinspection PyPep8Naming
    class Command_dev_lab(_Command):

        def main(self):
            with self.ui_app("dev_lab") as app:
                app.run()

    # noinspection PyPep8Naming
    class Command_testing(_Command):

        # noinspection PyPep8Naming
        class Command_plans(_Command):

            def sub_list(self, **_):
                for test_plan_name in krrez.testing.all_available_test_plans():
                    print(test_plan_name)

        # noinspection PyPep8Naming
        class Command_logs(_Command):

            def sub_list(self, **_):
                _list_logs(krrez.testing.all_test_sessions(self.context))

            def sub_show(self, *, session: str, verbose: bool, **_):
                _dump_session(session, verbose, self.context)

        # noinspection PyPep8Naming
        class Command_landmarks(_Command):

            def sub_list(self, **_):
                pass

            def sub_resume(self, *, session: str, **_):
                pass

            def sub_remove(self, *, session: str, **_):
                pass

        def main(self):
            with self.ui_app("testing") as app:
                app.run()

        def sub_run(self, *, plan: str, **_):
            with self.ui_app("testing", start_with_test_plan=plan) as app:
                app.run()

    # noinspection PyPep8Naming
    class Command_studio(_Command):

        def main(self):
            with self.ui_app("studio", unavailable_message="You are trying to open the Krrez main user interface,"
                                                           " but it cannot be used on your system.") as app:
                app.run()


def main():
    if os.environ.get("KRREZ_DEBUG_LOG", "") == "1":
        logging.basicConfig(level=logging.DEBUG)
    hallyd.cleanup.cleanup_after_exit()
    parser = get_parser(only_relevant=True)
    args = parser.parse_args()
    command_name = (args.command or "studio").replace("-", "_")
    command_type = getattr(Commands, f"Command_{command_name}")
    command = command_type(**args.__dict__)

    def goo():
        try:
            krrez.testing.clean_up_old_test_sessions(command.context)
            time.sleep(5)
            krrez.testing.landmark.clean_up_old_landmarks(command.context)
        except Exception:
            _logger.debug(traceback.format_exc())
    import threading; threading.Thread(target=goo).start()  # TODO

    try:
        command(**args.__dict__)
    except Exception as ex:
        _logger.debug(traceback.format_exc())
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
