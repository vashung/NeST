# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2019-2020 NITK Surathkal

"""
Base class for Quagga
"""

from abc import ABC, abstractmethod
import io
import shutil
from nest.engine.quagga import run_quagga, create_conf_file


class QuaggaBase(ABC):
    """
    Abstract class for Quagga related processes. This class should
    be inherited for adding other quagga daemons

    Attributes
    ----------
    conf: file-like
        In memory stream to temporarily hold configuration
    router_ns_id : str
        Router namespace id
    daemon : str
        quagga daemon to run(one of ['zebra', 'ospf'])
    conf_file : str
        config file path
    pid_file : str
        pid file path for the daemon process
    interfaces : List[Interface]
        interfaces present in the router
    """

    def __init__(self, router_ns_id, interfaces, daemon, conf_dir):
        self.conf = io.StringIO()
        self.router_ns_id = router_ns_id
        self.daemon = daemon
        self.conf_file = f'{conf_dir}/{self.router_ns_id}_{daemon}.conf'
        self.pid_file = f'{conf_dir}/{self.router_ns_id}_{daemon}.pid'
        self.interfaces = interfaces

    @abstractmethod
    def create_basic_config(self):
        """
        Created minimum configuration for `daemon`
        """

    def add_to_config(self, command):
        """
        Add a line to `self.conf`

        Parmeters
        ---------
        command : str
            command to add to config file
        """
        self.conf.write(f'{command}\n')

    def create_config(self):
        """
        Creates config file on disk from `self.conf`
        """
        create_conf_file(self.conf_file)
        with open(self.conf_file, 'w') as conf:
            self.conf.seek(0)
            shutil.copyfileobj(self.conf, conf)

    def run(self):
        """
        Run the `daemon` along with its config file
        """
        run_quagga(self.router_ns_id, self.daemon, self.conf_file, self.pid_file)