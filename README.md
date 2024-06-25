# Starlink Scraper

Starlink Scraper is a Python-based web scraper that checks the visibility of Starlink satellites and notifies the user about their visibility status and any upcoming launches. The scraper uses Selenium to extract visibility data from the Find Starlink website and checks the launch status through the SpaceDevs API.

## Features

- Scrapes visibility data for Starlink satellites from the Find Starlink website.
- Checks if there are any upcoming Starlink launches.
- Provides a notification (currently prints to the console) about visibility and launch status.

## Prerequisites

- Python 3.6+
- Google Chrome browser
- ChromeDriver

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/greg0109/starlinkScraper.git
   cd starlinkScraper
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Download and install [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) matching your Chrome browser version. Make sure to add ChromeDriver to your system PATH.

## Usage

Run the scraper using the following command:
```sh
python3 main.py
```

## Files

- `main.py`: Main script containing the `StarlinkScraper` class.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `Makefile`: Makefile for setting up the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- [Find Starlink](https://findstarlink.com) for providing visibility data.
- [The SpaceDevs API](https://thespacedevs.com) for launch information.
