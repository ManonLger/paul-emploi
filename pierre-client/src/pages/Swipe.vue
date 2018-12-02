<template>
  <div class="container">
    <Navbar :title="title"></Navbar>
    <div class="wrap">
      <div class="cards">
        <Card v-for="cardId in cardsIds"
            :card-id="cardId"
            :key="cardId.toString()+isFormation.toString()"
            :is-formation="isFormation"
            class="cards-item"
            :class="{
              'cards-item--active': cardsIds[0] === cardId,
            }" >
        </Card>
        <div>
          <p class='msg'>
            {{ msg }}
          </p>
        </div>
        <div class="cards-item">
          <p class="background-text">No more cards to swipe!<br/><br/>But you're welcome to come back tomorrow! :)</p>
        </div>
      </div>
      <div class="actions">
        <button class="button btn-dislike" v-on:click.prevent="action(like=false)"></button>
        <button class="button btn-like" v-on:click.prevent="action(like=true)"></button>
      </div>
    </div>
  </div>
</template>

<script>
  import Card from '../components/Card.vue'
  import Navbar from '../components/Navbar.vue'

  export default {
    name: 'Swipe',
    components: {
      Card,
      Navbar
    },
    data () {
      return {
        title: 'Swipe',
        cardsIds: [],
        isFormation: false,
        msg: ''
      }
    },
    methods: {
      getIds: function (url) {
        this.$http.get(url).then(
          function (resp) {
            this.cardsIds = this.cardsIds.concat(resp.body.map(card => card.toString()))
          },
          function (resp) {
            this.msg = resp.statusText
          }
        )
      },
      getOffersIds: function () {
        let url = 'api/profile/offers_to_show/'
        this.cardsIds = []
        this.getIds(url)
      },
      getFormationsIds: function () {
        let url = 'api/profile/formations_to_show/'
        this.getIds(url)
      },
      action: function (like) {
        let cardId = this.cardsIds[0]
        let urlStart = this.isFormation ? 'api/formations/' : 'api/offers/'
        let urlEnd = this.isFormation
          ? like
            ? '/keep/' : '/drop/'
          : like
            ? '/accept/' : '/refuse/'
        if (this.cardsIds.length === 1 && !this.isFormation) {
          this.isFormation = true
          this.getFormationsIds()
        }
        this.$http.post(urlStart + cardId + urlEnd)
        this.cardsIds.shift()
      }
    },
    created: function () {
      this.getOffersIds()
    }
  }
</script>

<style scoped>
.background-text {
  position: relative;
  top: 8em;
  z-index: -12;
  visibility: visible;
}
</style>
