import Vue from 'vue';
import Router from 'vue-router';
import Admin from '../components/Admin.vue';
// import Login from '../components/Login.vue';
import LoginMany from '../components/LoginMany.vue';
import Utility1 from '../components/Utility1.vue';
import Utility2 from '../components/Utility2.vue';
import Utility3 from '../components/Utility3.vue';
import Utility4 from '../components/Utility4.vue';
import Utility5 from '../components/Utility5.vue';
import ServiceProvider1 from '../components/ServiceProvider1.vue';
import ServiceProvider2 from '../components/ServiceProvider2.vue';
import ServiceProvider3 from '../components/ServiceProvider3.vue';
import ServiceProvider4 from '../components/ServiceProvider4.vue';
import ServiceProvider5 from '../components/ServiceProvider5.vue';
import ServiceProvider6 from '../components/ServiceProvider6.vue';
import DerOwners from '../components/DerOwners.vue';
import SecurityAdmins from '../components/SecurityAdmins.vue';
import SecurityAuditors from '../components/SecurityAuditors.vue';
import UtilitiesAdmin from '../components/UtilitiesAdmin.vue';
import SpAdmin from '../components/SpAdmin.vue';
import DerAdmin from '../components/DerAdmin.vue';
import Query from '../components/Query.vue';
import UserLogin from '../components/UserLogin.vue';
import Books from '../components/test/Books.vue';
import UserQuery from '../components/UserQuery.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'LoginMany',
      component: LoginMany,
    },
    {
      path: '/admin_authorized',
      name: 'Admin',
      component: Admin,
      meta: {
        title: 'Admin RBAC Dashboard',
      },
    },
    {
      path: '/user_authorized',
      name: 'UserLogin',
      component: UserLogin,
    },
    {
      path: '/admin_utilities',
      name: 'UtilitiesAdmin',
      component: UtilitiesAdmin,
    },
    {
      path: '/admin_sp',
      name: 'SpAdmin',
      component: SpAdmin,
    },
    {
      path: '/admin_der',
      name: 'DerAdmin',
      component: DerAdmin,
    },
    {
      path: '/utility1',
      name: 'Utility1',
      component: Utility1,
    },
    {
      path: '/utility2',
      name: 'Utility2',
      component: Utility2,
    },
    {
      path: '/utility3',
      name: 'Utility3',
      component: Utility3,
    },
    {
      path: '/utility4',
      name: 'Utility4',
      component: Utility4,
    },
    {
      path: '/utility5',
      name: 'Utility5',
      component: Utility5,
    },
    {
      path: '/sp1',
      name: 'ServiceProvider1',
      component: ServiceProvider1,
    },
    {
      path: '/sp2',
      name: 'ServiceProvider2',
      component: ServiceProvider2,
    },
    {
      path: '/sp3',
      name: 'ServiceProvider3',
      component: ServiceProvider3,
    },
    {
      path: '/sp4',
      name: 'ServiceProvider4',
      component: ServiceProvider4,
    },
    {
      path: '/sp5',
      name: 'ServiceProvider5',
      component: ServiceProvider5,
    },
    {
      path: '/sp6',
      name: 'ServiceProvider6',
      component: ServiceProvider6,
    },
    {
      path: '/derowners',
      name: 'DerOwners',
      component: DerOwners,
    },
    {
      path: '/secadmins',
      name: 'SecurityAdmins',
      component: SecurityAdmins,
    },
    {
      path: '/secauditors',
      name: 'SecurityAuditors',
      component: SecurityAuditors,
    },
    {
      path: '/books',
      name: 'Books',
      component: Books,
    },
    {
      path: '/query',
      name: 'Query',
      component: Query,
    },
    {
      path: '/userquery',
      name: 'UserQuery',
      component: UserQuery,
    },
  ],
});
