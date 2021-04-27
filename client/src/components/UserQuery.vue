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
    <h1 class="mt-4 text-center">Query Page - Find Permissions!</h1>
    <form>
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
    <div class="form-group col-md-1">
      <label for="perm_checkbox_read">Read</label>
      <input v-model="perm_checkbox_read" type="checkbox" class="form-control"
      id="inputPassword4" placeholder="Ex: InvSt">
    </div>
        <div class="form-group col-md-1">
      <label for="perm_checkbox">Write</label>
      <input v-model="perm_checkbox_write" type="checkbox" class="form-control"
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
      permissions: '',
      perm_username: '',
      perm_device: '',
      perm_operation: '',
      perm_model: '',
      address: '',
      add_role: 'Choose Role...',
      add_association: 'Choose Association...',
      perm_checkbox_read: false,
      perm_checkbox_write: false,
      enter_der: '',
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
      if (this.username === '') {
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information',
        });
      } else {
        this.username = this.username.trimEnd();
        this.username = this.username.trimStart();
        const payload = {
          username: this.username,
        };
        const path = 'http://localhost:5000/get_entity_info';
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
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: this.username.concat(' has an RBAC Role: ', response.data.role, ', within ', response.data.entity),
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
    },
    successPermAlert() {
      console.log(this.perm_checkbox_read);
      console.log(this.perm_checkbox_write);
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
        this.perm_device = this.perm_device.trimEnd();
        this.perm_device = this.perm_device.trimStart();
        this.perm_model = this.perm_model.trimEnd();
        this.perm_model = this.perm_model.trimStart();
        this.perm_operation = this.perm_operation.trimEnd();
        this.perm_operation = this.perm_operation.trimStart();
        console.log(this.perm_model);
        const payload = {
          username: this.perm_username,
          address: '',
          device: this.perm_device,
          model: this.perm_model,
          operation: this.perm_operation,
        };
        const path = `http://localhost:5000/get_entity_info/${payload.username}`;
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
                          || permAssociation2.includes(payload3.lastName)
                          || permAssociation2.includes(this.userr)) {
                            if (response3.data.answer === 'Yes') {
                              if (this.perm_checkbox_read === false
                                && this.perm_checkbox_write === false) {
                                this.$swal({
                                  icon: 'error',
                                  type: 'success',
                                  title: 'Search Results',
                                  text: 'The Register can be changed! Permissions:'.concat(response3.data.answer_op, '. Please provide an operation.'),
                                });
                              } else if (this.perm_checkbox_read === true
                                && this.perm_checkbox_write === false) {
                                this.permissions = 'R';
                              } else if (this.perm_checkbox_read === false
                                && this.perm_checkbox_write === true) {
                                this.permissions = 'W';
                              } else {
                                this.permissions = 'RW';
                              }
                              if (this.perm_checkbox_read === true
                                || this.perm_checkbox_write === true) {
                                if (response3.data.answer_op.includes(this.permissions)) {
                                  this.$swal({
                                    icon: 'info',
                                    type: 'success',
                                    title: 'Search Results',
                                    text: 'The Access Token is granted!',
                                  });
                                } else {
                                  this.$swal({
                                    icon: 'info',
                                    type: 'success',
                                    title: 'Search Results',
                                    text: 'The Access Token is not granted! User does not have this permissions.',
                                  });
                                }
                              }
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
      if (this.der_number === '') {
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information',
        });
      } else {
        const payload = {
          username: this.der_number,
        };
        const path = 'http://localhost:5000/get_der_info';
        axios.put(path, payload)
          .then((response) => {
            if (response.data.flag === 'False') {
              this.$swal({
                icon: 'error',
                type: 'success',
                title: 'Search Results',
                text: 'The requested DER is not found! Pleasy try again.',
              });
            } else {
              this.$swal({
                icon: 'info',
                type: 'success',
                title: 'Search Results',
                text: this.der_number.concat(' belongs to: ', response.data.sent_parent),
              });
            }
          })
          .catch((error) => {
            console.log(this.der_number);
            console.log(error);
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
        link.setAttribute('download', 'openLDAP_log.txt');
        document.body.appendChild(link);
        link.click();
      });
    },
    successVerifyAlert() {
      this.verify_name = this.verify_name.trimEnd();
      this.verify_address = this.verify_address.trimEnd();
      if ((this.verify_name === '') || this.verify_role === 'Choose Role...') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide more information',
        });
      } else {
        const payload = {
          username: this.verify_name,
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
                  text: 'User '.concat(this.verify_name, ' is authorized for the Role: ', this.verify_role, ', under ', response.data.sent_parent),
                });
              } else {
                this.$swal({
                  icon: 'error',
                  type: 'success',
                  title: 'Search Results',
                  text: 'User '.concat(this.verify_name, ' is not authorized for the Role: ', this.verify_role),
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
      if (this.delete_username === '') {
        // Not enough information
        this.$swal({
          icon: 'error',
          type: 'success',
          title: 'Error in Search',
          text: 'Please provide information for the user',
        });
      } else {
        const payload = {
          username: this.delete_username,
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
      const payload = {
        info: '',
      };
      const path = 'http://localhost:5000/find_info';
      axios.put(path, payload)
        .then((response) => {
          this.$swal({
            icon: 'info',
            type: 'success',
            title: 'Search Results',
            text: 'There have been executed '.concat(response.data.modify, ' MODIFY operations, ', response.data.add, ' ADD operations, ', response.data.delete, ' DELETE operations and have been transmitted ', response.data.transmitted, ' bytes'),
          });
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
