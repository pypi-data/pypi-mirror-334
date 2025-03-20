# import pandas as pd
#
#
# def identify_seasons(lightcurve_df, time_col, min_gap=40):
#     """
#     Identify seasons in a time series DataFrame.
#
#     Parameters:
#     lightcurve_df (pd.DataFrame): The DataFrame containing the time series.
#     time_col (str): Column name of the time series.
#     min_gap (int): Minimum gap (in days) to separate seasons.
#
#     Returns:
#     list of tuples: Each tuple contains (season_start, season_end).
#     """
#
#     # Ensure the DataFrame is sorted by time
#     lightcurves_from_nn_df = lightcurve_df.sort_values(by=time_col).reset_index(drop=True)
#
#     # Compute time differences
#     lightcurves_from_nn_df['time_diff'] = lightcurves_from_nn_df[time_col].diff()
#
#     # Identify season starts (first time point + where the gap is at least `min_gap`)
#     season_starts = [lightcurves_from_nn_df[time_col].iloc[0]]  # First timestamp is always a season start
#     for i in range(1, len(lightcurves_from_nn_df)):
#         if lightcurves_from_nn_df['time_diff'].iloc[i] >= min_gap:
#             season_starts.append(lightcurves_from_nn_df[time_col].iloc[i])  # New season start
#
#     # Define season intervals by finding the actual last data point before the next season
#     season_intervals = []
#     for i in range(len(season_starts) - 1):
#         # Find the last point before the next season starts
#         end_index = lightcurves_from_nn_df[lightcurves_from_nn_df[time_col] < season_starts[i + 1]].index[-1]
#         season_intervals.append((season_starts[i], lightcurves_from_nn_df[time_col].iloc[end_index]))
#
#     # Last season goes until the final available data point
#     season_intervals.append((season_starts[-1], lightcurves_from_nn_df[time_col].iloc[-1]))
#
#     return season_intervals
#
#
# def find_season_bounds(lightcurves_dfs, time_col, min_gap=40):
#     """
#     For each light curve DataFrame, identify the smallest starting data point
#     and the greatest ending data point for every season.
#
#     Parameters:
#     lightcurves_dfs (list of pd.DataFrame): List of light curve DataFrames.
#     time_col (str): Column name of the time series in each DataFrame.
#     min_gap (float): Minimum gap between seasons.
#
#     Returns:
#     pd.DataFrame: A DataFrame with columns for the smallest start and greatest end times for each season.
#     """
#     season_bounds = []
#
#     # Loop through each light curve DataFrame
#     for idx, lightcurves_from_nn_df in enumerate(lightcurves_dfs):
#         # Apply the identify_seasons function
#         seasons = identify_seasons(lightcurves_from_nn_df, time_col, min_gap)
#
#         for season_start, season_end in seasons:
#             # Collect the season bounds
#             season_bounds.append({
#                 'lightcurve_id': idx,  # Identify the light curve (or event_name)
#                 'season_start': season_start,
#                 'season_end': season_end,
#             })
#
#     # Convert the results to a DataFrame
#     bounds_df = pd.DataFrame(season_bounds)
#
#     # Find the smallest start and greatest end across all seasons
#     season_summary = bounds_df.groupby('lightcurve_id').agg(
#         smallest_start=('season_start', 'min'),
#         greatest_end=('season_end', 'max')
#     ).reset_index()
#
#     return season_summary
#
#
# # Example usage
#
# lc_df = pd.read_feather('/Users/stela/Documents/Scripts/ai_microlensing/merida/data/gb1-R-1-1-315.feather')
#
# seasons = identify_seasons(lc_df, 'HJD')
# modified_bounds = [(start - 10, end + 10) for start, end in seasons]
#
# # season_summary = find_season_bounds()
# print(seasons)
# print(modified_bounds)

seasons_intervals = {'2006': (3810.0, 4070.0),
                     '2007': (4120.0, 4430.0),
                     '2008': (4480.0, 4800.0),
                     '2009': (4840.0, 5160.0),
                     '2010': (5210.0, 5530.0),
                     '2011': (5580.0, 5890.0),
                     '2012': (5940.0, 6260.0),
                     '2013': (6310.0, 6620.0),
                     '2014': (6670.0, 6980.0)}
#
peaks = [6425.0, 3931.0, 3892.0, 4656.0, 3930.0, 4735.0,
         5428.0, 6021.0, 4240.0, 3976.0, 4080.0, 4550.0, 4213.0,
         6063.0, 4644.0, 5810.0, 4523.0, 6892.0, 5490.0, 5806.0, 5090.0,
         6899.0, 6600.0, 3937.0, 6501.0, 6020.0, 6585.0, 6455.0, 6424.0,
         4650.0, 5090.0, 6532.0, 6096.0, 5705.0, 4635.0, 4697.0, 6451.0,
         6048.0, 4591.0, 6526.0, 6111.0, 5311.0, 5364.0, 4015.0, 5318.0,
         6054.0, 6891.0,]
#
# peaks =[4080.0, ]

# Find the season for each peak
peak_seasons = {}
for peak in peaks:
    for season, (start, end) in seasons_intervals.items():
        if start <= peak <= end:
            peak_seasons[peak] = season
            break

print()
# print(peak_seasons)
for key, value in peak_seasons.items():
    print(f"{key}: {value}")