from fast_flights import FlightQuery, Passengers, create_query, get_flights
from itertools import product
import urllib.parse

# Dates we want to try for departure (MIA -> EZE)
departure_dates = ["2026-12-12", "2026-12-13", "2026-12-14", "2026-12-15"]

# Dates we want to try for the return flight (EZE -> MIA)
return_dates = ["2027-01-02", "2027-01-03"]

# These two variables will keep track of the best (cheapest) option
# found across ALL date combinations we test below.
# They start empty because we haven't checked anything yet.
cheapest_price = None
cheapest_details = None


def build_google_flights_link(from_airport, to_airport, dep_date, ret_date):
    """
    Builds a link to the Google Flights SEARCH RESULTS page for a given
    route and dates. This is NOT a link to buy one specific flight at one
    specific price -- Google doesn't allow that publicly. It just opens
    Google Flights with the search already filled in, ready to browse.
    """
    # Build a plain-English search query, the same way you'd type it
    # directly into Google Flights' search bar.
    query_text = f"Flights from {from_airport} to {to_airport} on {dep_date} through {ret_date}"

    # URLs can't contain spaces or certain symbols directly.
    # urllib.parse.quote() converts them into a safe format
    # (e.g. spaces become "%20").
    encoded = urllib.parse.quote(query_text)

    # Paste the encoded text onto Google Flights' base URL.
    return f"https://www.google.com/travel/flights?q={encoded}"


# product(departure_dates, return_dates) generates every possible pairing
# between the two lists. With 4 departure dates and 2 return dates,
# this gives us 4 x 2 = 8 combinations to check.
for dep_date, ret_date in product(departure_dates, return_dates):
    print(f"Checking {dep_date} -> {ret_date}...")

    # Build the search request: a round-trip, economy class,
    # 1 adult, for this specific departure/return date pair.
    query = create_query(
        flights=[
            FlightQuery(date=dep_date, from_airport="MIA", to_airport="EZE"),  # outbound leg
            FlightQuery(date=ret_date, from_airport="EZE", to_airport="MIA"),  # return leg
        ],
        trip="round-trip",
        seat="economy",
        passengers=Passengers(adults=1),
        currency="USD",
    )

    # Actually send the request to Google Flights and wait for results.
    results = get_flights(query)

    # If Google Flights returned an empty list, skip to the next
    # combination instead of crashing on an empty result.
    if not results:
        print("  No flights found for this combination.\n")
        continue

    # Out of all flights found for THIS specific date combination,
    # find the one with the lowest price.
    # key=lambda f: f.price tells min() to compare by the .price
    # attribute of each flight, instead of trying to compare
    # whole flight objects directly.
    cheapest_in_batch = min(results, key=lambda f: f.price)
    print(f"  Cheapest here: {cheapest_in_batch.airlines} - ${cheapest_in_batch.price}\n")

    # Compare this combination's cheapest flight against the best one
    # we've seen so far across ALL combinations, and keep whichever is lower.
    if cheapest_price is None or cheapest_in_batch.price < cheapest_price:
        cheapest_price = cheapest_in_batch.price
        cheapest_details = (dep_date, ret_date, cheapest_in_batch)

# Print a simple divider line for readability
print("=" * 40)

# After checking every combination, show the overall best option found.
if cheapest_details:
    dep_date, ret_date, flight = cheapest_details
    link = build_google_flights_link("MIA", "EZE", dep_date, ret_date)

    print(f"BEST OPTION: {dep_date} -> {ret_date}")
    print(f"Airline: {flight.airlines}")
    print(f"Price: ${flight.price}")
    print(f"Link: {link}")
else:
    # This only happens if every single combination returned no flights
    print("No flights found for any combination.")