/* eslint-disable no-console */
import Vue from 'vue';
import Router from 'vue-router';
import Reading from '@/components/Reading';
import Login from '@/components/Login';
import Main from '@/components/Main';
import Register from '@/components/Register';
import Cookies from 'js-cookie';
import Check from '@/components/Check';

Vue.use(Router);
export const constRouterMap = [{
  path: '/Login',
  component: Login,
  name: 'Login',
  hidden: true,
},
{
  path: '/Register',
  component: Register,
  hidden: true,
},
{
  path: '/',
  component: Main,
  children: [{
    path: '/Reading',
    name: 'Reading',
    component: Reading,
  }],
  // {
  //   path: '/Check',
  //   name: 'Check',
  //   component: Check,
  // }
  beforeEnter: (to, from, next) => {
    // ...
    const name = Cookies.get('name');
    console.log(name);
    if (!name) {
      // eslint-disable-next-line no-alert
      const answer = window.confirm('你还没有登陆');
      if (answer) {
        next('/Login');
      } else {
        next(false);
      }
    } else {
      next(true);
    }
  },
},
];

export default new Router({
  linkActiveClass: 'open active',
  routes: constRouterMap,
  mode: 'hash',
});

export const asyncRouterMap = [{
  path: '/',
  redirect: '/home',
  name: 'home',
  component: Main,
  hidden: false,
  children: [{
    path: '/Reading',
    name: 'Reading',
    component: Reading,
  }],
},
];
