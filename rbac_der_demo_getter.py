# Client-side demonstration of RBAC using pysunspec2

import sunspec2.file.client as file_client
import sunspec2.device as device
import os
import sys

log_file = open("./der_demo_output.txt","w")
sys.stdout = log_file

class RBAC_Interfaces(file_client.FileClientDevice):
    """
    SunSpec Modbus filter that can operate as a gateway or client-side security mechanism
    """

    def __init__(self, inv_path, token=None):
        super(RBAC_Interfaces, self).__init__(inv_path)

        """
        Instantiate a RBAC Modbus filter

        :param inv_path: SunSpec inverter json file for creating a file_client.FileClientDevice object
        :param token: role-based access control token - for now just the str of the role
        """

        self.token = token
        self.role = None
        self.parse_token(self.token)

    def parse_token(self, token):

        if isinstance(token, str):
            self.role = str(token)
        else:  # todo - look into IEC 62351-8 tokens...
            pass

    def print_modbus_map(self, models=None, w_labels=None, print_sf=True):
        """
        Prints the modbus map of the DER device

        :param models: model or models to read, if None read all
        :param w_labels: if True, print the modbus points with labels included
        :param print_sf: if True, print the scale factors for the points
        :return: None
        """

        model_list = []
        if models is None:
            model_list = self.get_models()
        elif isinstance(models, str):
            model_list = [models]
        elif isinstance(models, list):
            model_list = models
        else:
            Exception('Incorrect model format for printing modbus map.')

        if not w_labels:
            for m in model_list:
                mod = eval('self.%s[0]' % m)
                print('%s' % mod)
        else:
            for m in model_list:
                print('-' * 50)
                print('Model: %s' % m)
                print('')
                for pt in eval('self.%s[0].points.keys()' % m):
                    # print('pt: %s' % pt)
                    if pt != 'Pad':
                        if (pt[-3:] == '_SF' and print_sf) or (pt[-3:] != '_SF'):
                            label = eval('self.%s[0].points[pt].pdef["label"]' % m)
                            val = eval('self.%s[0].points[pt].cvalue' % m)
                            rbac = eval('self.%s[0].points[pt].pdef["rbac"]["%s"]' % (m, self.role))
                            if rbac == 'R':
                                permission = "Read Granted/Write Blocked"
                            elif rbac == 'RW':
                                permission = "Read/Write Granted"
                            else:
                                permission = "Read/Write Blocked"

                            if val is not None and eval('self.%s[0].points[pt].pdef.get("symbols")' % m) is not None:
                                symbol = eval('self.%s[0].points[pt].pdef.get("symbols")' % m)
                                # print('Symbols: %s' % symbol)
                                symb = None
                                if symbol is not None:
                                    if isinstance(symbol, list):
                                        for s in symbol:
                                            # print('s: %s' % s)
                                            if val == s.get('value'):
                                                symb = s.get("label")
                                    else:
                                        if symbol.get(val) is not None:
                                            symb = eval('self.%s[0].points[pt].pdef["symbols"][val]["label"]' % m)
                                print('%s [%s]: %s [%s] {%s}' % (label, pt, val, symb, permission))
                            else:
                                print('%s [%s]: %s {%s}' % (label, pt, val, permission))

                # Cycle through groups
                self.print_group(group_obj=eval('self.%s[0]' % m))

    def print_group(self, group_obj, tab_level=2):
        """
        Print out groups. Method calls itself for groups of groups

        :param group_obj: group object, must be a dict
        :param tab_level: print indention

        :return: None
        """
        if isinstance(group_obj.groups, dict):
            for group in group_obj.groups.keys():
                if isinstance(group_obj.groups[group], list):  # list of groups within the group
                    for i in range(len(group_obj.groups[group])):
                        print('\t' * (tab_level - 1) + '-' * 50)
                        print('\t' * (tab_level - 1) + 'Group: %s (#%d)' % (group, i + 1))

                        for pt in group_obj.groups[group][i].points.keys():
                            # print('pt: %s' % pt)
                            if pt != 'Pad':
                                try:
                                    label = group_obj.groups[group][i].points[pt].pdef["label"]
                                except Exception as e:
                                    label = group_obj.groups[group][i].points[pt].pdef["name"]
                                val = group_obj.groups[group][i].points[pt].cvalue
                                try:
                                    rbac = group_obj.groups[group][i].points[pt].pdef["rbac"][self.role]
                                except KeyError:
                                    print('ERROR with label=%s, val=%s' % (label, val))
                                if rbac == 'R':
                                    permission = "Read Granted/Write Blocked"
                                elif rbac == 'RW':
                                    permission = "Read/Write Granted"
                                else:
                                    permission = "Read/Write Blocked"

                                # symbol prints
                                if val is not None and \
                                        group_obj.groups[group][i].points[pt].pdef.get("symbols") is not None:
                                    symbol = group_obj.groups[group][i].points[pt].pdef.get("symbols")
                                    symb = None
                                    if isinstance(symbol, list):
                                        for s in symbol:
                                            # print('s: %s' % s)
                                            if val == s.get('value'):
                                                symb = s.get("label")
                                    else:
                                        if group_obj.symbol.get(val) is not None:
                                            symb = symbol[val]['label']
                                    print(
                                        '\t' * tab_level + '%s [%s]: %s [%s] {%s}' % (label, pt, val, symb, permission))
                                else:
                                    print('\t' * tab_level + '%s [%s]: %s {%s}' % (label, pt, val, permission))

                        # For cases of groups of groups, call this function again
                        new_obj = group_obj.groups[group][i]
                        # print('New Obj = %s' % new_obj)
                        self.print_group(group_obj=new_obj, tab_level=tab_level + 1)
                else:
                    print('\t' * (tab_level - 1) + '-' * 50)
                    print('\t' * (tab_level - 1) + 'Group: %s' % group)
                    for pt in group_obj.groups[group].points.keys():
                        # print('pt: %s' % pt)
                        if pt != 'Pad':
                            label = group_obj.groups[group].points[pt].pdef["label"]
                            val = group_obj.groups[group].points[pt].cvalue
                            rbac = group_obj.groups[group].points[pt].pdef["rbac"][self.role]
                            if rbac == 'R':
                                permission = "Read Granted/Write Blocked"
                            elif rbac == 'RW':
                                permission = "Read/Write Granted"
                            else:
                                permission = "Read/Write Blocked"

                            # symbol prints
                            if val is not None and group_obj.groups[group].points[pt].pdef.get("symbols") is not None:
                                symbol = group_obj.groups[group].points[pt].pdef.get("symbols")
                                symb = None
                                if isinstance(symbol, list):
                                    for s in symbol:
                                        # print('s: %s' % s)
                                        if val == s.get('value'):
                                            symb = s.get("label")
                                else:
                                    if group_obj.symbol.get(val) is not None:
                                        symb = symbol[val]['label']
                                print('\t' * tab_level + '%s [%s]: %s [%s] {%s}' % (label, pt, val, symb, permission))
                            else:
                                print('\t' * tab_level + '%s [%s]: %s {%s}' % (label, pt, val, permission))

                    # For cases of groups of groups, call this function again
                    new_obj = group_obj.groups[group]
                    # print('New Obj = %s' % new_obj)
                    self.print_group(group_obj=new_obj, tab_level=tab_level + 1)
        else:
            print('WARNING: group_obj was not dict')

    def get_models(self):
        """ Get SunSpec Models

        :return: list of models

        """
        model_dict = self.models
        models = []
        for k in model_dict.keys():
            if not isinstance(k, int) and k is not None:
                models.append(k)

        # print('Models = %s' % models)
        return models

    def create_write_rbac(self, verbose=False):
        """
        Removes DER points associated with the role are not permitted to write

        :return: None
        """
        self.edit_rw_points(permission='W', verbose=verbose)

    def create_read_rbac(self, verbose=False):
        """
        Removes DER points associated with the role are not permitted to read

        :return: None
        """
        self.edit_rw_points(permission='R', verbose=verbose)

    def edit_rw_points(self, models=None, permission='R', verbose=False):
        """
        Removes points from SunSpec object associated with the role and permissions

        :param models: model or models to read, if None read all
        :param permission: 'R' read or 'W' write.
        :return: None
        """

        model_list = []
        if models is None:
            model_list = self.get_models()
        elif isinstance(models, str):
            model_list = [models]
        elif isinstance(models, list):
            model_list = models
        else:
            Exception('Incorrect model format for printing modbus map.')

        for m in model_list:
            if verbose:
                print('-' * 50)
                print('Model: %s' % m)
                print('')

            eval_statements = []  # cannot change the point list in the for loop, so store points to remove here
            for pt in eval('self.%s[0].points.keys()' % m):
                # print('pt: %s' % pt)
                if pt != 'Pad':
                    label = eval('self.%s[0].points[pt].pdef["label"]' % m)

                    if verbose:
                        print('%s [%s] {Desired Access: %s}' % (label, pt, permission))
                    # collect points to remove
                    eval_statements.append(self.remove_rbac_points(pt_obj_path='self.%s[0]' % (m), label=label,
                                                                   pt=pt, permission=permission, verbose=verbose))

            # remove points from the points dictionary
            for pops in eval_statements:
                # print('pop commands: %s' % pops)
                if pops is not None:
                    eval(pops)

            # Cycle through groups
            self.edit_rw_groups(group_obj=eval('self.%s[0]' % m))

    def edit_rw_groups(self, group_obj, tab_level=2, permission='R', verbose=False, gpath='self'):
        """
        Removes points from SunSpec group associated with the role and permissions

        :param models: model or models to read, if None read all
        :param tab_level: number of tabs in the print statements
        :param permission: 'R' read or 'W' write.
        :return: None
        """
        if isinstance(group_obj.groups, dict):
            for group in group_obj.groups.keys():
                if isinstance(group_obj.groups[group], list):  # list of groups within the group
                    for i in range(len(group_obj.groups[group])):
                        if verbose:
                            print('\t' * (tab_level - 1) + '-' * 50)
                            print('\t' * (tab_level - 1) + 'Group: %s (#%d)' % (group, i + 1))

                        eval_statements = []
                        for pt in group_obj.groups[group][i].points.keys():
                            # print('pt: %s' % pt)
                            if pt != 'Pad':
                                try:
                                    label = group_obj.groups[group][i].points[pt].pdef["label"]
                                except Exception as e:
                                    label = group_obj.groups[group][i].points[pt].pdef["name"]

                                if verbose:
                                    print('\t' * tab_level + '%s [%s] {Desired Access: %s}' % (label, pt, permission))

                                if gpath == 'self':
                                    pt_obj_path = '%s.%s[0].groups["%s"][%d]' % (gpath, group_obj.gname, group, i)
                                else:
                                    pt_obj_path = '%s.groups["%s"][%d]' % (gpath, group, i)
                                    # print('gpath=%s, group=%s, i=%d' % (gpath, group, i))
                                eval_statements.append(
                                    self.remove_rbac_points(pt_obj_path=pt_obj_path,
                                                            label=label, pt=pt, permission=permission, tab=tab_level,
                                                            verbose=verbose))
                        # remove points from the points dictionary
                        for pops in eval_statements:
                            if pops is not None:
                                eval(pops)

                        # For cases of groups of groups, call this function again
                        new_obj = group_obj.groups[group][i]
                        # print('New Obj = %s' % new_obj)
                        if gpath == 'self':
                            pt_obj_path = '%s.%s[0].groups["%s"][%d]' % (gpath, group_obj.gname, group, i)
                        else:
                            pt_obj_path = '%s.groups["%s"][%d]' % (gpath, group, i)
                        self.edit_rw_groups(group_obj=new_obj, tab_level=tab_level + 1, gpath=pt_obj_path)
                else:
                    if verbose:
                        print('\t' * (tab_level - 1) + '-' * 50)
                        print('\t' * (tab_level - 1) + 'Group: %s' % group)

                    eval_statements = []  # cannot change the point list in the for loop, so store points to remove here
                    for pt in group_obj.groups[group].points.keys():
                        # print('pt: %s' % pt)
                        if pt != 'Pad':
                            label = group_obj.groups[group].points[pt].pdef["label"]

                            if verbose:
                                print('\t' * tab_level + '%s [%s] {Desired Access: %s}' % (label, pt, permission))

                            if gpath == 'self':
                                pt_obj_path = '%s.%s[0].groups["%s"]' % (gpath, group_obj.gname, group)
                            else:
                                pt_obj_path = '%s.groups["%s"]' % (gpath, group)
                                # print('gpath=%s, group=%s' % (gpath, group))
                            eval_statements.append(
                                self.remove_rbac_points(pt_obj_path=pt_obj_path,
                                                        label=label, pt=pt, permission=permission, tab=tab_level,
                                                        verbose=verbose))

                    # remove points from the points dictionary
                    for pops in eval_statements:
                        if pops is not None:
                            eval(pops)

                    # For cases of groups of groups, call this function again
                    new_obj = group_obj.groups[group]
                    # print('New Obj = %s' % new_obj)
                    if gpath == 'self':
                        pt_obj_path = '%s.%s[0].groups["%s"]' % (gpath, group_obj.gname, group)
                    else:
                        pt_obj_path = '%s.groups["%s"]' % (gpath, group)
                    self.edit_rw_groups(group_obj=new_obj, tab_level=tab_level + 1, verbose=verbose, gpath=pt_obj_path)
        else:
            print('WARNING: group_obj was not dict')

    def remove_rbac_points(self, pt_obj_path, label, pt, permission, tab=0, verbose=False):
        """
        Removes sunspec points based on permission, role, and object

        :param pt_obj_path: SunSpec object path may be removed, e.g., "inv.common[0].points['ID']"
        :param label: label of the point
        :param pt: point_name
        :param permission: R or W permission used to remove the point
        :param tab: number of tabs in the print
        :param verbose: print status when true
        :return: None
        """

        try:
            # print('%s.points["%s"].pdef["rbac"]["%s"]' % (pt_obj_path, pt, self.role))
            rbac = eval('%s.points["%s"].pdef["rbac"]["%s"]' % (pt_obj_path, pt, self.role))  # get the RBAC access
        except KeyError:
            print('ERROR with label=%s, val=%s' % (label, val))

        # check permissions for role. If no access, delete the SunSpec point
        if (rbac == '' or rbac == 'W') and permission == 'R':
            if verbose:
                print('\t' * 2 + 'Removing %s [%s]. RBAC Role-to-Right map for this point: "%s"' % (label, pt, rbac))
                print('\t' * 2 + 'Deleting %s' % str(pt_obj_path + '.points["%s"]' % pt).rstrip())
            return '%s.points.pop("%s")' % (pt_obj_path, pt)

        if (rbac == '' or rbac == 'R') and permission == 'W':
            if verbose:
                print('\t' * 2 + 'Removing %s [%s]. RBAC Role-to-Right map for this point: "%s"' % (label, pt, rbac))
                print('\t' * 2 + 'Deleting %s' % str(pt_obj_path + '.points["%s"]' % pt).rstrip())

            # special case for scale factors. Cannot remove them from the write objects if they are used for writing.
            # todo: remove SF points that are not used for write permission points
            if pt[-3:] == '_SF':
                return None

            return '%s.points.pop("%s")' % (pt_obj_path, pt)


''' Future work to create single object that handles all the read/writes
class RBAC_Inverter(object):
    """ Mapped DER with RBAC rules """

    def __init__(self, inv_path, role):
        """

        :param role: The role for the DER device
        """
        self.role = role

        # Create DER object with only the read permissions for the role
        self.read_inv = RBAC_Interfaces(inv_path=inv_path, token=self.role)
        self.read_inv.scan()
        self.read_inv.create_read_rbac(verbose=False)
        # print('\n **** Read permissions for role = %s' % self.role)
        # self.read_inv.print_modbus_map(models=None, w_labels=True)

        print('\n **** Read permissions for role = %s' % self.role)
        self.read_inv.print_modbus_map(models='common', w_labels=True)

        # Create DER object with only the write permissions for the role
        self.write_inv = RBAC_Interfaces(inv_path=inv_path, token=self.role)
        self.write_inv.scan()
        self.write_inv.create_write_rbac(verbose=False)
        # print('\n **** Write permissions for role = %s' % self.role)
        # self.write_inv.print_modbus_map(models=None, w_labels=True)

    def __get__(self, instance, owner):
        self.read_inv.__get__(item)

    def __getitem__(self, item):
        self.read_inv.__getitem__(item)

    def __getattr__(self, item):
        self.read_inv.__getattr__(item)

    def __set__(self, instance, value):
        self.write_inv.__set__(instance, value)

    def __set_name__(self, owner, name):
        self.write_inv.__set_name__(owner, name)

    def __setitem__(self, key, value):
        self.write_inv.__setitem__(key, value)

    def __setslice__(self, i, j, sequence):
        self.write_inv.__setslice__(i, j, sequence)

    def __setstate__(self, state):
        self.write_inv.__setattr__(state)

'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


DER_OWNER_PERM = {}
INSTALLER_PERM = {}
DER_VENDOR_PERM = {}
SERVICE_PROVIDER_PERM = {}
THIRD_PARTY_PERM = {}
AGGREGATOR_PERM = {}
UTILITY_PERM = {}
DSO_PERM = {}
ISO_PERM = {}
RTO_PERM = {}
TSO_PERM = {}
SECURITY_ADMIN_PERM = {}
SECURITY_AUDITOR_PERM = {}
RBAC_ADMIN_PERM = {}

def main():
    path = os.getcwd()
    device.model_defs_path.insert(0, os.path.join(path,'rbac_json'))  # override the model in SunSpec with the rbac_json models
    inv_path = os.path.join(path,'sunspec_device_1547.json')


    rbac_roles = [
        'der_owner',
        'installer',
        'der_vendor_or_service_provider',
        '3rd_party_or_aggregator',
        'utility_or_dso',
        'iso_rto_tso',
        'security_administrator',
        'security_auditor',
        'rbac_administrator',
    ]

    for r in rbac_roles:
        print(bcolors.HEADER + '\n **** Testing Permissions for role = %s' % r + bcolors.ENDC)

        print_permissions_for_role = False
        if print_permissions_for_role:
            inv = RBAC_Interfaces(inv_path=inv_path, token=r)  # DER object with all the functionality
            inv.scan()
            print('\n **** Read/Write permissions for role = %s' % r)
            # inv.print_modbus_map(models='common', w_labels=True)
            inv.print_modbus_map(models=None, w_labels=True)

        # Create DER object with only the read permissions for the role
        read_inv = RBAC_Interfaces(inv_path=inv_path, token=r)
        read_inv.scan()
        read_inv.create_read_rbac(verbose=False)
        # print('\n **** Read permissions for role = %s' % r)
        # read_inv.print_modbus_map(models=None, w_labels=True, print_sf=False)

        # Create DER object with only the write permissions for the role
        write_inv = RBAC_Interfaces(inv_path=inv_path, token=r)
        write_inv.scan()
        write_inv.create_write_rbac(verbose=False)
        # print('\n **** Write permissions for role = %s' % r)
        # write_inv.print_modbus_map(models=None, w_labels=True, print_sf=False)

        # Since this is a simulated DER stored in two objects in memory, when there is a write on
        # the write_inv, the read_inv must be updated as well.  A single object that accounts for that
        # update process should be built in the future.  Note that the SunSpec Modbus server will
        # act in that role in a physical device.

        # change inverter manufacturer
        try:
            read_inv.common[0].read()
            print(bcolors.OKBLUE + 'Original Manufacturer Setting:' + bcolors.ENDC)
            print(read_inv.common[0].Md.cvalue)
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read Manufacturer for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            write_inv.common[0].Md.cvalue = 'FakeMfr'
            write_inv.DERCapacity[0].write()
            # mirror action in read device, no need for write since it's simulated DER
            try:
                read_inv.common[0].Md.cvalue = 'FakeMfr'
            except Exception as e:
                print(
                    bcolors.FAIL + 'RBAC ERROR - Unable to write Manufacturer into read DER for role %s: %s' %
                    (r, e) + bcolors.ENDC)
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR in Manufacturer write for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            read_inv.common[0].read()
            print(bcolors.OKBLUE + 'Updated Manufacturer Setting:' + bcolors.ENDC)
            print(read_inv.common[0].Md.cvalue)

            if (r == 'der_owner'):
                DER_OWNER_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
            elif (r == 'installer'):
                INSTALLER_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
            elif(r == 'der_vendor_or_service_provider'):
                DER_VENDOR_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
                SERVICE_PROVIDER_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
            elif(r == '3rd_party_or_aggregator'):
                THIRD_PARTY_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
                AGGREGATOR_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
            elif(r == 'utility_or_dso'):
                UTILITY_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
                DSO_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
            elif(r == 'iso_rto_tso'):
                ISO_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
                RTO_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue
                TSO_PERM['Manufacturer_Setting'] = read_inv.common[0].Md.cvalue



        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read Manufacturer for role %s: %s' % (r, e) + bcolors.ENDC)

        # change nameplate rating of the DER
        try:
            read_inv.DERCapacity[0].read()
            print(bcolors.OKBLUE + '\nOriginal WMaxRtg Setting:' + bcolors.ENDC)
            print(str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n'))
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read WMaxRtg for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            write_inv.DERCapacity[0].WMaxRtg.cvalue = 5000
            write_inv.DERCapacity[0].write()
            # mirror action in read device, no need for write since it's simulated DER
            try:
                read_inv.DERCapacity[0].WMaxRtg.cvalue = 5000
            except Exception as e:
                print(bcolors.FAIL + 'RBAC ERROR - Unable to write WMaxRtg into read DER for role %s: %s' %
                      (r, e) + bcolors.ENDC)
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR in WMaxRtg write for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            read_inv.DERCapacity[0].read()
            print(bcolors.OKBLUE + 'Updated WMaxRtg Setting:' + bcolors.ENDC)
            print(str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n'))

            if (r == 'der_owner'):
                DER_OWNER_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
            elif (r == 'installer'):
                INSTALLER_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == 'der_vendor_or_service_provider'):
                DER_VENDOR_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
                SERVICE_PROVIDER_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == '3rd_party_or_aggregator'):
                THIRD_PARTY_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
                AGGREGATOR_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == 'utility_or_dso'):
                UTILITY_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
                DSO_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == 'iso_rto_tso'):
                ISO_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
                RTO_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()
                TSO_PERM['WMaxRtg'] = str(read_inv.DERCapacity[0].WMaxRtg).rstrip('\n').split(':',1)[1].lstrip()


        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read WMaxRtg for role %s: %s' % (r, e) + bcolors.ENDC)

        # change maximum voltage setting of the DER
        try:
            read_inv.DERCapacity[0].read()
            print(bcolors.OKBLUE + '\nOriginal VMax Setting:' + bcolors.ENDC)
            print(str(read_inv.DERCapacity[0].VMax).rstrip('\n'))
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read VMax for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            write_inv.DERCapacity[0].VMax.cvalue = 280
            write_inv.DERCapacity[0].write()
            # mirror action in read device, no need for write since it's simulated DER
            try:
                read_inv.DERCapacity[0].VMax.cvalue = 280
            except Exception as e:
                print(bcolors.FAIL + 'RBAC ERROR - Unable to write VMax into read DER for role %s: %s' %
                      (r, e) + bcolors.ENDC)
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR in VMax write for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            read_inv.DERCapacity[0].read()
            print(bcolors.OKBLUE + 'Updated VMax Setting:' + bcolors.ENDC)
            print(str(read_inv.DERCapacity[0].VMax).rstrip('\n'))

            if r == 'der_owner':
                DER_OWNER_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
            elif (r == 'installer'):
                INSTALLER_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == 'der_vendor_or_service_provider'):
                DER_VENDOR_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
                SERVICE_PROVIDER_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == '3rd_party_or_aggregator'):
                THIRD_PARTY_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
                AGGREGATOR_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == 'utility_or_dso'):
                UTILITY_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
                DSO_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
            elif(r == 'iso_rto_tso'):
                ISO_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
                RTO_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()
                TSO_PERM['VMax'] = str(read_inv.DERCapacity[0].VMax).rstrip('\n').split(':',1)[1].lstrip()


        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read VMax for role %s: %s' % (r, e) + bcolors.ENDC)

        # Write a volt-var curve
        try:
            read_inv.DERVoltVar[0].read()
            print(bcolors.OKBLUE + '\nOriginal VV Curve Settings:' + bcolors.ENDC)
            print(str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n'))
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read VV curve for role %s: %s' % (r, e) + bcolors.ENDC)
        v_pts = [95, 99, 101, 105]
        q_pts = [100, 0, 0, -100]
        try:
            for i in range(len(v_pts)):
                write_inv.DERVoltVar[0].Crv[0].Pt[i].V.cvalue = v_pts[i]
                write_inv.DERVoltVar[0].Crv[0].Pt[i].Var.cvalue = q_pts[i]
                # mirror the changes in the read DER
                try:
                    for i in range(len(v_pts)):
                        read_inv.DERVoltVar[0].Crv[0].Pt[i].V.cvalue = v_pts[i]  # mirror
                        read_inv.DERVoltVar[0].Crv[0].Pt[i].Var.cvalue = q_pts[i]  # mirror
                except Exception as e:
                    print(
                        bcolors.FAIL + 'RBAC ERROR - Unable to write VV curve into read DER for role %s: %s' %
                        (r, e) + bcolors.ENDC)
        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR in VV write for role %s: %s' % (r, e) + bcolors.ENDC)
        try:
            read_inv.DERVoltVar[0].read()
            print(bcolors.OKBLUE + 'Updated VV Curve Settings:' + bcolors.ENDC)
            print(str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n'))

            if r == 'der_owner':
                DER_OWNER_PERM['Crv(1)'] = []
                temp_perm = str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n').split('\n ')
                for i in range(1,len(temp_perm)):
                    if(temp_perm[i].split(':',1)[1] != '') :
                        DER_OWNER_PERM['Crv(1)'].append(temp_perm[i])
                if len(DER_OWNER_PERM['Crv(1)']) == 0 :
                    del DER_OWNER_PERM['Crv(1)']
            elif r == 'installer':
                INSTALLER_PERM['Crv(1)'] = []
                temp_perm = str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n').split('\n ')
                for i in range(1,len(temp_perm)):
                    INSTALLER_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
            elif(r == 'der_vendor_or_service_provider'):
                DER_VENDOR_PERM['Crv(1)'] = []
                SERVICE_PROVIDER_PERM['Crv(1)'] = []
                temp_perm = str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n').split('\n ')
                for i in range(1,len(temp_perm)):
                    DER_VENDOR_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
                    SERVICE_PROVIDER_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
            elif(r == '3rd_party_or_aggregator'):
                THIRD_PARTY_PERM['Crv(1)'] = []
                AGGREGATOR_PERM['Crv(1)'] = []
                temp_perm = str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n').split('\n ')
                for i in range(1,len(temp_perm)):
                    THIRD_PARTY_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
                    AGGREGATOR_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
            elif(r == 'utility_or_dso'):
                UTILITY_PERM['Crv(1)'] = []
                DSO_PERM['Crv(1)'] = []
                temp_perm = str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n').split('\n ')
                for i in range(1,len(temp_perm)):
                    UTILITY_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
                    DSO_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
            elif(r == 'iso_rto_tso'):
                ISO_PERM['Crv(1)'] = []
                RTO_PERM['Crv(1)'] = []
                TSO_PERM['Crv(1)'] = []
                temp_perm = str(read_inv.DERVoltVar[0].Crv[0]).rstrip('\n').split('\n ')
                for i in range(1,len(temp_perm)):
                    ISO_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
                    RTO_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())
                    TSO_PERM['Crv(1)'].append(temp_perm[i].lstrip().rstrip())

        except Exception as e:
            print(bcolors.FAIL + 'RBAC ERROR - Unable to read VV curve for role %s: %s' % (r, e) + bcolors.ENDC)

    print()
    print('****************************************************************** Roles to Rights Mapping Data *******************************************************************************')
    print('*******************************************************************************************************************************************************************************')
    print()
    print('DER OWNER PERMISSIONS: ' + str(DER_OWNER_PERM))
    print()
    print('INSTALLER PERMISSIONS: ' + str(INSTALLER_PERM))
    print()
    print('DER VENDOR PERMISSIONS: ' + str(DER_VENDOR_PERM))
    print()
    print('SERVICE PROVIDER PERMISSIONS: ' + str(SERVICE_PROVIDER_PERM))
    print()
    print('THIRD PARTY PERMISSIONS: ' + str(THIRD_PARTY_PERM))
    print()
    print('AGGREGATOR PERMISSIONS: ' + str(AGGREGATOR_PERM))
    print()
    print('UTILITY PERMISSIONS: ' + str(UTILITY_PERM))
    print()
    print('DSO PERMISSIONS: ' + str(DSO_PERM))
    print()
    print('ISO PERMISSIONS: ' + str(ISO_PERM))
    print()
    print('RTO PERMISSIONS: ' + str(RTO_PERM))
    print()
    print('TSO PERMISSIONS: ' + str(TSO_PERM))
    print()
    print('SECURITY ADMIN PERMISSIONS: ' + str(SECURITY_ADMIN_PERM))
    print()
    print('SECURITY AUDITOR PERMISSIONS: ' + str(SECURITY_AUDITOR_PERM))
    print()
    print('RBAC ADMIN PERMISSIONS: ' + str(RBAC_ADMIN_PERM))
    print()
    print('*******************************************************************************************************************************************************************************')
    print('*******************************************************************************************************************************************************************************')


    # Todo: create single object that performs all reads/writes seamlessly

    # der_owner_der = RBAC_Inverter(inv_path=inv_path, role=r)
    #
    # print(der_owner_der.read_inv.common[0])
    # print(der_owner_der.common[0])
    #
    # der_owner_der.commmon[0].Mn = 'RBAC Test'
    # print(der_owner_der.write_inv.common[0])
    # print(der_owner_der.common[0])


if __name__ == "__main__":
    main()
