# Dell Storage Center Backend for Cinder

## Overview

This charm provides a Dell SC storage backend for use with the Cinder charm.
This allows one or more SC arrays to be used in a Cinder deployment,
potentially along side other storage backends from other vendors.

To use:

    juju deploy cinder
    juju deploy cinder-dellsc
    juju add-relation cinder-dellsc cinder

Note: To use a local copy of the charm, you may need to clone a local copy
and move it into a subdirectory for your version:

    mkdir xenial
    mv charm-cinder-dellsc xenial/
    juju deploy --repository=. local:xenial/cinder-dellsc


## Configuration

The cinder-dellsc charm requires configuration to allow the driver to access
the storage management APIs for the Dell SC array:

    cinder-dellsc:
        protocol: iscsi
        mgmt-ip: dsm.host.or.ip
        mgmt-username: Admin
        mgmt-password: password
        dellsc-ssn: 11111

There are also additional configuration options that may be set to customize
behavior for your environment:

        api-port: 3033
        server-folder: openstack_servers
        volume-folder: openstack_volumes
        iscsi-port: 3260

Update these values in config.yaml prior to deploying the charm.

## Getting Help

For general information on Juju Charm usage, please see the official
[Juju Charms](https://jujucharms.com/) site.

For specific issues with the Dell SC charm, file a
[GitHub Issue](https://github.com/dellstorage/charm-dellsc/issues).

If you have any suggestions for an improvements, please feel free create a fork
in your repository, make any changes, and submit a pull request to have the
changes considered for merging. Community collaboration is welcome!

**As a community project, no warranties are provided for the use of this code.**

## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
