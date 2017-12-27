from classification import * 

# start by importing the file
df = pd.read_csv("~/Desktop/oraculo/petr4_feat.csv", index_col="Date",na_values="nan", parse_dates=True)

# separate into X and y
X,y = get_xy(df)

# evaluate features
# evaluate_features(X,y)

pprint(evaluate_prediction_power(df, 30)) 
