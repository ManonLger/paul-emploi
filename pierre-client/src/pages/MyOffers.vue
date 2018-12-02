<template>
  <div class="container">
    <Navbar :title="title"></Navbar>
    <div class="wrap">
      <div class="cards">
        <Card v-for="id in myIds"
            :card-id="id"
            :is-formation=false
            :key="id"
            class="cards-item"></Card>
      </div>
    </div>
  </div>
</template>

<script>
  import Card from '../components/Card.vue'
  import Navbar from '../components/Navbar.vue'

  export default {
    name: 'MyOffers',
    components: {
      Card,
      Navbar
    },
    data () {
      return {
        title: 'My Offers',
        myIds: []
      }
    },
    methods: {
      getMyIds: function () {
        let url = 'api/profile/accepted_offers'
        this.$http.get(url).then(function (resp) {
          this.myIds = resp.body.map(offer => offer.id.toString())
        })
      }
    },
    created: function () {
      this.getMyIds()
    }
  }
</script>

<style scoped>
.cards-item {
  visibility: visible;
  position: relative;
  margin: 15px;
}
</style>
