from itertools import product
from flagger import Flagger
from config import *
import operator
from models.baseline import Baseline
from models.antenna_status import AntennaStatus


class RFlagger(Flagger):
    def __init__(self, measurement_set):
        super(RFlagger, self).__init__(measurement_set)

    def get_bad_baselines(self):
        return self._r_based_bad_baselines('flux_calibration')

    def _r_based_bad_baselines(self, source):
        polarizations = GLOBAL_CONFIG['polarizations']
        source_properties = ALL_CONFIGS[source]
        scan_ids = self.measurement_set.scan_ids_for(source_properties['field'])
        channel = source_properties['channel']
        base_antenna = self.measurement_set.antennas[0]

        for polarization, scan_id in product(polarizations, scan_ids):
            _r_value_matrix = {}
            bad_antennas = self.identify_antennas(polarization, scan_id, channel, base_antenna, _r_value_matrix, set())
            print "Pol-",polarization, "Scan-",scan_id, "Bad-",bad_antennas

    def identify_antennas(self, polarization, scan_id, channel, base_antenna, _r_value_matrix, history):
        if base_antenna in history: return set()

        baselines = self.measurement_set.baselines_for(base_antenna)
        doubtful_antennas = set()
        bad_antennas = set()
        for (antenna1, antenna2) in baselines:
            # TODO: dont calculate again if present in r-matrix
            filter_params = {'scan_number': scan_id, 'antenna1': antenna1.id, 'antenna2': antenna2.id}
            phase_set = self.measurement_set.get_phase_data({'start': channel}, polarization, filter_params)
            r_value = phase_set.calculate_angular_dispersion()

            another_antenna = antenna2 if base_antenna == antenna1 else antenna1

            if base_antenna not in _r_value_matrix.keys():
                _r_value_matrix[base_antenna] = {}
            _r_value_matrix[base_antenna].update({another_antenna: r_value})

        for antenna, r_value in _r_value_matrix[base_antenna].iteritems():
            if r_value < 0.3:
                doubtful_antennas.add(antenna)
                antenna.update_state(polarization, scan_id, AntennaStatus.DOUBTFUL)

        if len(doubtful_antennas) < 3:
            sorted_r_value_matrix = sorted(_r_value_matrix[base_antenna].items(), key=operator.itemgetter(1))
            new_doubtful_antennas = set(dict(sorted_r_value_matrix[:3]).keys())
            for doubtful_antenna in new_doubtful_antennas:
                doubtful_antenna.update_state(polarization, scan_id, AntennaStatus.DOUBTFUL)

            doubtful_antennas = set().union(doubtful_antennas, new_doubtful_antennas)

        if len(doubtful_antennas) <= 10:  # 70% is good
            base_antenna.update_state(polarization, scan_id, AntennaStatus.GOOD)

        else:
            sorted_r_value_matrix = sorted(_r_value_matrix[base_antenna].items(), key=operator.itemgetter(1))
            doubtful_antennas = set(dict(sorted_r_value_matrix[:3]).keys())
            base_antenna.update_state(polarization, scan_id, AntennaStatus.BAD)
            bad_antennas.add(base_antenna)

        history.add(base_antenna)

        for doubtful_antenna in doubtful_antennas:
            new_bad_antennas = self.identify_antennas(polarization, scan_id, channel, doubtful_antenna, _r_value_matrix,
                                                history)
            bad_antennas = set.union(bad_antennas, new_bad_antennas)

        return bad_antennas