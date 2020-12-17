import os
import sys
from datetime import datetime
import pandas as pd
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url: str, browser: str = 'Firefox', headless: bool = True):
        self.results_folder = os.path.join(os.getcwd(), 'Results')
        if not os.path.exists(self.results_folder):
            os.mkdir(self.results_folder)
        self.result_file_name = ''
        self.result_file = os.path.join(self.results_folder, self.result_file_name)
        self.writer = pd.ExcelWriter(self.result_file, date_format='YYYY-MM-DD', datetime_format='YYYY-MM-DD')
        self.url = url
        if browser == 'Firefox':
            opts = webdriver.FirefoxOptions()
            if headless:
                opts.headless = True
            self.driver = webdriver.Firefox(options=opts)
        elif browser == 'Chrome':
            opts = webdriver.ChromeOptions()
            if headless:
                opts.headless = True
            self.driver = webdriver.Chrome(options=opts)
        self.time_checked = datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    def load_url(self):
        # logger.info(f'Gathering data from {self.url}')
        self.driver.get(self.url)

    def return_soup(self) -> BeautifulSoup:
        """
        Returns a BeautifulSoup object from the driver page source parsed as HTML
        :return: BeautifulSoup HTML parsed data
        """
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def parse_table(self, table_attrs: dict) -> pd.DataFrame:
        """
        Parses the table identified by the table attributes into a pandas dataframe
        :param table_attrs: dictionary of the table attributes for the table to be parsed
        :return: pandas dataframe of table
        """
        soup = self.return_soup()
        table_data = []
        table = soup.find('table', attrs=table_attrs)
        assert table is not None, f'Unable to find table with these attributes {table_attrs}'
        for row in table.find_all('tr'):
            cells = [c.text.strip() for c in row.find_all('td')]
            if len(cells) > 1:
                table_data.append(cells)
        cols = [c.text.strip() for c in table.find_all('th')]
        cols = cols[:len(table_data[0])]
        df = pd.DataFrame(table_data, columns=cols)
        return df

    def close(self):
        """
        Closes the browser window, don't forget to close when using a headless browser!
        :return: None
        """
        self.driver.close()

    @staticmethod
    def compare_existing_data(old_df: pd.DataFrame, new_df: pd.DataFrame, exclude_col=None) -> pd.DataFrame:
        """
        If there is already existing data, this function can be called to remove any duplicates.
        This function will remove any rows where all columns are the same except for time_checked
        :param old_df: DataFrame with existing data
        :param new_df: DataFrame with new data
        :param exclude_col: Column(s) that will be excluded when removing duplicate values in DataFrames.
                            Can be given either as a list of columns or a string with the column name.
        :return: DataFrame
        """
        df = pd.concat([old_df, new_df], ignore_index=True)
        if exclude_col and isinstance(exclude_col, str):
            ss = [col for col in df.columns.to_list() if col != exclude_col]
        elif exclude_col and isinstance(exclude_col, list):
            ss = [col for col in df.columns.to_list() if col not in exclude_col]
        else:
            ss = df.columns.to_list()
        df.drop_duplicates(subset=ss, inplace=True)
        return df

    def save_results(self):
        """
        Concatenates the data frames from the two tables together and saves the data
        :return: None
        """
        df = self.parse_table({'class': 'table'})
        if os.path.exists(self.result_file):
            df = self.compare_existing_data(pd.read_excel(self.result_file), df, exclude_col='time_checked')
        df.to_excel(self.writer, sheet_name='Data from Website', index=False, encoding='utf-8-sig', freeze_panes=(1, 0))
        self.writer.save()
        # logger.info(f'Results saved as {self.result_file_name}')


def main():
    ws = WebScraper(r'https://www.example.com/')
    try:
        ws.load_url()
        ws.save_results()
    except Exception as e:
    # logger.error(e, exc_info=sys.exc_info())
    # error_email(str(e))
    # logger.info('-' * 100)
    finally:
        ws.close()


if __name__ == '__main__':
    main()
