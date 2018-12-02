<template>
  <div class="container">
    <Navbar :title="title"></Navbar>
    <div class="panel panel-body">
      <div class="row">
        <div class="col-md-10 col-md-offset-1">
          <form>
            <br>
            <div class="well">
              <label class="pull-left">Location:</label>
                <input type='text' class="form-control" placeholder="Paris" v-model="location">
                <!-- TODO: Ajouter de la validation-->
              <label class="pull-left">Interests:</label>
                <select class="form-control" v-model="interests" multiple>
                  <option v-for="interest in availableInterests">{{ interest }}</option>
                </select>
              <label class="pull-left">Degrees:</label>
                <select class="form-control" v-model="degrees" multiple>
                  <option v-for="degree in availableDegrees">{{ degree }}</option>
                </select>
              <label class="pull-left">Skills:</label>
                <select class="form-control" v-model="skills" multiple>
                  <option v-for="skill in availableSkills">{{ skill }}</option>
                </select>
              <label class="pull-left">Languages :</label>
                <select class="form-control" v-model="languages" multiple>
                  <option v-for="language in availableLanguages">{{ language }}</option>
                </select>
              <label class="pull-left">Minimum salary (K euros):</label>
                <input class="form-control" type="number" v-model="minSalary">
              <label class="pull-left">Maximum salary (K euros):</label>
                <input class="form-control" type="number" v-model="maxSalary">
              <label class="pull-left">Contract type:</label>
                <select class="form-control" v-model="contract">
                  <option v-for="contract in availableContracts">{{ contract }}</option>
                </select>
                <br>
                <button name='save' class="btn btn-large btn-block form-control btn btn-success" v-on:click.prevent="saveProfile()">Save</button>
              <br>
              <div class="msg">
                {{ msg }}
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Navbar from '../components/Navbar.vue'

  export default {
    name: 'Profile',
    components: {
      Navbar
    },
    data () {
      return {
        title: 'Profile',
        msg: '',
        availableInterests: [],
        availableDegrees: [],
        availableSkills: [],
        availableLanguages: [],
        availableContracts: [],
        location: 'Paris',
        interests: [],
        degrees: [],
        skills: [],
        languages: [],
        minSalary: 0,
        maxSalary: 0,
        contract: ''
      }
    },
    methods: {
      getAvailable: function () {
        let url = 'api/fields/'
        this.$http.get(url).then(function (resp) {
          this.availableInterests = resp.body.interests_names
          this.availableDegrees = resp.body.degrees_names
          this.availableSkills = resp.body.skills_names
          this.availableLanguages = resp.body.languages_names
          this.availableContracts = resp.body.contract_types_names
        })
      },
      getProfile: function () {
        let url = 'api/profile/'
        this.$http.get(url).then(function (resp) {
          this.location = resp.body.desired_location
          this.interests = resp.body.interests
          this.degrees = resp.body.degrees
          this.skills = resp.body.skills
          this.languages = resp.body.languages
          this.minSalary = resp.body.desired_min_salary
          this.maxSalary = resp.body.desired_max_salary
          this.contract = resp.body.desired_contract
        })
      },
      saveProfile: function () {
        let url = 'api/profile/'
        let body = {
          desired_location: this.location,
          desired_contract: this.contract,
          interests: this.interests,
          degrees: this.degrees,
          skills: this.skills,
          languages: this.languages,
          desired_min_salary: this.min_salary,
          desired_max_salary: this.max_salary
        }
        this.$http.put(url, body).then(
          function () { alert('Changes saved!') },
          function (err) {
            if (err.status === 400) {
              this.msg = err.body.detail
            }
          }
        )
      }
    },
    created: function () {
      this.getAvailable()
      this.getProfile()
    }
  }
</script>

<style scoped>
.pull-left {
  margin-bottom : 0.5em;
  margin-top : 0.5em;
  color : #029f5b;
}
.msg {
  color: red;
}
</style>
