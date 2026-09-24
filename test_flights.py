from fast_flights import FlightQuery, Passengers, create_query, get_flights

# Build the search request (this doesn't search yet, just prepares it):
# - one-way flight
# - from Miami (MIA) to Buenos Aires (EZE)
# - departing 2026-12-10
# - economy class, 1 adult, prices in USD
query = create_query(
    flights=[
        FlightQuery(date="2026-12-10", from_airport="MIA", to_airport="EZE")
    ],
    trip="one-way",
    seat="economy",
    passengers=Passengers(adults=1),
    currency="USD",
)

# Send the request to Google Flights and wait for the results.
# "results" ends up being a list of flights found.
results = get_flights(query)

# Print how many flights were found in total.
# len(results) counts the items in the list.
# The f"..." is an f-string: it lets us insert a variable's value
# directly inside a piece of text.
print(f"Found {len(results)} flights:\n")

# Loop through the first 5 flights found (results[:5] takes only
# the first 5 items from the list, so we don't print everything
# if there are a lot of results).
for flight in results[:5]:
    # For each flight, print its airline and price.
    # flight.airlines and flight.price access those specific
    # pieces of data stored inside each flight object.
    print(f"{flight.airlines} - ${flight.price}")