from invoke import task
import os
import shutil


@task(aliases=["c"])
def clean(ctx):
    """Clean up build artifacts and temporary files."""
    patterns = ["build", "dist", "*.egg-info", "__pycache__", "*.pyc", "*.pyo"]

    for pattern in patterns:
        for path in ctx.run(f'find . -name "{pattern}"', hide=True).stdout.splitlines():
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


@task(aliases=["b"])
def build(ctx):
    """Build the project using uv."""
    ctx.run("uv build")


@task(aliases=["l"])
def lint(ctx):
    """Lint the project using ruff."""
    ctx.run("ruff check .")


@task(aliases=["f"])
def fmt(ctx):
    """Format the project using ruff."""
    ctx.run("ruff format  .")
