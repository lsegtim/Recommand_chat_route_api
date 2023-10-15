import pandas as pd

from shortest_path import generate_graph

save_path = "data/"

user_id = "60f4d5c5b5f0f0e5e8b2b5c9"
latitude = "6.828828828828828"
longitude = "79.86386702251839"
radius = "303.5087719298246"
start_time_restrictions = "7.00AM"
end_time_restrictions = "7.00PM"
accessibility = "Wheelchair-accessible car park, Wheelchair-accessible entrance"
historical_contexts = "Ancient Buddhist monastery"
hands_on_activities = "Photography, Sightseeing, Relaxing"
location_id = "652b9d229c8deef2485bf8e2"

# users.to_csv(save_path + "users.csv", index=False)
# interactions.to_csv(save_path + "interactions.csv", index=False)
locations = pd.read_csv(save_path + "locations.csv")

print(locations[locations["_id"] == location_id])

# current_location = (6.9271, 79.8612)
current_location = (float(latitude), float(longitude))

G, hamiltonian_cycle = generate_graph(current_location, locations.head())
print(hamiltonian_cycle)

# add 0 as

# from locations find the location_ids in the hamiltonian_cycle and get all the details of those locations
locations_in_hamiltonian_cycle = locations[locations["_id"].isin(hamiltonian_cycle)]
print(locations_in_hamiltonian_cycle)



