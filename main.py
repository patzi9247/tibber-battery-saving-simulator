from dotenv import load_dotenv
import os
from get_home_id import get_home_id
from get_power_consumption import get_power_consumption
from make_graph import make_consumption_graph
from find_timeframes import get_price_order_in_frame, find_frame_with_high_power_draw

def simulate_battery(
        TIBBER_TOKEN,
        start_date,
        end_date,
        charge_threshold,
        capacity,
        current_charge,
        load_per_hour,
        deload_per_hour,
        display_graph
):

    home_base_data = get_home_id(TIBBER_TOKEN)

    consumption_data, charge_log = get_power_consumption(
        TIBBER_TOKEN, 
        home_base_data[0]['home_id'],
        start_date,
        end_date
        )

    # find charge marker (points below threshold)
    start_charge = True
    charge_frames = []
    frame = {
        'start': None,
        'end': None
    }

    # TODO: calc charge_threshold for each day as local minimum
    # #charge points = capacity/load_per_hour
    # OR
    # start with 0.15 cent if you dont find 3 points increase by one cent
    for entry in consumption_data:
        if entry['price_kwh'] <= charge_threshold and start_charge:
            frame['start'] = entry['stamp']
            start_charge = False
        if entry['price_kwh'] >= charge_threshold and not start_charge:
            frame['end'] = entry['stamp']
            charge_frames.append(frame)
            start_charge = True
            frame = {
                'start': None,
                'end': None
            }

    # order the price by frame & load battery at the lowest points
    for f in charge_frames:
        f['price_list'] = get_price_order_in_frame(f, consumption_data)
        i = 0
        while current_charge < capacity and i < len(f['price_list']):
            price_item = f['price_list'][i]
            # print("charge", current_charge, price_item['stamp'])
            added_charge = load_per_hour
            if current_charge + added_charge > capacity:
                added_charge = capacity - current_charge
            current_charge = current_charge + added_charge
            log_entry = next((item for item in charge_log if item["stamp"] == price_item['stamp']), None)
            log_entry['added_charge'] = added_charge
            log_entry['price_kwh'] = price_item['price_kwh']
            i += 1

        # get the times where we need the power from the battery
        high_power_draw = find_frame_with_high_power_draw(
            f,
            charge_frames,
            consumption_data
        )
        i = 0
        while current_charge > 0 and i < len(high_power_draw):
            current_power_draw_frame = high_power_draw[i]
            # print("decharge", current_charge, current_power_draw_frame['stamp'])
            added_charge = -1 * current_power_draw_frame['consumption']
            if current_charge + added_charge < 0:
                added_charge = -1 * current_charge
            if added_charge < deload_per_hour:
                added_charge = deload_per_hour
            current_charge = current_charge + added_charge
            log_entry = next((item for item in charge_log if item["stamp"] == current_power_draw_frame['stamp']), None)
            log_entry['added_charge'] = added_charge
            log_entry['price_kwh'] = current_power_draw_frame['price_kwh']
            i += 1

    # calc charge in the charge_log from the added charges
    c = 0
    for l in charge_log:
        l['charge'] = c + l['added_charge']
        c = l['charge']

    if display_graph:
        make_consumption_graph(
            consumption_data, 
            charge_frames, 
            charge_log,
            False
        )

    # calc new consumption
    new_consumption_data = []
    old_price = 0
    new_price = 0
    for c in consumption_data:
        c_copy = c.copy()
        log_entry = next((item for item in charge_log if item["stamp"] == c['stamp']), None)
        c_copy['consumption'] = c['consumption'] + log_entry['added_charge']
        c_copy['cost'] = c_copy['consumption'] * c['price_kwh']
        new_consumption_data.append(c_copy)
        old_price = c['cost'] + old_price
        new_price = c_copy['cost'] + new_price

    if display_graph:
        make_consumption_graph(
            new_consumption_data, 
            charge_frames, 
            charge_log,
            True
        )

    print(start_date)
    print(end_date)
    print("threshold", charge_threshold, "€")
    print("capacity", capacity, "kWh")
    print("load_per_hour", load_per_hour, "KW")

    print("old_price:", old_price)
    print("new_price:", new_price)
    print("saved", old_price - new_price)
    return old_price, new_price

if __name__ == "__main__":

    load_dotenv()

    # -------------------------------------------------------------------
    TIBBER_TOKEN = os.getenv("TIBBER_TOKEN")
    charge_threshold = 0.15
    capacity = 1.6
    current_charge = 0
    load_per_hour = 1
    deload_per_hour = -0.8
    start_date = "2025-06-20 00:00"
    end_date = "2025-06-24 23:00"
    # -------------------------------------------------------------------

    op, np = simulate_battery( 
        TIBBER_TOKEN, 
        start_date,
        end_date,
        charge_threshold, 
        capacity, 
        0, 
        load_per_hour, 
        deload_per_hour, 
        True    
    )



    