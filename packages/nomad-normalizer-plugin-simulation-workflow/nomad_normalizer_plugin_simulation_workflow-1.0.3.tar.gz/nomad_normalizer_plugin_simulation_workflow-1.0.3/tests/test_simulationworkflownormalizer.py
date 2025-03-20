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

from nomad.utils import get_logger
from nomad.datamodel import EntryArchive, EntryMetadata
from nomad.normalizing import normalizers
from runschema.run import Run, Program
from runschema.calculation import Calculation
from simulationworkflowschema import (
    Elastic,
    MolecularDynamics,
    Phonon,
    SinglePoint,
    GeometryOptimization,
)

simulationworkflownormalizer = None
for normalizer in normalizers:
    if normalizer.__name__ == 'SimulationWorkflowNormalizer':
        simulationworkflownormalizer = normalizer

assert simulationworkflownormalizer is not None

@pytest.fixture()
def entry_archive():
    return EntryArchive(metadata=EntryMetadata())


@pytest.mark.parametrize(
    'program_name, workflow_class',
    [('elastic', Elastic), ('lammps', MolecularDynamics), ('phonopy', Phonon)],
)
def test_resolve_workflow_from_program_name(
    entry_archive, program_name, workflow_class
):
    run = Run(program=Program(name=program_name))
    entry_archive.run.append(run)

    simulationworkflownormalizer(entry_archive).normalize()
    assert isinstance(entry_archive.workflow2, workflow_class)


@pytest.mark.parametrize(
    'n_calculations, workflow_class', [(1, SinglePoint), (3, GeometryOptimization)]
)
def test_resolve_workflow_from_calculation(
    entry_archive, n_calculations, workflow_class
):
    run = Run(calculation=[Calculation() for _ in range(n_calculations)])
    entry_archive.run.append(run)
    simulationworkflownormalizer(entry_archive).normalize()
    assert isinstance(entry_archive.workflow2, workflow_class)
