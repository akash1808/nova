#    Copyright 2012 IBM Corp.
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

import oslo.config.cfg

from nova.conductor import api as conductor_api


def API(*args, **kwargs):
    use_local = kwargs.pop('use_local', False)
    if oslo.config.cfg.CONF.conductor.use_local or use_local:
        api = conductor_api.LocalAPI
    else:
        api = conductor_api.API
    return api(*args, **kwargs)


def ComputeTaskAPI(*args, **kwargs):
    use_local = kwargs.pop('use_local', False)
    if oslo.config.cfg.CONF.conductor.use_local or use_local:
        api = conductor_api.LocalComputeTaskAPI
    else:
        api = conductor_api.ComputeTaskAPI
    return api(*args, **kwargs)

bypass_scheduler_opt = oslo.config.cfg.BoolOpt('bypass_scheduler',
        default='False',
        help=('whether to use the nova scheduler to make instance '
              'placement decisions or bypass it and place requests '
              'directly on to the message queue for a random node '
              'to fulfill. Use the scheduler by default'))

CONF = oslo.config.cfg.CONF
CONF.register_opt(bypass_scheduler_opt)
