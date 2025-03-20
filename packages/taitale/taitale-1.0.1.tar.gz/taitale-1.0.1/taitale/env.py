import configparser
import platform
from pathlib import Path, PurePath
from typing import Dict


class TaitaleEnvironment:
    def __init__(self, **kwargs):
        """Initialize TaitaleEnvironment with optional configuration overrides.

        Args:
            runtime : Environment to run ASKAP on 'container' or 'native'.
                Defaults to 'container'
            image : If runtime is 'container', the following image will be used.
                Defaults to  'registry.gitlab.com/askapsdp/all_yandasoft'
            tag : If runtime is 'container', the following image will be used.
                Defaults to '1.1.x-latest-slim'
            engine : If runtime is 'container', the following OCI runtime will be used eg) 'podman or 'docker'.
                Defaults to 'docker'
            workload_manager : Workload manager to use for distribution. Currently supported 'mpi' or 'slurm'.
                Defaults to 'mpi'
            path : Path to executable.
                Defaults to None
            dryrun : If this is set to True, parset is printed to stdout, and execution is not run.
                Defaults to False
            user_defaults : If this is set to True, defaults are additionally read from askap-parsets.cfg.
                Defaults to True
        """
        self.config = {"user_defaults": True}
        self.kwargs = kwargs

    def read_defaults(self, file_name: str) -> configparser.ConfigParser:
        cfg = configparser.ConfigParser()
        cfg.optionxform = str

        cfg.clear()
        package_default_path = PurePath(Path(__file__).parent, file_name)
        if Path(package_default_path).exists():
            with open(package_default_path) as default_file:
                cfg.read_file(default_file)

        if self.config["user_defaults"] is True:
            if platform.system() != "Windows":
                try:
                    user_default_path = PurePath(Path.home(), ".taitale", file_name)
                    if Path(user_default_path).exists():
                        with open(user_default_path) as default_file:
                            cfg.read_file(default_file)
                except Exception:
                    print(
                        f"Error reading user defined config, please check the contents of {user_default_path}"
                    )

            try:
                local_default_path = PurePath(Path("."), file_name)
                if Path(local_default_path).exists():
                    with open(local_default_path) as default_file:
                        cfg.read_file(default_file)
            except Exception:
                print(
                    f"Error reading user defined config, please check the contents of {local_default_path}"
                )

        return cfg

    def yandameta(self) -> Dict:
        file_name = "taitale_env.cfg"
        meta = self.read_defaults(file_name)

        userconfig = dict(meta.items("taitale_env"))

        # Explicitly setting only MPI and Slurm
        userconfig["mpi"] = dict(meta.items("mpi"))
        userconfig["slurm"] = dict(meta.items("slurm"))

        userconfig["native"] = dict(meta.items("native"))
        userconfig["container"] = dict(meta.items("container"))

        return userconfig

    def __enter__(self) -> Dict:
        """Enter the context, setting up the environment configuration."""
        userconfig = self.yandameta()
        self.config = {**userconfig, **self.config, **self.kwargs}

        runtime = self.config.get("runtime")
        if runtime is None or (runtime != "container" and runtime != "native"):
            raise ValueError(
                "Unknown environment, must be either 'container' or 'native'"
            )

        workload_manager = self.config.get("workload_manager")
        if workload_manager is None or (
            workload_manager != "mpi" and workload_manager != "slurm"
        ):
            raise ValueError(
                "Unknown workload_manager, must be either 'mpi' or 'slurm'"
            )

        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context, cleaning up if necessary."""
        pass


# TODO: Revisit this
def taitale_env(**kwargs):
    """
    Args:
        runtime : Environment to run ASKAP on 'container' or 'native'.
            Defaults to 'container'
        image : If runtime is 'container', the following image will be used.
            Defaults to  'registry.gitlab.com/askapsdp/all_yandasoft'
        tag : If runtime is 'container', the following image will be used.
            Defaults to '1.1.x-latest-slim'
        engine : If runtime is 'container', the following OCI runtime will be used eg) 'podman or 'docker'.
            Defaults to 'docker'
        workload_manager : Workload manager to use for distribution. Currently supported 'mpi' or 'slurm'.
            Defaults to 'mpi'
        path : Path to executable.
            Defaults to None
        dryrun : If this is set to True, parset is printed to stdout, and execution is not run.
            Defaults to False
        ipy : If this is set to True, Ipython specific improvements are added.
            Defaults to False
        user_defaults : If this is set to True, defaults are additionally read from askap-parsets.cfg.
            Defaults to True

    Example:
        taitale_env(runtime='container', engine='podman')
        taitale_env(runtime='native', workload_manager='slurm')
    """

    with TaitaleEnvironment(**kwargs) as config:
        return config
