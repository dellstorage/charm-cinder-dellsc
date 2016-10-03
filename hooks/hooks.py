#!/usr/bin/python

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

"""Charm event hooks."""

import json
import sys

from charmhelpers.core import hookenv
from charmhelpers.payload import execd

import cinder_contexts

HOOKS = hookenv.Hooks()


@HOOKS.hook('install')
def install():
    """Perform ``install`` handling."""
    execd.execd_preinstall()


@HOOKS.hook('config-changed', 'upgrade-charm')
def upgrade_charm():
    """Perform ``config-changed`` or ``upgrade-charm`` handling."""
    for rid in hookenv.relation_ids('storage-backend'):
        storage_backend(rid)


@HOOKS.hook('storage-backend-relation-joined',
            'storage-backend-relation-changed',
            'storage-backend-relation-broken')
def storage_backend(rid=None):
    """Perform relation change handling.

    This handles ``storage-backend-relation-joined``,
    ``storage-backend-relation-changed``, and
    ``storage-backend-relation-broken`` events.

    :param rid: The relationship ID.
    """
    hookenv.relation_set(
        relation_id=rid,
        backend_name=hookenv.service_name(),
        subordinate_configuration=json.dumps(cinder_contexts.DellScContext())
    )


if __name__ == '__main__':
    try:
        HOOKS.execute(sys.argv)
    except hookenv.UnregisteredHookError as e:
        hookenv.log('Unknown hook %s' % e)
