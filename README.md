# Agent Flights

Personal AI agent project that searches and compares flight prices using Python.

## Current status (WIP)

Files so far:

- **`test_flights.py`** — Simple one-way flight search for a single date.
  Used to validate the setup works end to end.
- **`find_cheapest.py`** — Searches round-trip flights across a range of
  departure and return dates, finds the cheapest combination, and prints
  a Google Flights link to view/book it.
- **`flight_tool.py`** — Reusable version of the flight search logic,
  wrapped as a function (`search_cheapest_flight`) so it can be called
  with parameters instead of hardcoded dates. This is the "tool" the
  AI agent will use.
- **`test_ollama.py`** — Confirms the connection to a local LLM (Llama 3.1
  via Ollama) is working.

Example route: Miami (MIA) ↔ Buenos Aires (EZE)

## Setup

1. Create a conda environment: `conda create -n agent-flights python=3.11`
2. Activate it: `conda activate agent-flights`
3. Install dependencies: `pip install faster-flights requests`
4. Install [Ollama](https://ollama.com/download) and pull a model:
   `ollama pull llama3.1`
5. Run a simple search: `python test_flights.py`
6. Run the cheapest-combination search: `python find_cheapest.py`
7. Test the LLM connection: `python test_ollama.py`

## Roadmap

- ~~Connect an LLM (Ollama) as the agent's "brain"~~ ✅
- Turn flight search into a tool the agent can call (in progress: `agent.py`)
- Add persistent memory for tracked routes/prices
- Add scheduled price checks with alerts

## Known limitations

This project uses `faster-flights` (a fork of `fast-flights`), which scrapes
Google Flights instead of using an official API. This means:

- Results may not always match what you see in your own browser (Google
  personalizes results per session)
- The library can break if Google changes its internal structure
- Prices should always be verified on the actual Google Flights link
  before booking