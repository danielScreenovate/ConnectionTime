import csv
import os
import time

__author__ = 'daniel'


def write_logs(number_of_connections, successful_connections, failures, consecutive_failures):
    curr_time = time.time()
    directory = "test_results"
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists("%s/%s" % (directory, curr_time)):
        os.makedirs("%s/%s" % (directory, curr_time))

    with open('%s/%s/connection_times.csv' % (directory, curr_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(len(successful_connections)):
            csv_writer.writerow((x + 1, successful_connections[x]))

    with open('%s/%s/consecutive_failures.csv' % (directory, curr_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(len(consecutive_failures)):
            csv_writer.writerow((x + 1, consecutive_failures[x]))

    file = open('%s/%s/failures.txt' % (directory, curr_time), 'w+')
    file.write("Total connection attempts: %s\n" % number_of_connections)
    file.write("Total connection successes: %s\n" % len(successful_connections))
    file.write("Total connection failures: %s\n" % failures)
    file.close()