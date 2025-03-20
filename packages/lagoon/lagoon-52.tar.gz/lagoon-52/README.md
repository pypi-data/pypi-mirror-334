# lagoon
Concise layer on top of subprocess, similar to sh project

## Support
If you see an error along the lines of:
```
ImportError: cannot import name 'zyx' from 'lagoon.text'
```
This means the app requires command `zyx` to be available, and you don't have it on your system.
The solution is to install `zyx` in the usual way, e.g. via your package manager.

## Usage examples
Unlike with plain old subprocess, stdout is returned by default. Use the `print` token to send it to console:
```
from lagoon.text import docker

docker.run.__rm[print]('hello-world')
```
Attributes are treated as arguments, and their underscores are converted to dashes. Arguments in brackets are not transformed except for conversion to string.
Use the `partial` token to suppress launch via brackets, and use `with` to run a command in the background:
```
from lagoon.text import zcat
from lagoon.program import partial # Also works when imported from functools.
import sys

with zcat[partial]('/var/log/dmesg.1.gz') as f:
    for line in f:
        sys.stdout.write(line)
```
When there is just one value to return it is returned directly, otherwise CompletedProcess (or Popen in background case) is returned:
```
from lagoon.text import echo

assert 'word\n' == echo('word')
assert 'word\n' == echo('word', check = False).stdout
assert 0 == echo('word', check = False).returncode
assert 0 == echo[print]('word', check = False)
```

### Defaults different to subprocess
* The stdout is returned instead of being sent to console
* CalledProcessError is raised if the exit status is not zero i.e. check is True
* Environment variables are merged into the existing environment instead of replacing it
  * Set a variable to None to remove it from the environment
* When importing from `lagoon.text` all 3 streams are in text mode, use `lagoon.binary` for binary mode

### Irregular commands
You can use getattr if the command can't be imported in the usual way:
```
import lagoon.text

gplusplus = getattr(lagoon.text, 'g++')
```
Alternatively create a ProgramHandle manually:
```
from lagoon.program import Program
from shutil import which

gplusplus = Program.text(which('g++'))
```
Most commands are dash-separated so lagoon.text/lagoon.binary translate that to underscore for convenience. If your command already has an underscore in its name, it will be in lagoon.sic.text/lagoon.sic.binary instead:
```
from lagoon.text import debian_distro_info
from lagoon.sic.text import lsb_release
```
In the rare case a command has at least one dash, but translating its dashes to underscores would result in an unimportable name, it too will be in the `sic` modules:
```
import lagoon.sic.text

gplusplus_11 = getattr(lagoon.sic.text, 'g++-11')
```

## Commands

### dirpile
Using OverlayFS create a merged view of the given (read only) dirs plus a (writable) temporary dir, print its path, and stay running until stdin is closed.
The first given directory is the lowest in the pile (this is unlike the lowerdir mount option).
This program requires root and is designed to be invoked via sudo.

## API

<a id="dkrcache"></a>

### dkrcache

<a id="dkrcache.NORMAL"></a>

###### NORMAL

Accept normal outcomes.

<a id="dkrcache.ABRUPT"></a>

###### ABRUPT

Accept abrupt outcomes.

<a id="dkrcache.ALWAYS"></a>

###### ALWAYS

Accept all outcomes.

<a id="dkrcache.NEVER"></a>

###### NEVER

Do not accept any outcome.

<a id="dkrcache.ExpensiveTask"></a>

#### ExpensiveTask Objects

```python
class ExpensiveTask()
```

Arbitrary task accelerated by Docker cache.

<a id="dkrcache.ExpensiveTask.__init__"></a>

###### \_\_init\_\_

```python
def __init__(context, discriminator, task)
```

Create a task keyed by context directory and discriminator string.

<a id="dkrcache.ExpensiveTask.run"></a>

###### run

```python
def run(force=NEVER, cache=NORMAL)
```

Run the task, where `force` can be used to ignore a cached outcome, and `cache` can be used to deny caching an outcome.

<a id="dkrcache.util"></a>

### dkrcache.util

<a id="dkrcache.util.ContextStream"></a>

#### ContextStream Objects

```python
class ContextStream()
```

Fully customisable docker build context.

<a id="dkrcache.util.ContextStream.open"></a>

###### open

```python
@classmethod
@contextmanager
def open(cls, dockerstdin)
```

Attach to the given stdin of docker build, which should have been given `-` as context.

<a id="dkrcache.util.ContextStream.put"></a>

###### put

```python
def put(name, path)
```

Add the given path as the given archive name.

<a id="dkrcache.util.ContextStream.putstream"></a>

###### putstream

```python
def putstream(name, stream)
```

Add the given stream as the given archive name.

<a id="dkrcache.util.ContextStream.mkdir"></a>

###### mkdir

```python
def mkdir(name)
```

Create a directory in the context.

<a id="dkrcache.util.iidfile"></a>

###### iidfile

```python
@contextmanager
def iidfile()
```

Context manager yielding an object with `args` to pass to docker build, and a `read` function to get the image ID.

<a id="lagoon.binary"></a>

### lagoon.binary

Like lagoon.text module but ProgramHandle objects are in binary mode.

<a id="lagoon.program"></a>

### lagoon.program

<a id="lagoon.program.Program"></a>

#### Program Objects

```python
class Program()
```

Normally import an instance from `lagoon.text` or `lagoon.binary` module instead of instantiating manually.

<a id="lagoon.program.Program.text"></a>

###### text

```python
@classmethod
def text(cls, path)
```

Return text mode ProgramHandle for the executable at the given path.

<a id="lagoon.program.Program.binary"></a>

###### binary

```python
@classmethod
def binary(cls, path)
```

Return binary mode ProgramHandle for executable at given path.

<a id="lagoon.program.ProgramHandle"></a>

#### ProgramHandle Objects

```python
class ProgramHandle(Parabject)
```

<a id="lagoon.program.ProgramHandle.__getattr__"></a>

###### \_\_getattr\_\_

```python
def __getattr__(name)
```

Add argument, where underscore means dash.

<a id="lagoon.program.ProgramHandle.__getitem__"></a>

###### \_\_getitem\_\_

```python
def __getitem__(key)
```

Apply a style, e.g. `partial` to suppress execution or `print` to send stdout to console.

<a id="lagoon.program.ProgramHandle.__call__"></a>

###### \_\_call\_\_

```python
def __call__(*args, **kwargs)
```

Run program in foreground with additional args. Accepts many subprocess kwargs. Use `partial` style to suppress execution, e.g. before running in background. Otherwise return CompletedProcess, or one of its fields if the rest are redirected, or None if all fields redirected.

<a id="lagoon.program.ProgramHandle.__enter__"></a>

###### \_\_enter\_\_

```python
def __enter__()
```

Start program in background yielding the Popen object, or one of its fields if the rest are redirected.

<a id="lagoon.program.NOEOL"></a>

#### NOEOL Objects

```python
@singleton
class NOEOL()
```

Style to strip trailing newlines from stdout, in the same way as shell does.

<a id="lagoon.program.ONELINE"></a>

###### ONELINE

```python
def ONELINE(text)
```

Style to assert exactly one line of output, using `splitlines`.

<a id="lagoon.sic.binary"></a>

### lagoon.sic.binary

Commands with an underscore already in their name, binary mode.

<a id="lagoon.sic.text"></a>

### lagoon.sic.text

Commands with an underscore already in their name, text mode.

<a id="lagoon.text"></a>

### lagoon.text

Text mode instances of ProgramHandle for every executable, with dash translated to underscore e.g. `from lagoon.text import pkg_config` for `pkg-config`.

<a id="lagoon.url"></a>

### lagoon.url

<a id="lagoon.util"></a>

### lagoon.util

<a id="lagoon.util.unmangle"></a>

###### unmangle

```python
def unmangle(name)
```

Undo name mangling.

<a id="lagoon.util.atomic"></a>

###### atomic

```python
@contextmanager
def atomic(path)
```

Context manager yielding a temporary Path for atomic write to the given path. Parent directories are created automatically. Also suitable for making a symlink atomically. Leaves the given path unchanged if an exception happens.

<a id="lagoon.util.threadlocalproperty"></a>

#### threadlocalproperty Objects

```python
class threadlocalproperty()
```

Like `property` but each thread has its own per-object values.

<a id="lagoon.util.threadlocalproperty.__init__"></a>

###### \_\_init\_\_

```python
def __init__(defaultfactory)
```

The `defaultfactory` should return the initial value per object (per thread).

<a id="lagoon.util.onerror"></a>

###### onerror

```python
@contextmanager
def onerror(f)
```

Context manager that runs the given function if an exception happens, like `finally` excluding the happy path.

<a id="lagoon.util.mapcm"></a>

###### mapcm

```python
@contextmanager
def mapcm(f, obj)
```

Invoke `obj` as a context manager, apply `f` to its yielded value, and yield that. For example apply `Path` to the string yielded by `TemporaryDirectory()`.

<a id="lagoon.util.stripansi"></a>

###### stripansi

```python
def stripansi(text)
```

Remove ANSI control sequences from the given text, to make it black and white.

<a id="lagoon.util.HarnessCase"></a>

#### HarnessCase Objects

```python
class HarnessCase(TestCase)
```

Enter context managers in setUp and exit them in tearDown.

<a id="lagoon.util.HarnessCase.harness"></a>

###### harness

```python
def harness()
```

Must yield exactly once.

<a id="lagoon.util.wrappercli"></a>

###### wrappercli

```python
def wrappercli()
```

Same as sys.argv[1:] if `--` is present there, otherwise `--` is prepended. This is for sending all options to a wrapped command by default.

<a id="multifork"></a>

### multifork

<a id="screen"></a>

### screen

GNU Screen interface, smoothing over its many gotchas.

<a id="screen.stuffablescreen"></a>

###### stuffablescreen

```python
def stuffablescreen(doublequotekey)
```

Return text mode ProgramHandle for screen, with the given environment variable set to double quote.

<a id="screen.Stuff"></a>

#### Stuff Objects

```python
class Stuff()
```

<a id="screen.Stuff.__init__"></a>

###### \_\_init\_\_

```python
def __init__(session, window, doublequotekey)
```

Target the given screen session and window, using the given environment variable for double quote.

<a id="screen.Stuff.__call__"></a>

###### \_\_call\_\_

```python
def __call__(text)
```

Send the given text so that it is received literally.

<a id="screen.Stuff.eof"></a>

###### eof

```python
def eof()
```

Send EOF, may have no effect if not at the start of a line.

