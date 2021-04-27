#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: geo_fragkos
@scope : Use of Web3.py library to connect with Ethereum Private blockchain
         and interact with RBAC.sol.

         Automating the process of connecting to the blockchain and interacting with the
         RBAC.sol smart contract. The automation and population of the Ethereum blockchain
         is based on the provided
"""


#%% -- Contract Creation -- %%
from web3 import Web3, HTTPProvider
import json
import subprocess
import rbac_generation
import time
from web3.auto import w3
import sys
import os
import signal
import rbac_der_demo_getterv2 as getter

start = time.time()
log_file = open("./log.txt","w")
sys.stdout = log_file


blockchain_network_id = sys.argv[1]                            # Blockchain Network ID: Defined by Admin
#blockchain_network_id = 1200
blockchain_accounts   = rbac_generation.total_accounts + 1      # Total Accounts in the Ethereum Network - defined by rbac_generation.py
net_ip = '127.0.0.1'  # Demo running in localhost
port   =  '9545'

print('************************************** Blockchain Account Generation **************************************')
pro = subprocess.Popen(['./accounts_creator.sh %s %s %s %s' %(blockchain_network_id, blockchain_accounts, port, '.ganache/data'+str(blockchain_network_id))], shell = True)

t = 65                                                      # Sleep for 30 seconds until the subprocess has began
time.sleep(t)
print('***********************************************************************************************************')
print()
print()

print('************************ Connect with Ethereum Blockchain at http://localhost:'+ str(port) +' ***************************************')
# Private Ethereum Blockchain Address provided by ganache-cli tool
blockchain_address = 'http://'+net_ip+':'+port

# Node instance to interact with the Private Ethereum blockchain
web3 = Web3(HTTPProvider(blockchain_address,request_kwargs={'timeout': 120}))
print('Connection with Private Ethereum Blockchain:' + str(web3.isConnected()))

# Set the default account - Administrator's Address in the RBAC Model [Account 0]
web3.eth.defaultAccount = web3.eth.accounts[0]
print('RBAC Administrator Address:'+str(web3.eth.defaultAccount))


# Migrate the RBAC.sol Smart Contract for potential changes
# Note: If you have new functions in your smart contract enable the --reset flag
print('************************************** RBAC Smart Contract Migration **************************************')
subprocess.Popen(['./RBAC_sc_migrator.sh'], shell=True)
t = 120       # Sleep for 30 seconds until the subprocess has began
time.sleep(t)
print('***********************************************************************************************************')
print()
print()

# Path to the compiled RBAC smart contract JSON file -- This is configurable
compiled_contract_path = '/home/george/Desktop/Sandia_RBAC/Decentralized_Ethereum/build/contracts/RBAC.json'

# Contract Address - Get that from Json File after Smart Contract Migration [Automatic]
with open(compiled_contract_path) as file:
    contract_json = json.load(file)       # Load Contract Information as JSON file
    contract_abi  = contract_json['abi']  # Fetch RBAC smart contract's abi - Call its functions
    contract_address  = contract_json['networks'][str(blockchain_network_id)]['address']


# Fetch deployed RBAC smart contract instance
contract = web3.eth.contract(address = contract_address, abi = contract_abi)
print('Deployed RBAC Contract Address:' + str(contract_address))
print('****************************************************************************************************************************')
print()
print()



#%% -- Helper Functions/Queries that connect with the Ethereum Blockchain --
# They all connect with the RBAC.sol in the Ethereum Blockchain [Queries - No transactions]
def find_Address(username):
    util_address =  contract.functions.profileAddress(username).call()
    return util_address

def find_Username(address):
    username = contract.functions.profileUsername(address).call()
    return username

def findAssociation(child_entity, parent_entity):
    ischild = contract.functions.isChild(child_entity, parent_entity).call()
    return ischild

def findAssociationAddress(child_entity_addr, parent_entity_addr):
    ischild = contract.functions.isChild_address(child_entity_addr, parent_entity_addr).call()
    return ischild

def findAllChildren(username):
    children_list = contract.functions.getChildrenNames(username).call()
    time.sleep(5)
    for child in children_list:
        child_string = Web3.toText(child)
        child_string = child_string.split("\x00")
        final_child_string = child_string[0]
        print(final_child_string)

def findAllChildrenAddress(address):
    children_list = contract.functions.getChildrenAddresses(address).call()
    for child in children_list:
        print(child)

def getRolesFromNames(username):
    roles_list = contract.functions.getRolesfromNames(username).call()
    for _role in roles_list:
        role_string = Web3.toText(_role)
        role_string = role_string.split("\x00")
        final_role_string = role_string[0]
        print(final_role_string)

def getRolesFromAddress(address):
    roles_list = contract.functions.getRolesfromAddress(address).call()
    for _role in roles_list:
        role_string = Web3.toText(_role)
        role_string = role_string.split("\x00")
        final_role_string = role_string[0]
        print(final_role_string)

def hasrole(username, role):
    flag = contract.functions.hasRole(username, role).call()
    return flag
### ------------------------------------------------------------


account_index = 1           # Keep track of the accounts

#%% -- Automatically Create DERs' Profiles (In case that we assume that they will have a public/private pair)--
print('************************************** Utilities Automation **************************************')
for i in range(1, len(rbac_generation.der_list) + 1):   # The first Ethereum account is of the RBAC Administrator
    # Check if that account already exists in the Ethereum blockchain
    username = rbac_generation.der_list[i-1]
    if(find_Address(username) != '0x0000000000000000000000000000000000000000'):     # 0x000.. -> No such address exists in the blockchain
        account_index  = account_index + 1
        continue

    der_account = web3.eth.accounts[i]
    created_profile_hash = contract.functions.createProfile(username, der_account).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
    mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
    account_index  = account_index + 1          # Update account index tracker
    print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')
    print()

#%% -- Automatically Create Utilities' Profiles --
for i in range(1,rbac_generation.n_utilities+1):
    username     = 'Utility ' + str(i)
    util_account = web3.eth.accounts[i - 1 + account_index]
    if(find_Address(username) == '0x0000000000000000000000000000000000000000'):     # 0x000.. -> No such address exists in the blockchain
        created_profile_hash = contract.functions.createProfile(username, util_account).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

        # -- Create Permissions for this person -- #
        for ( model,perms ) in getter.perm_dict['utility_or_dso'].items():
            perms_string = json.dumps(perms[0])
            created_perm_hash = contract.functions.addPermissions(username, str(model), util_account, perms_string).transact()
            # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
            tx_receipt = web3.eth.waitForTransactionReceipt(created_perm_hash)
            mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
            print('New Permission with hash ' + str(str(Web3.toHex(created_perm_hash))) + ' is successfully created!')



    if (i == rbac_generation.n_utilities):
        account_index  = account_index + rbac_generation.n_utilities        # Update account index tracker



    # Add the entities under the Utilities organization -- DERs and People
    person_account_temp = 0
    for entity in rbac_generation.rbac[username]:
        if entity == 'DER':  # Value of nested dictionary: DERs that are associated with this Utility
            util_der_list = rbac_generation.rbac[username][entity]
            for der in util_der_list:
                der_address   = find_Address(der)  # Find the Ethereum address of the DER

                # Create new Association: 'Utility X' controls 'DER Y'
                already_created_flag = contract.functions.isChild(der, username).call()   # Check if this association is already existing in the blockchain
                if(not already_created_flag):
                    created_assoc = contract.functions.addChild(der, username, der_address, util_account).transact()
                    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                    tx_receipt = web3.eth.waitForTransactionReceipt(created_assoc)
                    mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                    print('New Association: '+ str(der)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')
                    print()

        else:               # Value of nested dictionary: People -- Create new profiles AND associations with this utility
            # Create new Association: 'Person Y' belongs to 'Utility X'
            if(find_Address(entity) == '0x0000000000000000000000000000000000000000'):     # 0x000.. -> No such address exists in the blockchain
                entity_account = web3.eth.accounts[person_account_temp + account_index]
                created_profile_hash = contract.functions.createProfile(entity, entity_account).transact()
                # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
                mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')
                print()


            already_created_flag = contract.functions.isChild(entity, username).call()
            if(not already_created_flag):
                person_account = web3.eth.accounts[person_account_temp + account_index]
                created_assoc = contract.functions.addChild(entity, username, person_account, util_account).transact()
                # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                tx_receipt = web3.eth.waitForTransactionReceipt(created_assoc)
                mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                print('New Association: '+ str(entity)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')
                print()

            # Create New Role: 'Person Y' has 'Role X'
            role = rbac_generation.rbac[username][entity]
            already_created_flag = hasrole(entity, role)
            if(not already_created_flag):
                # Add the roles to people
                created_utr = contract.functions.addRoleToUser(entity, person_account, role).transact()
                # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                tx_receipt = web3.eth.waitForTransactionReceipt(created_utr)
                mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                print('New User to Role Assignment: '+ str(entity)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')
                print()


            person_account_temp = person_account_temp + 1

    account_index = account_index + (len(rbac_generation.rbac[username])-1)  # We have already counted the DERs' accounts
    print()
print('***********************************************************************************************************')
print()
print()


#%% -- Automatically Create Service Providers' Profiles --
print('************************************** Service Providers Automation **************************************')
for i in range(1, rbac_generation.n_sp + 1):
    username     = 'Service Provider ' + str(i)
    sp_account = web3.eth.accounts[i - 1 + account_index]
    if(find_Address(username) == '0x0000000000000000000000000000000000000000'):
        created_profile_hash = contract.functions.createProfile(username, sp_account).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

        # Create permissions for this Person
        # -- Create Permissions for this person -- #
        for ( model,perms ) in getter.perm_dict['der_vendor_or_service_provider'].items():
            perms_string = json.dumps(perms[0])
            created_perm_hash = contract.functions.addPermissions(username, str(model), util_account, perms_string).transact()
            # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
            tx_receipt = web3.eth.waitForTransactionReceipt(created_perm_hash)
            mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
            print('New Permission with hash ' + str(str(Web3.toHex(created_perm_hash))) + ' is successfully created!')


    if (i == rbac_generation.n_sp):
        account_index  = account_index + rbac_generation.n_sp

    # Add the entities under the Utilities organization -- DERs and People
    person_account_temp = 0
    for entity in rbac_generation.rbac[username]:
        if entity == 'DER':  # Value of nested dictionary: DERs that are associated with this Utility
            sp_der_list = rbac_generation.rbac[username][entity]
            for der in sp_der_list:
                der_address   = find_Address(der)  # Find the Ethereum address of the DER

                already_created_flag = contract.functions.isChild(der, username).call()   # Check if this association is already existing in the blockchain
                if(not already_created_flag):
                    created_assoc = contract.functions.addChild(der, username, der_address, sp_account).transact()
                    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                    tx_receipt = web3.eth.waitForTransactionReceipt(created_assoc)
                    mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                    print('New Association: '+ str(der)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')
                    print()

        else:               # Value of nested dictionary: People -- Create new profiles AND associations with this utility

            if(find_Address(entity) == '0x0000000000000000000000000000000000000000'):     # 0x000.. -> No such address exists in the blockchain
                entity_account = web3.eth.accounts[person_account_temp + account_index]
                created_profile_hash = contract.functions.createProfile(entity, entity_account).transact()
                # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
                mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')
                print()

            already_created_flag = contract.functions.isChild(entity, username).call()
            if(not already_created_flag):
                person_account = web3.eth.accounts[person_account_temp + account_index]
                created_assoc = contract.functions.addChild(entity, username, person_account, sp_account).transact()
                # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                tx_receipt = web3.eth.waitForTransactionReceipt(created_assoc)
                mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                print('New Association: '+ str(entity)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')
                print()

            role = rbac_generation.rbac[username][entity]
            already_created_flag = hasrole(entity, role)
            if(not already_created_flag):
                # Add the roles to people
                created_utr = contract.functions.addRoleToUser(entity, person_account, role).transact()
                # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
                tx_receipt = web3.eth.waitForTransactionReceipt(created_utr)
                mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
                print('New User to Role Assignment: '+ str(entity)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')
                print()


            person_account_temp = person_account_temp + 1

    account_index = account_index + (len(rbac_generation.rbac[username])-1)  # We have already counted the DERs' accounts
    print()
print('**************************************************************************************************************')
print()
print()


#%% -- Automatically Create DER Owners' Profiles --
print('************************************** DER Owners Automation **************************************')
der_people_list = list(rbac_generation.rbac['DER Device'].keys())
test_username = 'DER Owners'
# -- Create Permissions for this person -- #
for ( model,perms ) in getter.perm_dict['der_owner'].items():
    perms_string = json.dumps(perms[0])
    created_perm_hash = contract.functions.addPermissions(test_username, str(model), util_account, perms_string).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = web3.eth.waitForTransactionReceipt(created_perm_hash)
    mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
    print('New Permission with hash ' + str(str(Web3.toHex(created_perm_hash))) + ' is successfully created!')


for i in range(1, len(der_people_list) + 1):
    username = der_people_list[i-1]

    if(i-1 + account_index >= rbac_generation.total_accounts):
        new_account = web3.eth.account.create()
        user_account = new_account.address
    else:
        user_account = web3.eth.accounts[i - 1 + account_index]

    # First create a new profile for the DER Owner
    if(find_Address(username) == '0x0000000000000000000000000000000000000000'):
        created_profile_hash = contract.functions.createProfile(username, user_account).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

    if (i == len(der_people_list)):
        account_index  = account_index + len(der_people_list)

    der = rbac_generation.rbac['DER Device'][username]
    der_address = find_Address(der)

    already_created_flag = contract.functions.isChild(der, username).call()
    if(not already_created_flag):
        created_assoc = contract.functions.addChild(der, username, der_address, user_account).transact()
        # Wait for  transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_assoc)
        mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New Association: '+ str(der)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')
        print()

    role = 'DER Owner'
    already_created_flag = hasrole(username, role)
    if(not already_created_flag):
        # Add the role to person
        created_utr = contract.functions.addRoleToUser(username, user_account, role).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_utr)
        mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New User to Role Assignment: '+ str(username)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')
        print()


        person_account_temp = person_account_temp + 1

print('***************************************************************************************************')
print()
print()

#%% -- Automatically Create Security Administrators Profiles --
print('************************************** Security Administrators Automation **************************************')
admins_list = list(rbac_generation.rbac['Security Administrator'].keys())
for i in range(1, len(admins_list) + 1):
    username = admins_list[i-1]

    if(i-1 + account_index >= rbac_generation.total_accounts):
        new_account = web3.eth.account.create()
        user_account = new_account.address
    else:
        user_account = web3.eth.accounts[i - 1 + account_index]

    if(find_Address(username) == '0x0000000000000000000000000000000000000000'):
        created_profile_hash = contract.functions.createProfile(username, user_account).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

    if (i == len(admins_list)):
        account_index = account_index + len(admins_list)

    role = 'Security Administrator'
    already_created_flag = hasrole(username, role)
    if(not already_created_flag):
        created_utr = contract.functions.addRoleToUser(username, user_account, role).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_utr)
        mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New User to Role Assignment: '+ str(username)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')
        print()

print('****************************************************************************************************************')
print()
print()

#%% -- Automatically Create Security Auditors Profiles --
print('************************************** Security Auditors Automation **************************************')
auditors_list = list(rbac_generation.rbac['Security Auditor'].keys())
for i in range(1,len(auditors_list)+1):
    username = auditors_list[i-1]

    if(i-1 + account_index >= rbac_generation.total_accounts):
        new_account = web3.eth.account.create()
        user_account = new_account.address
    else:
        user_account = web3.eth.accounts[i - 1 + account_index]

    if(find_Address(username) == '0x0000000000000000000000000000000000000000'):
        created_profile_hash = contract.functions.createProfile(username, user_account).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt    = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

    if (i == len(admins_list)):
        account_index = account_index + len(auditors_list)

    role = 'Security Auditor'
    already_created_flag = hasrole(username, role)
    if(not already_created_flag):
        created_utr = contract.functions.addRoleToUser(username, user_account, role).transact()
        # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
        tx_receipt = web3.eth.waitForTransactionReceipt(created_utr)
        mined_receipt = web3.eth.contract(address = tx_receipt.contractAddress, abi = contract_abi)
        print('New User to Role Assignment: '+ str(username)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')
        print()

print('****************************************************************************************************************')
print()
print()

end = time.time()
print('The overall elapsed time is:'+str(end-start))

log_file.close()
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
