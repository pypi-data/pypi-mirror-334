import itertools
from collections import defaultdict
from collections.abc import Iterator, Mapping

from recsa import (Assembly, Component, InterReaction, IntraReaction,
                   calc_graph_hash_of_assembly)
from recsa.algorithms.hashing import calc_graph_hash_of_assembly

from .inter import explore_inter_reactions
from .intra import explore_intra_reactions


def explore_reactions(
        id_to_assembly: Mapping[int, Assembly],
        metal_kind: str, leaving_kind: str, entering_kind: str,
        component_structures: Mapping[str, Component],
        ) -> Iterator[IntraReaction | InterReaction]:
    hash_to_ids = defaultdict(list)
    for assem_id, assembly in id_to_assembly.items():
        hash_ = calc_graph_hash_of_assembly(assembly, component_structures)
        hash_to_ids[hash_].append(assem_id)
    
    # Intra-molecular ligand exchange
    for assem_id in id_to_assembly.keys():
        yield from explore_intra_reactions(
            assem_id, metal_kind, leaving_kind, entering_kind,
            id_to_assembly, hash_to_ids, component_structures)
    
    # Inter-molecular ligand exchange
    for init_assem_id, entering_assem_id in itertools.product(
            id_to_assembly.keys(), repeat=2):
        yield from explore_inter_reactions(
            init_assem_id, entering_assem_id, 
            metal_kind, leaving_kind, entering_kind,
            id_to_assembly, hash_to_ids, component_structures)
