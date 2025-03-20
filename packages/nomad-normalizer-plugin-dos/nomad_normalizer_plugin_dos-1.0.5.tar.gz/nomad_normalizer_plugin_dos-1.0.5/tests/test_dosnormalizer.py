#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest
from typing import List, Union
import numpy as np
import json

from nomad.units import ureg
from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.normalizing import normalizers
from nomad.utils import get_logger
from nomad.metainfo import Quantity, MSection, Section, SubSection

from nomad_dos_fingerprints import DOSFingerprint  # pylint: disable=import-error
from dosnormalizer.dos_integrator import integrate_dos
from runschema.run import Run, Program
from runschema.system import System, Atoms
from runschema.method import (
    Method,
    BasisSetContainer,
    BasisSet,
    Electronic,
    DFT,
    XCFunctional,
    Functional,
)
from runschema.calculation import (
    Calculation,
    Energy,
    EnergyEntry,
    Dos,
    DosValues,
)
from simulationworkflowschema import GeometryOptimization


LOGGER = get_logger(__name__)


def approx(value, abs=0, rel=1e-1):
    return pytest.approx(value, abs=abs, rel=rel)


def normalize_all(entry_archive: EntryArchive) -> None:
    for normalizer_class in normalizers:
        normalizer_class(entry_archive).normalize()


def get_template_computation() -> EntryArchive:
    """Returns a basic archive template for a computational calculation"""
    template = EntryArchive()
    run = Run()
    template.run.append(run)
    run.program = Program(name='VASP', version='4.6.35')
    system = System()
    run.system.append(system)
    system.atoms = Atoms(
        lattice_vectors=[
            [5.76372622e-10, 0.0, 0.0],
            [0.0, 5.76372622e-10, 0.0],
            [0.0, 0.0, 4.0755698899999997e-10],
        ],
        positions=[
            [2.88186311e-10, 0.0, 2.0377849449999999e-10],
            [0.0, 2.88186311e-10, 2.0377849449999999e-10],
            [0.0, 0.0, 0.0],
            [2.88186311e-10, 2.88186311e-10, 0.0],
        ],
        labels=['Br', 'K', 'Si', 'Si'],
        periodic=[True, True, True],
    )
    scc = Calculation()
    run.calculation.append(scc)
    scc.system_ref = system
    scc.energy = Energy(
        free=EnergyEntry(value=-1.5936767191492225e-18),
        total=EnergyEntry(value=-1.5935696296699573e-18),
        total_t0=EnergyEntry(value=-3.2126683561907e-22),
    )
    return template


def get_template_dft() -> EntryArchive:
    """Returns a basic archive template for a DFT calculation."""
    template = get_template_computation()
    run = template.run[-1]
    method = Method()
    run.method.append(method)
    method.electrons_representation = [
        BasisSetContainer(
            type='plane waves',
            scope=['wavefunction'],
            basis_set=[
                BasisSet(
                    type='plane waves',
                    scope=['valence'],
                )
            ],
        )
    ]
    method.electronic = Electronic(method='DFT')
    xc_functional = XCFunctional(exchange=[Functional(name='GGA_X_PBE')])
    method.dft = DFT(xc_functional=xc_functional)
    scc = run.calculation[-1]
    scc.method_ref = method
    template.workflow2 = GeometryOptimization()
    return template


def add_template_dos(
    template: EntryArchive,
    fill: List = [[[0, 1], [2, 3]]],
    energy_reference_fermi: Union[float, None] = None,
    energy_reference_highest_occupied: Union[float, None] = None,
    energy_reference_lowest_unoccupied: Union[float, None] = None,
    n_values: int = 101,
    type: str = 'electronic',
) -> EntryArchive:
    """Used to create a test data for DOS.

    Args:
        fill: List containing the energy ranges (eV) that should be filled with
            non-zero values, e.g. [[[0, 1], [2, 3]]]. Defaults to single channel DOS
            with a gap.
        energy_fermi: Fermi energy (eV)
        energy_reference_highest_occupied: Highest occupied energy (eV) as given by a parser.
        energy_reference_lowest_unoccupied: Lowest unoccupied energy (eV) as given by a parser.
        type: 'electronic' or 'vibrational'
        has_references: Whether the DOS has energy references or not.
    """
    if len(fill) > 1 and type != 'electronic':
        raise ValueError('Cannot create spin polarized DOS for non-electronic data.')
    scc = template.run[0].calculation[0]
    energies = np.linspace(-5, 5, n_values)
    for i, range_list in enumerate(fill):
        dos = Dos()
        scc[f'dos_{type}'].append(dos)
        dos.spin_channel = i if (len(fill) == 2 and type == 'electronic') else None
        dos.energies = energies * ureg.electron_volt
        dos_total = DosValues()
        dos.total.append(dos_total)
        dos_value = np.zeros(n_values)
        for r in range_list:
            idx_bottom = (np.abs(energies - r[0])).argmin()
            idx_top = (np.abs(energies - r[1])).argmin()
            dos_value[idx_bottom:idx_top] = 1
        dos_total.value = dos_value

    if energy_reference_fermi is not None:
        energy_reference_fermi *= ureg.electron_volt
    if energy_reference_highest_occupied is not None:
        energy_reference_highest_occupied *= ureg.electron_volt
    if energy_reference_lowest_unoccupied is not None:
        energy_reference_lowest_unoccupied *= ureg.electron_volt
    scc.energy = Energy(
        fermi=energy_reference_fermi,
        highest_occupied=energy_reference_highest_occupied,
        lowest_unoccupied=energy_reference_lowest_unoccupied,
    )
    return template


def get_template_dos(
    fill: List = [[[0, 1], [2, 3]]],
    energy_reference_fermi: Union[float, None] = None,
    energy_reference_highest_occupied: Union[float, None] = None,
    energy_reference_lowest_unoccupied: Union[float, None] = None,
    n_values: int = 101,
    type: str = 'electronic',
    normalize: bool = True,
) -> EntryArchive:
    archive = get_template_dft()
    archive = add_template_dos(
        archive,
        fill,
        energy_reference_fermi,
        energy_reference_highest_occupied,
        energy_reference_lowest_unoccupied,
        n_values,
        type,
    )
    if normalize:
        normalize_all(archive)
    return archive


def parse(filepath, parser_class):
    archive = EntryArchive(metadata=EntryMetadata(domain='dft'))
    parser_class().parse(filepath, archive, LOGGER)
    normalize_all(archive)
    return archive


def load_archive(filepath: str):
    archive = EntryArchive.m_from_dict(json.load(open(filepath)))
    # TODO investigate: for some reason, ref are not updated when loading archive from file
    for calc in archive.run[0].calculation:
        calc.system_ref = calc.system_ref.m_resolved()
        calc.method_ref = calc.method_ref.m_resolved()
    normalize_all(archive)
    return archive


@pytest.fixture
def dos_si_vasp():
    return load_archive('tests/data/dos_si_vasp.archive.json')


@pytest.fixture
def dos_si_exciting():
    return load_archive('tests/data/dos_si_exciting.archive.json')


@pytest.fixture
def dos_si_fhiaims():
    # TODO remove fhiiams-specifix metainfo usage from method normalizer.
    # We do not want to import the electronicparsers project for this!
    class section_controlIn_basis_set(MSection):
        m_def = Section(validate=False)

        x_fhi_aims_controlIn_species_name = Quantity(
            type=str,
            shape=[],
        )

    class XMethod(Method):
        m_def = Section(extends_base_section=True)

        x_fhi_aims_section_controlIn_basis_set = SubSection(
            sub_section=section_controlIn_basis_set, repeats=True
        )

    return load_archive('tests/data/dos_si_fhiaims.archive.json')


def test_fingerprint(dos_si_vasp):
    # Check if DOS fingerprint was created
    dos_fingerprint_dict = dos_si_vasp.m_xpath(
        """
        run[*].calculation[*].dos_electronic[*].fingerprint
        """
    )[-1][-1][0]
    dos_fingerprint = DOSFingerprint().from_dict(dos_fingerprint_dict)
    assert dos_fingerprint.get_similarity(dos_fingerprint) == 1
    assert dos_fingerprint.filling_factor != 0
    assert dos_fingerprint.filling_factor != 1


@pytest.mark.parametrize(
    'ranges, highest, lowest, fermi, expected_highest, expected_lowest, n',
    [
        # Explicit highest/lowest occupied given by parser: The current
        # behaviour is to override these values based on the data that is
        # actually stored in the DOS if there is a minor difference.
        ([[[0, 1], [2, 3]]], [1.04], [1.94], None, [1], [1.9], 101),
        # Fermi energy in the middle of a gap, inaccuracy due to discretization.
        ([[[0, 1], [2, 3]]], None, None, [1.5], [1.0], [1.9], 101),
        # Fermi energy near the top of the valence band. Since Fermi energy
        # is close enough to the zero value, gap is detected.
        ([[[0, 1], [2, 3]]], None, None, [0.99], [1.0], [1.9], 101),
        # Fermi energy near the top of the valence band, but still too far away
        # for a gap to be detected.
        ([[[0, 1], [2, 3]]], None, None, [0.89], [0.9], [0.9], 101),
        # Fermi energy near the bottom of the conduction band. Since Fermi energy
        # is close enough to the zero value, gap is detected.
        ([[[0, 1], [2, 3]]], None, None, [1.91], [1.0], [1.9], 101),
        # Fermi energy near the bottom of the conduction band, but still too
        # far away for a gap to be detected.
        ([[[0, 1], [2, 3]]], None, None, [2.01], [2.0], [2.0], 101),
        # Fermi energy at the center of a tiny peak.
        ([[[1, 1.1]]], None, None, [1], [1], [1], 101),
    ],
)
def test_energy_reference_detection(
    ranges, highest, lowest, fermi, expected_highest, expected_lowest, n
):
    """Checks that the energy reference detection for DOS works in different
    scenarios.
    """
    fermi = fermi[0] if fermi else fermi
    lowest = lowest[0] if lowest else lowest
    highest = highest[0] if highest else highest
    archive = get_template_dos(ranges, fermi, highest, lowest, n)
    assert len(archive.run[0].calculation[0].dos_electronic) == 1
    dos = archive.run[0].calculation[0].dos_electronic[0]
    gap = dos.band_gap[0]
    assert gap.energy_highest_occupied.to(
        ureg.electron_volt
    ).magnitude == pytest.approx(expected_highest[0])
    assert gap.energy_lowest_unoccupied.to(
        ureg.electron_volt
    ).magnitude == pytest.approx(expected_lowest[0])


@pytest.mark.skip(reason='Metainfo error')
def test_dos_magnitude(dos_si_vasp, dos_si_exciting, dos_si_fhiaims):
    """
    Verify that the raw DOS extracted from similar systems describes the same number of
    electrons. Testing for VASP, exciting and FHI-aims DOS Si2 parsing.
    """
    dos_ints = [
        integrate_dos(dos_si.run[0].calculation[-1].dos_electronic)
        for dos_si in [dos_si_vasp, dos_si_exciting, dos_si_fhiaims]
    ]

    # Compare each DOS with its neighbor
    for index in range(len(dos_ints))[:-1]:
        assert approx(dos_ints[index]) == approx(dos_ints[index + 1])
