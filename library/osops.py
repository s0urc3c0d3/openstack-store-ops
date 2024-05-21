#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule


import openstack
from time import sleep

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        flavor=dict(type='str', required=True),
        sleep=dict(type='int', required=False, default=5),
        retry=dict(type='int', required=False, default=10),
        auth=dict(type='dict', required=True, options=dict(
            auth_url=dict(type='str',required=True),
            project_name=dict(type='str',required=True),
            username=dict(type='str',required=True),
            password=dict(type='str',required=True),
            region_name=dict(type='str',required=False, default='RegionOne'),
            user_domain_name=dict(type='str',required=True),
            project_domain_name=dict(type='str',required=True)
            )
        )
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'


    conn = openstack.connect(auth_url=module.params['auth']['auth_url'],
        project_name=module.params['auth']['project_name'],
        username=module.params['auth']['username'],
        password=module.params['auth']['password'],
        region_name=module.params['auth']['region_name'],
        user_domain_name=module.params['auth']['user_domain_name'],
        project_domain_name=module.params['auth']['project_domain_name'])

    instance = conn.search_servers(module.params['name'])[0]
    flavor = conn.search_flavors(module.params['flavor'])[0]

    conn.compute.resize_server(instance,flavor)

    licznik=0
    sukces=0

    while (licznik < module.params['retry'] and sukces == 0):
        if conn.compute.get_server(instance).status == 'VERIFY_RESIZE':
            conn.compute.confirm_server_resize(instance)
            sukces=1
        sleep(module.params['sleep'])
        licznik=licznik+1

    if sukces == 1:
        result['changed'] = True
    else:
        module.fail_json(msg='Resize did not end in specified time window', **result)


    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
