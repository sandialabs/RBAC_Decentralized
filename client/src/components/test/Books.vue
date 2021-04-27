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
          <img src="../images/Sandia_logo.png" alt="Lattes theme logo"></a>
      </div>
      <!-- Collect the nav links, forms, and other content for toggling -->
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
         <ul class="nav navbar-right">
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
         placeholder="Filter by Author or Title"
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
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, key) in filteredRows" :key="key">
              <td contenteditable='true' @input="handleInput($event, 'title')">
                {{ book.title }}</td>
              <td contenteditable='true' @input="handleInput($event, 'author')">
                {{ book.author }}</td>
              <td>
                <span v-if="book.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
              <button
                      type="button"
                      class="btn btn-warning btn-sm" style='font-size:15px;'
                      @click="onClickItem(key, book.title, book.id); successAlert()">
                  Update
              </button>
      <button type="button" class="btn btn-danger btn-sm" style='font-size:15px;'>Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
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
      image: { backgroundImage: 'url(http://cdn.hipwallpaper.com/m/67/5/cK0jh9.jpg)' },
      books: [],
      filter: '',
      editForm: {
        id: '',
        title: '',
        author: '',
        read: [],
      },
    };
  },
  computed: {
    filteredRows() {
      return this.books.filter((book) => {
        const title = book.title.toString().toLowerCase();
        const author = book.author.toLowerCase();
        const searchTerm = this.filter.toLowerCase();
        return title.includes(searchTerm) || author.includes(searchTerm);
      });
    },
  },
  methods: {
    successAlert() {
      this.$swal({
        type: 'success',
        title: 'Update Success',
        text: 'DER Entity is successfuly added!',
      });
    },
    handleInput(e, column) {
      this.content = e.target.innerHTML;
      this.edit_column = column;
      console.log(this.content);
    },
    onClickItem(key, newtitle, bookid) {
      if (this.edit_column === 'title') {
        const payload = {
          title: this.content,
          author: 'George',
          read: true,
        };
        this.updateBook(payload, bookid);
        console.log(key, payload.title, bookid);
      } else {
        const payload = {
          title: newtitle,
          author: 'George',
          read: true,
        };
        this.updateBook(payload, bookid);
        console.log(key, payload.title, bookid);
        this.message = 'Book Updated Successfully!';
        this.showMessage = true;
      }
    },
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
          console.log(this.books);
        })
        .catch((error) => {
          // eslint-disable-next-line
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
    signout() {
      delete localStorage.token;
      this.$router.replace(this.$route.query.redirect || '/');
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book Updated Successfully!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
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
  created() {
    this.getBooks();
  },
};
</script>

<style scoped>
@import url(https://fonts.googleapis.com/css?family=Open+Sans);

.yourDivClass {
  background: url('../images/utility_bg.jpg') no-repeat center center / cover
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
</style>
