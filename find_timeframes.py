from datetime import timedelta, datetime, timezone

def get_price_order_in_frame(frame, energy_data):
    ret_data = []
    for entry in energy_data:
        if frame['start'] <= entry['stamp'] and entry['stamp'] <= frame['end']:
            ret_data.append(entry)
    sorted_data = sorted(ret_data, key=lambda x: x["price_kwh"])
    return sorted_data

def find_frame_with_high_power_draw(
        current_charge_frame,
        charge_frames,
        consumption_data
):
    high_power_draw_times = []

    # Sort just in case
    periods_sorted = sorted(charge_frames, key=lambda x: x["start"])

    # Find the target block and determine next range
    result = None

    for i, block in enumerate(periods_sorted):
        if block["start"] == current_charge_frame["start"] and block["end"] == current_charge_frame["end"]:
            start = block["end"]
            if i + 1 < len(periods_sorted):
                end = periods_sorted[i + 1]["start"]
            else:
                end = consumption_data[-1]['stamp']
            result = {"start": start + timedelta(hours=1), "end": end - timedelta(hours=1)}
            break
    
    for entry in consumption_data:
        if result['start'] <= entry['stamp'] and entry['stamp'] <= result['end']:
            high_power_draw_times.append(entry)

    sorted_data = sorted(high_power_draw_times, key=lambda x: x["price_kwh"], reverse=True)
    return sorted_data