import marimo

__generated_with = "0.10.17"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        """
        # Jedi-Knights
        
        ## Soccer Core Notebook
        """
    )

    return (mo,)


if __name__ == "__main__":
    app.run()
