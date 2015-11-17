import csv
import os
import time

__author__ = 'daniel'


def write_logs(number_of_connections, successful_connections, failures, consecutive_failures):
    curr_time = time.time()
    sum_connection_times = 0
    number_of_succesful_connections = len(successful_connections)
    directory = "test_results"
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists("%s/%s" % (directory, curr_time)):
        os.makedirs("%s/%s" % (directory, curr_time))

    with open('%s/%s/connection_times.csv' % (directory, curr_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(number_of_succesful_connections):
            csv_writer.writerow((x + 1, successful_connections[x]))
            sum_connection_times += successful_connections[x]

    with open('%s/%s/consecutive_failures.csv' % (directory, curr_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(len(consecutive_failures)):
            csv_writer.writerow((x + 1, consecutive_failures[x]))

    file = open('%s/%s/stats.txt' % (directory, curr_time), 'w+')
    file.write("Total connection attempts: %s\n" % number_of_connections)
    file.write("Succesful connetions: %s\n" % number_of_succesful_connections)
    if number_of_succesful_connections != 0:
        file.write("Average connection time: %s\n" % (sum_connection_times / len(successful_connections)))
    file.write("Total connection failures: %s\n" % failures)
    file.close()

#
#
# def _run_logcat():
#     print "*** in process ***"
#     os.system("adb logcat | findstr %s" % PRINTING_FRAME_LINE)
#     end_time = time.time()
#     print "*** updated end time as: %s ***" % end_time
#
# def get_end_time():
#     # Start _run_logcat as a process
#     print "starting get end time"
#     p = multiprocessing.Process(target=_run_logcat, args=(15,))
#     print "started logcat process"
#     p.start()
#
#     # Wait 10 seconds for foo
#     time.sleep(15)
#
#     # Terminate foo
#     print "terminating process"
#     p.terminate()
#
#     # Cleanup
#     p.join()