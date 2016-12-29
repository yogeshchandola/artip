import numpy

from configs.debugging_config import DEBUG_FLAG_ELEMENTS


def calculate_median(list):
    return numpy.median(numpy.array(list))


def minus(list1, list2):
    return filter(lambda elm: elm not in list2, list1)


def delete_indexes(array, indexes):
    result = []
    for index, time_index in enumerate(indexes):
        result = numpy.delete(array, time_index, 0) if index == 0 else numpy.delete(result, time_index - 1, 0)
    return result


class Debugger:
    def __init__(self, measurement_set):
        self._measurement_set = measurement_set

    def flag_antennas(self, polarization, scan_id):
        self._measurement_set.flag_antennas(polarization, scan_id, DEBUG_FLAG_ELEMENTS['antennas'])

    def flag_baselines(self, polarization, scan_id):
        self._measurement_set.flag_baselines(polarization, scan_id, DEBUG_FLAG_ELEMENTS['baselines'])