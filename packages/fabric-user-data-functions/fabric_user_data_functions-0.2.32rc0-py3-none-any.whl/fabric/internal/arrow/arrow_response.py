# flake8: noqa: I005
# import azure.functions as func
# import pyarrow as pa
# import pandas as pd

# class arrow_response():

#     def __init__(self, df: pd.DataFrame):
#         self._df = df

#     def to_bytes(self) -> bytes:
#         sink = pa.BufferOutputStream()
#         batch_arrow = pa.RecordBatch.from_pandas(self._df)
#         writer = pa.ipc.new_stream(sink, batch_arrow.schema)
#         writer.write_batch(batch_arrow)
#         writer.close()
#         return sink.getvalue().to_pybytes()