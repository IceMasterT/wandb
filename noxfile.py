import platform

import nox

NEXUS_VERSION = "0.0.1a3"


@nox.session(python=False, name="build-nexus")
def build_nexus(session):
    """Builds the nexus binary for the current platform.

    Usage: nox -s build-nexus [target_system]

    target_system: The target system to build for. Defaults to the current system.
                   Use format: <system>-<arch> (e.g. linux-amd64, darwin-arm64)
                   Use "all" to build for all known platforms.
    """
    if session.posargs:
        target_system = session.posargs[0]
    else:
        system = platform.system().lower()
        arch = "amd64" if platform.machine() == "x86_64" else platform.machine()
        target_system = f"{system}-{arch}"
    session.run(
        "python",
        "-m",
        "build",
        "-w",  # only build the wheel
        "-n",  # disable building the project in an isolated virtual environment
        "-x",  # do not check that build dependencies are installed
        "./nexus",
        f"-C--build-option=bdist_wheel --nexus-build={target_system}",
        external=True,
    )


@nox.session(python=False, name="install-nexus")
def install_nexus(session):
    """Installs the nexus wheel into the current environment."""
    session.run(
        "pip",
        "install",
        "--force-reinstall",
        f"./nexus/dist/wandb_core-{NEXUS_VERSION}-py3-none-any.whl",
        external=True,
    )
