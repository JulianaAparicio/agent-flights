# Agent Flights

Personal AI agent project that searches flight prices using Python.

## Current status (WIP)
- Searches one-way flights between two airports using the `fast-flights` library
- Example: Miami (MIA) → Buenos Aires (EZE)

## Setup
1. Create a conda environment: `conda create -n agent-flights python=3.11`
2. Activate it: `conda activate agent-flights`
3. Install dependencies: `pip install fast-flights`
4. Run: `python test_flights.py`

## Roadmap
- [ ] Connect an LLM (Ollama) as the agent's "brain"
- [ ] Turn flight search into a tool the agent can call
- [ ] Add persistent memory for tracked routes/prices
- [ ] Add scheduled price checks with alerts

## Known limitations
This project uses `fast-flights`, which scrapes Google Flights instead of
using an official API. This means:
- Results may not always match what you see in your own browser (Google
  personalizes results per session)
- The library can break if Google changes its internal structure
- Prices should always be verified on the actual Google Flights link
  before booking