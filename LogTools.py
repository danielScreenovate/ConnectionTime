import csv
import os
import time
import subprocess

__author__ = 'daniel'


def write_logs(successful_connections_list, failures, consecutive_failures, source_serial, sink_serial, script_start_time):
    sum_connection_times = 0
    number_of_succesful_connections = len(successful_connections_list)
    EXTERNAL_DIRECTORY = "test_results"
    TODAY_DIRECTORY = "{0}/{1}".format(EXTERNAL_DIRECTORY, time.strftime("%Y_%m_%d"))
    INNER_DIRECTORY = "{0}/Source-{1}_Sink-{2}".format(TODAY_DIRECTORY, source_serial, sink_serial)
    if not os.path.exists(EXTERNAL_DIRECTORY):
        os.makedirs(EXTERNAL_DIRECTORY)
    if not os.path.exists(TODAY_DIRECTORY):
        os.makedirs(TODAY_DIRECTORY)
    if not os.path.exists(INNER_DIRECTORY):
        os.makedirs(INNER_DIRECTORY)
    if not os.path.exists("%s/%s" % (INNER_DIRECTORY, script_start_time)):
        os.makedirs("%s/%s" % (INNER_DIRECTORY, script_start_time))

    with open('%s/%s/connection_times.csv' % (INNER_DIRECTORY, script_start_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(number_of_succesful_connections):
            csv_writer.writerow((x + 1, successful_connections_list[x]))
            sum_connection_times += successful_connections_list[x]

    with open('%s/%s/consecutive_failures.csv' % (INNER_DIRECTORY, script_start_time), 'w+') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(len(consecutive_failures)):
            csv_writer.writerow((x + 1, consecutive_failures[x]))

    file = open('%s/%s/stats.txt' % (INNER_DIRECTORY, script_start_time), 'w+')
    number_of_connection_attempts = number_of_succesful_connections + failures
    file.write("Total connection attempts: %s\n" % number_of_connection_attempts)
    file.write("Succesful connetions: %s\n" % number_of_succesful_connections)
    if number_of_succesful_connections != 0:
        file.write("Average connection time: %s\n" % (sum_connection_times / len(successful_connections_list)))
    file.write("Total connection failures: %s\n" % failures)
    file.close()




#
# def background_logs(source_serial, sink_serial, start_time):
#     EXTERNAL_DIRECTORY = "test_results"
#     INNER_DIRECTORY = "%s/Source_%s-Sink_%s" % (EXTERNAL_DIRECTORY, source_serial, sink_serial)
#     if not os.path.exists(EXTERNAL_DIRECTORY):
#         os.makedirs(EXTERNAL_DIRECTORY)
#     if not os.path.exists(INNER_DIRECTORY):
#         os.makedirs(INNER_DIRECTORY)
#     if not os.path.exists("%s/%s" % (INNER_DIRECTORY, start_time)):
#         os.makedirs("%s/%s" % (INNER_DIRECTORY, start_time))
#
#     proc = subprocess.Popen(['adb', 'logcat', '>', '%s/log.txt' % INNER_DIRECTORY])
#     TODO: implement proc.kill at end of script.
#     proc.kill()

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