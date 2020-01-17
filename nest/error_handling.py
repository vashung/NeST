# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2019-2020 NITK Surathkal

##################################################
# This file contains all error checks and messages
##################################################

def type_verify(parameter_name, parameter, type_name, expected_type, supported_parameters = None):
        """
        Helper to verify parameters passed to the constructor

        :param parameter_name: Name of the parameter being verified
        :type parameter_name: string
        :param parameter: parameter to be verified
        :param type_name: Name of the type in string
        :type type_name: string
        :param expected_type: expected type of the parameter
        :param supported_parameters: set of supported parameters
        :type supported_parameters: list{string}
        """

        if type(parameter) is not expected_type:
            raise ValueError('{} expects type {}'.format(parameter_name, type_name))
        
        if supported_parameters is not None and parameter not in supported_parameters:
            raise ValueError('{} is not a supported {}'.format(parameter, parameter_name))