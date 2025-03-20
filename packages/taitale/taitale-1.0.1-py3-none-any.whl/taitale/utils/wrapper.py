import datetime
import subprocess
import time
from shlex import quote

from taitale.utils.argumentset import ArgumentSet


def getstamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d-%H-%M-%S")


def executor(appname, run_cmd, config, mpi_compartible, logfile=None, **kwargs):
    if mpi_compartible:
        workers = kwargs.get("workers")
        if workers is not None:
            workload_manager = config["workload_manager"]
            if workload_manager != "mpi" and workload_manager != "slurm":
                raise ValueError("Given workload distributor is not supported")

            # TODO: A lot of was this can go wrong, make it simple and fail proof
            nodes = kwargs.get("nodes", 1)
            run_cmd = config[workload_manager]["workload_exec"].format(
                cmd=run_cmd,
                **config,
                **config[workload_manager],
                workers=quote(str(workers)),
                nodes=nodes,
            )
        else:
            raise ValueError("workers must be defined")

    timestamp = getstamp()
    if logfile is None:
        logfile = f"{appname}-{timestamp}.log"

    if config["runtime"] == "container":
        container_run = config["container"]["exec"]
        run_cmd = container_run.format(
            workload_exec=run_cmd, logfile=quote(logfile), **config
        )
    elif config["runtime"] == "native":
        native_run = config["native"]["exec"]
        run_cmd = native_run.format(
            workload_exec=run_cmd, logfile=quote(logfile), **config
        )

    print(f"Starting {appname}")
    if config["dryrun"] is True:
        print(run_cmd)
    else:
        if config["ipy"] is True:
            from taitale.widgets import ICmdRunWithLogTrail

            status_code = ICmdRunWithLogTrail(run_cmd, logfile)
            if status_code:
                raise subprocess.CalledProcessError(status_code, run_cmd)
        else:
            out = subprocess.run(f"{run_cmd}", shell=True)
            out.check_returncode()

    print(f"{appname} complete")


def parset_app(
    name,
    parset,
    out_parset_name,
    cmd,
    # TODO: Define this flag to remove mpiexec if the user want to
    mpi_compartible=False,
    pipestderr=False,
):

    def parset_cmd_execute(env, **kwargs):
        # Filter out workers from parset update
        parset_kwargs = kwargs["args"] if "args" in kwargs else {}
        output = parset.merge(ArgumentSet(args=parset_kwargs))
        env["pipestderr"] = " 2>&1" if pipestderr else ""

        if env["dryrun"] is True:
            print(parset.to_string())
        else:
            parset.serialize(out_parset_name)

        run_cmd = cmd.format(parset_name=quote(out_parset_name))
        executor(name, run_cmd, env, mpi_compartible=mpi_compartible, **kwargs)
        return output

    return parset_cmd_execute


def cli_app(
    name,
    cli_args,
    cmd,
    mpi_compartible=False,
    pipestderr=False,
):
    def cli_cmd_execute(env, **kwargs):
        parset_kwargs = kwargs["args"] if "args" in kwargs else ""
        output = cli_args.parse_string(parset_kwargs)
        env["pipestderr"] = " 2>&1" if pipestderr else ""

        run_cmd = cmd.format(option=cli_args.to_string())
        executor(name, run_cmd, env, mpi_compartible=mpi_compartible, **kwargs)
        return output

    return cli_cmd_execute
