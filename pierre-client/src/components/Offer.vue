<template>
  <div>
    <h1>Offer</h1>
    <p>Title: {{ title }}</p>
    <p>Company: {{ company }}</p>
    <p>Language: {{ language }}</p>
    <p>Location: {{ location }}</p>
    <p>Degree: {{ degree }}</p>
    <p>Minimum Salary: {{ minSalary }}</p>
    <p>Maximum Salary: {{ maxSalary }}</p>
    <p>Contract Type: {{ contractType }}</p>
  </div>
</template>

<script>
  export default {
    name: 'Offer',
    props: {
      offerId: {
        type: String,
        default: '1'
      }
    },
    data () {
      return {
        title: '',
        company: '',
        language: '',
        location: '',
        degree: '',
        minSalary: 0,
        maxSalary: 0,
        contractType: ''
      }
    },
    methods: {
      getOffer: function (id) {
        let url = 'api/offers/' + id + '/'
        this.$http.get(url).then(function (resp) {
          this.title = resp.body.title
          this.company = resp.body.company
          this.language = resp.body.language
          this.location = resp.body.location
          this.degree = resp.body.degree
          this.contractType = resp.body.contract_type
        })
      }
    },
    created: function () {
      this.getOffer(this.offerId)
    }
  }
</script>
