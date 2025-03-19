import inspect

import pytest

from struphy.models.tests.util import call_test


@pytest.mark.parametrize(
    "map_and_equil", [("Cuboid", "HomogenSlab"), ("HollowTorus", "AdhocTorus"), ("Tokamak", "EQDSKequilibrium")]
)
def test_hybrid(
    map_and_equil: tuple | list,
    fast: bool,
    vrbose: bool,
    verification: bool,
    show_plots: bool,
    *,
    model: str = None,
    Tend: float = None,
):
    """Tests all models in models/hybrid.py.

    If model is not None, tests the specified model.
    The argument "fast" is a pytest option that can be specified at the command line (see conftest.py)."""

    from mpi4py import MPI

    from struphy.models import hybrid

    comm = MPI.COMM_WORLD

    if model is None:
        for key, val in inspect.getmembers(hybrid):
            if inspect.isclass(val) and key not in {"StruphyModel", "Propagator"}:
                if fast and "Cuboid" not in map_and_equil[0]:
                    print(f"Fast is enabled, mapping {map_and_equil[0]} skipped ...")
                    continue
                call_test(
                    key,
                    val,
                    map_and_equil,
                    Tend=Tend,
                    verbose=vrbose,
                    comm=comm,
                    verification=verification,
                    show_plots=show_plots,
                )
    else:
        val = getattr(hybrid, model)
        call_test(
            model,
            val,
            map_and_equil,
            Tend=Tend,
            verbose=vrbose,
            comm=comm,
            verification=verification,
            show_plots=show_plots,
        )


if __name__ == "__main__":
    # This is called in struphy_test in case "group" is a model name
    import sys

    model = sys.argv[1]
    if sys.argv[2] == "None":
        Tend = None
    else:
        Tend = float(sys.argv[2])
    fast = sys.argv[3] == "True"
    vrbose = sys.argv[4] == "True"
    verification = sys.argv[5] == "True"
    show_plots = sys.argv[6] == "True"

    map_and_equil = ("Cuboid", "HomogenSlab")
    test_hybrid(
        map_and_equil,
        fast,
        vrbose,
        verification,
        show_plots,
        model=model,
        Tend=Tend,
    )

    if not fast and not verification:
        map_and_equil = ("HollowTorus", "AdhocTorus")
        test_hybrid(
            map_and_equil,
            fast,
            vrbose,
            verification,
            show_plots,
            model=model,
            Tend=Tend,
        )

        map_and_equil = ("Tokamak", "EQDSKequilibrium")
        test_hybrid(
            map_and_equil,
            fast,
            vrbose,
            verification,
            show_plots,
            model=model,
            Tend=Tend,
        )
