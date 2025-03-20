import os

import pytest
import yaml
from click.testing import CliRunner

from recsa.cli.commands import run_enum_bond_subsets_pipeline


def test_cli_command_a(tmp_path):
    runner = CliRunner()

    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'bond_adjacency': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3},
        },
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
            run_enum_bond_subsets_pipeline,
            [input_path, output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)

        assert actual_output == EXPECTED


if __name__ == '__main__':
    pytest.main(['-v', __file__])
