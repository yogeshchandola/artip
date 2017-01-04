from configs.config import DATASET, CASAPY_CONFIG
import os
import subprocess
import time
from datetime import datetime
import logging
import casac


class CasaRunner:
    @staticmethod
    def _run(script, script_parameters=DATASET, casapy_path=CASAPY_CONFIG['path']):
        CasaRunner._unlock_dataset(DATASET)
        script_full_path = os.path.realpath(script)
        command = "{0} --nologger --nogui -c {1} {2}".format(casapy_path, script_full_path, script_parameters)
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        logging.debug("Casapy Process Started at {0}".format(str(datetime.now())))
        logging.debug("process Id= {0}".format(process.pid))
        while process.poll() is None:
            time.sleep(0.5)
        logging.debug("Casapy Process Completed at {0}".format(str(datetime.now())))

    @staticmethod
    def flagdata(reason):
        script_path = 'casa_scripts/flag.py'
        script_parameters = "{0} {1}".format(DATASET, reason)
        CasaRunner._run(script_path, script_parameters, CASAPY_CONFIG['path'])

    @staticmethod
    def apply_flux_calibration():
        script_path = 'casa_scripts/calibration.py'
        CasaRunner._run(script_path, DATASET, CASAPY_CONFIG['path'])

    @staticmethod
    def _unlock_dataset(dataset):
        table = casac.casac.table()
        table.open(dataset)
        table.unlock()