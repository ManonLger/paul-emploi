<template>
  <div>
    <h1>Detailed Offer</h1>
    <p>Company Description: {{ companyDescription }}</p>
    <p>Company Website: {{ website }}</p>
    <p>Skill: {{ skill }}</p>
    <p>Offer Description: {{ offerDescription }}</p>
    <p>Weekly Work Time: {{ weeklyWorkTime }}</p>
    <p>Experience Name: {{ experienceName }}</p>
  </div>
</template>

<script>
  export default {
    name: 'OfferExpanded',
    props: {
      offerId: {
        type: String,
        default: '1'
      }
    },
    data () {
      return {
        companyDescription: '',
        website: '',
        skill: '',
        offerDescription: '',
        weeklyWorkTime: 0,
        experienceName: 0
      }
    },
    methods: {
      getExpandedOffer: function (id) {
        let url = 'api/offers/' + id + '/expand/'
        this.$http.get(url).then(function (resp) {
          this.companyDescription = resp.body.company.description
          this.website = resp.body.company.url
          this.skill = resp.body.skill
          this.offerDescription = resp.body.description
          this.weeklyWorkTime = resp.body.weekly_work_time
          this.experienceName = resp.body.experience_name
        })
      }
    },
    created: function () {
      this.getExpandedOffer(this.offerId)
    }
  }
</script>
