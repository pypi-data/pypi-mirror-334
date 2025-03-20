# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "cotwo==0.1.0",
# ]
# ///

import marimo

__generated_with = "0.11.18"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import cotwo as ct
    return ct, mo


@app.cell
def _():
    file = "/Users/freddy/Documents/Projects/cyclam_azides/Cyclam_Azides/calculations/fe_cyclam-ac/new/m2/tddft_tpssh/tddft_tpssh.xyz"
    return (file,)


@app.cell
def _(ct, file):
    fig = ct.StructureRenderer(file)
    return (fig,)


@app.cell
def _(fig):
    fig.show()
    return


@app.cell
def _(fig):
    fig.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
