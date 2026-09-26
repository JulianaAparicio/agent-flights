from fast_flights import FlightQuery, Passengers, create_query, get_flights
import urllib.parse


def build_google_flights_link(from_airport, to_airport, dep_date, ret_date):
    """Builds a link to the Google Flights search results page."""
    query_text = f"Flights from {from_airport} to {to_airport} on {dep_date} through {ret_date}"
    encoded = urllib.parse.quote(query_text)
    return f"https://www.google.com/travel/flights?q={encoded}"


def search_cheapest_flight(from_airport, to_airport, departure_date, return_date):
    """
    Searches for a round-trip flight and returns the cheapest option found.
    This is the function the LLM will be able to call.
    """
    query = create_query(
        flights=[
            FlightQuery(date=departure_date, from_airport=from_airport, to_airport=to_airport),
            FlightQuery(date=return_date, from_airport=to_airport, to_airport=from_airport),
        ],
        trip="round-trip",
        seat="economy",
        passengers=Passengers(adults=1),
        currency="USD",
    )

    results = get_flights(query)

    if not results:
        return {"error": "No flights found for these dates."}

    cheapest = min(results, key=lambda f: f.price)
    link = build_google_flights_link(from_airport, to_airport, departure_date, return_date)

    return {
        "airline": str(cheapest.airlines),
        "price": cheapest.price,
        "departure_date": departure_date,
        "return_date": return_date,
        "link": link,
    }


if __name__ == "__main__":
    resultado = search_cheapest_flight("MIA", "EZE", "2026-12-11", "2027-01-03")
    print(resultado)