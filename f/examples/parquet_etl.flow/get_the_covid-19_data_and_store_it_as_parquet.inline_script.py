import pandas as pd
import pathlib
import fastparquet

def main():
  nytimes = pd.read_csv(
      'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv',
      index_col=['date'], parse_dates=['date']).asfreq(freq='D')

  # Transform: add new columns with useful transformations
  nytimes['new_cases'] = nytimes['cases'].diff()
  nytimes['new_cases_ma7'] = nytimes['new_cases'].rolling(7).mean()

  anomalous_dates = ['2020-09-21', '2020-11-26', '2020-12-11', '2020-12-25']
  nytimes['anomaly'] = False
  nytimes.loc[anomalous_dates, 'anomaly'] = True

  nytimes_path = pathlib.Path('./shared/nytimes')
  nytimes_path.mkdir(parents=True, exist_ok=True)
  path = nytimes_path / 'us.parquet'
  nytimes.to_parquet(path)
  return path