# Infinite Coffee

A lightweight Python app that monitors a connected scale once daily to track coffee consumption. It calculates how much coffee is used and remaining, and proactively sends a text message when supply is running low. With user confirmation, it can automatically trigger a coffee reorder.

---

## Features

- Reads coffee weight via serial from a SparkFun OpenScale.
- Maintains historical data to track daily usage.
- Calculates expected run-out date based on consumption trends.
- Sends SMS alerts when coffee is low.
- Handles automated reordering upon text confirmation.
- Designed to run on Raspberry Pi Zero or other small systems.
- Environment-configurable via `.env` file.
- Easy setup with [Poetry](https://python-poetry.org/).

---

##  Installation

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- A serial-connected scale (e.g., SparkFun OpenScale)
- A personal Textbelt API key
- A personal Terminal.shop API key

**Note**: The app assumes that you have already saved a default shipping address and payment method in your Terminal.shop account. The top address and card on file will be used when placing an order.

### Clone and Install

```bash
git clone https://github.com/connortm20/infinite-coffee
cd infinite-coffee
poetry install
```

## Configuration

Create a `.env` file in the root directory. You can use `.env.example` as a starting point.

your `.env` should define all values shown in the example

---

## Usage

```bash
poetry run python src/coffee_scale/main.py
```

Set this up as a daily cron job or scheduled task depending on your platform.

#### Scheduling with Cron (Linux)

To run the script daily at 2 AM, add this to your crontab (`crontab -e`):

```
0 2 * * * cd /path/to/infinite-coffee && poetry run python src/coffee_scale/main.py
```

###  Simulating a Scale Reading

For testing or development without a physical scale connected, you can simulate a weight reading by passing a numeric value as a command-line argument:

```bash
poetry run python src/coffee_scale/main.py 412.7
```

This overrides the live reading and uses the provided value (in grams) as the scale input.


