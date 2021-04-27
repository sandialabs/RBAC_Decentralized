<template>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login Template</title>
  <link href="https://fonts.googleapis.com/css?family=Karla:400,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.materialdesignicons.com/4.8.95/css/materialdesignicons.min.css">
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
  <link rel="stylesheet" href="./login_css/login.css">
</head>
<body>
  <main>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-6 login-section-wrapper">
          <div class="brand-wrapper">
            <img src="./login_images/logo.png" alt="logo" class="logo">
          </div>
          <div class="login-wrapper my-auto">
            <h1 class="login-title"> RBAC Blockchain </h1>
            <h1 class="login-title">Log in as:</h1>
            <div class="alert alert-danger" v-if="error">{{ error }}</div>
            <!-- <form class="form-signin" @submit.prevent="login">
              <div class="form-group">
                <label for="inputEmail">Email</label>
                <input v-model="email" type="email" name="email" id="inputEmail"
                class="form-control" placeholder="email@example.com" required autofocus>
              </div>
              <div class="form-group mb-4">
                <label for="inputPassword">Password</label>
                <input v-model="password" type="password" name="password" id="inputPassword"
                class="form-control" placeholder="enter your passsword" require>
              </div>
              <input name="login" id="login" class="btn
              btn-block login-btn" type="submit" value="Login">
            </form> -->
            <input name="login" id="login" class="btn
              btn-block login-btn" type="submit" v-on:click='login_user' value="User">
            <input name="login" id="login" class="btn
              btn-block login-btn" type="submit" v-on:click='login_admin' value="Admin">
            <input name="login" id="login" class="btn
              btn-block login-btn" type="submit" v-on:click='login_utilities_admin'
              value="Utilities Admin">
            <input name="login" id="login" class="btn
              btn-block login-btn" type="submit" v-on:click='login_sp_admin'
              value="Service Providers Admin">
            <input name="login" id="login" class="btn
              btn-block login-btn" type="submit" v-on:click='login_der_admin'
               value="DER Owners Admin">
          </div>
        </div>
        <div class="col-sm-6 px-0 d-none d-sm-block">
          <img src="./login_images/login.jpg" alt="login image" class="login-img">
        </div>
      </div>
    </div>
  </main>
  <script type="application/javascript" src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
  <script type="application/javascript" src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
  <script type="application/javascript" src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
</body>
</html>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: false,
    };
  },
  methods: {
    login_user() {
      const path = 'http://localhost:5000/auth';
      axios.post(path, { user: '', password: '', case: 'admin' })
        .then((request) => this.loginSuccessful_user(request))
        .catch(() => this.loginFailed());
    },
    login_admin() {
      const path = 'http://localhost:5000/auth';
      axios.post(path, { user: '', password: '', case: 'admin' })
        .then((request) => this.loginSuccessful_admin(request))
        .catch(() => this.loginFailed());
    },
    login_utilities_admin() {
      const path = 'http://localhost:5000/auth';
      axios.post(path, { user: '', password: '', case: 'utilities_admin' })
        .then((request) => this.loginSuccessful_utilities_admin(request))
        .catch(() => this.loginFailed());
    },
    login_sp_admin() {
      const path = 'http://localhost:5000/auth';
      axios.post(path, { user: '', password: '', case: 'sp_admin' })
        .then((request) => this.loginSuccessful_sp_admin(request))
        .catch(() => this.loginFailed());
    },
    login_der_admin() {
      const path = 'http://localhost:5000/auth';
      axios.post(path, { user: '', password: '', case: 'der_admin' })
        .then((request) => this.loginSuccessful_der_admin(request))
        .catch(() => this.loginFailed());
    },
    loginSuccessful_user(req) {
      if (!req.data.token) {
        this.loginFailed();
        return;
      }
      localStorage.token = req.data.token;
      this.error = false;

      this.$router.replace(this.$route.query.redirect || '/user_authorized');
    },
    loginSuccessful_admin(req) {
      if (!req.data.token) {
        this.loginFailed();
        return;
      }
      localStorage.token = req.data.token;
      this.error = false;

      this.$router.replace(this.$route.query.redirect || '/admin_authorized');
    },
    loginSuccessful_utilities_admin(req) {
      if (!req.data.token) {
        this.loginFailed();
        return;
      }

      localStorage.token = req.data.token;
      this.error = false;

      this.$router.replace(this.$route.query.redirect || '/admin_utilities');
    },
    loginSuccessful_sp_admin(req) {
      if (!req.data.token) {
        this.loginFailed();
        return;
      }

      localStorage.token = req.data.token;
      this.error = false;

      this.$router.replace(this.$route.query.redirect || '/admin_sp');
    },
    loginSuccessful_der_admin(req) {
      if (!req.data.token) {
        this.loginFailed();
        return;
      }

      localStorage.token = req.data.token;
      this.error = false;

      this.$router.replace(this.$route.query.redirect || '/admin_der');
    },
    checkCurrentLogin() {
      if (localStorage.token) {
        this.$router.replace(this.$route.query.redirect || '/admin_authorized');
      }
    },
    loginFailed() {
      this.error = 'Login Failed! Credentials are incorrect!';
      delete localStorage.token;
    },
  },
  created() {
    this.checkCurrentLogin();
  },
  updated() {
    this.checkCurrentLogin();
  },
};
</script>

<style lang="scss" scoped>
@import './login_css/login.css';
</style>
