import ibis

# from immundata.data import ImmunData


# class GroupedImmunData:
#     def __init__(self, grouped_table: ibis.GroupedTable):
#         """
#         Initializes the GroupedImmunData object.

#         Parameters:
#             grouped_table (ibis.expr.types.GroupedTable): The grouped table expression.
#         """
#         self.grouped_table = grouped_table

#     def aggregate(self, metrics: dict[str, ibis.expr.types.ValueExpr]) -> ImmunData:
#         """
#         Performs aggregation on the grouped table.

#         Parameters:
#             metrics (dict): Dictionary mapping metric names to aggregation expressions.

#         Returns:
#             ImmunData: An ImmunData instance with aggregated results.
#         """
#         aggregated_table = self.grouped_table.aggregate(**metrics)
#         return ImmunData(aggregated_table)

#     def having(
#         self,
#         predicates: list[ibis.expr.types.BooleanValue] | ibis.expr.types.BooleanValue,
#     ) -> "GroupedImmunData":
#         """
#         Applies a filter condition on aggregated data.

#         Parameters:
#             predicates (list | ibis.expr.types.BooleanValue): Boolean expressions to filter the aggregated results.

#         Returns:
#             GroupedImmunData: A new GroupedImmunData instance with filtered groups.
#         """
#         having_grouped = self.grouped_table.having(predicates)
#         return GroupedImmunData(having_grouped)

#     def mutate(
#         self, mutations: dict[str, ibis.expr.types.ValueExpr]
#     ) -> "GroupedImmunData":
#         """
#         Adds or modifies columns within the grouped table.

#         Parameters:
#             mutations (dict): Dictionary mapping new column names to expressions.

#         Returns:
#             GroupedImmunData: A new GroupedImmunData instance with mutated columns.
#         """
#         mutated_grouped = self.grouped_table.mutate(**mutations)
#         return GroupedImmunData(mutated_grouped)
