import matplotlib.pyplot as plt
import pandas as pd
import fastparquet
import base64

def main(path: str):
  fig, ax = plt.subplots(figsize=(15, 6), dpi=200)

  # Colors
  normal_color = '#cf1111'
  anomaly_color = '#ffe4ad'

  # Subset our data for plotting, and separate into normal and anomalous
  to_plot = pd.read_parquet(
      path,
      columns=['new_cases', 'new_cases_ma7', 'anomaly']).loc['2020-03':]
  normal = to_plot.query('not anomaly')
  anomalous = to_plot.query('anomaly')

  # Add new cases rolling average and annotation
  to_plot['new_cases_ma7'].plot(color=normal_color, ax=ax)

  label_date = '2020-07-26'
  ax.annotate('7-day\naverage',
              xy=(label_date, to_plot['new_cases_ma7'].loc[label_date]),
              xytext=(0, 16), textcoords='offset points',
              horizontalalignment='center',
              arrowprops=dict(arrowstyle="-"),
              color=normal_color)

  # Add new cases bar plot and annotation
  ax.bar(normal.index, normal['new_cases'], width=0.6, color=normal_color,
        alpha=0.3)
  ax.bar(anomalous.index, anomalous['new_cases'], width=0.6, color=anomaly_color)

  label_date = normal.index[normal.new_cases.argmax()]
  ax.annotate('New\ncases',
              xy=(label_date, to_plot['new_cases'].loc[label_date]),
              xytext=(-20, 0), textcoords='offset points',
              horizontalalignment='right',
              verticalalignment='center',
              arrowprops=dict(arrowstyle="-"),
              color=normal_color)

  # Add and annotate horizontal grid lines
  ax.hlines(100_000, to_plot.index[0], to_plot.index[-1], color='lightgray',
            linestyle='--', linewidth=1)
  ax.hlines(200_000, to_plot.index[0], to_plot.index[-1], color='lightgray',
            linestyle='--', linewidth=1)

  ax.annotate('200,000 cases',
              xy=('2020-03-01', 200_000),
              xytext=(0, 5), textcoords='offset points',
              fontsize='large', color='gray')
  ax.annotate('100,000',
              xy=('2020-03-01', 100_000),
              xytext=(0, 5), textcoords='offset points',
              fontsize='large', color='gray')

  # Styling
  [ax.spines[spine].set_visible(False)
  for spine in ['top', 'right', 'bottom', 'left']]
  ax.yaxis.set_ticks([])
  ax.minorticks_off()
  ax.set_xlabel('');
  plt.savefig('out.png')
  with open('out.png', "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('ascii')

  return {"png": encoded_string}
