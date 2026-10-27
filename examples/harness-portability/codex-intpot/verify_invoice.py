"""Run with the pinned environment's Python; no installation or network needed.

Portable command: /path/to/pinned/.venv/bin/python -B verify_invoice.py
The sibling intpot executable is used. Every run preserves its own scratch folder,
exact subprocess argv/shell commands, stdout, stderr, and assertion results.
Native invoice.app.eject('cli') returns source; intpot.load() instead discovers
framework apps and returns IntpotApp with to_cli()/write() conversion methods.
Only native CLI export is tested here, not API/MCP or framework conversion.
"""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SCRATCH = ROOT / 'scratch'
SCRATCH.mkdir(exist_ok=True)
OUT = Path(tempfile.mkdtemp(prefix='invoice-verification-', dir=SCRATCH))
PYTHON = sys.executable
INTPOT = str(Path(PYTHON).with_name('intpot'))
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SCRATCH),
           PYTHONPYCACHEPREFIX=str(OUT / 'pycache'), NO_COLOR='1', TERM='dumb')
LOG = OUT / 'verification.jsonl'

def record(**entry):
    with LOG.open('a') as stream:
        stream.write(json.dumps(entry) + '\n')

def check(condition, description):
    record(assertion=description, passed=bool(condition))
    if not condition:
        raise AssertionError(description)

def run(*args, expected=0):
    args = list(map(str, args))
    result = subprocess.run(args, cwd=ROOT, env=ENV, text=True,
                            capture_output=True, timeout=30)
    record(argv=args, command=shlex.join(args), cwd=str(ROOT),
           returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
    if expected is not None:
        check(result.returncode == expected, f'exit status {expected}: {shlex.join(args)}')
    return result

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    record(operation='import module', path=str(path), name=name)
    return module

def main():
    record(python=sys.version, executable=PYTHON,
           invocation=shlex.join([PYTHON, '-B', str(Path(__file__).resolve())]),
           environment={k: ENV[k] for k in ('PYTHONDONTWRITEBYTECODE', 'TMPDIR', 'PYTHONPYCACHEPREFIX', 'NO_COLOR', 'TERM')},
           source_sha256=hashlib.sha256((ROOT / 'invoice.py').read_bytes()).hexdigest(),
           supplied_source_revision='8e583cc4b2b6785955268d09a12dfdd955194b88')
    run(INTPOT, '--version')
    run(INTPOT, '--help')
    run(INTPOT, 'eject', '--help')
    pip = run(PYTHON, '-m', 'pip', 'show', 'intpot', expected=None)
    if pip.returncode:
        record(note='pip metadata command failed; preserved above; use installed distribution metadata')
    run(PYTHON, '-c', "import importlib.metadata as m, intpot; print(m.version('intpot')); print(intpot.__file__)")
    source = load(ROOT / 'invoice.py', 'invoice_original')
    from intpot import App
    check(isinstance(source.app, App), 'source is native intpot.App')
    cli_path = OUT / 'invoice_cli.py'
    native_path = OUT / 'invoice_native.py'
    run(INTPOT, 'eject', 'invoice.py', '--to', 'cli', '--output', cli_path)
    code = source.app.eject('cli')
    record(operation="invoice.app.eject('cli')", return_type=type(code).__name__)
    check(isinstance(code, str), 'native App.eject returns source text')
    native_path.write_text(code)
    record(operation='write native export', path=str(native_path))
    check(cli_path.read_text() == code, 'CLI and Python native exports are identical')
    cases = [(2, 1250, None, 2500), (2, 1250, 500, 2000),
             (3, 0, None, 0), (2, 1250, 2500, 0)]
    invalid = [(0, 1250, None), (-1, 1250, None), (1, 100, 101)]
    for path in (cli_path, native_path):
        tree = ast.parse(path.read_text())
        imports = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
        imports += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
        check(not any(n and n.split('.')[0] == 'intpot' for n in imports), 'standalone export has no intpot import')
        run(PYTHON, '-m', 'py_compile', path)
        generated = load(path, path.stem)
        check(callable(generated.app), 'generated Typer app imports')
        run(PYTHON, path, '--help')
        for quantity, price, discount, expected in cases:
            kwargs = {} if discount is None else {'discount_cents': discount}
            original = source.quote(quantity, price, **kwargs)
            check(original == expected, f'original quote{quantity, price, discount} == {expected}')
            args = [str(quantity), str(price)]
            if discount is not None:
                args += ['--discount-cents', str(discount)]
            result = run(PYTHON, path, *args)
            check(result.stdout.strip() == str(original), f'{path.name} matches original: {args}')
        for quantity, price, discount in invalid:
            kwargs = {} if discount is None else {'discount_cents': discount}
            try:
                source.quote(quantity, price, **kwargs)
            except ValueError as exc:
                message = str(exc)
                record(original_exception=type(exc).__name__, message=message, args=[quantity, price, discount])
            else:
                raise AssertionError('Original must reject invalid case')
            args = [str(quantity), str(price)]
            if discount is not None:
                args += ['--discount-cents', str(discount)]
            if quantity < 0:
                args.insert(0, '--')
            result = run(PYTHON, path, *args, expected=None)
            check(result.returncode != 0, f'{path.name} rejects {args}')
            check('ValueError' in result.stderr and message in result.stderr,
                  'CLI retains original ValueError and message')
    record(status='PASS', scope='Two native CLI exports; compile, import, four valid and three invalid cases each. API/MCP and conversion not exercised.')

if __name__ == '__main__':
    try:
        main()
    except BaseException:
        record(status='FAIL', traceback=traceback.format_exc())
        raise
    finally:
        print(f'Artifacts and preserved results: {OUT.relative_to(ROOT)}')
