# flake8: noqa: I005

# import azure.functions as func
# import pyarrow as pa
# import tracemalloc
# import pandas as pd

# class arrow_request():

#     def __init__(self, req: func.HttpRequest):
#         self._body = req.get_body()

#     def to_dataframe(self) -> pd.DataFrame:
#         reader = pa.ipc.open_stream(self._body)  # Use the buffer here
#         table = reader.read_all()
#         return table.to_pandas()