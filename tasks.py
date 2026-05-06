import os
import shutil

from invoke import task
from invoke.context import Context


@task(aliases=["c"])
def clean(ctx: Context) -> None:
    """Clean up build artifacts and temporary files."""
    patterns = [
        "build",
        "dist",
        "*.egg-info",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "junit.xml",
        ".coverage",
    ]

    for pattern in patterns:
        for path in ctx.run(f'find . -name "{pattern}"', hide=True).stdout.splitlines():
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


@task(aliases=["b"])
def build(ctx: Context) -> None:
    """Build the project using uv."""
    ctx.run("uv build")


@task(aliases=["m"])
def mypy(ctx: Context) -> None:
    """Run mypy for static type checking."""
    ctx.run("mypy src/jk_soccer_core")


@task(aliases=["l"], pre=[mypy])
def lint(ctx: Context) -> None:
    """Lint the project using ruff."""
    ctx.run("ruff check .")


@task(aliases=["f"])
def fmt(ctx: Context) -> None:
    """Format the project using ruff."""
    ctx.run("ruff format  .")


@task(aliases=["t"])
def test(ctx: Context) -> None:
    """Run tests using pytest."""
    ctx.run("uv run pytest -v --cov=src tests/unit --junitxml=junit.xml")


@task(pre=[lint, test], default=True)
def ci(ctx: Context) -> None:
    """Run lint and tests."""


@task(aliases=["i"])
def install(ctx: Context) -> None:
    """Install Python dependencies using uv."""
    ctx.run("uv sync --all-extras --dev")
