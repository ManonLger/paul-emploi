<template>
  <div class="container">
    <Navbar :title="title"></Navbar>
    <router-link to="/swipe" class="btn btn-success">Start & swipe the best offers!</router-link>
    <br>
    <router-link to="/profile/my_offers" class="btn btn-info my-offers">My Offers</router-link>
    <br>
    <br>
    <router-link to="/profile/my_formations" class="btn btn-info my-offers">My Formations</router-link>
  </div>
</template>

<script>
  import Navbar from '../components/Navbar.vue'

  export default {
    name: 'Home',
    components: {
      Navbar
    },
    data () {
      return {
        title: 'Home'
      }
    }
  }
</script>

<style scoped>
.my-offers {
  position: relative;
  top: 30px;
}
</style>
