<template>
  <div class="container">
    <div class="msg">
      {{ msg }}
    </div>
    <div class="row">
      <div class="col-md-6 col-md-offset-3">
        <div class="panel panel-login">
          <div class="panel-heading">
            <div class="row">
              <div class="col-xs-6">
                <a v-on:click='loginLinkClick()' ><router-link to="/login" class="active" id="login-form-link">Login</router-link></a>
              </div>
              <div class="col-xs-6">
                <a v-on:click='registerLinkClick()'><router-link to="/login" id="register-form-link">Register</router-link></a>
              </div>
            </div>
            <hr>
          </div>
          <div class="panel-body">
            <div class="row">
              <div class="col-lg-12">
                <form id="login-form" method="post" role="form" style="display: block;">
                  <div class="form-group">
                    <input type="email" tabindex="1" class="form-control" placeholder="Email Address" v-model='email'>
                  </div>
                  <div class="form-group">
                    <input type="password" tabindex="2" class="form-control" placeholder="Password" v-model='password'>
                  </div>
                  <div class="form-group">
                    <div class="row">
                      <div class="col-sm-6 col-sm-offset-3">
                        <input type="submit" name="login-submit" id="login-submit" tabindex="4" class="form-control btn btn-login" value="Log In" v-on:click.prevent='login()'>
                      </div>
                    </div>
                  </div>
                </form>
                <form id="register-form" method="post" role="form" style="display: none;">
                  <div class="form-group">
                    <input type="email" tabindex="1" class="form-control" placeholder="Email Address" v-model="email">
                  </div>
                  <div class="form-group">
                    <input type="password" tabindex="2" class="form-control" placeholder="Password" v-model="password">
                  </div>
                  <div class="form-group">
                    <input type="password" tabindex="2" class="form-control" placeholder="Confirm Password" v-model="confirmPassword">
                  </div>
                  <div class="form-group">
                    <div class="row">
                      <div class="col-sm-6 col-sm-offset-3">
                        <input type="submit" name="register-submit" id="register-submit" tabindex="4" class="form-control btn btn-register" value="Register Now" v-on:click.prevent='register()'>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      title: 'Login',
      email: '',
      password: '',
      confirmPassword: '',
      msg: '',
      redirected: false
    }
  },
  methods: {
    setMsg: function () {
      if (this.$route.params.errors === 401 || this.$route.params.errors === 403) {
        this.redirected = true
        this.msg = 'You have to login to see this page.'
      }
    },
    login: function () {
      let url = 'auth/get-token/'
      let body = {
        username: this.$data.email,
        password: this.$data.password
      }
      this.$http.post(url, body).then(
        function (resp) {
          this.$cookies.set('token', resp.body.token)
          if (this.redirected) {
            this.$router.go(-1)
          } else {
            this.$router.push({ name: 'Home' })
          }
        },
        function (err) {
          if (err.status === 400) {
            this.msg = err.body.detail
          }
        }
      )
    },
    register: function () {
      if (this.$data.password === this.$data.confirmPassword) {
        let url = 'api/users/'
        let body = {
          email: this.$data.email,
          password: this.$data.password
        }
        this.$http.post(url, body).then(
          function () {
            this.login()
          },
          function (err) {
            if (err.status === 400) {
              this.msg = err.body.detail
            }
          }
        )
      } else {
        this.msg = 'Passwords do not match.'
      }
    },
    loginLinkClick: function (e) {
      $('#login-form').delay(100).fadeIn(100)
      $('#register-form').fadeOut(100)
      $('#register-form-link').removeClass('active')
      $('#login-form-link').addClass('active')
      e.preventDefault()
    },
    registerLinkClick: function (e) {
      $('#register-form').delay(100).fadeIn(100)
      $('#login-form').fadeOut(100)
      $('#login-form-link').removeClass('active')
      $('#register-form-link').addClass('active')
      e.preventDefault()
    }
  },
  created: function () {
    this.setMsg()
  }
}
</script>

<style scoped>

</style>
