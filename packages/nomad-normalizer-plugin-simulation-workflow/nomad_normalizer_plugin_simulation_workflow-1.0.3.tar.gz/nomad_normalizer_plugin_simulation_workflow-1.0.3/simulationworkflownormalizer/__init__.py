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
from nomad.config.models.plugins import NormalizerEntryPoint


class SimulationWorkflowNormalizerEntryPoint(NormalizerEntryPoint):
    def load(self):
        import simulationworkflownormalizer
        from .normalizer import SimulationWorkflowNormalizer

        simulationworkflownormalizer.SimulationWorkflowNormalizer = SimulationWorkflowNormalizer

        return SimulationWorkflowNormalizer(**self.dict())


simulationworkflow_normalizer_entry_point = SimulationWorkflowNormalizerEntryPoint(
    name='SimulationWorkflowNormalizer',
    description='Normalizer for the simulation workflow data.',
)

