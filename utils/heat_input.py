import re

# ---------------------------------------------------
# Welding Process Efficiency
# ---------------------------------------------------

PROCESS_EFFICIENCY = {
    "SMAW": 0.80,
    "GTAW": 0.60,
    "GMAW": 0.90,
    "SAW": 0.95
}

# ---------------------------------------------------
# Extract numeric value
# Example:
# "130-160 A" -> 145
# "24-26 V" -> 25
# ---------------------------------------------------

def extract_average(value):

    text = str(value)

    numbers = re.findall(r"\d+\.?\d*", text)

    if len(numbers) == 0:
        return 0

    numbers = [float(x) for x in numbers]

    return sum(numbers) / len(numbers)

# ---------------------------------------------------
# Heat Input
# ---------------------------------------------------

def calculate_heat_input(
    process,
    current,
    voltage,
    travel_speed
):

    current = extract_average(current)
    voltage = extract_average(voltage)
    travel_speed = extract_average(travel_speed)

    efficiency = PROCESS_EFFICIENCY.get(process, 0.80)

    heat_input = (
        efficiency *
        voltage *
        current *
        60
    ) / (1000 * travel_speed)

    return round(heat_input, 2)