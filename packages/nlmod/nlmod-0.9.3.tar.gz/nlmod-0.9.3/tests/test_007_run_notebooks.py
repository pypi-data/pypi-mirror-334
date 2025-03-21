"""run notebooks in the examples directory."""

# ruff: noqa: D103
import os

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

tst_dir = os.path.dirname(os.path.realpath(__file__))
nbdir = os.path.join(tst_dir, "..", "docs", "examples")


def _run_notebook(nbdir, fname):
    fname_nb = os.path.join(nbdir, fname)
    with open(fname_nb) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=6000)
    out = ep.preprocess(nb, {"metadata": {"path": nbdir}})

    return out


@pytest.mark.notebooks
def test_run_notebook_00_model_from_scratch():
    _run_notebook(nbdir, "00_model_from_scratch.ipynb")


@pytest.mark.notebooks
def test_run_notebook_01_basic_model():
    _run_notebook(nbdir, "01_basic_model.ipynb")


@pytest.mark.notebooks
def test_run_notebook_02_surface_water():
    _run_notebook(nbdir, "02_surface_water.ipynb")


@pytest.mark.notebooks
def test_run_notebook_03_local_grid_refinement():
    _run_notebook(nbdir, "03_local_grid_refinement.ipynb")


@pytest.mark.notebooks
def test_run_notebook_04_modifying_layermodels():
    _run_notebook(nbdir, "04_modifying_layermodels.ipynb")


@pytest.mark.notebooks
def test_run_notebook_05_caching():
    _run_notebook(nbdir, "05_caching.ipynb")


@pytest.mark.notebooks
def test_run_notebook_06_gridding_vector_data():
    _run_notebook(nbdir, "06_gridding_vector_data.ipynb")


@pytest.mark.notebooks
def test_run_notebook_07_resampling():
    _run_notebook(nbdir, "07_resampling.ipynb")


@pytest.mark.notebooks
def test_run_notebook_08_gis():
    _run_notebook(nbdir, "08_gis.ipynb")


@pytest.mark.notebooks
def test_run_notebook_09_schoonhoven():
    _run_notebook(nbdir, "09_schoonhoven.ipynb")


@pytest.mark.notebooks
def test_run_notebook_10_modpath():
    _run_notebook(nbdir, "10_modpath.ipynb")


@pytest.mark.notebooks
def test_run_notebook_11_grid_rotation():
    _run_notebook(nbdir, "11_grid_rotation.ipynb")


@pytest.mark.notebooks
def test_run_notebook_12_layer_generation():
    _run_notebook(nbdir, "12_layer_generation.ipynb")


@pytest.mark.notebooks
def test_run_notebook_13_plot_methods():
    _run_notebook(nbdir, "13_plot_methods.ipynb")


@pytest.mark.notebooks
def test_run_notebook_14_stromingen_example():
    _run_notebook(nbdir, "14_stromingen_example.ipynb")


@pytest.mark.notebooks
def test_run_notebook_15_geotop():
    _run_notebook(nbdir, "15_geotop.ipynb")


@pytest.mark.notebooks
def test_run_notebook_16_groundwater_transport():
    _run_notebook(nbdir, "16_groundwater_transport.ipynb")


@pytest.mark.notebooks
def test_run_notebook_17_unsaturated_zone_flow():
    _run_notebook(nbdir, "17_unsaturated_zone_flow.ipynb")
