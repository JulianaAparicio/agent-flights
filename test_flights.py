from fast_flights import FlightQuery, Passengers, create_query, get_flights

# Search for a one-way flight from Miami (MIA) to Buenos Aires (EZE)
query = create_query(
    flights=[
        FlightQuery(date="2026-12-10", from_airport="MIA", to_airport="EZE")
    ],
    trip="one-way",
    seat="economy",
    passengers=Passengers(adults=1),
    currency="USD",
)

results = get_flights(query)

print(f"Found {len(results)} flights:\n")
for flight in results[:5]:
    print(f"{flight.airlines} - ${flight.price}")