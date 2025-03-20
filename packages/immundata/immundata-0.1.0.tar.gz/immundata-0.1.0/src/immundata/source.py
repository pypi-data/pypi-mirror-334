import os

import polars as pl
from polars import DataFrame, LazyFrame


# Parser: format -> change columns AIRR-compatible one. Converter - rules for convert columns
# Processors: remove nonproductive sequences, fix genes following the strategy, etc.
# Gene segments: strategy on how to merge together gene segments for clonotypes

# Idea: tra.junction / trb.junction
# Idea: rearrange columns
# Idea: create cdr3.nt, cdr3.aa, etc. columns
# Idea: AnnDataSource, 10xSource, AIRRSource, etc. and Readers (input -> ImmunData) / Annotators for them

# ImmunData: clonotypes ARE ALREADY GROUPED. So you are already working on specific clonotypes with correct counts.
#  Question: what if we want to do some analysis on nucleteotide sequences? Well, create a cdr.nt-based clonotype ImmunData, there is no problem.

# ImmunData: first __getitem__ gets a repertoire, second __getitem__ gets a column like ibis.Table


class BaseSource:
    _format: str

    def __init__(self):
        self._format = ""

    def read(self):
        raise NotImplementedError


class FileSource:
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._format = "airr"

    def read_file(
        self, filename: str, sample_col: str = "sample_id", separator: str = ","
    ) -> DataFrame:
        data_frame = pl.read_csv(filename, separator=separator)
        if sample_col not in data_frame.columns:
            data_frame = data_frame.with_columns(
                sample_id=os.path.splitext(filename)[0]
            )
        else:
            data_frame = data_frame.rename({sample_col: "sample_id"})
        return data_frame

    def combine_tables(self, tables: list[DataFrame | LazyFrame]):
        return pl.concat(tables)

    def process_combined_table(
        self, table: DataFrame | LazyFrame
    ) -> DataFrame | LazyFrame:
        return table

    def validate_data(self, table: DataFrame | LazyFrame):
        required_columns = [
            "sequence_id",
            "v_call",
            "j_call",
            "junction",
            "junction_aa",
            "productive",
            "sample_id",
        ]

        for col in required_columns:
            if col not in table.columns:
                raise ValueError(
                    f"Data does not conform to AIRR format: can't find the column '{col}'"
                )

    def read(self):
        if os.path.isdir(self._path):
            tables = []

            for file in os.listdir(self._path):
                if not file.startswith("."):
                    table = self.read_file(os.path.join(self._path, file))
                    tables.append(table)

            if not tables:
                raise FileNotFoundError(f"No repertoire files found in {self._path}")

            combined_table = pl.concat(tables)

        elif os.path.isfile(self._path):
            combined_table = self.read_file(self._path)

        else:
            raise ValueError(f"{self._path} is neither a file nor a directory")

        combined_table = self.process_combined_table(combined_table)

        self.validate_data(combined_table)

        return combined_table


AIRRSource = FileSource


# class IndexedTenXSource(FileSource):
#     def __init__(self, path: str):
#         super().__init__(path)
#         self._format = "i10x"

#     def read_file(self, filename: str, sample_col: str = "sample_id") -> ibis.Table:
#         table = ibis.read_csv(
#             filename,
#             quote="",
#             delim=" ",
#             header=True,
#             null_padding=True,
#             normalize_names=False,
#         ).rename(lambda x: x.replace('"', ""))

#         table = table.rename(
#             {
#                 table.columns[i]: table.columns[i + 1]
#                 for i in range(len(table.columns) - 1)
#             }
#         )

#         if sample_col not in table.columns:
#             table = table.mutate(sample_id=ibis.Value(os.path.splitext(filename)[0]))
#         else:
#             table = table.rename({"sample_id": sample_col})

#         return table

#     def process_combined_table(self, table: ibis.Table) -> ibis.Table:
#         # Convert 10x format to AIRR format
#         rename_dict = {
#             "sequence_id": "barcode",
#             "v_call": "v_gene",
#             "j_call": "j_gene",
#             "c_call": "c_gene",
#             "junction": "cdr3_nt",
#             "junction_aa": "cdr3",
#             "consensus_count": "umis",
#         }

#         return table.rename(rename_dict)


class MixcrSource(FileSource):
    def __init__(self, path: str):
        super().__init__(path)
        self._format = "mixcr"

    def read_file(self, filename: str, sample_col: str = "Subject id") -> DataFrame:
        return super().read_file(filename, sample_col=sample_col, separator="\t")

    def process_combined_table(
        self, table: DataFrame | LazyFrame
    ) -> DataFrame | LazyFrame:
        rename_dict = {
            "cloneId": "sequence_id",
            "clonalSequence": "sequence",
            "allVHitsWithScore": "v_call",
            "allJHitsWithScore": "j_call",
            "allCHitsWithScore": "c_call",
            "nSeqCDR3": "junction",
            "aaSeqCDR3": "junction_aa",
            "cloneCount": "consensus_count",
        }

        table = table.rename(rename_dict).with_columns(
            productive=pl.col("junction_aa").str.find("*", literal=True) != -1
        )

        return table.with_columns(
            v_call=pl.col("v_call").str.replace_all(r"\(.*?\)", ""),
            j_call=pl.col("j_call").str.replace_all(r"\(.*?\)", ""),
            c_call=pl.col("c_call").str.replace_all(r"\(.*?\)", ""),
        )


# class ImmunarchSource(FileSource):
#     # immunarch format saved from MiXCR files
#     def __init__(self, path: str):
#         super().__init__(path)
#         self._format = "immunarch"

#     def read_file(self, filename: str, sample_col: str = "Sample") -> ibis.Table:
#         return super().read_file(filename, sample_col)

#     def process_combined_table(self, table: ibis.Table) -> ibis.Table:
#         rename_dict = {
#             "sequence_id": "Clone.ID",
#             "sequence": "Sequence",
#             "v_call": "V.name",
#             "j_call": "J.name",
#             "c_call": "D.name",
#             "junction": "CDR3.nt",
#             "junction_aa": "CDR3.aa",
#             "consensus_count": "Clones",
#         }

#         table = table.rename(rename_dict).mutate(
#             productive=(ibis._.junction_aa.find("*") != -1).ifelse(False, True)
#         )

#         return table.mutate(
#             v_call=ibis._.v_call.re_replace(r"\(.*?\)", ""),
#             j_call=ibis._.j_call.re_replace(r"\(.*?\)", ""),
#             c_call=ibis._.c_call.re_replace(r"\(.*?\)", ""),
#         )
