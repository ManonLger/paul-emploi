<template>
  <div>
    <h1>Formation</h1>
    <p>Name: {{ name }}</p>
    <p>Acquired skills:</p>
      <ul>
        <li v-for="skill in acquiredSkills">{{ skill }}</li>
      </ul>
    <p>Acquired degree: {{ acquiredDegree }}</p>
    <p>Duration: {{ duration }}</p>
    <p>Location: {{ location }}</p>
    <p>Language: {{ language }}</p>
  </div>
</template>

<script>
  export default {
    name: 'Formation',
    props: {
      formationId: {
        type: String,
        default: '1'
      }
    },
    data () {
      return {
        name: '',
        acquiredSkills: [],
        acquiredDegree: '',
        duration: '',
        location: '',
        language: ''
      }
    },
    methods: {
      getFormation: function (id) {
        let url = 'api/formations/' + id + '/'
        this.$http.get(url).then(function (resp) {
          this.name = resp.body.name
          this.acquiredSkills = resp.body.acquired_skills.name
          this.acquiredDegree = resp.body.acquired_degree.name
          this.duration = resp.body.duration
          this.location = resp.body.location
          this.language = resp.body.language
        })
      }
    },
    created: function () {
      this.getFormation(this.formationId)
    }
  }
</script>

<style scoped>

</style>
