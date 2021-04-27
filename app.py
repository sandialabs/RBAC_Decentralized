from flask import Flask, jsonify, request, abort, send_file
from flask_cors import CORS
from web3 import Web3, HTTPProvider
import json
from web3.auto import w3
import subprocess
import rbac_generation
import time
import uuid
import rbac_generation
import sys
import rbac_der_demo_getterv2 as getter

log_file = open("./log.txt","w")
sys.stdout = log_file

# Configuration
DEBUG = False

# Instantiate the application
app = Flask(__name__)
app.config.from_object(__name__)

# Enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def find_Address(username):
    util_address =  blockchain.contract.functions.profileAddress(username).call()
    return util_address

def add_owner(username, role, association):
    new_account = blockchain.web3.eth.account.create()
    user_account = new_account.address
    association_account = find_Address(association)

    created_profile_hash = blockchain.contract.functions.createProfile(username, user_account).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    mined_receipt  = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

    created_utr = blockchain.contract.functions.addRoleToUser(username, user_account, role).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_utr)
    mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New User to Role Assignment: '+ str(entity)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')


    created_assoc = blockchain.contract.functions.addChild(username, association, user_account, association_account).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_assoc)
    mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Association: '+ str(entity)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')

    item = {
        'name': username,
        'address': user_account,
        'role': role
    }

    if(association == 'Utility 1'):
        UTILITY1.append(item)
    elif(association == 'Utility 2'):
        UTILITY2.append(item)
    elif(association == 'Utility 3'):
        UTILITY3.append(item)
    elif(association == 'Utility 4'):
        UTILITY4.append(item)
    elif(association == 'Utility 5'):
        UTILITY5.append(item)
    elif(association == 'Service Provider 1'):
        SP1.append(item)
    elif(association == 'Service Provider 2'):
        SP2.append(item)
    elif(association == 'Service Provider 3'):
        SP3.append(item)
    elif(association == 'Service Provider 4'):
        SP4.append(item)
    elif(association == 'Service Provider 5'):
        SP5.append(item)
    elif(association == 'Security Auditor'):
        SECAUDITORS.append(item)
    else:
        SECADMINS.append(item)





def add_owner_device(username, role, device):
    new_account = blockchain.web3.eth.account.create()
    user_account = new_account.address

    new_account = blockchain.web3.eth.account.create()
    device_account = new_account.address

    created_profile_hash = blockchain.contract.functions.createProfile(username, user_account).transact()

    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    mined_receipt    = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

    created_profile_hash = blockchain.contract.functions.createProfile(device, device_account).transact()

    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    mined_receipt    = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Profile with Username: "'+str(device)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')

    created_utr = blockchain.contract.functions.addRoleToUser(username, user_account, role).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_utr)
    mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New User to Role Assignment: '+ str(username)+ ' -> ' + str(role) +' with hash ' + str(Web3.toHex(created_utr)) + ' is successfully created')

    created_assoc = blockchain.contract.functions.addChild(device, username, device_account, user_account).transact()
    # Wait for  transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_assoc)
    mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Association: '+ str(device)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')

    item = {
        'name': username,
        'address': user_account,
        'role': device
    }
    DEROWNERS.append(item)


@app.route('/showperm2', methods=['PUT'])
def show_perm2():
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    if(request.method == 'PUT'):
        post_data = request.get_json()
        username = post_data.get('name')
        address = post_data.get('address')

        # Check Username and Address -- Matching
        if (username == ''):
            username = blockchain.contract.functions.profileUsername(address).call()
        elif (address == ''):
            address = find_Address(username)
        elif(username != '' and address != ''):
            check_username = blockchain.contract.functions.profileUsername(address).call()
            check_address = find_Address(username)
            if(check_username != username or check_address != address):
                response_object['flag'] = 'False'

        if('DER' in username):
            response_object['flag'] = 'False'
        else:
            role = blockchain.contract.functions.getRolesfromNames(username).call()
            parent = blockchain.contract.functions.returnParent(username).call()
            if(role == 'DER Owner'):
                parent = 'DER Owners'
            elif(role == ''):
                response_object['flag'] = 'False'

            model = 'DERCapacity'
            perms_string = blockchain.contract.functions.queryPermissions(parent,model).call()
            response_object[model] = perms_string

    end = time.time()
    print('Show Permissions Query Time: ' + str(end-start))
    return jsonify(response_object)


@app.route('/show_permissions', methods=['PUT'])
def show_permissions():
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    response_object['NoPerm'] = 'False'
    response_object['permissions'] = ''
    if request.method == 'PUT':
        post_data = request.get_json()
        username = post_data.get('username')
        address = post_data.get('address')
        device = post_data.get('der')


        # Check Username and Address -- Matching
        if (username == ''):
            username = blockchain.contract.functions.profileUsername(address).call()
        elif (address == ''):
            address = find_Address(username)
        elif(username != '' and address != ''):
            check_username = blockchain.contract.functions.profileUsername(address).call()
            check_address = find_Address(username)
            if(check_username != username or check_address != address):
                response_object['flag'] = 'False'

        # Check Username and DER - Can Username do an operation to this DER
        parent_list = blockchain.contract.functions.getParentsNames(username).call()
        username_parent_string = ''
        for parent in parent_list:
            parent_string = Web3.toText(parent)
            parent_string = parent_string.split("\x00")
            username_parent_string += parent_string[0] + ','

        username_parent_string = username_parent_string[0:-1]  # Subtract the comma

        parent_list = blockchain.contract.functions.getParentsNames(device).call()
        der_parent_string = ''
        for parent in parent_list:
            parent_string = Web3.toText(parent)
            parent_string = parent_string.split("\x00")
            der_parent_string += parent_string[0] + ','

        ischild = blockchain.contract.functions.isChild(der, username)
        if ((username_parent_string in der_parent_string) or ischild):
            # Ask for permissions
            perm_list = blockchain.contract.functions.queryPermissions(username).call
            permissions_string = ''
            for perm in perm_list:
                perm_string = Web3.toText(perm)
                perm_string = perm_string.split("\x00")
                permissions_string += perm_string[0] + ','

            response_object['permissions'] = permissions_string
        else:
            response_object['NoPerm'] = 'True'
    end = time.time()
    print('Permissions Query Time: '+ str(end-start))
    return jsonify(response_object)





@app.route('/download', methods=['POST'])
def download():
    f = '/Users/geo_fragkos/Documents/PhD_Documents/Sandia/Documents/der_cyber/rbac_eth_demo/truffle_based/log.txt'
    return send_file(f,attachment_filename='test.txt',as_attachment=True)

@app.route('/verify_utr', methods=['PUT'])
def verify_utr():
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    if request.method == 'PUT':
        post_data = request.get_json()
        username = post_data.get('username')
        address = post_data.get('address')
        role = post_data.get('role')

        if (username == ''):
            username = blockchain.contract.functions.profileUsername(address).call()
        elif (address == ''):
            address = find_Address(username)
        elif(username != '' and address != ''):
            check_username = blockchain.contract.functions.profileUsername(address).call()
            check_address = find_Address(username)
            if(check_username != username or check_address != address):
                response_object['flag'] = 'False'



        parent_list = blockchain.contract.functions.getParentsNames(username).call()
        final_parent_string = ''
        for parent in parent_list:
            parent_string = Web3.toText(parent)
            parent_string = parent_string.split("\x00")
            final_parent_string += parent_string[0] + ','
        response_object['sent_parent'] = final_parent_string



        verification = blockchain.contract.functions.hasRole(username, role).call()
        response_object['sent_username'] = username
        response_object['sent_address'] = address
        response_object['sent_role'] = role
        response_object['sent_verification'] = verification
    end = time.time()
    print('Verify User Query Time: '+ str(end-start))
    return jsonify(response_object)


@app.route('/add_user', methods=['PUT'])
def add_user():
    start = time.time()
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        first_name = post_data.get('firstName')
        last_name = post_data.get('lastName')
        role = post_data.get('role')
        association = post_data.get('association')
        device = post_data.get('device')
        username = first_name + ' ' + last_name

        if (role == 'DER Owner'):
            if (find_Address(username) != '0x0000000000000000000000000000000000000000'):
                response_object['sent_response'] = 'Existing User'

            if (find_Address(device) != '0x0000000000000000000000000000000000000000'):
                response_object['sent_response'] = 'Existing DER Device'

            if(find_Address(username) == '0x0000000000000000000000000000000000000000' and find_Address(device) == '0x0000000000000000000000000000000000000000'):
                add_owner_device(username, role, device)

        else:
            if (find_Address(username) != '0x0000000000000000000000000000000000000000'):
                response_object['sent_response'] = 'Existing User'
            else:
                add_owner(username,role,association)
    end = time.time()
    print('Add User Query Time: '+str(end-start))
    return jsonify(response_object)

def delete_fun(username, address):
    if (not 'DER' in username):
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        role = blockchain.contract.functions.getRolesfromNames(username).call()
        parent_list = blockchain.contract.functions.getParentsNames(username).call()
        final_parent_string = ''
        parentt = ''
        for parent in parent_list:
            parent_string = Web3.toText(parent)
            parent_string = parent_string.split("\x00")
            final_parent_string += parent_string[0] + ','
            parentt = parent_string[0]
            # Delete the Name Association with Utility
            created_profile_hash = blockchain.contract.functions.deleteAssoc(username, parent_string[0]).transact()
            tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
            mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
            print(tx_receipt)

            # Delete the Name Association with Utility
            parent_address = find_Address(parent_string[0])
            created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
            tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
            mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
            print(tx_receipt)

        item = {
            'name': username,
            'address': address,
            'role': role
        }

        if(parentt == 'Utility 1'):
            UTILITY1.remove(item)
        elif(parentt == 'Utility 2'):
            UTILITY2.remove(item)
        elif(parentt == 'Utility 3'):
            UTILITY3.remove(item)
        elif(parentt == 'Utility 4'):
            UTILITY4.remove(item)
        elif(parentt == 'Utility 5'):
            UTILITY5.remove(item)
        elif(parentt == 'Service Provider 1'):
            SP1.remove(item)
        elif(parentt == 'Service Provider 2'):
            SP2.remove(item)
        elif(parentt == 'Service Provider 3'):
            SP3.remove(item)
        elif(parentt == 'Service Provider 4'):
            SP4.remove(item)
        elif(parentt == 'Service Provider 5'):
            SP5.remove(item)
        elif(parentt == 'Security Auditor'):
            SECAUDITORS.remove(item)
        else:
            SECADMINS.remove(item)


        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(username, address, role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        parent_list = blockchain.contract.functions.getParentsNames(username).call()
        final_parent_string = ''
        for parent in parent_list:
            parent_string = Web3.toText(parent)
            parent_string = parent_string.split("\x00")
            final_parent_string += parent_string[0] + ','
            # Delete the Name Association with Utility
            created_profile_hash = blockchain.contract.functions.deleteAssoc(username, parent_string[0]).transact()
            tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
            mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
            print(tx_receipt)

            # Delete the Name Association with Utility
            parent_address = find_Address(parent_string[0])
            created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
            tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
            mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
            print(tx_receipt)

            item = {
                'name': username,
                'address': address,
                'role': ''
            }

            if(parent_string[0] == 'Utility 1'):
                UTILITY1.remove(item)
            elif(parent_string[0] == 'Utility 2'):
                UTILITY2.remove(item)
            elif(parent_string[0] == 'Utility 3'):
                UTILITY3.remove(item)
            elif(parent_string[0] == 'Utility 4'):
                UTILITY4.remove(item)
            elif(parent_string[0] == 'Utility 5'):
                UTILITY5.remove(item)
            elif(parent_string[0] == 'Service Provider 1'):
                SP1.remove(item)
            elif(parent_string[0] == 'Service Provider 2'):
                SP2.remove(item)
            elif(parent_string[0] == 'Service Provider 3'):
                SP3.remove(item)
            elif(parent_string[0] == 'Service Provider 4'):
                SP4.remove(item)
            elif(parent_string[0] == 'Service Provider 5'):
                SP5.remove(item)
            else: # Case that a user has this DER
                item = {
                    'name': parent_string[0],
                    'address': parent_address,
                    'role': username
                }

                # Delete the Role Association
                created_profile_hash = blockchain.contract.functions.revokeRole(parent_string[0], parent_address, 'DER Owner').transact()
                tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
                mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
                print(tx_receipt)

                DEROWNERS.remove(item)



@app.route('/delete_user', methods=['PUT'])
def delete_user():
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    if request.method == 'PUT':
        post_data = request.get_json()
        username = post_data.get('username')
        address = post_data.get('address')

        if (username == ''):
            username = blockchain.contract.functions.profileUsername(address).call()
        elif (address == ''):
            address = find_Address(username)
        elif(username != '' and address != ''):
            check_username = blockchain.contract.functions.profileUsername(address).call()
            check_address = find_Address(username)
            if(check_username != username or check_address != address):
                response_object['flag'] = 'False'
                return jsonify(response_object)


        if (find_Address(username) == '0x0000000000000000000000000000000000000000'):
            response_object['flag'] = 'False'
            return jsonify(response_object)
        else:
            delete_fun(username, address)
            end = time.time()
            print('Delete User Query Time: '+str(end-start))
            return jsonify(response_object)

@app.route('/find_transaction', methods=['PUT'])
def find_transaction():
    start = time.time()
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        trx = post_data.get('transaction')
        info = blockchain.web3.eth.getTransaction(trx)
        response_object['sent_block'] = info['blockNumber']
        response_object['sent_from'] = info['from']
        response_object['sent_to'] = info['to']
        response_object['sent_gas'] = info['gas']
        end = time.time()
        print('Find Trx Query Time: '+str(end-start))
        return jsonify(response_object)

@app.route('/find_block', methods=['PUT'])
def find_block():
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    if request.method == 'PUT':
        post_data = request.get_json()
        block = int(post_data.get('block'))
        latest_block = blockchain.web3.eth.get_block('latest')
        if(block > latest_block['number'] or block < 0):
            response_object['flag'] = 'False'
        info = blockchain.web3.eth.get_block(block)
        response_object['sent_hash'] = info['hash'].hex()
        response_object['sent_size'] = info['size']
        response_object['sent_trx'] = info['transactions'][0].hex()
    return jsonify(response_object)

def der_create_profile(username):
    new_account = blockchain.web3.eth.account.create()
    der_account = new_account.address

    created_profile_hash = blockchain.contract.functions.createProfile(username, der_account).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    mined_receipt    = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Profile with Username: "'+str(username)+ '" and with hash ' + str(str(Web3.toHex(created_profile_hash))) + ' is successfully created!')


def add_der(username, association):
    der_account = find_Address(username)
    association_account = find_Address(association)
    created_assoc = blockchain.contract.functions.addChild(username, association, der_account, association_account).transact()
    # Wait for the transaction to be mined in the blockchain, and get the transaction receipt
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_assoc)
    mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
    print('New Association: '+ str(der)+' & '+str(username) +' with hash ' + str(Web3.toHex(created_assoc)) + ' is successfully created')

    item = {
        'name': username,
        'address': der_account,
        'role': ''
    }

    if(association == 'Utility 1'):
        UTILITY1.append(item)
    elif(association == 'Utility 2'):
        UTILITY2.append(item)
    elif(association == 'Utility 3'):
        UTILITY3.append(item)
    elif(association == 'Utility 4'):
        UTILITY4.append(item)
    elif(association == 'Utility 5'):
        UTILITY5.append(item)
    elif(association == 'Service Provider 1'):
        SP1.append(item)
    elif(association == 'Service Provider 2'):
        SP2.append(item)
    elif(association == 'Service Provider 3'):
        SP3.append(item)
    elif(association == 'Service Provider 4'):
        SP4.append(item)
    else:
        SP5.append(item)


@app.route('/showperm', methods=['PUT'])
def show_perm():
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    response_object['answer'] = 'No'
    response_object['answer_op'] = ''
    if request.method == 'PUT':
        post_data = request.get_json()
        first_name = post_data.get('firstName')
        last_name = post_data.get('lastName')
        organization = post_data.get('parent')
        model = post_data.get('model')
        print(model)
        operation = post_data.get('operation')
        print(organization)
        if('DER' in first_name):
            response_object['flag'] = 'False'
        else:
            perms_string = blockchain.contract.functions.queryPermissions(organization,model).call()
            perms_dict = json.loads(perms_string)
            if (operation in perms_dict):
                response_object['answer'] = 'Yes'
                response_object['answer_op'] = perms_dict[operation]

    end = time.time()
    print('Show Permissions Query Time: '+str(end-start))
    return jsonify(response_object)




@app.route('/add_der_device', methods=['PUT'])
def add_der_device():
    start = time.time()
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        username = post_data.get('device')
        associations = post_data.get('association')

        if (find_Address(username) != '0x0000000000000000000000000000000000000000'):
            response_object['sent_response'] = 'Existing DER'
        else:
            der_create_profile(username)
            for association in associations:
                add_der(username, association)
    end = time.time()
    print('Add DER Query Time: '+str(end-start))
    return jsonify(response_object)

@app.route('/get_der_info', methods=['PUT'])
def get_der_info():
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    response_object['sent_owner'] = ''       # JSON field in case we have a DER Owner
    if request.method == 'PUT':
        post_data = request.get_json()
        username = post_data.get('username')
        address = post_data.get('address')

        if (username != '' and address == ''):
            address = find_Address(username)
            parent_list = blockchain.contract.functions.getParentsNames(username).call()
            final_parent_string = ''
            for parent in parent_list:
                parent_string = Web3.toText(parent)
                parent_string = parent_string.split("\x00")
                final_parent_string += parent_string[0] + ','
            response_object['sent_parent'] = final_parent_string

        elif (username == '' and address != ''):
            username =  blockchain.contract.functions.profileUsername(address).call()

            parent_list = blockchain.contract.functions.getParentsNames(username).call()
            final_parent_string = ''
            for parent in parent_list:
                parent_string = Web3.toText(parent)
                parent_string = parent_string.split("\x00")
                final_parent_string += parent_string[0] + ','
            response_object['sent_parent'] = final_parent_string

        else:
            check_username =  blockchain.contract.functions.profileUsername(address).call()
            check_address = find_Address(username)
            if((check_username != username) or (check_address != address) ):
                abort(500)

            # Check if the user is a DER Owner
            parent_list = blockchain.contract.functions.getParentsNames(username).call()
            final_parent_string = ''
            for parent in parent_list:
                parent_string = Web3.toText(parent)
                parent_string = parent_string.split("\x00")
                final_parent_string += parent_string[0] + ', '
            response_object['sent_parent'] = final_parent_string


        response_object['message'] = 'Entity is updated!'
        response_object['sent_name'] = username
        response_object['sent_address'] = address
        print(response_object['sent_address'])
    end = time.time()
    print('Search DER Info Query Time: '+str(end-start))
    return jsonify(response_object)


@app.route('/get_entity_info/<entity_id>', methods=['PUT'])
def get_info(entity_id):
    start = time.time()
    response_object = {'status': 'success'}
    response_object['flag'] = 'True'
    response_object['sent_owner'] = ''       # JSON field in case we have a DER Owner
    if request.method == 'PUT':
        post_data = request.get_json()
        username = post_data.get('username')
        address = post_data.get('address')

        if (username != '' and address == ''):
            address = find_Address(username)
            role = blockchain.contract.functions.getRolesfromNames(username).call()
            parent = blockchain.contract.functions.returnParent(username).call()
            if (role == 'Security Administrator'):
                parent = 'Security Administrators'
            elif (role == 'Security Auditor'):
                parent = 'Security Auditors'
            elif (role == 'DER Owner'):
                parent = 'DER Owners'
            # Check if the user is a DER Owner
            if(role == 'DER Owner'):
                children_list = blockchain.contract.functions.getChildrenNames(username).call()
                child_string = Web3.toText(children_list[0])
                child_string = child_string.split("\x00")
                final_child_string = child_string[0]
                response_object['sent_owner'] = final_child_string

        elif (username == '' and address != ''):
            username =  blockchain.contract.functions.profileUsername(address).call()
            role = blockchain.contract.functions.getRolesfromAddress(address).call()
            if (role == 'Security Administrator'):
                parent = 'Security Administrators'
            elif (role == 'Security Auditor'):
                parent = 'Security Auditors'
            elif (role == 'DER Owner'):
                parent = 'DER Owners'
            else:
                parent = blockchain.contract.functions.returnParent(username).call()

            # Check if the user is a DER Owner
            if(role == 'DER Owner'):
                children_list = blockchain.contract.functions.getChildrenNames(username).call()
                child_string = Web3.toText(children_list[0])
                child_string = child_string.split("\x00")
                final_child_string = child_string[0]
                response_object['sent_owner'] = final_child_string

        else:
            check_username =  blockchain.contract.functions.profileUsername(address).call()
            check_address = find_Address(username)
            if((check_username != username) or (check_address != address) ):
                abort(500)
            role = blockchain.contract.functions.getRolesfromNames(username).call()
            role = blockchain.contract.functions.getRolesfromAddress(address).call()
            if (role == 'Security Administrator'):
                parent = 'Security Administrators'
            elif (role == 'Security Auditor'):
                parent = 'Security Auditors'
            elif (role == 'DER Owner'):
                parent = 'DER Owners'
            else:
                parent = blockchain.contract.functions.returnParent(username).call()

            # Check if the user is a DER Owner
            if(role == 'DER Owner'):
                children_list = blockchain.contract.functions.getChildrenNames(username).call()
                child_string = Web3.toText(children_list[0])
                child_string = child_string.split("\x00")
                final_child_string = child_string[0]
                response_object['sent_owner'] = final_child_string


        response_object['message'] = 'Entity is updated!'
        response_object['sent_name'] = username
        response_object['sent_address'] = address
        print(response_object['sent_address'])
        response_object['sent_role'] = role
        response_object['sent_parent'] = parent
    end = time.time()
    print('Search User Query Time: ' + str(end-start))
    return jsonify(response_object)

@app.route('/auth', methods=['POST'])
def auth():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    if (post_data['user'] == '' and post_data['password'] == ''):
        response_object['token'] = 'Token Granted'

        # Login Cases
        if (post_data['case'] == 'utilities_admin'):
            blockchain.web3.eth.defaultAccount = blockchain.web3.eth.accounts[-1]
        elif (post_data['case'] == 'admin'):
            blockchain.web3.eth.defaultAccount = blockchain.web3.eth.accounts[0]
        elif (post_data['case'] == 'sp_admin'):
            blockchain.web3.eth.defaultAccount = blockchain.web3.eth.accounts[-2]
        elif (post_data['case'] == 'der_admin'):
            blockchain.web3.eth.defaultAccount = blockchain.web3.eth.accounts[-3]
    else:
        response_object['token'] = ''
    return jsonify(response_object)


def update_profile_util1(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Utility 1').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        # Delete the Name Association with Utility
        parent_address = find_Address('Utility 1')
        created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        mined_receipt = blockchain.web3.eth.contract(address = tx_receipt.contractAddress, abi = blockchain.contract_abi)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Utility 1')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Utility 1', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def revoke_role_util(address, new_role, old_username, old_role):
    # Delete the Role Association
    created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)

    # Create role
    created_profile_hash = blockchain.contract.functions.addRoleToUser(old_username, address, new_role).transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)

def revoke_role_derowners(address, new_role, old_username, device):
    # Delete the Role Association
    created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, 'DER Owner').transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)

    # Delete the Name Association with Utility
    created_profile_hash = blockchain.contract.functions.deleteAssoc(device, old_username).transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)


    # Delete the Name Association with Utility
    child_address = find_Address(device)
    created_profile_hash = blockchain.contract.functions.deleteAssocAddress(child_address, address).transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)

def revoke_role_secadmins(address, new_role, old_username, old_role):
    # Delete the Role Association
    created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, 'Security Administrator').transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)

def revoke_role_secauditors(address, new_role, old_username, old_role):
    # Delete the Role Association
    created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, 'Security Auditor').transact()
    tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
    print(tx_receipt)

def update_profile_util2(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Utility 2').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        parent_address = find_Address('Utility 2')
        created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Utility 2')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Utility 2', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_util3(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Utility 3').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

       # Delete the Name Association with Utility
        parent_address = find_Address('Utility 3')
        created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Utility 3')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Utility 3', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_util4(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Utility 4').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

       # Delete the Name Association with Utility
        parent_address = find_Address('Utility 4')
        created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Utility 4')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Utility 4', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_util5(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Utility 5').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

       # Delete the Name Association with Utility
        parent_address = find_Address('Utility 5')
        created_profile_hash = blockchain.contract.functions.deleteAssocAddress(address, parent_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Utility 5')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Utility 5', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_sp1(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Service Provider 1').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)


        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Service Provider 1')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Service Provider 1', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_sp2(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Service Provider 2').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Service Provider 2')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Service Provider 2', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_sp3(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Service Provider 3').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)
        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Service Provider 3')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Service Provider 3', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_sp4(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Service Provider 4').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Service Provider 4')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Service Provider 4', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_sp5(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Service Provider 5').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Service Provider 5')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Service Provider 5', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_sp6(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_username, 'Service Provider 6').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, old_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address('Service Provider 6')
        created_profile_hash = blockchain.contract.functions.addChild(new_username, 'Service Provider 6', address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, new_role).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_derowners(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Name Association with Utility
        created_profile_hash = blockchain.contract.functions.deleteAssoc(old_role, old_username).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, 'DER Owner').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create new association
        util_address = find_Address(old_role)
        created_profile_hash = blockchain.contract.functions.addChild(new_username, old_role, address, util_address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, 'DER Owner').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)


def update_profile_secadmins(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, 'Security Administrator').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)


        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, 'Security Administrator').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def update_profile_secauditors(new_username,address, new_role, old_username, old_role):
    if(new_username == old_username and new_role == old_role):
        return
    else:
        # Delete the old Profile
        created_profile_hash = blockchain.contract.functions.deleteProfile(old_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Delete the Role Association
        created_profile_hash = blockchain.contract.functions.revokeRole(old_username, address, 'Security Auditor').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

        # Create a new profile
        created_profile_hash = blockchain.contract.functions.createProfile(new_username, address).transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)


        # Create role
        created_profile_hash = blockchain.contract.functions.addRoleToUser(new_username, address, 'Security Auditor').transact()
        tx_receipt = blockchain.web3.eth.waitForTransactionReceipt(created_profile_hash)
        print(tx_receipt)

def remove_entity_util1(entity_id):
    for entity in UTILITY1:
        if entity['address'] == entity_id:
            UTILITY1.remove(entity)
            return True
    return False

def remove_entity_util2(entity_id):
    for entity in UTILITY2:
        if entity['address'] == entity_id:
            UTILITY2.remove(entity)
            return True
    return False

def remove_entity_util3(entity_id):
    for entity in UTILITY3:
        if entity['address'] == entity_id:
            UTILITY3.remove(entity)
            return True
    return False

def remove_entity_util4(entity_id):
    for entity in UTILITY4:
        if entity['address'] == entity_id:
            UTILITY4.remove(entity)
            return True
    return False

def remove_entity_util5(entity_id):
    for entity in UTILITY5:
        if entity['address'] == entity_id:
            UTILITY5.remove(entity)
            return True
    return False


def remove_entity_sp1(entity_id):
    for entity in SP1:
        if entity['address'] == entity_id:
            SP1.remove(entity)
            return True
    return False

def remove_entity_sp2(entity_id):
    for entity in SP2:
        if entity['address'] == entity_id:
            SP2.remove(entity)
            return True
    return False

def remove_entity_sp3(entity_id):
    for entity in SP3:
        if entity['address'] == entity_id:
            SP3.remove(entity)
            return True
    return False

def remove_entity_sp4(entity_id):
    for entity in SP4:
        if entity['address'] == entity_id:
            SP4.remove(entity)
            return True
    return False

def remove_entity_sp5(entity_id):
    for entity in SP5:
        if entity['address'] == entity_id:
            SP5.remove(entity)
            return True
    return False

def remove_entity_derowners(entity_id):
    for entity in DEROWNERS:
        if entity['address'] == entity_id:
            DEROWNERS.remove(entity)
            return True
    return False

def remove_entity_secadmins(entity_id):
    for entity in SECADMINS:
        if entity['address'] == entity_id:
            SECADMINS.remove(entity)
            return True
    return False

def remove_entity_secauditors(entity_id):
    for entity in SECAUDITORS:
        if entity['address'] == entity_id:
            SECAUDITORS.remove(entity)
            return True
    return False

@app.route('/utility1', methods=['GET'])
def entities_utility1():
    response_object = {'status': 'success'}
    response_object['entities'] = UTILITY1
    return jsonify(response_object)

@app.route('/utility2', methods=['GET'])
def entities_utility2():
    response_object = {'status': 'success'}
    response_object['entities'] = UTILITY2
    return jsonify(response_object)

@app.route('/utility3', methods=['GET'])
def entities_utility3():
    response_object = {'status': 'success'}
    response_object['entities'] = UTILITY3
    return jsonify(response_object)

@app.route('/utility4', methods=['GET'])
def entities_utility4():
    response_object = {'status': 'success'}
    response_object['entities'] = UTILITY4
    return jsonify(response_object)

@app.route('/utility5', methods=['GET'])
def entities_utility5():
    response_object = {'status': 'success'}
    response_object['entities'] = UTILITY5
    return jsonify(response_object)

@app.route('/sp1', methods=['GET'])
def entities_sp1():
    response_object = {'status': 'success'}
    response_object['entities'] = SP1
    return jsonify(response_object)

@app.route('/sp2', methods=['GET'])
def entities_sp2():
    response_object = {'status': 'success'}
    response_object['entities'] = SP2
    return jsonify(response_object)

@app.route('/sp3', methods=['GET'])
def entities_sp3():
    response_object = {'status': 'success'}
    response_object['entities'] = SP3
    return jsonify(response_object)


@app.route('/sp4', methods=['GET'])
def entities_sp4():
    response_object = {'status': 'success'}
    response_object['entities'] = SP4
    return jsonify(response_object)

@app.route('/sp5', methods=['GET'])
def entities_sp5():
    response_object = {'status': 'success'}
    response_object['entities'] = SP5
    return jsonify(response_object)

@app.route('/derowners', methods=['GET'])
def entities_derowners():
    response_object = {'status': 'success'}
    response_object['entities'] = DEROWNERS
    return jsonify(response_object)

@app.route('/secadmins', methods=['GET'])
def entities_secadmins():
    response_object = {'status': 'success'}
    response_object['entities'] = SECADMINS
    return jsonify(response_object)

@app.route('/secauditors', methods=['GET'])
def entities_secauditors():
    response_object = {'status': 'success'}
    response_object['entities'] = SECAUDITORS
    return jsonify(response_object)

@app.route('/utilities/<entity_id>', methods=['PUT'])
def single_entity(entity_id):
    start = time.time()
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_util1(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_util1(new_name, entity_id, new_role, old_name, old_role)
        UTILITY1.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    end = time.time()
    print('The Utility Update Time is:'+str(end-start))
    return jsonify(response_object)

@app.route('/utilitiesrevoke/<entity_id>', methods=['PUT'])
def single_entity_revoke(entity_id):
    start = time.time()
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_util1(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        UTILITY1.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    end = time.time()
    print('The revoke time is:'+str(end-start))
    return jsonify(response_object)


@app.route('/utilities2revoke/<entity_id>', methods=['PUT'])
def single_entity2_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_util2(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        UTILITY2.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities3revoke/<entity_id>', methods=['PUT'])
def single_entity3_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_util3(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        UTILITY3.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities4revoke/<entity_id>', methods=['PUT'])
def single_entity4_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_util4(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        UTILITY4.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities5revoke/<entity_id>', methods=['PUT'])
def single_entity5_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_util5(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        UTILITY5.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp1revoke/<entity_id>', methods=['PUT'])
def single_sp_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_sp1(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        SP1.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp2revoke/<entity_id>', methods=['PUT'])
def single_sp2_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_sp2(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        SP2.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp3revoke/<entity_id>', methods=['PUT'])
def single_sp3_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_sp3(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        SP3.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp4revoke/<entity_id>', methods=['PUT'])
def single_sp4_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_sp4(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        SP4.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp5revoke/<entity_id>', methods=['PUT'])
def single_sp5_revoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_sp5(entity_id)

        # Update blockchain entries
        old_role = post_data.get('oldRole')
        new_role = ''
        revoke_role_util(entity_id, new_role, old_name, old_role)
        SP5.append({
            'name': old_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/derownersrevoke/<entity_id>', methods=['PUT'])
def single_derownersrevoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_derowners(entity_id)

        # Update blockchain entries
        device = post_data.get('oldRole')
        new_role = ''
        revoke_role_derowners(entity_id, new_role, old_name, device)
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/secadminsrevoke/<entity_id>', methods=['PUT'])
def single_secadminsrevoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_secadmins(entity_id)

        # Update blockchain entries
        device = post_data.get('oldRole')
        new_role = ''
        revoke_role_secadmins(entity_id, new_role, old_name, device)
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/secauditorsrevoke/<entity_id>', methods=['PUT'])
def single_secauditorsrevoke(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('name')
        remove_entity_secauditors(entity_id)

        # Update blockchain entries
        device = post_data.get('oldRole')
        new_role = ''
        revoke_role_secauditors(entity_id, new_role, old_name, device)
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities2/<entity_id>', methods=['PUT'])
def single_entity2(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_util2(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_util2(new_name, entity_id, new_role, old_name, old_role)
        UTILITY2.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities3/<entity_id>', methods=['PUT'])
def single_entity3(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_util3(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_util3(new_name, entity_id, new_role, old_name, old_role)
        UTILITY3.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities4/<entity_id>', methods=['PUT'])
def single_entity4(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_util4(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_util4(new_name, entity_id, new_role, old_name, old_role)
        UTILITY4.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/utilities5/<entity_id>', methods=['PUT'])
def single_entity5(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_util5(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_util5(new_name, entity_id, new_role, old_name, old_role)
        UTILITY5.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp1/<entity_id>', methods=['PUT'])
def single_sp1(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_sp1(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_sp1(new_name, entity_id, new_role, old_name, old_role)
        SP1.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp2/<entity_id>', methods=['PUT'])
def single_sp2(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_sp2(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_sp2(new_name, entity_id, new_role, old_name, old_role)
        SP2.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp3/<entity_id>', methods=['PUT'])
def single_sp3(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_sp3(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_sp3(new_name, entity_id, new_role, old_name, old_role)
        SP3.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp4/<entity_id>', methods=['PUT'])
def single_sp4(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_sp4(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_sp4(new_name, entity_id, new_role, old_name, old_role)
        SP4.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/sp5/<entity_id>', methods=['PUT'])
def single_sp5(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_sp5(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_sp5(new_name, entity_id, new_role, old_name, old_role)
        SP5.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/derowners/<entity_id>', methods=['PUT'])
def single_derowners(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_derowners(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_derowners(new_name, entity_id, new_role, old_name, old_role)
        DEROWNERS.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/secadmins/<entity_id>', methods=['PUT'])
def single_secadmins(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_secadmins(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_secadmins(new_name, entity_id, new_role, old_name, old_role)
        SECADMINS.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/secauditors/<entity_id>', methods=['PUT'])
def single_secauditors(entity_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        old_name = post_data.get('oldName')
        old_role = post_data.get('oldRole')
        remove_entity_secauditors(entity_id)

        # Update blockchain entries
        new_name = post_data.get('name')
        new_role = post_data.get('role')
        update_profile_secauditors(new_name, entity_id, new_role, old_name, old_role)
        SECAUDITORS.append({
            'name': new_name,
            'address': entity_id,
            'role': new_role
        })
        response_object['message'] = 'Entity is updated!'
    return jsonify(response_object)

@app.route('/get_admin_address', methods=['GET'])
def get_admin_address():
    return jsonify(blockchain.web3.eth.defaultAccount)

@app.route('/get_admin_balance',methods=['GET'])
def get_admin_balance():
    return jsonify(str(blockchain.web3.fromWei(blockchain.web3.eth.getBalance(blockchain.web3.eth.defaultAccount),'ether')))

@app.route('/get_sc_address',methods=['GET'])
def get_sc_address():
    return jsonify(blockchain.contract_address)

@app.route('/get_blocks',methods=['GET'])
def get_blocks():
    block = blockchain.web3.eth.get_block('latest')
    block_number = block['number']
    return jsonify(str(block_number + 1))

@app.route('/get_entities',methods=['GET'])
def get_entities():
    return jsonify(str(blockchain.blockchain_accounts))

class Blockchain_Connector:
    def __init__(self, net_id, net_ip, port):
        self.blockchain_network_id = net_id
        self.net_ip = net_ip
        self.port = port
        self.blockchain_accounts = rbac_generation.total_accounts + 1

        self.pro = subprocess.Popen(['./accounts_creator.sh %s %s %s %s' %(self.blockchain_network_id, self.blockchain_accounts, self.port, '.ganache/data'+str(net_id))], shell = True)
        t = 60
        time.sleep(t)

        self.blockchain_address = 'http://'+ self.net_ip + ':' + self.port
        self.web3 = Web3(HTTPProvider(self.blockchain_address))
        print('Connection with Private Ethereum Blockchain:' + str(self.web3.isConnected()))

        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        print('RBAC Administrator Address:'+str(self.web3.eth.defaultAccount))

        # subprocess.Popen(['./RBAC_sc_migrator.sh'], shell=True)
        # t = 270       # Sleep for 30 seconds until the subprocess has began
        # time.sleep(t)

        self.compiled_contract_path = '/home/george/Desktop/Sandia_RBAC/Decentralized_Ethereum/build/contracts/RBAC.json'

        # Contract Address - Get that from Json File after Smart Contract Migration [Automatic]
        with open(self.compiled_contract_path) as file:
            self.contract_json = json.load(file)       # Load Contract Information as JSON file
            self.contract_abi  = self.contract_json['abi']  # Fetch RBAC smart contract's abi - Call its functions
            self.contract_address  = self.contract_json['networks'][str(self.blockchain_network_id)]['address']


        # Fetch deployed RBAC smart contract instance
        self.contract = self.web3.eth.contract(address = self.contract_address, abi = self.contract_abi)
        print('Deployed RBAC Contract Address:' + str(self.contract_address))
        print('************************ Connection with Blockchain is done ******************************')


if __name__ == '__main__':
    # Sleep in order the RBAC Model to be generated
    starting = time.time()
    t = 30
    time.sleep(t)
    print('Starting app.py ...')
    #net_id = sys.argv[1]
    net_id = 1200
    blockchain = Blockchain_Connector(net_id, '127.0.0.1', '9545')
    t = 5
    time.sleep(t)
    print('Connection is done with Contract Address:'+str(blockchain.contract_address))

    # ---------------- Utility 1 - JSON Creation ------------------ #
    UTILITY1 = []
    for (entity,value) in rbac_generation.rbac['Utility 1'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                UTILITY1.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            UTILITY1.append(item)

    # ---------------- Utility 2 - JSON Creation ------------------ #
    UTILITY2 = []
    for (entity,value) in rbac_generation.rbac['Utility 2'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                UTILITY2.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            UTILITY2.append(item)

    # ---------------- Utility 3 - JSON Creation ------------------ #
    UTILITY3 = []
    for (entity,value) in rbac_generation.rbac['Utility 3'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                UTILITY3.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            UTILITY3.append(item)

    # ---------------- Utility 4 - JSON Creation ------------------ #
    UTILITY4 = []
    for (entity,value) in rbac_generation.rbac['Utility 4'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                UTILITY4.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            UTILITY4.append(item)

    # ---------------- Utility 5 - JSON Creation ------------------ #
    UTILITY5 = []
    for (entity,value) in rbac_generation.rbac['Utility 5'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                UTILITY5.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            UTILITY5.append(item)

# ---------------- SP 1 - JSON Creation ------------------ #
    SP1 = []
    for (entity,value) in rbac_generation.rbac['Service Provider 1'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                SP1.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            SP1.append(item)

# ---------------- SP 2 - JSON Creation ------------------ #
    SP2 = []
    for (entity,value) in rbac_generation.rbac['Service Provider 2'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                SP2.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            SP2.append(item)

# ---------------- SP 3 - JSON Creation ------------------ #
    SP3 = []
    for (entity,value) in rbac_generation.rbac['Service Provider 3'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                SP3.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            SP3.append(item)

# ---------------- SP 4 - JSON Creation ------------------ #
    SP4 = []
    for (entity,value) in rbac_generation.rbac['Service Provider 4'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                SP4.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            SP4.append(item)

# ---------------- SP 5 - JSON Creation ------------------ #
    SP5 = []
    for (entity,value) in rbac_generation.rbac['Service Provider 5'].items():
        if entity == 'DER':
            for der in value:
                item = {
                    'name': der,
                    'address': find_Address(der),
                    'role': ''
                }
                SP5.append(item)
        else:
            item = {
                'name': entity,
                'address': find_Address(entity),
                'role': value
            }
            SP5.append(item)

# ---------------- SP 5 - JSON Creation ------------------ #
    DEROWNERS = []
    for (entity,value) in rbac_generation.rbac['DER Device'].items():
        item = {
            'name': entity,
            'address': find_Address(entity),
            'role': value
        }
        DEROWNERS.append(item)

# ---------------- SP 5 - JSON Creation ------------------ #
    SECADMINS = []
    for (entity,value) in rbac_generation.rbac['Security Administrator'].items():
        item = {
            'name': entity,
            'address': find_Address(entity),
            'role': value
        }
        SECADMINS.append(item)

    SECAUDITORS = []
    for (entity,value) in rbac_generation.rbac['Security Auditor'].items():
        item = {
            'name': entity,
            'address': find_Address(entity),
            'role': value
        }
        SECAUDITORS.append(item)

    ending = time.time()
    print('Server Initiation Time is: '+ str(ending-starting))
    app.run()

