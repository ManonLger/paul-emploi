import Vue from 'vue'

import VueCookies from 'vue-cookies'
import VueResource from 'vue-resource'
import VueRouter from 'vue-router'

import Home from '@/pages/Home'
import Login from '@/pages/Login'
import MyOffers from '@/pages/MyOffers'
import NotFound from '@/pages/NotFound'
import Profile from '@/pages/Profile'
import Swipe from '@/pages/Swipe'
import MyFormations from '@/pages/MyFormations'

Vue.use(VueRouter)
Vue.use(VueCookies)
Vue.use(VueResource)
Vue.http.options.root = 'https://germoon.nebulae.co/' // Si Django tourne en local : */ 'http://localhost:8000/'
Vue.http.interceptors.push(function (request, next) {
  if (Vue.cookies.get('token') !== null) {
    request.headers.set('Authorization', 'Token ' + Vue.cookies.get('token'))
  }
  next(function (resp) {
    if (resp.status === 401 || resp.status === 403) {
      this.$router.push({ name: 'Login', params: { errors: resp.status } })
    }
  })
})

export default new VueRouter({
  routes: [
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/swipe',
      name: 'Swipe',
      component: Swipe
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    },
    {
      path: '/profile/my_offers',
      name: 'MyOffers',
      component: MyOffers
    },
    {
      path: '/profile/my_formations',
      name: 'MyFormations',
      component: MyFormations
    }
  ]
})
