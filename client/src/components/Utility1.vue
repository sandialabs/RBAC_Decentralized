<template>
<div class="yourDivClass">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
  <script type="application/javascript" src="jquery-3.5.1.min.js"></script>
    <body id="page-top">

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
            <a v-on:click='dashboard' class="page-scroll">My Dashboard</a>
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
  <br>
  <br>
  <br>
    <h1 style='font-size:45px;'>Utility 1</h1>
     <br>

      <input type="text"
         placeholder="Filter by Name or Ethereum Address"
         v-model="filter" size="40"  style="height:30px" static /><font size="2">
           <span class="fa fa-search"></span></font>
    <div class="row">
      <div class="col-sm-30">
        <div>
        </div>
        <hr><br>
         <br>
        <table class="table table-hover" style='font-size:15px;'>
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Ethereum Address</th>
              <th scope="col">RBAC Role</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entity, key) in filteredRows" :key="key">
              <td contenteditable='true' @input="handleInput($event, 'name')">
                {{ entity.name }}</td>
              <td>
                {{ entity.address }}</td>
              <td contenteditable='true' @input="handleInput($event, 'role')">
                {{ entity.role }}</td>
              <td>
                <div class="btn-group" role="group">
              <button
                      type="button"
                      class="btn btn-warning btn-sm" style='font-size:15px;'
                      @click="onClickItem(key, entity.name, entity.address, entity.role);
                      successAlert()">
                  Update Entity
              </button>
              <button
                      type="button"
                      class="btn btn-danger btn-sm" style='font-size:15px;'
                      @click="onClickItemRevoke(key, entity.name, entity.address, entity.role);
                      revokeAlert()">
                  Revoke Role
              </button>
              <button
                      type="button"
                      class="btn btn-success btn-sm" style='font-size:15px;'
                      @click="onClickItemPerm(key, entity.name, entity.address, entity.role);
                      permAlert()">
                  Show Permissions
              </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="topFunction()" id="myBtn" title="Go to top">Go to Top</button>
    </div>
  </div>
  </body>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      entities: [],
      filter: '',
    };
  },
  computed: {
    filteredRows() {
      return this.entities.filter((entity) => {
        const name = entity.name.toString().toLowerCase();
        const address = entity.address.toLowerCase();
        const role = entity.role.toLowerCase();
        const searchTerm = this.filter.toLowerCase();
        return name.includes(searchTerm) || address.includes(searchTerm)
        || role.includes(searchTerm);
      });
    },
  },
  methods: {
    successAlert() {
      this.$swal({
        type: 'success',
        title: 'Update Success',
        text: 'DER Entity is successfuly updated!',
      });
    },
    revokeAlert() {
      this.$swal({
        type: 'success',
        title: 'Revoke Role Success',
        text: 'Role is successfuly revoked!',
      });
    },
    handleInput(e, column) {
      this.content = e.target.innerHTML;
      this.edit_column = column;
      console.log(this.content);
    },
    topFunction() {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    },
    onClickItem(key, oldname, oldaddress, oldrole) {
      if (this.edit_column === 'name') {
        this.content = this.content.trimStart();
        const payload = {
          oldName: oldname,
          oldRole: oldrole,
          name: this.content,
          address: oldaddress,
          role: oldrole,
        };
        this.updateEntity(payload, oldaddress);
        console.log(key, payload.name, oldaddress);
      } else {
        this.content = this.content.trimStart();
        const payload = {
          oldName: oldname,
          oldRole: oldrole,
          name: oldname,
          address: oldaddress,
          role: this.content,
        };
        this.updateEntity(payload, oldaddress);
        console.log(key, payload.title, oldaddress);
      }
    },
    onClickItemRevoke(key, oldname, oldaddress, oldrole) {
      const payload = {
        oldRole: oldrole,
        username: oldname,
        address: oldaddress,
        role: '',
      };
      this.revokeRole(payload, oldaddress);
      console.log(key, payload.name, oldaddress);
    },
    onClickItemPerm(key, parsedName, parsedAddress, parsedRole) {
      console.log(parsedRole);
      const payload = {
        name: parsedName,
        address: parsedAddress,
        role: '',
      };
      this.showPerm(payload);
    },
    showPerm(payload) {
      const path = 'http://localhost:5000/showperm2';
      axios.put(path, payload)
        .then((res) => {
          console.log(res.data);
          if (res.data.flag === 'False') {
            this.$swal({
              icon: 'info',
              type: 'success',
              title: 'Permission Results',
              text: 'No Permissions to show.',
            });
          } else {
            this.$swal({
              icon: 'info',
              type: 'success',
              title: 'Permission Results',
              text: 'The DERCapacity Model is: '.concat(res.data.DERCapacity),
            });
          }
        })
        .catch((error) => {
          console.error(error);
          this.getEntities();
        });
    },
    getEntities() {
      const path = 'http://localhost:5000/utility1';
      axios.get(path)
        .then((res) => {
          this.entities = res.data.entities;
          console.log(this.entities);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book Updated Successfully!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.read = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.read = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      let read = false;
      if (this.addBookForm.read[0]) read = true;
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        read, // property shorthand
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    editBook(book) {
      this.editForm = book;
    },
    dashboard() {
      this.$router.go(-1);
    },
    signout() {
      delete localStorage.token;
      this.$router.replace(this.$route.query.redirect || '/');
    },
    updateEntity(payload, entityID) {
      console.log(payload.name);
      const path = `http://localhost:5000/utilities/${entityID}`;
      axios.put(path, payload)
        .then(() => {
          this.getEntities();
        })
        .catch((error) => {
          console.error(error);
          this.getEntities();
        });
    },
    revokeRole(payload, entityID) {
      const path = `http://localhost:5000/utilitiesrevoke/${entityID}`;
      axios.put(path, payload)
        .then(() => {
          this.getEntities();
        })
        .catch((error) => {
          console.error(error);
          this.getEntities();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks(); // why?
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        read,
      };
      this.updateBook(payload, this.editForm.id);
    },
  },
  updated() {
    if (!localStorage.token && this.$route.path !== '/') {
      this.$router.push('/?redirect='.concat(this.$route.path));
      this.$router.replace(this.$route.query.redirect || '/');
    }
  },
  created() {
    this.getEntities();
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
