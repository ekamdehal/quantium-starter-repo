import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

df = pd.read_csv("data/pink_morsels_formatted.csv")
df["Date"] = pd.to_datetime(df["Date"])

daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales"
)

# Add the vertical line WITHOUT annotation_text
fig.add_vline(
    x="2021-01-15",
    line_dash="dash"
)

# Optional separate annotation
fig.add_annotation(
    x="2021-01-15",
    y=daily_sales["Sales"].max(),
    text="Price increase",
    showarrow=True,
    arrowhead=1,
    yshift=10
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)