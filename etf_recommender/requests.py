import requests as req

# Mock user input
params = {
    'region': 'United States',
    'sector': 'Technology',
    'assetClass': 'Equity',
    'risk_appetite':'low'
}


# Send a GET request to the API endpoint with the mock user input
response = req.get('http://127.0.0.1:5000', params=params)

# Print the top recommended ETFs
print(response.json())
# def filter_etfs(etf_df, region=None, sector=None, asset_type=None, risk=None):
#     """
#     Filters the ETFs based on the given criteria.
#
#     Parameters:
#         - etf_df (pandas.DataFrame): The DataFrame containing the ETF data.
#         - region (str): The region to filter by (default: None).
#         - sector (str): The sector to filter by (default: None).
#         - asset_type (str): The asset type to filter by (default: None).
#
#     Returns:
#         A pandas.DataFrame containing the ETFs that match the criteria.
#     """
#     # Apply the filters if provided
#     etf_df = etf_df.loc[((etf_df[region]>= 15)& (etf_df[sector]>=15) & (etf_df['assetClass']==asset_type) & (etf_df['risk_appetite']==risk)) ].reset_index(drop=True)
#
#     return etf_df

# def recommend_etfs():
#     # Get the filter criteria from the request body
#     filter_criteria = request.json
#
#     # Filter the ETFs based on the criteria
#     filtered_etfs = filter_etfs(etf_df, **filter_criteria)
#
#     # Get the top 5 recommended ETFs
#     top_etfs_df = get_top_etfs(filtered_etfs)
#
#     # Convert the DataFrame to JSON
#     top_etfs_json = top_etfs_df.to_json(orient='records')
#
#     # Return the JSON response
#     return jsonify(top_etfs_json)