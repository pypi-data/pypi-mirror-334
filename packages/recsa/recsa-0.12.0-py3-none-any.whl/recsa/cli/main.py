import click

from recsa.cli.commands import (run_bondsets_to_assemblies_pipeline,
                                run_concat_assembly_lists_pipeline,
                                run_enum_assemblies_pipeline,
                                run_enum_bond_subsets_pipeline)


@click.group()
def main():
    """RECSA CLI"""
    pass

main.add_command(run_enum_bond_subsets_pipeline)
main.add_command(run_concat_assembly_lists_pipeline)
main.add_command(run_bondsets_to_assemblies_pipeline)
main.add_command(run_enum_assemblies_pipeline)

if __name__ == '__main__':
    main()
