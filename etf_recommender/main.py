from flask import Flask, jsonify, request
import pandas as pd
import numpy as np


# Load the ETF data into a pandas DataFrame
etf_df = pd.read_csv('recommender.csv')

app = Flask(__name__)




def get_top_etfs(etf_df, n=5, weights=None):
    """
    Returns the top-N recommended ETFs based on the given criteria.

    Parameters:
        - etf_df (pandas.DataFrame): The DataFrame containing the ETF data.
        - n (int): The number of ETFs to recommend (default: 5).
        - weights (dict): The weights for each criterion (default: None).
            If None, the default weights will be used.

    Returns:
        A pandas.DataFrame containing the top-N recommended ETFs and their scores.
    """
    print('test')
    # Define the default weights for the criteria
    default_weights = {
        'final_performance': 1,
        'final_risk': -1,
        'final_tracking_error': -1,
        'analytics.expenseRatio': -1
    }

    # Use the default weights if weights is None
    if weights is None:
        weights = default_weights

    criteria_df = etf_df[list(weights.keys())]
    min_criteria = criteria_df.min()
    max_criteria = criteria_df.max()
    norm_criteria_df = (criteria_df - min_criteria)/(max_criteria - min_criteria)
    weight_series = pd.Series(weights)
    scores = norm_criteria_df [list(weights.keys())].dot(weight_series)
    top_etfs = etf_df.loc[scores.nlargest(n).index]
    top_etfs['score'] = scores.nlargest(n).values


    return top_etfs[['legalName', 'fund.fundFamilyName', 'analytics.expenseRatio', 'category','assetClass']]


@app.route('/api/v1/', methods=['POST'])
def etf_recommendations():
    input_json = request.get_json(force=True)
    
    # default values
    region= 'United States'
    sector='Energy' 
    asset_Class='Equity'
    risk_appetite ='low'

    print('data from client:', input_json)

    region = input_json['region'] or ''
    sector = input_json['sector'] or ''
    asset_Class = input_json['asset'] or ''
    risk_appetite = input_json['risk'] or ''
    
    #Filter the ETF data based on user inputs
    filtered_df = etf_df.loc[((etf_df[region]>= 15)& (etf_df[sector]>=15) & (etf_df['assetClass']==asset_Class) & (etf_df['risk_appetite']==risk_appetite)) ].reset_index(drop=True)

    # Define the weights for the criteria
    weights = {
    'final_performance': 2,
    'final_risk': -1,
    'final_tracking_error': -1,
    'analytics.expenseRatio': -2
    }

    # Get the top recommended ETFs
    top_etfs_df = get_top_etfs(filtered_df, weights=weights)

    # Convert the DataFrame to a JSON object and return it
    return jsonify(top_etfs_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/')
# def hello_world():
#     test = {'ETF':'ishares'}
#     return  test
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     app.run()
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

