<template>
  <div>
    <div v-if="!isFormation">
      <div v-if="!isExpanded">
        <Offer :offer-id="cardId"></Offer>
        <button v-on:click.prevent="toggle()" class="button btn-details"></button>
      </div>
      <div v-else>
        <OfferExpand :offer-id="cardId"></OfferExpand>
        <button v-on:click.prevent="toggle()" class="button btn-back"></button>
      </div>
    </div>
    <div v-else>
      <Formation :formation-id="cardId"></Formation>
    </div>
  </div>
</template>

<script>
  import Offer from './Offer.vue'
  import OfferExpanded from './OfferExpanded.vue'
  import Formation from './Formation.vue'

  export default {
    name: 'Card',
    components: {
      Offer,
      OfferExpanded,
      Formation
    },
    props: {
      cardId: {
        type: String,
        default: '1'
      },
      isFormation: {
        type: Boolean,
        default: false
      }
    },
    data () {
      return {
        isExpanded: false
      }
    },
    methods: {
      toggle: function () {
        this.isExpanded = !this.isExpanded
      }
    }
  }
</script>

<style scoped>
.button {
  width: 35px;
  height: 35px;
  margin: 0 auto;
  background-color:rgb(246, 255, 249);
}
.btn-details {
  background-image: url(../assets/question.png);
}
.btn-back {
  background-image: url(../assets/back.png);
}
</style>
