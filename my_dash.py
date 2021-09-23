import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


output = []
#here you can define your logic on how many times you want to loop
data = pd.read_csv("mock_data_wm.csv", parse_dates=["CONTAINER_DATE", "CONTAINER_DONE"])
df = data.copy() # copy of data
days = (df["CONTAINER_DONE"].max() - df["CONTAINER_DONE"].min()).days
#print(f"Number of days worth of service in dataset : {days}")
# ### Univariate Analysis
counter = 1
# #### Categorical Columns 
for column in df.select_dtypes("object").columns: # bar plots on categorical data
    vc = df[column].value_counts(normalize=True)
    if vc.count() > 1 and vc.count() < 5:
        #plt.figure()
        new_df = pd.DataFrame({'FuncGroup':vc.index, 'Count':vc.values})
        output.append(dcc.Graph(id='plotly_graph'+str(counter),figure={'data': [go.Bar(x=new_df['Count'],y=new_df['FuncGroup'],name="yaxis",orientation='h')]}))
        counter += 1

qty_ts = df[["QUANTITY", "CONTAINER_DATE"]].copy()
print(qty_ts.head())
qty_ts.sort_values(by="CONTAINER_DATE", inplace=True)
qty_ts.set_index("CONTAINER_DATE", inplace=True)

qty_ts = pd.pivot_table(qty_ts, values=["QUANTITY"], index=["CONTAINER_DATE"], aggfunc="sum")#.plot(figsize=(20,10))
new_df = pd.DataFrame(qty_ts.to_records())
print(new_df)



print(f"Total quantity served : {int(qty_ts.sum().values[0])}")
print(qty_ts)


print(f"Total days served : {qty_ts.count().values[0]}")

output.append(dcc.Graph(id='univariate_plotly_graph',figure={'data': [go.Scatter(x=new_df['CONTAINER_DATE'],y=new_df['QUANTITY'],name="lines",mode='lines')]}))
# data_canada = new_df
# fig = px.bar(data_canada, x='CONTAINER_DATE', y='QUANTITY')
# fig.show()
output.append(dcc.Graph(id='univariate_plotly_graph2',figure={'data': [go.Bar(x=new_df['CONTAINER_DATE'],y=new_df['QUANTITY'])]}))

# ### Bi-variate Analysis 

# #### SUBLOB vs EVENT 
data = []
for w,v in df.groupby('SUBLOB'):
    print(w)
    for xx in v.EVENT.unique():
        data_f = v[v["EVENT"] == xx]
        print(data_f.head())
        print('###############################################################')
        trace = go.Bar(x=data_f["SUBLOB"], y=[data_f["EVENT"].shape[0]], name = xx)
        data.append(trace)
output.append(dcc.Graph(id='Bivariate_plotly_graph1',figure={'data': data}))

# ### SERVICE_STATUS vs SUBLOB
data = []
for w,v in df.groupby('SERVICE_STATUS'):
    print(w)
    for xx in v.SUBLOB.unique():
        data_f = v[v["SUBLOB"] == xx]
        print(data_f.head())
        print('###############################################################')
        trace = go.Bar(x=data_f["SERVICE_STATUS"], y=[data_f["SUBLOB"].shape[0]], name = xx)
        data.append(trace)
output.append(dcc.Graph(id='Bivariate_plotly_graph2',figure={'data': data}))

# #### Top 10 Customers serviced interms of Trash/Waste Quantity
'''
pt = pd.pivot_table(df, values=["QUANTITY"], index=["CUSTOMER_UNIQUEID"], aggfunc="sum").sort_values("QUANTITY", ascending=False).head(10)
data_f = pd.DataFrame(pt.to_records())
#data_f['CUSTOMER_UNIQUEID'] = (pd.Categorical(data_f.CUSTOMER_UNIQUEID))
data_f['CUSTOMER_UNIQUEID'] = data_f['CUSTOMER_UNIQUEID'].astype('category')
print(data_f)
output.append(dcc.Graph(id='bivariate_3',figure={'data': [go.Bar(x=data_f['CUSTOMER_UNIQUEID'],y=data_f['QUANTITY'])]}))
'''

app.layout = html.Div(children=output)
if __name__ == '__main__':
    app.run_server(debug=True)