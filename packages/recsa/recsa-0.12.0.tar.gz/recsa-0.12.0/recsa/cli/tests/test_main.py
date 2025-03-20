import os

import pytest
import yaml
from click.testing import CliRunner

from recsa import Assembly, Component, is_isomorphic
from recsa.cli.main import main


def test_enumerate_assemblies(tmp_path):
    runner = CliRunner()

    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: [2],
            2: [1, 3],
            3: [2, 4],
            4: [3],
        },
        'sym_ops': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        },
        'component_kinds': {
            'L': Component(['a', 'b']),
            'M': Component(['a', 'b']),
            'X': Component(['a']),
        },
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
        },
        'capping_config': {
            'target_component_kind': 'M',
            'capping_component_kind': 'X',
            'capping_binding_site': 'a'
        }
    }

    EXPECTED = {
        # L1--M1--X1
        0: Assembly(
            {'L1': 'L', 'M1': 'M', 'X1': 'X'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'X1.a')]),
        # L1--M1--L2
        1: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a')]),
        # X1--M1--L2--M2--X2
        2: Assembly(
            {'X1': 'X', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'X2': 'X'}, 
            [('X1.a', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'),
             ('M2.b', 'X2.a')]),
        # L1--M1--L2--M2--X1
        3: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'X1': 'X'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'),
             ('M2.b', 'X1.a')]),
        # L1--M1--L2--M2--L3
        4: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'L3': 'L'}, 
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'), 
             ('M2.b', 'L3.a')]),
        }

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        input_path = os.path.join(td, 'input.yaml')
        output_path = os.path.join(td, 'output.yaml')
        wip_dir = os.path.join(td, 'wip')

        with open(input_path, 'w') as f:
            yaml.dump(INPUT_DATA, f)
        
        result = runner.invoke(
            main,
            [
                'enumerate-assemblies',
                str(input_path), str(output_path), 
                '--wip-dir', str(wip_dir), 
                '--overwrite', '--verbose']
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)

        for key, assembly in EXPECTED.items():
            assert is_isomorphic(
                actual_output[key], assembly, 
                INPUT_DATA['component_kinds'])  # type: ignore


def test_enum_bond_subsets(tmp_path):
    runner = CliRunner()

    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3}},
        'sym_ops': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        }
    }

    EXPECTED = {
        0: [1], 1: [2], 2: [1, 2], 3: [2, 3], 4: [1, 2, 3], 5: [1, 2, 3, 4]
    }

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        input_path = os.path.join(td, 'input.yaml')
        output_path = os.path.join(td, 'output.yaml')

        with open(input_path, 'w') as f:
            yaml.safe_dump(INPUT_DATA, f)
        
        result = runner.invoke(
            main,
            ['enumerate-bond-subsets', input_path, output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)

        assert actual_output == EXPECTED


def test_bondsets_to_assemblies(tmp_path):
    runner = CliRunner()

    BONDSETS_DATA = {
        0: [1],
        1: [1, 2],
        2: [2, 3],
        3: [1, 2, 3],
        4: [1, 2, 3, 4]
    }

    STRUCTURE_DATA = {
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

    EXPECTED = {
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

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        bondsets_path = os.path.join(td, 'bondsets.yaml')
        structure_data_path = os.path.join(td, 'structure_data.yaml')
        output_path = os.path.join(td, 'output.yaml')

        with open(bondsets_path, 'w') as f:
            yaml.safe_dump(BONDSETS_DATA, f)

        with open(structure_data_path, 'w') as f:
            yaml.safe_dump(STRUCTURE_DATA, f)

        result = runner.invoke(
            main,
            ['bondsets-to-assemblies', bondsets_path, structure_data_path, 
             output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)
        
        assert actual_output == EXPECTED


if __name__ == '__main__':
    pytest.main(['-v', __file__])
