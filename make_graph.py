import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timezone, timedelta

def make_consumption_graph(
    data_dict, 
    charge_frames, 
    charge_log,
    show_battery
):

    df = pd.DataFrame(data_dict)
    df_2 = pd.DataFrame(charge_log)

    # Convert to a DataFrame if needed
    highlight_shapes = []

    for interval in charge_frames:
        start = interval["start"]
        end = interval["end"]

        # Add a 15-minute buffer to avoid zero-width shapes
        if start == end:
            end += timedelta(minutes=15)

        shape = {
            "type": "rect",
            "xref": "x",
            "yref": "paper",
            "x0": start,
            "x1": end,
            "y0": 0,
            "y1": 1,
            "fillcolor": "lightgreen",
            "opacity": 0.3,
            "layer": "below",
            "line": {"width": 0},
        }
        highlight_shapes.append(shape)

    # Create the plot
    fig = go.Figure()

    # Consumption as bar
    fig.add_trace(go.Bar(
        x=df["stamp"],
        y=df["consumption"],
        name="Consumption (kWh)",
        yaxis="y1"
    ))

    if show_battery:
        fig.add_trace(go.Bar(
            x=df_2["stamp"],
            y=df_2["added_charge"],
            name="load (kW)",
            yaxis="y1"
        ))

    # Price as line
    fig.add_trace(go.Scatter(
        x=df["stamp"],
        y=df["price_kwh"],
        mode="lines+markers",
        name="Price (€/kWh)",
        yaxis="y2"
    ))

    # battery charge as line
    if show_battery:
        fig.add_trace(go.Scatter(
            x=df_2["stamp"],
            y=df_2["charge"],
            mode="lines+markers",
            name="Battery Level (Kw)",
            yaxis="y1"
        ))

    # Add background shapes
    fig.update_layout(
        shapes=highlight_shapes,
        title="Electricity Data with Highlighted Time Ranges",
        xaxis=dict(title="Timestamp"),
        yaxis=dict(title="Consumption (kWh)", side="left"),
        yaxis2=dict(title="Price (€/kWh)", overlaying="y", side="right"),
        #yaxis3=dict(title="Charge (W)", overlaying="y", side="right"),
        legend=dict(x=0.01, y=0.99),
        bargap=0.2
    )

    fig.show()