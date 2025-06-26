import requests
from datetime import datetime, timezone

def get_power_consumption(
        TIBBER_TOKEN,
        HOME_ID,
        from_date,
        to_date
):
    charge_log_init = []

    from_date = datetime.strptime(from_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    to_date = datetime.strptime(to_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    difference = now - from_date
    hours_ago = round(difference.total_seconds() / 3600)+24

    print("hours ago:",hours_ago)

    query = f"""
        {{
        viewer {{
            home(id: "{HOME_ID}") {{
            consumption(resolution: HOURLY, last: {hours_ago}) {{
                nodes {{
                from
                to
                consumption
                cost
                unitPrice
                unitPriceVAT
                currency
                }}
            }}
            }}
        }}
        }}
    """

    response = requests.post(
        "https://api.tibber.com/v1-beta/gql",
        headers={"Authorization": f"Bearer {TIBBER_TOKEN}"},
        json={"query": query}
    )

    data = response.json()

    consumption_data = data["data"]["viewer"]["home"]["consumption"]["nodes"]
    
    return_data = []

    for entry in consumption_data:
        timestamp = datetime.fromisoformat(entry["from"])
        timestamp = timestamp.astimezone(timezone.utc)
        tmp_data = {
            'stamp': timestamp,
            'consumption': entry['consumption'],
            'cost': entry['cost'],
            'price_kwh': entry['unitPrice']
        }
        if from_date <= timestamp and timestamp <= to_date: 
            return_data.append(tmp_data)
            charge_log_init.append({
                'stamp': timestamp,
                'charge': 0,
                'added_charge': 0,
                'price_kwh': entry['unitPrice']
            })
    return return_data, charge_log_init
