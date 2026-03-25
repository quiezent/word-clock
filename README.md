# Word Clock

A simple Tkinter-based word clock that displays time as words (for example, **"TWENTY FIVE PAST TWO"**) with four dots to indicate extra minutes between 5-minute intervals.

## Features

- 10x11 letter grid with highlighted words for the current time
- 4 minute dots for minutes not divisible by 5
- Supports both live local time and a fixed `HH:MM` input for testing/demo
- Handles 24-hour input by converting to 12-hour word output

## Requirements

- Python 3.10+
- Tkinter (typically bundled with standard Python installs)

## Run

### Live clock

```bash
python word_clock.py
```

### Fixed time (24-hour `HH:MM`)

```bash
python word_clock.py 13:15
```

The fixed-time mode validates input and accepts only values from `00:00` to `23:59`.

## Test

```bash
pytest -q
```

## Notes for headless environments

This project uses Tkinter and requires a display server to render the UI. In headless CI/container environments without `$DISPLAY`, UI instantiation will fail even when logic tests pass.
