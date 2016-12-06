from models.antenna_status import AntennaStatus


class Report:
    def __init__(self, antennas):
        self.__antennas = antennas

    def generate_report(self, scan_ids):
        print "AntennaId,Polarisation,ScanId,Status"
        for ant in self.__antennas:
            for state in ant.get_states():
                if state.scan_id in scan_ids and state.get_closure_phase_status() == AntennaStatus.BAD:
                    print ant.id, state.polarization, state.scan_id, state.get_closure_phase_status()