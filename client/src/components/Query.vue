<template>
  <body>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
      <script type="application/javascript" src="jquery-3.5.1.min.js"></script>
      <script type="application/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/downloadjs/1.4.8/download.min.js"></script>
        <div class="container" >
      <!-- Navigation -->
      <nav class="navbar-default navbar-fixed-top">
    <div class="container">
      <!-- Brand and toggle get grouped for better mobile display -->
      <div class="navbar-header page-scroll">
        <button type="button" class="navbar-toggle"
        data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand page-scroll" href="#page-top">
          <img src="./images/Sandia_logo.png" alt="Lattes theme logo"></a>
      </div>
      <!-- Collect the nav links, forms, and other content for toggling -->
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
         <ul class="nav navbar-right">
        <li>
            <a v-on:click='dashboard' class="page-scroll">My dashboard</a>
          </li>
          <li>
            <a v-on:click='signout' class="page-scroll">Sign Out</a>
          </li>
        </ul>
      </div>
      <!-- /.navbar-collapse -->
    </div>
    <!-- /.container-fluid -->
  </nav>
   </div>
    <h1 class="mt-4 text-center">Query Page - Find what you want!</h1>
    <form>
        <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
        <h2>Search User </h2>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="username" class="col-form-label">Username</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="username" id="inputPassword6"
                class="form-control"
                placeholder="Ex: George Fragkos">
            </div>
            <div class="col-auto">
                <span id="passwordHelpInline" class="form-text">
                (Must contain First Name and Last Name)
                </span>
            </div>
        </div>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="address" class="col-form-label">Ethereum <br> Address</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="address"
                class="form-control"
                placeholder="Ex: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1">
            </div>
            <div class="col-auto">
                <span id="passwordHelpInline" class="form-text">
                (Must be a hexadecimal)
                </span>
            </div>
        </div>
        <br>
      <button type="button" @click="onSubmit,successAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Search
      </button>
      </div>
      <br>
      <br>
      <br>
      <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
      <h2>Add User </h2>
        <br>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="add_firstname">First Name</label>
      <input v-model="add_firstname" type="text" class="form-control"
      id="inputEmail4" placeholder="Ex: George">
    </div>
    <div class="form-group col-md-3">
      <label for="add_lastname">Last Name</label>
      <input v-model="add_lastname" type="text" class="form-control"
      id="inputPassword4" placeholder="Ex: Fragkos">
    </div>
  </div>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="add_role">Role</label>
      <select  v-model="add_role" id="inputState" class="form-control">
        <option selected>Choose Role...</option>
        <option>Utility DERMS Team</option>
        <option>Utility Software</option>
        <option>Utility Billing</option>
        <option>Utility Auditing</option>
        <option>DER Installers</option>
        <option>Aggregation/VPP Team</option>
        <option>Firmware/Patching</option>
        <option>Billing</option>
        <option>DER Owner</option>
        <option>Security Administrator</option>
        <option>Security Auditor</option>
      </select>
    </div>
    <div class="form-group col-md-3">
      <label for="inputState">Association</label>
      <select v-model="add_association" id="inputState" class="form-control">
        <option selected>Choose Association...</option>
        <option>Utility 1</option>
        <option>Utility 2</option>
        <option>Utility 3</option>
        <option>Utility 4</option>
        <option>Utility 5</option>
        <option>Service Provider 1</option>
        <option>Service Provider 2</option>
        <option>Service Provider 3</option>
        <option>Service Provider 4</option>
        <option>Service Provider 5</option>
        <option>DER Owners</option>
        <option>Security Entities</option>
      </select>
    </div>
        <div class="form-group col-md-3">
      <label for="enter_der">DER Device</label>
      <input v-model="enter_der" type="text" class="form-control"
      id="inputPassword4" placeholder="Ex: DER 123">
    </div>

    </div>
      <button type="button" @click="onSubmit,successAddAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Add
      </button>
   </div>
   <br>
   <br>
   <br>
      <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
        <h2>Search DER </h2>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="der_number" class="col-form-label">DER Device</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="der_number" id="inputPassword6"
                class="form-control"
                placeholder="Ex: DER 1234">
            </div>
            <div class="col-auto">
            </div>
        </div>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="der_address" class="col-form-label">Ethereum <br> Address</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="der_address"
                class="form-control"
                placeholder="Ex: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1">
            </div>
            <div class="col-auto">
                <span id="passwordHelpInline" class="form-text">
                (Must be a hexadecimal)
                </span>
            </div>
        </div>
        <br>
      <button type="button" @click="onSubmit,successDERSearchAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Search
      </button>
      </div>
      <br>
      <br>
      <br>
            <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
      <h2>Add DER Device </h2>
        <br>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="add_der_device">DER Device</label>
      <input v-model="add_der_device" type="text" class="form-control"
      id="inputEmail4" placeholder="Ex: DER 1234">
    </div>

  </div>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="add_der_association">Association</label>
      <select v-model="add_der_association" id="inputState" class="form-control" multiple>
        <option selected>Choose Association...</option>
        <option>Utility 1</option>
        <option>Utility 2</option>
        <option>Utility 3</option>
        <option>Utility 4</option>
        <option>Utility 5</option>
        <option>Service Provider 1</option>
        <option>Service Provider 2</option>
        <option>Service Provider 3</option>
        <option>Service Provider 4</option>
        <option>Service Provider 5</option>
      </select>
    </div>
    </div>
      <button type="button" @click="onSubmit,successAddDERAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Add
      </button>
   </div>
   <br>
   <br>
   <br>
         <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
      <h2>Verify User-To-Role Assignment </h2>
        <br>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="verify_name">Username</label>
      <input v-model="verify_name" type="text" class="form-control"
      id="inputEmail4" placeholder="Ex: George Fragkos">
    </div>
    <div class="form-group col-md-3">
      <label for="verify_address">Ethereum Address</label>
      <input v-model="verify_address" type="text" class="form-control"
      id="inputPassword4" placeholder="Ex: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1">
    </div>
  </div>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="verify_role">Role</label>
      <select  v-model="verify_role" id="inputState" class="form-control">
        <option selected>Choose Role...</option>
        <option>Utility DERMS Team</option>
        <option>Utility Software</option>
        <option>Utility Billing</option>
        <option>Utility Auditing</option>
        <option>DER Installers</option>
        <option>Aggregation/VPP Team</option>
        <option>Firmware/Patching</option>
        <option>Billing</option>
        <option>DER Owner</option>
        <option>Security Administrator</option>
        <option>Security Auditor</option>
      </select>
    </div>
    </div>
      <button type="button" @click="onSubmit,successVerifyAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Verify
      </button>
   </div>
   <br>
   <br>
   <br>
      <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
        <h2>Delete User </h2>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="delete_username" class="col-form-label">Username</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="delete_username" id="inputPassword6"
                class="form-control"
                placeholder="Ex: George Fragkos">
            </div>
            <div class="col-auto">
                <span id="passwordHelpInline" class="form-text">
                (Must contain First Name and Last Name)
                </span>
            </div>
        </div>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="delete_address" class="col-form-label">Ethereum <br> Address</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="delete_address"
                class="form-control"
                placeholder="Ex: 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1">
            </div>
            <div class="col-auto">
                <span id="passwordHelpInline" class="form-text">
                (Must be a hexadecimal)
                </span>
            </div>
        </div>
        <br>
      <button type="button" @click="onSubmit,successDeleteAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Delete
      </button>
      </div>
      <br>
      <br>
      <br>
       <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
      <h2>Check Permissions </h2>
        <br>
  <div class="form-row">
    <div class="form-group col-md-3">
      <label for="perm_username">Username</label>
      <input v-model="perm_username" type="text" class="form-control"
      id="inputEmail4" placeholder="Ex: George Fragkos">
    </div>
    <div class="form-group col-md-3">
      <label for="perm_address">Address</label>
      <input v-model="perm_address" type="text" class="form-control"
      id="inputEmail4" placeholder="Ex: 0xe25d6b083A5Fb172f9C2E468379d5f8D148a7003">
    </div>
    <div class="form-group col-md-3">
      <label for="perm_device">Device</label>
      <input v-model="perm_device" type="text" class="form-control"
      id="inputPassword4" placeholder="Ex: DER 1234">
    </div>
    <div class="form-group col-md-3">
      <label for="perm_model">Model</label>
      <input v-model="perm_model" type="text" class="form-control"
      id="inputPassword4" placeholder="Ex: DERMeasureAC">
    </div>
    <div class="form-group col-md-3">
      <label for="perm_operation">Register</label>
      <input v-model="perm_operation" type="text" class="form-control"
      id="inputPassword4" placeholder="Ex: InvSt">
    </div>
  </div>
      <button type="button" @click="onSubmit,successPermAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Check
      </button>
   </div>
      <br>
      <br>
      <br>
        <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
        <h2>Search Block </h2>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="block_number" class="col-form-label">Block Number</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="block_number" id="inputPassword6"
                class="form-control"
                placeholder="Ex: 1">
            </div>
        </div>
        <br>
      <button type="button" @click="onSubmit,successBlockAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Search
      </button>
      </div>
      <br>
      <br>
      <br>
                 <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
        <h2>Search Transaction </h2>
        <br>
        <div class="row g-3 align-items-center">
            <div class="col-auto">
                <label for="transaction_number" class="col-form-label">Transaction Hash</label>
            </div>
            <div class="col-auto">
                <input type="text" v-model="transaction_number" id="inputPassword6"
                class="form-control"
                placeholder=
                "Ex: 0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060">
            </div>
        </div>
        <br>
      <button type="button" @click="onSubmit,successTransactionAlert()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Search
      </button>
      </div>
      <br>
      <br>
      <br>
           <div  onmouseover="this.style.background='#E0E0E0';"
        onmouseout="this.style.background='#f2f2f2';">
      <h2>Download Log File </h2>
        <br>
        <button type="button" @click="Download()"
      class="btn btn-danger btn-sm" style='font-size:15px;'>
        Download
      </button>
        </div>
        <br>
        <br>
        <br>
    </form>
    <button @click="topFunction()" id="myBtn" title="Go to top">Go to Top</button>
    </body>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      entities: [],
      username: '',
      address: '',
      perm_username: '',
      perm_address: '',
      perm_device: '',
      perm_operation: '',
      perm_model: '',
      add_role: 'Choose Role...',
      add_association: 'Choose Association...',
      enter_der: '',
      userr: '',
      add_firstname: '',
      add_lastname: '',
      der_number: '',
      der_address: '',
      add_der_device: '',
      add_der_association: 'Choose Association...',
      add_der_address: '',
      verify_name: '',
      verify_address: '',
      verify_role: 'Choose Role...',
      delete_username: '',
      delete_address: '',
      block_number: '',
      transaction_number: '',
    };
  },
  methods: {
    successAlert() {
      if (this.username === '' && this.address === '') {
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information',
        });
      } else if (this.username !== '' && this.address === '') {
        this.username = this.username.trimEnd();
        const payload = {
          username: this.username,
          address: this.address,
        };
        const path = `http://localhost:5000/get_entity_info/${payload.username}`;
        axios.put(path, payload)
          .then((response) => {
            if (response.data.sent_address === '0x0000000000000000000000000000000000000000') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The requested User is not found! Pleasy try again.',
              });
            } else {
              // Check if the user is a DER Owner
              if (response.data.sent_owner !== '') {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: this.username.concat(' has an Ethereum Address: ', response.data.sent_address, ' and an RBAC Role: ', response.data.sent_role, ', and the device is: ', response.data.sent_owner),
                });
              }
              if (response.data.sent_owner === '') {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: this.username.concat(' has an Ethereum Address: ', response.data.sent_address, ' and an RBAC Role: ', response.data.sent_role, ', within ', response.data.sent_parent),
                });
              }
            }
          })
          .catch((error) => {
            console.error(error);
          });
      } else if (this.username === '' && this.address !== '') {
        this.address = this.address.trimEnd();
        const payload = {
          username: this.username,
          address: this.address,
        };
        const path = `http://localhost:5000/get_entity_info/${payload.address}`;
        axios.put(path, payload)
          .then((response) => {
            if (response.data.sent_owner === '') {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: this.address.concat(' has a Username: ', response.data.sent_name, ', and an RBAC Role: ', response.data.sent_role, ', within ', response.data.sent_parent),
              });
            } else {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: this.address.concat(' has a Username: ', response.data.sent_name, ', and an RBAC Role: ', response.data.sent_role, ', and the device is ', response.data.sent_owner),
              });
            }
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'The requested Ethereum Address is not found! Pleasy try again.',
            });
          });
      } else {
        this.address = this.address.trimEnd();
        this.username = this.username.trimEnd();
        const payload = {
          username: this.username,
          address: this.address,
        };
        const path = `http://localhost:5000/get_entity_info/${payload.username}`;
        axios.put(path, payload)
          .then((response) => {
            if (response.data.sent_address === '0x0000000000000000000000000000000000000000') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The requested User is not found! Pleasy try again.',
              });
            } else {
              if (response.data.sent_owner === '') {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: this.username.concat(' has an Ethereum Address: ', response.data.sent_address, ' and an RBAC Role: ', response.data.sent_role, ', within ', response.data.sent_parent),
                });
              }
              if (response.data.sent_owner !== '') {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: this.username.concat(' has an Ethereum Address: ', response.data.sent_address, ' and an RBAC Role: ', response.data.sent_role, ', and the device is: ', response.data.sent_owner),
                });
              }
            }
          })
          .catch((error) => {
            console.error(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'The requested Ethereum Address is not found! Pleasy try again.',
            });
          });
      }
    },
    successPermAlert() {
      const t0 = performance.now();
      if ((this.perm_username === '' && this.perm_address === '') || this.perm_model === ''
      || this.perm_device === '' || this.perm_operation === '') {
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information',
        });
      } else {
        this.perm_username = this.perm_username.trimEnd();
        this.perm_username = this.perm_username.trimStart();
        this.perm_address = this.perm_address.trimEnd();
        this.perm_address = this.perm_address.trimStart();
        this.perm_device = this.perm_device.trimEnd();
        this.perm_device = this.perm_device.trimStart();
        this.perm_model = this.perm_model.trimEnd();
        this.perm_model = this.perm_model.trimStart();
        this.perm_operation = this.perm_operation.trimEnd();
        this.perm_operation = this.perm_operation.trimStart();
        console.log(this.perm_model);
        const payload = {
          username: this.perm_username,
          address: this.perm_address,
          device: this.perm_device,
          model: this.perm_model,
          operation: this.perm_operation,
        };
        let temp = 'a';
        if (!(payload.username)) {
          temp = payload.address;
        } else {
          temp = payload.username;
        }
        const path = `http://localhost:5000/get_entity_info/${temp}`;
        axios.put(path, payload)
          .then((response) => {
            if (response.data.flag === 'False') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The requested User is not found! Pleasy try again.',
              });
            } else {
              const permAssociation = response.data.sent_parent;
              this.userr = response.data.sent_name;
              console.log(permAssociation);
              const payload2 = {
                username: this.perm_device,
                address: '',
              };
              const path2 = 'http://localhost:5000/get_der_info';
              axios.put(path2, payload2)
                .then((response2) => {
                  if (response2.data.flag === 'False') {
                    this.$swal({
                      icon: 'error',
                      type: 'success',
                      title: 'Search Results',
                      text: 'The requested DER is not found! Pleasy try again.',
                    });
                  } else {
                    const permAssociation2 = response2.data.sent_parent.split(',');
                    console.log(permAssociation2);
                    const payload3 = {
                      firstName: this.userr.split(' ')[0],
                      lastName: this.userr.split(' ')[1],
                      parent: permAssociation,
                      model: this.perm_model,
                      operation: this.perm_operation,
                    };
                    const path3 = 'http://localhost:5000/showperm';
                    axios.put(path3, payload3)
                      .then((response3) => {
                        if (response3.data.flag === 'False') {
                          this.$swal({
                            icon: 'error',
                            type: 'success',
                            title: 'Search Results',
                            text: 'The requested User is not found! Pleasy try again.',
                          });
                        } else {
                          const permAssociation3 = response3.data;
                          console.log(permAssociation3);

                          if (permAssociation2.includes(permAssociation)
                          || permAssociation2.includes(payload3.lastName)) {
                            if (response3.data.answer === 'Yes') {
                              this.$swal({
                                icon: 'info',
                                type: 'success',
                                title: 'Search Results',
                                text: 'The requested Register can be accessed! Permissions:'.concat(response3.data.answer_op),
                              });
                            } else {
                              this.$swal({
                                icon: 'error',
                                type: 'success',
                                title: 'Search Results',
                                text: 'No Permissions for this Register or Register not existing!',
                              });
                            }
                          } else {
                            this.$swal({
                              icon: 'error',
                              type: 'success',
                              title: 'Search Results',
                              text: 'This User cannot perform an operation to this DER.',
                            });
                          }
                        }
                      })
                      .catch((error) => {
                        console.error(error);
                        this.$swal({
                          icon: 'error',
                          type: 'success',
                          title: 'Search Results',
                          text: 'The requested User is not found! Pleasy try again.',
                        });
                      });
                  }
                })
                .catch((error) => {
                  console.error(error);
                  this.$swal({
                    icon: 'error',
                    type: 'success',
                    title: 'Search Results',
                    text: 'The requested User is not found! Pleasy try again.',
                  });
                });
            }
          })
          .catch((error) => {
            console.error(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'The requested User is not found! Pleasy try again.',
            });
          });
      }
      const t1 = performance.now();
      console.log((t1 - t0));
    },
    successAddAlert() {
      if (this.add_firstname === '' || this.add_lastname === '' || this.add_role === 'Choose Role...' || this.add_association === 'Choose Association...') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide more information',
        });
      } else {
        this.add_role = this.add_role.trimEnd();
        this.enter_der = this.enter_der.trimEnd();
        this.add_firstname = this.add_firstname.trimEnd();
        this.add_lastname = this.add_lastname.trimEnd();
        console.log(this.add_role);
        if (this.add_role === 'DER Owner' && this.enter_der === '') {
          this.$swal({
            icon: 'error',
            type: 'success',
            title: 'Error in Search',
            text: 'Please provide a DER Device',
          });
        } else if (this.add_role === 'DER Owner' && this.enter_der !== '') {
          const payload = {
            firstName: this.add_firstname,
            lastName: this.add_lastname,
            role: this.add_role,
            association: this.add_association,
            device: this.enter_der,
          };
          const path = 'http://localhost:5000/add_user';
          axios.put(path, payload)
            .then((response) => {
              if (response.data.sent_response === 'Existing User') {
                this.$swal({
                  icon: 'error',
                  type: 'success',
                  title: 'Search Results',
                  text: 'The provided user already exists in the system. Please try again!',
                });
              } else if (response.data.sent_response === 'Existing DER Device') {
                this.$swal({
                  icon: 'error',
                  type: 'success',
                  title: 'Search Results',
                  text: 'The provided DER Device already exists in the system. Please try again!',
                });
              } else {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: 'The User is added in the system!',
                });
              }
            })
            .catch((error) => {
              console.log(error);
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'There is an error in the system. Please try again!',
              });
            });
          console.log(2);
        } else {
          const payload = {
            firstName: this.add_firstname,
            lastName: this.add_lastname,
            role: this.add_role,
            association: this.add_association,
            device: this.enter_der,
          };
          const path = 'http://localhost:5000/add_user';
          axios.put(path, payload)
            .then((response) => {
              if (response.data.sent_response === 'Existing User') {
                this.$swal({
                  icon: 'error',
                  type: 'success',
                  title: 'Search Results',
                  text: 'The provided user already exists in the system. Please try again!',
                });
              } else {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: 'The User is added in the system!',
                });
              }
            })
            .catch((error) => {
              console.log(error);
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'There is an error in the system. Please try again!',
              });
            });
          console.log(2);
        }
      }
    },
    topFunction() {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    },
    dashboard() {
      this.$router.go(-1);
    },
    signout() {
      delete localStorage.token;
      this.$router.replace(this.$route.query.redirect || '/');
    },
    successDERSearchAlert() {
      this.der_number = this.der_number.trimEnd();
      this.der_address = this.der_address.trimEnd();
      if (this.der_number === '' && this.der_address === '') {
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information',
        });
      } else if (this.der_number !== '' && this.der_address === '') {
        const payload = {
          username: this.der_number,
          address: this.der_address,
        };
        const path = 'http://localhost:5000/get_der_info';
        axios.put(path, payload)
          .then((response) => {
            if (response.data.sent_address === '0x0000000000000000000000000000000000000000') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The requested User is not found! Pleasy try again.',
              });
            } else {
              console.log(1);
              if (response.data.sent_owner === '') {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: this.der_number.concat(' has an Ethereum Address: ', response.data.sent_address, ', within ', response.data.sent_parent),
                });
              }
            }
          })
          .catch((error) => {
            console.log(this.der_number);
            console.log(error);
          });
      } else if (this.der_number === '' && this.der_address !== '') {
        const payload = {
          username: this.der_number,
          address: this.der_address,
        };
        const path = 'http://localhost:5000/get_der_info';
        axios.put(path, payload)
          .then((response) => {
            console.log(1);
            if (response.data.sent_owner === '') {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: this.der_address.concat(' is the device: ', response.data.sent_name, ', within ', response.data.sent_parent),
              });
            }
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'The requested Ethereum Address is not found! Pleasy try again.',
            });
          });
      } else {
        const payload = {
          username: this.der_number,
          address: this.der_address,
        };
        const path = 'http://localhost:5000/get_der_info';
        axios.put(path, payload)
          .then((response) => {
            if (response.data.sent_address === '0x0000000000000000000000000000000000000000') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The requested User is not found! Pleasy try again.',
              });
            } else {
              console.log(1);
              if (response.data.sent_owner === '') {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: this.der_number.concat(' has an Ethereum Address: ', response.data.sent_address, ', within ', response.data.sent_parent),
                });
              }
            }
          })
          .catch((error) => {
            console.error(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'The requested Ethereum Address is not found! Pleasy try again.',
            });
          });
      }
    },
    successAddDERAlert() {
      this.add_der_device = this.add_der_device.trimEnd();
      if (this.add_der_device === '' || this.add_der_association[0] === 'Choose Association...') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide correct information',
        });
      } else {
        console.log(this.add_der_association);
        const payload = {
          device: this.add_der_device,
          association: this.add_der_association,
        };
        const path = 'http://localhost:5000/add_der_device';
        axios.put(path, payload)
          .then((response) => {
            if (response.data.sent_response === 'Existing DER') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The provided DER Device already exists in the system. Please try again!',
              });
            } else {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: 'The DER Device is added in the system!',
              });
            }
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'There is an error in the system. Please try again!',
            });
          });
        console.log(2);
      }
    },
    Download() {
      axios({
        url: 'http://localhost:5000/download',
        method: 'POST',
        responseType: 'blob', // important
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'blockchain_log.txt');
        document.body.appendChild(link);
        link.click();
      });
    },
    successVerifyAlert() {
      this.verify_name = this.verify_name.trimEnd();
      this.verify_address = this.verify_address.trimEnd();
      if ((this.verify_name === '' && this.verify_address === '') || this.verify_role === 'Choose Role...') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide more information',
        });
      } else {
        console.log(this.verify_address);
        const payload = {
          username: this.verify_name,
          address: this.verify_address,
          role: this.verify_role,
        };
        const path = 'http://localhost:5000/verify_utr';
        axios.put(path, payload)
          .then((response) => {
            console.log(response.data.sent_verification);
            if (response.data.flag === 'True') {
              if (response.data.sent_verification) {
                this.$swal({
                  icon: 'info',
                  type: 'success',
                  title: 'Search Results',
                  text: 'User '.concat(response.data.sent_username, ' (', response.data.sent_address, ') is authorized for the Role: ', response.data.sent_role, ', under ', response.data.sent_parent),
                });
              } else {
                this.$swal({
                  icon: 'error',
                  type: 'success',
                  title: 'Search Results',
                  text: 'User '.concat(response.data.sent_username, ' (', response.data.sent_address, ') is not authorized for the Role: ', response.data.sent_role),
                });
              }
            } else {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'Please provide correct information for the user',
              });
            }
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'Please provide correct information for the user',
            });
          });
      }
    },
    successDeleteAlert() {
      this.delete_username = this.delete_username.trimEnd();
      this.delete_address = this.delete_address.trimEnd();
      if (this.delete_username === '' && this.delete_address === '') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information for the user',
        });
      } else {
        console.log(this.delete_address);
        const payload = {
          username: this.delete_username,
          address: this.delete_address,
        };
        const path = 'http://localhost:5000/delete_user';
        axios.put(path, payload)
          .then((response) => {
            console.log(response.data.sent_verification);
            if (response.data.flag === 'True') {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: 'User is successfully deleted!',
              });
            } else {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'Please provide correct information for the user',
              });
            }
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'There is an error in the system',
            });
          });
      }
    },
    successBlockAlert() {
      this.block_number = this.block_number.trimEnd();
      if (this.block_number === '') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information for the block',
        });
      } else {
        console.log(this.block_number);
        const payload = {
          block: this.block_number,
        };
        const path = 'http://localhost:5000/find_block';
        axios.put(path, payload)
          .then((response) => {
            console.log(response.data.sent_hash);
            if (response.data.flag === 'False') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'Block Number is wrong. Please try again',
              });
            } else {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: 'Block '.concat(this.block_number, ' with hash ', response.data.sent_hash, ', has size ', response.data.sent_size, ' and the mined transaction hash is ', response.data.sent_trx),
              });
            }
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'There is an error in the system',
            });
          });
      }
    },
    successTransactionAlert() {
      this.tramsaction_number = this.transaction_number.trimEnd();
      if (this.transaction_number === '') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide the hash for the transaction',
        });
      } else {
        console.log(this.transaction_number);
        const payload = {
          transaction: this.transaction_number,
        };
        const path = 'http://localhost:5000/find_transaction';
        axios.put(path, payload)
          .then((response) => {
            console.log(response.data.sent_block);
            this.$swal({
              icon: 'info',
              type: 'success',
              title: 'Search Results',
              text: 'Transaction '.concat('with hash ', this.transaction_number, ' is in block ', response.data.sent_block, ', from ', response.data.sent_from),
            });
          })
          .catch((error) => {
            console.log(error);
            this.$swal({
              icon: 'error',
              type: 'success',
              title: 'Search Results',
              text: 'Please provide an existing Transaction Hash',
            });
          });
      }
    },
  },
};
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Open+Sans);

.yourDivClass {
  background: url('./images/utility_bg.jpg') no-repeat center center / cover
}
body{
  background: #f2f2f2;
  font-family: 'Open Sans', sans-serif;
}

.search {
  width: 100%;
  position: relative;
  display: flex;
}

.searchTerm {
  width: 100%;
  border: 3px solid #00B4CC;
  border-right: none;
  padding: 5px;
  height: 20px;
  border-radius: 5px 0 0 5px;
  outline: none;
  color: #9DBFAF;
}

.searchTerm:focus{
  color: #00B4CC;
}

.searchButton {
  width: 40px;
  height: 36px;
  border: 1px solid #00B4CC;
  background: #00B4CC;
  text-align: center;
  color: #fff;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  font-size: 20px;
}

/*Resize the wrap to see the search bar change!*/
.wrap{
  width: 30%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

#myBtn {
  position: fixed; /* Fixed/sticky position */
  bottom: 20px; /* Place the button at the bottom of the page */
  right: 30px; /* Place the button 30px from the right */
  z-index: 99; /* Make sure it does not overlap */
  border: none; /* Remove borders */
  outline: none; /* Remove outline */
  background-color: grey; /* Set a background color */
  color: white; /* Text color */
  cursor: pointer; /* Add a mouse pointer on hover */
  padding: 15px; /* Some padding */
  border-radius: 10px; /* Rounded corners */
  font-size: 13px; /* Increase font size */
}

#myBtn:hover {
  background-color: #555; /* Add a dark-grey background on hover */
}
</style>
