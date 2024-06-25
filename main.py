"""
Starlink finder
"""
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests


class StarlinkScraper:
    """
    Starlink visibility checker
    """
    URL = 'https://findstarlink.com/#3117735;3' # Madrid, Spain
    LAUNCH_API_URL = 'https://ll.thespacedevs.com/2.0.0/launch/upcoming/?format=json'

    def __init__(self):
        self.visibility_status = {
            'good': [],
            'average': [],
            'visibility': False,
            'launch_today': False
        }
        self.current_time = datetime.now()
        self.twenty_four_hours_ago = self.current_time - timedelta(hours=24)
        self.twenty_four_hours_from_now = self.current_time + timedelta(hours=24)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)

    def check_date(self, date_to_check, yesterday=False):
        """
        Check if the date to check is today
        """
        if yesterday:
            start_time = self.twenty_four_hours_ago
            end_time = self.current_time
        else:
            start_time = self.current_time
            end_time = self.twenty_four_hours_from_now

        return start_time <= date_to_check < end_time

    def parse_visibility_status(self):
        """
        Parse the visibility status from the page content
        """

        time_entry_base = {
            'date': '',
            'dim': '',
            'direction': '',
            'visible': '',
        }

        def parse_timing_entries(timings_element):
            timing_entries = timings_element.find_elements(By.CLASS_NAME, 'timingEntry')
            times = []
            for timing_entry in timing_entries:
                time_entry = time_entry_base.copy()
                date = timing_entry.find_element(By.CLASS_NAME, 'entryTiming').text
                date_of_view = datetime.strptime(date, "%I:%M %p, %d %b %Y")
                if not self.check_date(date_of_view):
                    continue
                dim = timing_entry.find_element(By.CLASS_NAME, 'dimLabel').text
                timing_entry_data = timing_entry.find_element(By.CLASS_NAME, 'timingEntryBottom')
                directions_rough = timing_entry_data.find_elements(By.CLASS_NAME, 'bold')
                directions = '-'.join([direction.text for direction in directions_rough])
                visible = timing_entry.find_element(By.CLASS_NAME, 'timingNote').text
                time_entry['date'] = date
                time_entry['dim'] = dim
                time_entry['direction'] = directions
                time_entry['visible'] = visible
                times.append(time_entry)
            return times

        try:
            self.driver.find_element(By.ID, 'noVisibilityReminderNudge')
        except NoSuchElementException:
            self.visibility_status['visibility'] = True

        try:
            self.driver.find_element(By.ID, 'goodTimingsError')
        except NoSuchElementException:
            good_timings = self.driver.find_element(By.ID, 'goodTimings')
            self.visibility_status['good'] = parse_timing_entries(good_timings)

        try:
            self.driver.find_element(By.ID, 'avgTimingsError')
        except NoSuchElementException:
            average_timings = self.driver.find_element(By.ID, 'avgTimings')
            self.visibility_status['average'] = parse_timing_entries(average_timings)

    def check_visibility(self):
        """
        Check the visibility status of Starlink satellites
        """
        self.driver.get(self.URL)
        self.parse_visibility_status()

    def check_launch_today(self):
        """
        Check if there's a Starlink satellite launch today
        """
        response = requests.get(self.LAUNCH_API_URL, timeout=30)
        if response.status_code == 200:
            data = response.json()
            for launch in data['results']:
                if 'Starlink Group' in launch['name']:
                    launch_date = datetime.strptime(
                        launch['window_start'], "%Y-%m-%dT%H:%M:%SZ")
                    if self.check_date(launch_date, yesterday=True):
                        self.visibility_status['launch_today'] = True
                        break

    def notify(self):
        """
        Notify the user about the visibility status of Starlink satellites
        """
        visibility_status = self.visibility_status
        sections = []

        if not visibility_status['visibility']:
            sections.append("Starlink Not Visible")

        for category in ['good', 'average']:
            if visibility_status[category]:
                sections.append(f"\n{category.capitalize()} visibility:")
                sections.extend(
                    f"{entry['date']} \n {entry['visible']} \n {entry['direction']}"
                    for entry in visibility_status[category]
                )

        if visibility_status['launch_today']:
            sections.append("\nStarlink satellite launch today!")

        sections.append(f"\n{self.URL}")

        if any(len(visibility_status[category]) > 0 for category in ['good', 'average']):
            print("\n".join(sections))

    def run(self):
        """
        Run the Starlink visibility checker
        """
        try:
            self.check_visibility()
            self.check_launch_today()
            self.notify()
        except requests.exceptions.RequestException as e:
            print(
                f"Network error occurred while checking Starlink visibility: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            self.driver.quit()


if __name__ == '__main__':
    checker = StarlinkScraper()
    checker.run()
