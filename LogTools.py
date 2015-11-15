import csv
import os
import time

__author__ = 'daniel'


def write_to_csv(connection_times):
    curr_time = time.time()
    directory = "test_results"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('%s/test_%s.csv' % (directory, curr_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(len(connection_times)):
            csv_writer.writerow((x + 1, connection_times[x]))