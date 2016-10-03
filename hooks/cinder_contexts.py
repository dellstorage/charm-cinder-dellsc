#    Copyright 2016 Dell Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Helper for generating template context to be added to cinder.conf."""

from charmhelpers.contib.openstack import context
from charmhelpers.core import hookenv


class DellScInvalidConfigException(Exception):
    """Exception thrown if required config settings are missing."""


class DellScContext(context.OSContextGenerator):
    """Dell SC Cinder driver config generator."""

    def __call__(self):

        config_keys = {
            'mgmt-ip': 'san_ip',
            'mgmt-username': 'san_login',
            'mgmt-password': 'san_password',
            'dellsc-ssn': 'dell_sc_ssn',
            'api-port': 'dell_sc_api_port',
            'server-folder': 'dell_sc_server_folder',
            'volume-folder': 'dell_sc_volume_folder',
            'iscsi-port': 'iscsi_port',
        }

        required_keys = ['protocol', 'mgmt-ip',
                         'mgmt-password', 'dellsc-ssn']

        driver_base = 'cinder.volume.drivers.dell.dell_storagecenter_%s'
        drivers = {
            'iscsi': driver_base % 'iscsi.DellStorageCenterISCSIDriver',
            'fc': driver_base % 'fc.DellStorageCenterFCDriver',
        }

        for key in required_keys:
            if not hookenv.config(key):
                raise DellScInvalidConfigException(
                    'Missing required config setting "%s"' % key)

        protocol = hookenv.config('protocol').lower()
        if protocol not in drivers.keys():
            raise DellScInvalidConfigException(
                '"%s" is not a valid protocol option' % protocol)

        service = hookenv.service_name()
        driver_config = {
            'volume_backend_name': service,
            'volume_driver': drivers[protocol],
        }

        for k in config_keys.keys():
            value = hookenv.config(k)
            if value:
                driver_config[config_keys[k]] = value

        return {
            'cinder': {
                '/etc/cinder/cinder.conf': {
                    'sections': {
                        service: driver_config
                    }
                }
            }
        }
