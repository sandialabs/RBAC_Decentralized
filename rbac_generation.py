"""
World
    Corporation
        DERs
        User
            Role
"""


import names
import random
import pprint

random.seed(0)   # Always generate the same dataset

n_utilities  = 5
n_providers  = 6
n_sp         = 5
admins       = 4
sec_auditors = 2
n_der = n_utilities * n_providers * 50
total_accounts = n_utilities + n_providers + n_sp + admins + sec_auditors + n_der + n_der
der_per_util = int(n_der/n_utilities)
der_per_sp = int(n_der/n_providers)

der_list = []
for d in range(1, n_der+1):
    der_list.append('DER %d' % d)

# create utilities
rbac = {}
for corporation in range(n_utilities):
    utilities_people = random.randint(20,60)
    total_accounts = total_accounts + utilities_people
    rbac['Utility %d' % (corporation + 1)] = {}
    util_slice = [corporation * der_per_util, (corporation + 1) * der_per_util - 1]
    # DER under the utility's control
    rbac['Utility %d' % (corporation + 1)]['DER'] = der_list[util_slice[0]: util_slice[1]]
    for people in range(utilities_people):
        for role in ['Utility DERMS Team', 'Utility Software', 'Utility Billing', 'Utility Auditing']:
            rbac['Utility %d' % (corporation + 1)][names.get_full_name()] = role

# create service providers
for corporation in range(n_sp):
    sp_people = random.randint(10,30)
    total_accounts = total_accounts + sp_people
    rbac['Service Provider %d' % (corporation + 1)] = {}
    sp_slice = [corporation * der_per_sp, (corporation + 1) * der_per_sp - 1]
    # DER under the service provider's control
    random.shuffle(der_list)  # randomize the list so different SPs and utilities want access to the DER
    rbac['Service Provider %d' % (corporation + 1)]['DER'] = der_list[sp_slice[0]: sp_slice[1]]
    for people in range(sp_people):
        for role in ['DER Installers', 'Aggregation/VPP Team', 'Firmware/Patching', 'Billing', 'Utility Auditing']:
            rbac['Service Provider %d' % (corporation + 1)][names.get_full_name()] = role

# DER owners
rbac['DER Owner'] = {}
rbac['DER Device'] = {}
for people in range(n_der):
    for role in ['DER Owner']:
        name = names.get_full_name()
        rbac['DER Owner'][name] = role

        # Fixed: Create a dictionary with all the DER Owners and their DER Devices that they own
        rbac['DER Device'][name] = 'DER %d' % (people + 1)


# RBAC Admins
rbac['Security Administrator'] = {}
for people in range(admins):
    for role in ['Security Administrator']:
        rbac['Security Administrator'][names.get_full_name()] = role

# RBAC Auditor
rbac['Security Auditor'] = {}
for people in range(sec_auditors):
    for role in ['Security Auditor']:
        rbac['Security Auditor'][names.get_full_name()] = role

#pprint.pprint(rbac)