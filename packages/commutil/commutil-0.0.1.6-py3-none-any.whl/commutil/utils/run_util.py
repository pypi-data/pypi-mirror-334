from .debug_util import dbg
from typing import Callable, Dict, Optional, List, Union, Any
from functools import partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Pool
import subprocess


def run_cmd(cmd, shell=True):
    # if logger:
    #     logger.info(f"Run  $ {command}")
    # else:
    #     dbg(command, head="Run  $", show_type=False)
    process = subprocess.Popen(cmd, shell=shell)
    process.wait()


def multi_wrapper(cmd_list, choice="thread", n=2, **kwargs):
    run_cmd_wrapper = partial(run_cmd, **kwargs)

    # if choice in ["thread", "t", "th", "T", "threads"]:
    # with ThreadPoolExecutor(max_workers=n) as executor:
    # executor.map(run_cmd_wrapper, commands)
    # elif choice in ["process", "p", "pro", "P", "processes"]:
    #     with ProcessPoolExecutor(max_workers=n) as executor:
    #         executor.map(run_cmd_wrapper, commands)

    if choice in ["thread", "t", "th", "T", "threads"]:
        with ThreadPoolExecutor(max_workers=n) as executor:
            futures = [executor.submit(run_cmd_wrapper, cmd) for cmd in cmd_list]
            for future in futures:
                future.result()
    elif choice in ["process", "p", "pro", "P", "processes"]:
        with ProcessPoolExecutor(max_workers=n) as executor:
            futures = [executor.submit(run_cmd_wrapper, cmd) for cmd in cmd_list]
            for future in futures:
                future.result()
    elif choice in ["pool", "po", "poo", "Pool"]:
        with Pool(processes=n) as pool:
            pool.map(run_cmd_wrapper, cmd_list)

    else:
        raise ValueError("Invalid choice")


def run_cmd_list(cmd_list: List[str], logger: Optional[Callable] = None, n: int = 1, **kwargs):
    if n == 1:
        for cmd in cmd_list:
            if logger:
                logger.info(f"Stream $ {cmd}")
                # logger.info(f"Paras: {kwargs}")
            else:
                dbg(cmd, head="Stream $")
                # dbg(kwargs, head="Paras ")
            run_cmd(cmd, **kwargs)
    else:
        if logger:
            for cmd in cmd_list:
                logger.info(f"List $ {cmd}")
            # logger.info(f"Paras: {kwargs}")
        else:
            for cmd in cmd_list:
                dbg(cmd, head="List $")
            # dbg(kwargs, head="Paras ")
        multi_wrapper(cmd_list=cmd_list, n=n, **kwargs)


class CommandGenerator:
    def __init__(self, format_cmd: str = None, script="python run.py", **kwargs):
        if format_cmd is None:
            args = " ".join([f"--{k} {{{k}}}" for k, v in kwargs.items()])
            format_cmd = f"{script} {args}"

        self.format_cmd = format_cmd
        self.config_list = self._gen_config_list(**kwargs)
        self._original_kwargs = kwargs
        self._filter_conditions: Dict[str, Union[List, None]] = {
            k: None for k in kwargs.keys()
        }

    def _gen_config_list(self, **kwargs) -> List[Dict]:
        lengths = {k: len(v) if isinstance(v, (list, tuple)) else 1 for k, v in kwargs.items()}
        from itertools import product
        indices = product(*[range(lengths[k]) for k in kwargs.keys()])

        config_list = []
        for idx_combo in indices:
            current_args = {}
            for (key, value), idx in zip(kwargs.items(), idx_combo):
                if isinstance(value, (list, tuple)):
                    current_args[key] = value[idx]
                else:
                    current_args[key] = value
            config_list.append(current_args)
        return config_list

    def filter(self, **kwargs) -> 'CommandGenerator':
        for key, value in kwargs.items():
            if key not in self._filter_conditions:
                raise KeyError(f"Filter key '{key}' not found in original parameters")
            if value is not None:
                self._filter_conditions[key] = (
                    value if isinstance(value, (list, tuple)) else [value]
                )
            else:
                self._filter_conditions[key] = None
        return self

    def reset_filter(self) -> 'CommandGenerator':
        self._filter_conditions = {k: None for k in self._original_kwargs.keys()}
        return self

    def _apply_filters(self, config: Dict[str, Any]) -> bool:
        for key, filter_values in self._filter_conditions.items():
            if filter_values is None:  # None dnotes accept all values
                continue
            if key not in config:
                return False
            if config[key] not in filter_values:
                return False
        return True

    def gen_cmd_list(self) -> List[str]:
        return [
            self.format_cmd.format(**config)
            for config in self.config_list
            if self._apply_filters(config)
        ]
