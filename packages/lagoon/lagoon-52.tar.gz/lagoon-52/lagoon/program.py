from .util import threadlocalproperty, unmangle
from aridity.util import solo
from diapyr.util import singleton
from parabject import Parabject, register
from pathlib import Path
import functools, json, os, re, shlex, subprocess, sys

class Program:
    'Normally import an instance from `lagoon.text` or `lagoon.binary` module instead of instantiating manually.'

    bginfo = threadlocalproperty(lambda: None)

    @staticmethod
    def _strornone(arg):
        return arg if arg is None else str(arg)

    @classmethod
    def text(cls, path):
        'Return text mode ProgramHandle for the executable at the given path.'
        return cls(path, True, None, (), {}, _fgmode, 0).handle

    @classmethod
    def binary(cls, path):
        'Return binary mode ProgramHandle for executable at given path.'
        return cls(path, None, None, (), {}, _fgmode, 0).handle

    @classmethod
    def of(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(self, path, textmode, cwd, args, kwargs, runmode, ttl):
        self.handle = register(self, ProgramHandle)
        self.path = path
        self.textmode = textmode
        self.cwd = cwd
        self.args = args
        self.kwargs = kwargs
        self.runmode = runmode
        self.ttl = ttl

    def _resolve(self, path):
        return Path(path) if self.cwd is None else self.cwd / path

    def cd(self, cwd):
        return self.of(self.path, self.textmode, self._resolve(cwd), self.args, self.kwargs, self.runmode, self.ttl).handle

    def getattr(self, name):
        return self.of(self.path, self.textmode, self.cwd, self.args + (unmangle(name).replace('_', '-'),), self.kwargs, self.runmode, self.ttl).handle

    def getitem(self, keys):
        for k in keys:
            self = styles[k](self)
        return self.handle

    def _mergedkwargs(self, kwargs):
        merged = {**self.kwargs, **kwargs}
        k = 'env'
        if k in self.kwargs and k in kwargs:
            d1 = self.kwargs[k]
            if d1 is not None: # Otherwise d2 wins, whatever it is.
                d2 = kwargs[k]
                merged[k] = d1 if d2 is None else {**d1, **d2}
        return merged

    def _transform(self, args, kwargs, checkxform):
        args = self.args + args
        kwargs = self._mergedkwargs(kwargs)
        if bool == kwargs.get('check'):
            kwargs['check'] = False
            mapcode = lambda rc: not rc
        else:
            kwargs.setdefault('check', True)
            mapcode = lambda rc: rc
        kwargs.setdefault('stdout', subprocess.PIPE)
        kwargs.setdefault('stderr', None)
        kwargs.setdefault('universal_newlines', self.textmode)
        kwargs['cwd'] = self._strornone(self._resolve(kwargs['cwd']) if 'cwd' in kwargs else self.cwd)
        env = kwargs.get('env')
        kwargs['env'] = (None if env is None else
                {**{k: v for k, v in os.environ.items() if env.get(k, v) is not None}, **{k: v for k, v in env.items() if v is not None}})
        aux = kwargs.pop('aux', None)
        readables = {i for i, f in enumerate(args) if getattr(f, 'readable', lambda: False)()}
        if readables:
            i, = readables
            if 'stdin' in kwargs:
                raise ValueError
            kwargs['stdin'] = args[i]
        def transformargs():
            for i, arg in enumerate(args):
                yield '-' if i in readables else (arg if isinstance(arg, bytes) else str(arg))
        def xforms():
            def streamxforms(name):
                val = kwargs[name]
                if val == subprocess.PIPE:
                    yield lambda res: getattr(res, name)
                elif val in {NOEOL, ONELINE, json.loads}:
                    kwargs[name] = subprocess.PIPE
                    yield lambda res: val(getattr(res, name))
            if not kwargs['check']:
                yield functools.partial(checkxform, mapcode)
            if kwargs.get('stdin') == subprocess.PIPE:
                yield lambda res: res.stdin
            for stream in 'stdout', 'stderr':
                yield from streamxforms(stream)
            if aux is not None:
                yield lambda res: getattr(res, aux)
        xforms = xforms()
        try:
            xform = next(xforms)
            try:
                next(xforms)
                xform = lambda res: res
            except StopIteration:
                pass
        except StopIteration:
            xform = lambda res: None
        return [self._xformpath(), *transformargs()], kwargs, xform

    def _xformpath(self):
        try:
            is_absolute = self.path.is_absolute
        except AttributeError:
            return self.path
        return self.path if is_absolute() else f"{os.curdir}{os.sep}{self.path}"

    def call(self, args, kwargs):
        if self.ttl:
            return self.of(self.path, self.textmode, self.cwd, self.args + args, self._mergedkwargs(kwargs), self.runmode, self.ttl - 1).handle
        return self.runmode(self, *args, **kwargs)

    def str(self):
        return ' '.join(shlex.quote(str(w)) for w in [self.path, *self.args])

    def enter(self):
        assert not self.ttl
        cmd, kwargs, xform = self._transform((), {}, lambda mapcode, res: lambda: mapcode(res.wait()))
        check = kwargs.pop('check')
        process = subprocess.Popen(cmd, **kwargs)
        try:
            result = xform(process)
            self.bginfo = self.bginfo, cmd, check, process
            return result
        except:
            with process:
                raise

    def exit(self, exc_info):
        self.bginfo, cmd, check, process = self.bginfo
        with process:
            pass # XXX: Propagate our exc_info?
        if check and process.returncode:
            raise subprocess.CalledProcessError(process.returncode, cmd)

class ProgramHandle(Parabject):

    def __getattr__(self, name):
        'Add argument, where underscore means dash.'
        return (-self).getattr(name)

    def __getitem__(self, key):
        'Apply a style, e.g. `partial` to suppress execution or `print` to send stdout to console.'
        return (-self).getitem(key if isinstance(key, tuple) else [key])

    def __call__(self, *args, **kwargs):
        'Run program in foreground with additional args. Accepts many subprocess kwargs. Use `partial` style to suppress execution, e.g. before running in background. Otherwise return CompletedProcess, or one of its fields if the rest are redirected, or None if all fields redirected.'
        return (-self).call(args, kwargs)

    def __str__(self):
        return (-self).str()

    def __enter__(self):
        'Start program in background yielding the Popen object, or one of its fields if the rest are redirected.'
        return (-self).enter()

    def __exit__(self, *exc_info):
        return (-self).exit(exc_info)

@singleton
class NOEOL:
    'Style to strip trailing newlines from stdout, in the same way as shell does.'

    t, b = (re.compile(x(r'[\r\n]*$')) for x in [lambda s: s, lambda s: s.encode('ascii')])

    def __call__(self, text):
        return text[:(self.t if hasattr(text, 'encode') else self.b).search(text).start()]

def ONELINE(text):
    'Style to assert exactly one line of output, using `splitlines`.'
    return solo(text.splitlines())

def _boolstyle(program):
    return -program.handle[partial](check = bool)

def _partialstyle(program):
    return program.of(program.path, program.textmode, program.cwd, program.args, program.kwargs, program.runmode, program.ttl + 1)

def _fgmode(program, *args, **kwargs):
    cmd, kwargs, xform = program._transform(args, kwargs, lambda mapcode, res: mapcode(res.returncode))
    return xform(subprocess.run(cmd, **kwargs))

def _stdoutstyle(token):
    return lambda program: -program.handle[partial](stdout = token)

def _teestyle(program):
    return program.of(program.path, program.textmode, program.cwd, program.args, program.kwargs, _teemode, program.ttl)

def _teemode(program, *args, **kwargs):
    def lines():
        with program.handle[partial](*args, **kwargs) as stdout:
            while True:
                line = stdout.readline()
                if not line:
                    break
                yield line
                sys.stdout.write(line)
    return ''.join(lines())

def _execstyle(program):
    return program.of(program.path, program.textmode, program.cwd, program.args, program.kwargs, _execmode, program.ttl)

def _execmode(program, *args, **kwargs): # XXX: Flush stdout (and stderr) first?
    supportedkeys = {'cwd', 'env'}
    keys = kwargs.keys()
    if not keys <= supportedkeys:
        raise Exception("Unsupported keywords: %s" % (keys - supportedkeys))
    cmd, kwargs, _ = program._transform(args, kwargs, lambda: None)
    cwd, env = (kwargs[k] for k in ['cwd', 'env'])
    if cwd is None:
        os.execvpe(cmd[0], cmd, env)
    # First replace this program so that failure can't be caught after chdir:
    precmd = [sys.executable, '-c', 'import os, sys; cwd, *cmd = sys.argv[1:]; os.chdir(cwd); os.execvp(cmd[0], cmd)', cwd, *cmd]
    os.execve(precmd[0], precmd, os.environ if env is None else env)

bg = partial = object()
tee = object()
styles = {
    bool: _boolstyle,
    exec: _execstyle,
    functools.partial: _partialstyle,
    json: _stdoutstyle(json.loads),
    NOEOL: _stdoutstyle(NOEOL),
    ONELINE: _stdoutstyle(ONELINE),
    partial: _partialstyle,
    print: _stdoutstyle(None),
    tee: _teestyle,
}
