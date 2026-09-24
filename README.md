# Agent Flights

Personal AI agent project that searches and compares flight prices using Python.

## Current status (WIP)

Two scripts so far:

- **`test_flights.py`** — Simple one-way flight search for a single date.
  Used to validate the setup works end to end.
- **`find_cheapest.py`** — Searches round-trip flights across a range of
  departure and return dates, finds the cheapest combination, and prints
  a Google Flights link to view/book it.

Example route: Miami (MIA) ↔ Buenos Aires (EZE)

## Setup

1. Create a conda environment: `conda create -n agent-flights python=3.11`
2. Activate it: `conda activate agent-flights`
3. Install dependencies: `pip install faster-flights`
4. Run a simple search: `python test_flights.py`
5. Run the cheapest-combination search: `python find_cheapest.py`

## Roadmap

- Connect an LLM (Ollama) as the agent's "brain"
- Turn flight search into a tool the agent can call
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