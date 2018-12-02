<template>
  <div>
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target='#myNavbar'>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Paul Emploi</a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
          <div class="navbar-text"><strong>{{ title }}</strong></div>
          <ul class="nav navbar-nav navbar-right" :class="{'navbar-right--hidden': !loggedIn}">
            <li><router-link to="/profile/my_offers">My Offers</router-link></li>
            <li><router-link to="/profile/my_formations">My Formations</router-link></li>
            <li><router-link to="/profile">Profile</router-link></li>
            <li class="navbar-btn btn btn-danger" v-on:click.prevent="logout()">Logout</li>
          </ul>
          <ul class="nav navbar-nav navbar-right" :class="{'navbar-right--hidden': loggedIn}">
            <li class="navbar-btn btn btn-primary" v-on:click.prevent="login()">Login</li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
  export default {
    name: 'Navbar',
    props: {
      title: {
        type: String,
        default: ''
      }
    },
    data () {
      return {
        loggedIn: this.$cookies.get('token') !== null
      }
    },
    methods: {
      login: function () {
        this.$router.push({ name: 'Login' })
      },
      logout: function () {
        let url = 'auth/logout/'
        this.$http.get(url).then(function () {
          this.$cookies.remove('token')
          this.$router.push({ name: 'Login' })
        })
      }
    }
  }
</script>

<style scoped>
.navbar-right--hidden {
  display: none;
}
</style>
