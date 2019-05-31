<template>
  <div style="margin: 0 auto">
    <p id="menu">NLP标注平台</p>
    <el-row>
      <el-col :span="12" :offset="6">
        <el-form :model="loginForm" :rules="rules" label-width="100px">
          <el-form-item label="email" prop="email">
            <el-input v-model="loginForm.email" placeholder="请输入email"></el-input>
          </el-form-item>
          <el-form-item label="password" prop="password">
            <el-input v-model="loginForm.password" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="get_login">submit</el-button>
            <router-link :to="{path:'/Register'}">注册</router-link>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        name: '',
        email: '',
        password: '',
      },
      rules: {
        email: [{ required: true, message: '请输入email', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      },
      base_url: 'http://172.16.41.49:5000/',
    };
  },
  methods: {
    get_login() {
      const path = `${this.base_url}login`;
      let success;
      axios
        .post(path, {
          form: this.loginForm,
        })
        .then((response) => {
          console.log(response);
          const data = response.data;
          if (data !== 'wa') {
            Cookies.set('name', data);
            Cookies.set('email', this.loginForm.email);
            // setCookie("email", this.form.email, 3600 * 12);
            setTimeout(
              () => {
                this.$router.push('/Reading');
              },
              500,
            );
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.el-form-item {
  /* position: fixed; */
  text-align: center;
}
.el-form {
  margin-top: 30%;
}
#menu {
  font-size: x-large;
  margin-left: 50%;
  margin-bottom: 20px;
}
</style>
