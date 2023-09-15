# pyreaddbc

**pyreaddbc** is a Python library for working with [DBase database file](https://docs.fileformat.com/database/dbf/). Legacy systems from the Brazilian Ministry of Health still uses DBF and DBC formats to Publicize data. This package was developed to help [PySUS](https://github.com/AlertaDengue/pysus) to extract data from these formats to more modern ones. Pyreaddbc can also be used to convert DBC files from any other source.


## Installation

You can install **pyreaddbc** using pip:

```bash
pip install pyreaddbc
```

## Usage

**Note**: *Extracting the DBF from a DBC may require to specify the encoding of the original data, if known.*

### Reading DBC Files

To read a DBC file and convert it to a pandas DataFrame, use the `read_dbc` function:

```python
import pyreaddbc

dfs = pyreaddbc.read_dbc("LTPI2201.dbc", encoding="iso-8859-1")
```

### Exporting to CSV.GZ

To export a DataFrame to a compressed CSV file (CSV.GZ), you can use pandas:

```python
import pyreaddbc

df = pyreaddbc.read_dbc("./LTPI2201.dbc", encoding="iso-8859-1")
df.to_csv("LTPI2201.csv.gz", compression="gzip", index=False)
```

### Exporting to Parquet

To export a DataFrame to a Parquet file, you can use the `pyarrow` library:

```python
import pyreaddbc
import pyarrow.parquet as pq
import pandas as pd
from pathlib import Path

# Read DBC file and convert to DataFrame
df = pyreaddbc.read_dbc("./LTPI2201.dbc", encoding="iso-8859-1")

# Export to CSV.GZ
df.to_csv("LTPI2201.csv.gz", compression="gzip", index=False)

# Export to Parquet
pq.write_table(pa.Table.from_pandas(df), "parquets/LTPI2201.parquet")

# Read the Parquet files and decode DataFrame columns
parquet_dir = Path("parquets")
parquets = parquet_dir.glob("*.parquet")

chunks_list = [
    pd.read_parquet(str(f), engine='fastparquet') for f in parquets
]

# Concatenate DataFrames
df_parquet = pd.concat(chunks_list, ignore_index=True)

```
---

## License

[GNU Affero General Public License (AGPL-3.0)](./LICENSE)

This license ensures that the software remains open-source and free to use, modify, and distribute while requiring that any changes or enhancements made to the codebase are also made available to the community under the same terms.

<span>
<b>Acknowledge</b></br>
============
</span> 

    
This program decompresses .dbc files to .dbf. This code is based on the work
of Mark Adler <madler@alumni.caltech.edu> (zlib/blast), Pablo Fonseca
(https://github.com/eaglebh/blast-dbf).

[PySUS](https://github.com/AlertaDengue/PySUS) has further extended and adapted this code to
create **pyreaddbc**. The original work of Mark Adler and Pablo Fonseca is much appreciated for its contribution to this project.

**Note**: *pyreaddbc* is maintained with funding from [AlertaDengue](https://github.com/AlertaDengue).
