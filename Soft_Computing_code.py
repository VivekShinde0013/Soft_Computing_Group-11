import random

print(" Intelligent Fuel Efficiency Advisor Using Genetic Algorithm")

distance = float(input("Enter total distance to travel (in km): "))
time = float(input("Enter time to cover distance (in hours): "))
load = float(input("Enter engine load % (e.g. 70): "))
temp = float(input("Enter ambient temperature °C (e.g. 35): "))
vehicle_type = input("Enter vehicle type (gasoline/diesel/hybrid): ").strip().lower()

speed = distance / time
print(f"\n Average speed based on distance and time: {speed:.2f} km/h")

def recommend_ranges(vehicle, speed):
    if vehicle == "gasoline":
        return (1800, 2500), (60, 90), (40, 60)
    elif vehicle == "diesel":
        return (1500, 2200), (50, 80), (35, 55)
    elif vehicle == "hybrid":
        return (1200, 2000), (40, 70), (30, 50)
    else:
        return (1600, 2500), (60, 90), (40, 60)

rpm_range, speed_range, throttle_range = recommend_ranges(vehicle_type, speed)

def fitness_function(params, speed, load, temp):
    injection, afr, ignition, throttle = params
    base_eff = (100 - abs(14.7 - afr)) * (1 - abs(throttle - 50)/100) - abs(injection - 10)
    penalty = abs(speed - 60)/30 + abs(load - 50)/50 + abs(temp - 25)/10
    return base_eff - penalty

def mutate(chromosome):
    return [gene + random.uniform(-1, 1) for gene in chromosome]

def crossover(parent1, parent2):
    return [(g1 + g2) / 2 for g1, g2 in zip(parent1, parent2)]

def run_ga():
    pop_size = 10
    generations = 50
    population = [
        [random.uniform(5, 15), random.uniform(12, 16), random.uniform(5, 15), random.uniform(0, 100)]
        for _ in range(pop_size)
    ]

    for _ in range(generations):
        population.sort(key=lambda x: -fitness_function(x, speed, load, temp))
        next_gen = population[:2]
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(population[:5], 2)
            child = mutate(crossover(p1, p2))
            next_gen.append(child)
        population = next_gen

    best = max(population, key=lambda x: fitness_function(x, speed, load, temp))
    return {
        "fuel_injection": round(best[0], 2),
        "air_fuel_ratio": round(best[1], 2),
        "ignition_timing": round(best[2], 2),
        "throttle_position": round(best[3], 2),
        "efficiency_score": round(fitness_function(best, speed, load, temp), 2)
    }

optimized = run_ga()

print("\n Optimized Engine Parameters Based on Your Trip:")
for k, v in optimized.items():
    print(f"{k.replace('_', ' ').title()}: {v}")

print("\n Suggested Ideal Ranges for Your Vehicle Type:")
print(f" Engine RPM: {rpm_range[0]} - {rpm_range[1]} RPM")
print(f" Speed: {speed_range[0]} - {speed_range[1]} km/h")
print(f" Throttle Position: {throttle_range[0]}% - {throttle_range[1]}%")
print(f" Aim for Efficiency Score > 70 for good fuel economy")

print("\n Fuel-Saving Tips:")
print("- Maintain a steady speed and avoid aggressive acceleration.")
print("- Avoid engine over-revving; shift gears appropriately.")
print("- Keep tires properly inflated and engine tuned.")
print("- Minimize idling and use cruise control on highways.")
