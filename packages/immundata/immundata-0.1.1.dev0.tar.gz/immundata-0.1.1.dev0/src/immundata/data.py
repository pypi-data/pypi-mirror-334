from typing import Any, Literal, Optional, Sequence, Union

import pandas as pd
import polars as pl
from polars import DataFrame, LazyFrame
from pydantic import BaseModel

from immundata.models import ReceptorSignature


class RepertoireSignature:
    pass


class ImmunMeta_data:
    pass


class ImmunDataSchema:
    receptor: ReceptorSignature

    repertoire: Optional[RepertoireSignature] = None

    meta_data: Optional[ImmunMeta_data] = None

    sample_column: str = "sample_id"

    count_column: str = "consensus_count"

    uid_column: str = "sequence_id"

    def __init__(self, receptor_signature: ReceptorSignature):
        self.receptor = receptor_signature


class ImmunData:
    """
    Checks for the schema
    """

    _data: DataFrame | LazyFrame

    schema: ImmunDataSchema

    def __init__(self, data: DataFrame | LazyFrame, schema: ImmunDataSchema):
        """
        Initializes the ImmunData object.

        Parameters:
            _data (str | pd.DataFrame | ibis.expr.types.Table): The input _data. Can be a file path, pandas DataFrame, or ibis Table.
        """
        self._data = data

        # TODO: This could be an expensive operation in case of LazyFrame
        if "sample_id" not in self._data.collect_schema().names():
            print(self._data.columns)
            raise ValueError("Missing required columns: sample_id.")

        self.schema = schema

        self._samples = None

    ####
    # Operations that preserve the schema contingency
    ####

    def filter(self, *predicates, **constraints) -> "ImmunData":
        # saves state

        # Filter, applied separately to each repertoire
        # – filtering by clonotype
        # – filtering by repertoire name -> immun_data.filter(ibis._.sample_id == "RepertoireName")
        # – filtering by meta_data of repertoires -> immun_data.filter(ibis._.covid_status == "COVID+").group_by("sample_id").count()
        # – filtering by computed statistics of repertoires -> immun_data.filter( ??? ) – как считать на ходу характеристики?
        return self.__class__(
            data=self._data.filter(*predicates, **constraints),
            schema=self.schema,
        )

    def head(self, n: int = 5) -> "ImmunData":
        return self.__class__(data=self.data.head(n=n), schema=self.schema)

    def top_receptors(self, n: int = 10) -> "ImmunData":
        return self.__class__(
            data=self.data.sort(
                by=pl.col(self.schema.count_column), descending=True
            ).head(n=n),
            schema=self.schema,
        )

    def __getitem__(self, samples: str | list[str]) -> "ImmunData":
        # Select a specific sample
        if isinstance(samples, str):
            samples = [samples]
        return self.filter(pl.col(self.schema.sample_column).is_in(samples))

    ## join / concat operations - bringing together ImmunData with other data sources

    ## if paired chain, get an ImmunData for only one chain; also get a schema/list of all chains, and easier access to get chains

    ####
    # Access for the underlying data for more complex operations
    ####

    @property
    def data(self) -> DataFrame | LazyFrame:
        return self._data

    @data.setter
    def data(self, new_value: Any):
        raise AttributeError(
            "ImmunData error: assignment to `data` is forbidden as it breaks the immutability property."
        )

    ####
    # Data frame supporting operations
    ####

    def count(self) -> DataFrame | LazyFrame:
        return self._data.count()

    def collect(self, **kwargs) -> DataFrame:
        return self._data.collect(**kwargs)

    # len

    def to_pandas(self, **kwargs) -> pd.DataFrame:
        return self._data.collect(**kwargs).to_pandas()

    ####
    # ImmunData support functions
    ####

    def unique_receptors(
        self, count: bool = False, uid: bool = False, sample: bool = False
    ) -> DataFrame | LazyFrame:
        # Three building blocks:
        # 1) clonotype columns - sequences + genes
        # 2) clonotype counts
        # 3) clonotype IDs
        columns_to_select = list(self.schema.receptor.columns())

        if count:
            columns_to_select.append(self.schema.count_column)

        if uid:
            columns_to_select.append(self.schema.uid_column)

        if sample:
            columns_to_select.append(self.schema.sample_column)

        return self.data.select(columns_to_select)

    @property
    def samples(self) -> list[str]:
        if self._samples is None:
            self._samples = (
                self.data.select(self.schema.sample_column)
                .unique()
                .collect()
                .to_numpy()
                .flatten()
                .tolist()
            )
        return self._samples

    @samples.setter
    def samples(self, new_value: Any):
        raise AttributeError(
            "ImmunData error: assignment to samples` is forbidden as samples are computed internally and strictly follow the data schema."
        )

    # @property
    # def v_call(self) -> ibis.Table:
    #     return self._data.v_call

    # @property
    # def d_call(self) -> ibis.Table:
    #     return self._data.v_call

    # @property
    # def j_call(self) -> ibis.Table:
    #     return self._data.v_call

    @property
    def columns(self) -> list[str]:
        return self._data.columns
