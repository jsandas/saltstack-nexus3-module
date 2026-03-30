import nox


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session):
    session.install("-e", ".[tests,tests-integration]")
    session.run("pytest", "tests/unit", "tests/functional")


@nox.session
def integration(session):
    session.install("-e", ".[tests-integration]")
    session.run("pytest", "tests/integration")


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", "src")


@nox.session
def docs(session):
    session.install("-e", ".[docs]")
    session.run("sphinx-build", "-b", "html", "docs", "docs/_build/html")


@nox.session
def changelog(session):
    session.install("towncrier>=24.8", "-e", ".")
    session.run("towncrier", "build", "--draft")
