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

from nomad.utils import get_logger
from nomad.normalizing.normalizer import Normalizer
from simulationworkflowschema import (
    SinglePoint,
    GeometryOptimization,
    MolecularDynamics,
    Phonon,
    Elastic,
)
from nomad.datamodel import EntryArchive


class SimulationWorkflowNormalizer(Normalizer):
    """
    This normalizer produces information specific to a simulation workflow.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._elastic_programs = ['elastic']
        self._phonon_programs = ['phonopy']
        self._molecular_dynamics_programs = ['lammps']

    def _resolve_workflow(self, archive: EntryArchive):
        if not archive.run:
            return

        # resolve it from parser
        workflow = None
        try:
            program_name = archive.run[-1].program.name
        except Exception:
            program_name = None

        if program_name:
            program_name = program_name.lower()

        if program_name in self._elastic_programs:
            workflow = Elastic()

        elif program_name in self._molecular_dynamics_programs:
            workflow = MolecularDynamics()

        elif program_name in self._phonon_programs:
            workflow = Phonon()

        # resolve if from scc
        if workflow is None:
            # workflow references always to the last run
            # TODO decide if workflow should map to each run
            if len(archive.run[-1].calculation) == 1:
                workflow = SinglePoint()
            else:
                workflow = GeometryOptimization()

        return workflow

    def normalize(self, archive: EntryArchive, logger=None) -> None:
        logger = logger if logger is not None else get_logger(__name__)
        super().normalize(archive, logger)

        # Do nothing if run section is not present
        if not archive.run:
            return

        if not archive.workflow2:
            archive.workflow2 = self._resolve_workflow(archive)
