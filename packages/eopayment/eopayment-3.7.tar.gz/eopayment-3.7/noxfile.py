from pathlib import Path

import nox


def run_hook(name, *args, **kwargs):
    for file in [Path(__name__).parent / '.nox-hooks.py', Path('~/.config/nox/eo-hooks.py').expanduser()]:
        if not file.exists():
            continue

        globals_ = {}
        exec(file.read_text(), globals_)
        hook = globals_.get(name, None)
        if hook:
            hook(*args, **kwargs)


def setup_venv(session, *packages):
    packages = [
        'coverage',
        'pytest',
        'pytest-cov',
        'pytest-freezer',
        'mock<4',
        'httmock',
        'lxml',
        'responses',
        *packages,
    ]
    run_hook('setup_venv', session, packages)
    session.install('-e', '.', *packages, silent=False)


def hookable_run(session, *args, **kwargs):
    args = list(args)
    run_hook('run', session, args, kwargs)
    session.run(*args, **kwargs)


@nox.session()
def tests(session):
    setup_venv(session)

    args = ['py.test']
    if '--coverage' in session.posargs or not session.interactive:
        while '--coverage' in session.posargs:
            session.posargs.remove('--coverage')
        args += [
            '--cov=eopayment/',
            '--cov-report=term-missing',
        ]
        if not session.interactive:
            args += [
                '-v',
                '--cov-report=xml',
                '--cov-report=html',
                '--junitxml=junit-coverage.xml',
            ]

    args += session.posargs + ['tests/']

    hookable_run(
        session,
        *args,
    )


@nox.session
def codestyle(session):
    session.install('pre-commit')
    session.run('pre-commit', 'run', '--all-files', '--show-diff-on-failure')


@nox.session
def check_manifest(session):
    # django is only required to compile messages
    session.install('django', 'check-manifest')
    # compile messages and css
    ignores = [
        'VERSION',
    ]
    session.run('check-manifest', '--ignore', ','.join(ignores))
