pragma solidity ^0.5.0;


contract RBAC{

uint256 constant NO_ROLE = 0;


event ProfileAdded(string username, address _address);
event AssociationAdded(string child, string parent, address _child, address _parent);
event BearerAdded(address account, uint256 role);
event BearerRemoved(address account, uint256 role);


struct Profile{
    string profile_description;
    address username;
}

Profile[] public profiles;

struct Association{
    string __child;
    string __parent;
    address childd;
    address parentt;
}

Association[] public associations;

struct Role{
    string description;
    mapping (address => bool) bearers;
}

Role[] public roles;
address admin = msg.sender;


mapping (string => address) public profileExists;
mapping (address => string) public profileName;
mapping (string => mapping(string => bool)) public isAssoc;
mapping (address => mapping(address=>bool)) public isAssoc_address;
mapping (string => Profile[]) allChildren;
mapping (address => Profile[]) allChildrenAddress;
mapping (string => string[]) allParents;
mapping (string => string) public allRoles_Names;
mapping (address => string) public allRoles_Address;
mapping (string => mapping(string => bool)) public has_Role;
mapping (string => string) public names_to_parents;
mapping (address => string) public address_to_parents;
mapping (string => mapping(string => string)) public user_to_perm;       // DER Entity Name -> Model -> Permission
mapping (address => mapping(string => string)) public address_to_perm;  // DER Entity Address -> Model -> Permission


function addPermissions(string memory user, string memory model, address _user, string memory perm) public
{
    user_to_perm[user][model] = (perm);
    address_to_perm[_user][model] = (perm);
}



function queryPermissions(string memory user, string memory model) public view returns(string memory children)
{
    // uint256 length = user_to_perm[user][model].length;
    // children = new bytes32[](length);

    // for(uint256 i = 0; i < length; i++)
    // {
    //     children[i] = stringToBytes32(user_to_perm[user][model]);
    // }
    return user_to_perm[user][model];
}

function queryAddressPermissions(address _user, string memory model) public view returns(string memory children)
{
    // uint256 length = address_to_perm[_user][model].length;
    // children = new bytes32[](length);

    // for(uint256 i = 0; i < length; i++)
    // {
    //     children[i] = stringToBytes32(address_to_perm[_user][model][i]);
    // }
    return address_to_perm[_user][model];
}

function createProfile(string memory _username, address user) public returns(uint256)
{

    uint256 profile_id = profiles.push(Profile({profile_description: _username, username:user})) - 1;
    profileExists[_username] = user;
    profileName[user] = _username;
    emit ProfileAdded(_username, user);
    return profile_id;
}

function deleteProfile(string memory _username, address user) public
{
    delete profileExists[_username];
    delete profileName[user];
}

function profileAddress(string memory _username) public view returns(address)
{
    return profileExists[_username];
}

function profileUsername(address user) public view returns(string memory)
{
    return profileName[user];
}

function addChild(string memory _child, string memory _parent, address child, address parent) public returns(uint256)
{
    uint association = associations.push(Association({__child: _child, __parent:_parent, childd: child, parentt:parent})) - 1;
    isAssoc[_child][_parent] = true;
    isAssoc_address[child][parent] = true;
    names_to_parents[_child] = _parent;
    address_to_parents[child] = _parent;
    Profile memory temp_profile = Profile(_child, child);
    allChildren[_parent].push(temp_profile);
    allParents[_child].push(_parent);
    allChildrenAddress[parent].push(temp_profile);
    emit AssociationAdded(_child, _parent, child, parent);
    return association;
}

function deleteAssoc(string memory _child, string memory _parent) public
{
    isAssoc[_child][_parent] = false;
    delete names_to_parents[_child];

}

function deleteAssocAddress(address _child, address _parent) public
{
    isAssoc_address[_child][_parent] = false;
    delete address_to_parents[_child];
}

function isChild(string memory _child, string memory _parent) public view returns(bool)
{
    return isAssoc[_child][_parent];
}

function returnParent(string memory _child) public view returns(string memory)
{
    return names_to_parents[_child];
}

function returnParentFromAddress(address _child) public view returns(string memory)
{
return address_to_parents[_child];
}

function isChild_address(address child, address parent) public view returns(bool)
{
    return isAssoc_address[child][parent];
}

// Make sure that the string is no longer than 32 bytes or results will be cut
function stringToBytes32(string memory source) private pure returns (bytes32 result)
{
    bytes memory tempEmptyStringTest = bytes(source);
    if(tempEmptyStringTest.length == 0)
    {
        return 0x0;
    }

    assembly
    {
        result := mload(add(source,32))
    }
}


function getChildrenNames(string memory username) public view returns(bytes32[] memory children)
{
    uint256 length = allChildren[username].length;
    children = new bytes32[](length);

    for(uint256 i = 0; i < length; i++)
    {
        children[i] = stringToBytes32(allChildren[username][i].profile_description);
    }

}

function getParentsNames(string memory username) public view returns(bytes32[] memory parents)
{
    uint256 length = allParents[username].length;
    parents = new bytes32[](length);

    for(uint256 i = 0; i < length; i++)
    {
        parents[i] = stringToBytes32(allParents[username][i]);
    }
}

function getChildrenAddresses(address _parent) public view returns(address[] memory children)
{
    uint256 length = allChildrenAddress[_parent].length;
    children = new address[](length);

    for(uint256 i = 0; i < length; i++)
    {
        children[i] = allChildrenAddress[_parent][i].username;
    }

}

function addRoleToUser(string memory username, address _user ,string memory _role) public
{
    allRoles_Names[username] = _role;
    has_Role[username][_role] = true;
    allRoles_Address[_user] = _role;
}

function revokeRole(string memory username, address _user, string memory _role) public
{
    delete allRoles_Names[username];
    delete allRoles_Address[_user];
    has_Role[username][_role] = false;
}

function hasRole(string memory username, string memory _role) public view returns(bool)
{
    return has_Role[username][_role];
}

function getRolesfromNames(string memory username) public view returns(string memory)
{
    return allRoles_Names[username];
}

function getRolesfromAddress(address _user) public view returns(string memory)
{
    // uint256 length = allRoles_Address[_user].length;
    // all_roles = new bytes32[](length);

    // for(uint256 i = 0; i < length; i++)
    // {
    //     all_roles[i] = stringToBytes32(allRoles_Address[_user][i]);
    // }

    return allRoles_Address[_user];
}


}