from immundata.data import ImmunData, ImmunDataSchema
from immundata.models import ReceptorSignature
from immundata.source import BaseSource


class ImmunDataReader:
    def __init__(self, source: BaseSource):
        """
        Initializes the ImmunDataReader with a BaseSource object.

        Parameters:
            source (BaseSource): The data source to read from (e.g., AIRRSource, TenXSource).
        """
        self._source = source

    def read(self, clonotype_model: list[str]) -> ImmunData:
        """
        Reads the data from the source and returns an ImmunData object.

        Parameters:
            clonotype_model (List[str]): List of columns to use for clonotype definition.

        Returns:
            ImmunData: The ImmunData object containing the processed data.
        """
        # Read data from the source
        data_frame = self._source.read().lazy()

        # Create and return ImmunData object
        return ImmunData(
            data=data_frame,
            schema=ImmunDataSchema(
                receptor_signature=ReceptorSignature(clonotype_model)
            ),
        )

    def annotate_source(
        self, data: ImmunData, data_col: list[str], target_col: list[str]
    ) -> ImmunData:
        """
        Annotates the ImmunData object with additional information.

        Parameters:
            data (ImmunData): The ImmunData object to annotate.
            data_col (List[str]): List of columns to use as source for annotation.
            target_col (List[str]): List of columns to create with the annotation.

        Returns:
            ImmunData: The annotated ImmunData object.
        """
        assert len(data_col) == len(target_col), (
            "data_col and target_col must have the same length"
        )

        # Implement annotation logic here
        # This is a placeholder - you'll need to implement the actual annotation logic
        # based on your specific requirements
        for source, target in zip(data_col, target_col):
            data.data = data.data.mutate(**{target: data.data[source]})

        return data
