<template>
<div>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="">
  <link rel="icon" href="favicon.ico">
  <title>Sandia National Laboratories - Blockchain RBAC</title>
  <!-- Bootstrap core CSS -->

  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css">
  <!-- Custom styles for this template -->

  <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
  <script type="application/javascript" src="js/ie-emulation-modes-warning.js"></script>
  <link href="/Users/geo_fragkos/Downloads/lattes-template/css/style.css" rel="stylesheet">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
  <!-- Custom styles for this template -->
  <link href="/Users/geo_fragkos/Downloads/lattes-template/css/owl.carousel.css" rel="stylesheet">
  <link href="/Users/geo_fragkos/Downloads/lattes-template/css/owl.theme.default.min.css"
    rel="stylesheet">

    rel="stylesheet">
  </head>
  <body id="page-top">
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
          <li class="hidden">
            <a href="#page-top"></a>
          </li>
          <li>
            <a class="page-scroll" href="#utilities">Utilities</a>
          </li>
          <li>
            <a class="page-scroll" v-on:click='query'>Query</a>
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
  <!-- Header -->
  <header>
    <div class="container" >
      <div class="slider-container">
        <div class="intro-text">
          <div class="intro-lead-in">Welcome RBAC Utilities Administrator!</div>
          <div class="intro-heading">This is your Ethereum Blockchain Dashboard</div>
          <a href="#profile_info" class="page-scroll btn-xl">Your Profile</a>
        </div>
      </div>
    </div>
  </header>
  <section id="profile_info" class="light-bg">
    <div class="container">
      <div class="row">
        <div class="col-lg-12 text-center">
          <div class="section-title">
            <h2>Profile Information</h2>
            <p>Below please find the information regarding your RBAC Admin profile </p>
          </div>
        </div>
      </div>
      <div class="row justify-content-center align-items-center">
        <!-- about module -->
        <div class="col-md-4 text-center">
          <div class="mz-module-about">
            <i class="fab fa-ethereum ot-circle" style="font-size:55px"></i>
            <h3>Ethereum Address</h3>
            <p> {{ admin_address }} </p>
          </div>
        </div>
        <!-- end about module -->
        <!-- about module -->
        <!-- <div class="col-md-3 text-center">
          <div class="mz-module-about">
            <i class="fab fa-keycdn ot-circle"  style="font-size:55px"></i>
            <h3>Private Key</h3>
            <p></p>
          </div>
        </div> -->
        <!-- end about module -->
        <!-- about module -->
        <div class="col-md-4 text-center">
          <div class="mz-module-about">
            <i class="fas fa-wallet ot-circle"  style="font-size:53px"></i>
            <h3>Ethereum Balance</h3>
            <p>{{ admin_balance }} Ethers</p>
          </div>
        </div>
        <!-- end about module -->
        <!-- about module -->
        <div class="col-md-4 text-center">
          <div class="mz-module-about">
            <i class="fas fa-file-signature ot-circle"  style="font-size:53px"></i>
            <h3>RBAC Smart Contract</h3>
            <p> {{ sc_address }}</p>
          </div>
        </div>
        <!-- end about module -->
      </div>
    </div>
    <!-- /.container -->
  </section>
  <section >
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <div class="skills-text">
            <h2>Insight Metrics</h2>
            <p>Ethereum Blockchain Info</p>
          </div>
        </div>
        <div class="col-md-6">
          <!-- skill bar item -->
          <div class="skillbar-item">
            <div class="skillbar-score">
              <span class="score">7</span><span class="percent">%</span>
            </div>
            <div class="skillbar" data-percent="7%">
              <h3>RBAC SC Percentage Cost</h3>
              <div class="skillbar-bar">
                <div class="skillbar-percent" style="width: 7%;">
                </div>
              </div>
            </div>
          </div>
          <!-- skill bar item -->
          <div class="skillbar-item">
            <div class="skillbar-score">
              <span class="score">100</span><span class="percent">%</span>
            </div>
            <div class="skillbar" data-percent="100%">
              <h3>Used Ethereum Accounts</h3>
              <div class="skillbar-bar">
                <div class="skillbar-percent" style="width: 100%;">
                </div>
              </div>
            </div>
          </div>
          <!-- skill bar item -->
        </div>
      </div>
    </div>
  </section>
  <section class="overlay-dark bg-img1 dark-bg short-section">
    <div class="container text-center">
      <div class="row">
        <div class="col-md-3 mb-sm-30">
          <div class="counter-item">
            <h2>{{ rbac_blocks }}</h2>
            <h6>RBAC Blocks</h6>
          </div>
        </div>
        <div class="col-md-3 mb-sm-30">
          <div class="counter-item">
            <h2>{{ rbac_blocks }}</h2>
            <h6>RBAC Transactions</h6>
          </div>
        </div>
        <div class="col-md-3 mb-sm-30">
          <div class="counter-item">
            <h2>1</h2>
            <h6>RBAC Smart Contracts</h6>
          </div>
        </div>
        <div class="col-md-3 mb-sm-30">
          <div class="counter-item">
            <h2>{{ rbac_entities }}</h2>
            <h6>RBAC Entities</h6>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section id="utilities" class="light-bg">
    <div class="container">
    <div class="row">
      <div class="col-lg-12 text-center">
        <div class="section-title">
          <h2>Utilities</h2>
          <p>Choose your Utility!</p>
        </div>
      </div>
    </div>
    <div class="row">
      <!-- start portfolio item -->
      <div class="col-md-4">
        <div class="ot-portfolio-item">
          <figure class="effect-bubba">
            <img src="./images/demo/utility-1.jpg" alt="img02" class="img-responsive" />
            <figcaption>
              <h2>Utility 1</h2>
              <p>Albuquerque, NM</p>
              <a v-on:click='utility1' class="page-scroll">View Information</a>
            </figcaption>
          </figure>
        </div>
      </div>
      <!-- end portfolio item -->
      <!-- start portfolio item -->
      <div class="col-md-4">
        <div class="ot-portfolio-item">
          <figure class="effect-bubba">
            <img src="./images/demo/utility-2.jpg" alt="img02" class="img-responsive" />
            <figcaption>
              <h2>Utility 2</h2>
              <p>Albuquerque, NM</p>
              <a v-on:click='utility2' class="page-scroll">View Information</a>
            </figcaption>
          </figure>
        </div>
      </div>
      <!-- end portfolio item -->
      <!-- start portfolio item -->
      <div class="col-md-4">
        <div class="ot-portfolio-item">
          <figure class="effect-bubba">
            <img src="./images/demo/utility-3.jpg" alt="img02" class="img-responsive" />
            <figcaption>
              <h2>Utility 3</h2>
              <p>Albuquerque, NM</p>
              <a v-on:click='utility3' class="page-scroll">View Information</a>
            </figcaption>
          </figure>
        </div>
      </div>
      <!-- end portfolio item -->
    </div>
    <div class="row">
      <!-- start portfolio item -->
      <div class="col-md-4">
        <div class="ot-portfolio-item">
          <figure class="effect-bubba">
            <img src="./images/demo/utility-4.jpg" alt="img02" class="img-responsive" />
            <figcaption>
              <h2>Utility 4</h2>
              <p>Albuquerque, NM</p>
              <a v-on:click='utility4' class="page-scroll">View Information</a>
            </figcaption>
          </figure>
        </div>
      </div>
      <!-- end portfolio item -->
      <!-- start portfolio item -->
      <div class="col-md-4">
        <div class="ot-portfolio-item">
          <figure class="effect-bubba">
            <img src="./images/demo/utility-5.jpg" alt="img02" class="img-responsive" />
            <figcaption>
              <h2>Utility 5</h2>
              <p>Albuquerque, NM</p>
              <a v-on:click='utility5' class="page-scroll">View Information</a>
            </figcaption>
          </figure>
        </div>
      </div>
      <!-- end portfolio item -->

    </div>
    </div><!-- end container -->
  </section>
  <section id="contact">
    <div class="container">
      <div class="row">
        <div class="col-lg-12 text-center">
          <div class="section-title">
            <h2>Contact Us</h2>
            <p>Please provide your feedback regarding our RBAC Blockchain Demo!</p>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-3">
          <h3>Sandia National Laboratories</h3>
          <p>1515 Eubank SE, Albuquerque, NM 87123</p>
          <p><i class="fa fa-phone"></i> +1 505 459 9573</p>
          <p><i class="fa fa-envelope"></i> gfragkos@unm.edu</p>
        </div>
        <div class="col-md-6">
<form action="https://getform.io/f/9b9c4e35-0f22-48ff-b718-edd0061b3dec" method="POST" id="contactForm" novalidate="">
  <div class="row">
    <div class="col-md-6">
      <div class="form-group">
        <input type="text" class="form-control" placeholder="Your Name *" id="name"
        required="" data-validation-required-message="Please enter your name." name="name">
        <p class="help-block text-danger"></p>
      </div>
    </div>
    <div class="col-md-6">
      <div class="form-group">
        <input type="email" class="form-control" placeholder="Your Email *"
        id="email" required="" data-validation-required-message="Please enter
        your email address." name="email">
        <p class="help-block text-danger"></p>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <div class="form-group">
        <input type="text" class="form-control" placeholder="Your Message *"
        id="message" required="" data-validation-required-message="Please enter
        a message." name="message">
        <p class="help-block text-danger"></p>
      </div>
    </div>
    <div class="clearfix"></div>
  </div>
  <div class="row">
    <div class="col-lg-12 text-center">
      <div id="success"></div>
      <button type="submit" class="btn">Send Message</button>
    </div>
  </div>
</form>

        </div>
      </div>
    </div>
  </section>
  <p id="back-top">
    <a href="#top"><i class="fa fa-angle-up"></i></a>
  </p>
  <footer>
    <div class="container text-center">
      <p>Designed by <a href="https://www.sandia.gov">Sandia National Laboratories</a></p>
    </div>
  </footer>

  <!-- Modal for portfolio item 1 -->
  <div class="modal fade" id="Modal-1" tabindex="-1" role="dialog" aria-labelledby="Modal-label-1">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"
          aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="Modal-label-1">Dean & Letter</h4>
        </div>
        <div class="modal-body">
          <img src="./images/demo/portfolio-1.jpg"
                    alt="img01" class="img-responsive"/>
          <div class="modal-works"><span>Branding</span><span>Web Design</span></div>
          <p>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for portfolio item 2 -->
  <div class="modal fade" id="Modal-2" tabindex="-1" role="dialog" aria-labelledby="Modal-label-2">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"
          aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="Modal-label-2">Startup Framework</h4>
        </div>
        <div class="modal-body">
          <img src="images/demo/portfolio-2.jpg" alt="img01" class="img-responsive" />
          <div class="modal-works"><span>Branding</span><span>Web Design</span></div>
          <p>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for portfolio item 3 -->
  <div class="modal fade" id="Modal-3" tabindex="-1" role="dialog" aria-labelledby="Modal-label-3">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"
          aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="Modal-label-3">Lamp & Velvet</h4>
        </div>
        <div class="modal-body">
          <img src="images/demo/portfolio-3.jpg" alt="img01" class="img-responsive" />
          <div class="modal-works"><span>Branding</span><span>Web Design</span></div>
          <p>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for portfolio item 4 -->
  <div class="modal fade" id="Modal-4" tabindex="-1" role="dialog" aria-labelledby="Modal-label-4">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"
          aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="Modal-label-4">Smart Name</h4>
        </div>
        <div class="modal-body">
          <img src="./images/demo/portfolio-4.jpg" alt="img01" class="img-responsive" />
          <div class="modal-works"><span>Branding</span><span>Web Design</span></div>
          <p>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for portfolio item 5 -->
  <div class="modal fade" id="Modal-5" tabindex="-1" role="dialog" aria-labelledby="Modal-label-5">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal"
          aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title" id="Modal-label-5">Fast People</h4>
        </div>
        <div class="modal-body">
          <img src="./images/demo/portfolio-5.jpg" alt="img01" class="img-responsive" />
          <div class="modal-works"><span>Branding</span><span>Web Design</span></div>
          <p>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Bootstrap core JavaScript
    ================================================== -->
  <!-- Placed at the end of the document so the pages load faster -->
  <script type="application/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script type="application/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.3/jquery.easing.min.js"></script>
  <script type="application/javascript" src="./js/bootstrap.min.js"></script>
  <script type="application/javascript" src="./js/owl.carousel.min.js"></script>
  <script type="application/javascript" src="./js/cbpAnimatedHeader.js"></script>
  <script type="application/javascript" src="./js/theme-scripts.js"></script>
  <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
  <script type="application/javascript" src="./js/ie10-viewport-bug-workaround.js"></script>
  </body>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Admin',
  data() {
    return {
      msg: '',
      admin_address: '',
      admin_balance: '',
      sc_address: '',
      rbac_blocks: '',
      rbac_entities: '',
    };
  },
  methods: {
    getAdminAddress() {
      const path = 'http://localhost:5000/get_admin_address';
      axios.get(path)
        .then((res) => {
          this.admin_address = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAdminBalance() {
      const path = 'http://localhost:5000/get_admin_balance';
      axios.get(path)
        .then((res) => {
          this.admin_balance = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getScAddress() {
      const path = 'http://localhost:5000/get_sc_address';
      axios.get(path)
        .then((res) => {
          this.sc_address = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getBlocks() {
      const path = 'http://localhost:5000/get_blocks';
      axios.get(path)
        .then((res) => {
          this.rbac_blocks = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getAccounts() {
      const path = 'http://localhost:5000/get_entities';
      axios.get(path)
        .then((res) => {
          this.rbac_entities = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    signout() {
      delete localStorage.token;
      this.$router.replace(this.$route.query.redirect || '/');
    },
    query() {
      this.$router.replace(this.$route.query.redirect || '/query');
    },
    utility1() {
      this.$router.replace(this.$route.query.redirect || '/utility1');
    },
    utility2() {
      this.$router.replace(this.$route.query.redirect || '/utility2');
    },
    utility3() {
      this.$router.replace(this.$route.query.redirect || '/utility3');
    },
    utility4() {
      this.$router.replace(this.$route.query.redirect || '/utility4');
    },
    utility5() {
      this.$router.replace(this.$route.query.redirect || '/utility5');
    },
  },
  updated() {
    if (!localStorage.token && this.$route.path !== '/') {
      this.$router.push('/?redirect='.concat(this.$route.path));
      this.$router.replace(this.$route.query.redirect || '/');
    }
  },
  created() {
    this.getAdminAddress();
    this.getAdminBalance();
    this.getScAddress();
    this.getBlocks();
    this.getAccounts();
  },
};
</script>

<style>
@import './css/style.css';
@import './css/bootstrap.css';
</style>
