import multiprocessing
import time
import os
import csv
import signal

start_time = time.time()

FILE_PATH = 'Naamloze spreadsheet - Blad1.csv' #insert way file. It's all.
NAME_AND_PATH_OUTPUT_FILE = 'output file check WP2.csv' #you can change this name file


class Timeout:
    def __init__(self, seconds=1, error_message='TimeoutError'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


list_url = []


with open(FILE_PATH, encoding='utf-8') as r_file:
    for row in r_file:
        list_url.append(row.replace('\n', ''))

print(list_url)

list_url_complete = []

def handler(list_links):
    print(list_links)
    with Timeout(seconds=15, error_message='JobX took too much time'):
        try:
            if 'may not be using WordPress.' in (os.popen(f"wpdetect {list_links}").read()).split('\n')[-3]:
                print('not WP')
                list_url_complete.append([list_links, 'not WP'])
                result_input = [list_links, 'not WP']
            elif list_links == '':
                print('')
                list_url_complete.append([list_links, ''])
                result_input = [list_links, '']
            else:
                print('yes WP')
                list_url_complete.append([list_links, 'yes WP'])
                result_input = [list_links, 'yes WP']
            print('----------')
        except TimeoutError as e:
            print('no connection to website')
            list_url_complete.append([list_links, 'no connection to website'])
            result_input = [list_links, 'no connection to website']
            print('----------')

    with open(NAME_AND_PATH_OUTPUT_FILE, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(result_input)


with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
    process.map(handler, list_url)

print("--- %s seconds ---" % (time.time() - start_time))