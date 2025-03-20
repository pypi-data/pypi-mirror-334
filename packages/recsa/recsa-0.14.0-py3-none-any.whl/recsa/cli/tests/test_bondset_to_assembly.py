import os

import pytest
import yaml
from click.testing import CliRunner

from recsa import Assembly
from recsa.cli.commands import run_bondsets_to_assemblies_pipeline


@pytest.fixture
def bondsets_data():
    return {
        0: [1],
        1: [1, 2],
        2: [2, 3],
        3: [1, 2, 3],
        4: [1, 2, 3, 4]
    }


@pytest.fixture
def structure_data():
    return {
        'components_and_their_kinds': {
            'M1': 'M',
            'M2': 'M',
            'L1': 'L',
            'L2': 'L',
            'L3': 'L'
        },
        'bonds_and_their_binding_sites': {
            1: ['L1.b', 'M1.a'],
            2: ['M1.b', 'L2.a'],
            3: ['L2.b', 'M2.a'],
            4: ['M2.b', 'L3.a']
        }
    }


@pytest.fixture
def expected_assemblies():
    return {
        0: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),
        1: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a')]),
        2: Assembly(
            {'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        3: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        4: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'L3': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'), 
             ('M2.b', 'L3.a')])
    }


def test_cli_command_a(tmp_path, bondsets_data, structure_data, expected_assemblies):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        bondset_path = os.path.join(td, 'input.yaml')
        structure_path = os.path.join(td, 'structure.yaml')
        output_path = os.path.join(td, 'output.yaml')

        with open(bondset_path, 'w') as f:
            yaml.safe_dump(bondsets_data, f)

        with open(structure_path, 'w') as f:
            yaml.safe_dump(structure_data, f)
        
        result = runner.invoke(
            run_bondsets_to_assemblies_pipeline,
            [bondset_path, structure_path, output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)
            
        assert actual_output == expected_assemblies


if __name__ == '__main__':
    pytest.main(['-v', __file__])
