import os
import sys
import shlex
import runpy
import hashlib
import subprocess
import importlib.util
from abc import abstractmethod
from typing import Union, Callable, List, Iterable


class TargetType:

    command = 'command'
    python_callable = 'python_callable'
    python_script_callable = 'python_script_callable'
    python_module_callable = 'python_module_callable'
    python_script = 'python_script'
    python_module = 'python_module'


class Target:

    @classmethod
    def make(
            cls,
            source: Union[Callable, str, List[str]],
            args = (),
            kwargs  = {},
    ):
        if callable(source):
            impl = PythonCallableTarget
        elif isinstance(source, str):
            parts = shlex.split(source)
            if not parts:
                raise ValueError(f'invalid source "{source}"')
            impl = None
            if len(parts) == 1:
                if ':' in source:
                    domain_str, func_str = source.split(':')
                    if domain_str.endswith('.py'):
                        impl = PythonScriptCallableTarget
                    else:
                        impl = PythonModuleCallableTarget
                elif source.endswith('.py'):
                    impl = PythonScriptTarget
                elif '.' in source:
                    impl = PythonModuleTarget
            if impl is None:
                impl = CommandTarget
        elif isinstance(source, list):
            impl = CommandTarget
        else:
            raise ValueError(f'invalid target source "{source}"')

        return impl(source, args, kwargs)

    def __init__(self, source, args, kwargs):
        self.source = source
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.prepare_call()
        return self.do_call()

    @abstractmethod
    def prepare_call(self):
        pass

    @abstractmethod
    def do_call(self):
        pass
    
    @property
    def kwargs_as_cmdline_options(self):
        def gen():
            for key, value in self.kwargs.items():
                yield f'--{key}'
                yield f'{value}'
        return list(gen())
    
    @property
    def cwd(self):
        return os.getcwd()  # TODO: configurable


class CallableTarget(Target):

    def prepare_call(self):
        self.func = None

    def do_call(self):
        return self.func(*self.args, **self.kwargs)


class PythonCallableTarget(CallableTarget):

    type = TargetType.python_callable

    def prepare_call(self):
        self.func = self.source


class PythonScriptCallableTarget(CallableTarget):

    type = TargetType.python_script_callable

    def prepare_call(self):
        path, func_name = self.source.split(':')
        name = hashlib.md5(str(path).encode('utf-8')).hexdigest()
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.func = getattr(module, func_name)


class PythonModuleCallableTarget(CallableTarget):

    type = TargetType.python_module_callable

    def prepare_call(self):
        module_name, func_name = self.source.split(':')
        spec = importlib.util.find_spec(module_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.func = getattr(module, func_name)


class PythonScriptTarget(Target):

    type = TargetType.python_script

    def do_call(self):
        return runpy.run_path(self.source, {}, run_name = '__main__')


class PythonModuleTarget(Target):

    type = TargetType.python_module

    def do_call(self):
        proc = subprocess.Popen(
            [sys.executable, '-m', self.source, *self.args, *self.kwargs_as_cmdline_options],
            cwd=self.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # redirect to stdout
            bufsize=1,
            encoding='utf-8',
            universal_newlines=True,
        )
        try:
            for line in iter(proc.stdout.readline, ''):
                print(line, end='')
        except KeyboardInterrupt:
            pass
        finally:
            proc.wait()

        return proc.returncode


class CommandTarget(Target):

    type = TargetType.command

    def do_call(self):
        cmd = self.source
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd)
        proc.wait()
        return proc.returncode
