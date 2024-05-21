import openstack
from time import sleep

vmname = 'srv'

target_flavor = 'c2'

conn = openstack.connect(auth_url='http://192.168.122.170:5000',project_name='admin',username='gd',password='test123',region_name='RegionOne',user_domain_name='Default',project_domain_name='Default')

instance = conn.search_servers('srv')[0]

flavor = conn.search_flavors('c2')[0]

conn.compute.resize_server(instance,flavor)

licznik=0
sukces=0
while (licznik < 20 and sukces == 0):
  print("iteracja:",licznik," ",conn.compute.get_server(instance).status)
  if conn.compute.get_server(instance).status == 'VERIFY_RESIZE':
    print("confirm")
    conn.compute.confirm_server_resize(instance)
    sukces=1
  sleep(1)
  licznik=licznik+1
  
if sukces == 1:
  print("udalo sie")
else:
  print("nie udalo sie")

#connector = openstack.connect(cloud="piasprod",verify=False)
