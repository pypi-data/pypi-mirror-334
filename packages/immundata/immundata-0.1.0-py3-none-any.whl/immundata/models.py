from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel

# Get unique values / categories for a column
# Receptor type in Enum for rows

# DataManipulationInterface
# InputOutputInterface
# BasicAnalysisInterface
# SequenceSimilarityInterface

# 1) compute statistics over all or some repertoires, maybe merge results afterwards
# -> agg by repertoire/clonotype model -> do stuff
# 2) compare several or all pairwise repertoires
# -> agg by repertoire/clonotype -> apply pairwise functions or iterate over
# -> step by step select each pair of repertoires and do stuff over them

# repertoire-level/clonotype-level stats - this just means different grouping usuall, and different target
# we either get a stats from a repertoire, or focus on sequences and get sequence-level stats


# Clonotype aggregation / repertoire aggregation / cell metadata aggregation strategies


@dataclass
class Columns:
    barcode: str = "sequence_id"
    cdr3_nt: str = "junction"


fr_names = Literal["fr1", "fr2", "fr3", "fr4"]
cdr_names = Literal["cdr1", "cdr2", "cdr3"]
gene_names = Literal["v_call", "j_call", "d_call", "c_call"]


class ReceptorSignature:
    # fr: dict[framework_names, bool]
    # cdr: dict[cdr_names, bool]
    # gene: dict[gene_names, bool]
    # chain: list[str]

    def __init__(self, clonotype_model_columns: list[str]):
        self._columns = tuple(clonotype_model_columns)

    # def __init__(self, cdr, gene, fr):

    def columns(self) -> tuple[str]:
        return self._columns

    # v -> tuple[str]

    # chain -> tuple[ReceptorSignature]
