/* eslint-disable no-alert */
<template>
  <div style="margin: 0 auto">
    <p id="menu">NLP标注平台</p>
    <el-row>
      <el-col :span="12" :offset="6">
        <el-form :model="form" :rules="rules" label-width="100px" ref="form">
          <el-form-item label="name" prop="name">
            <el-input v-model="form.name" placeholder="请输入姓名"></el-input>
          </el-form-item>
          <el-form-item label="email" prop="email">
            <el-input v-model="form.email" placeholder="请输入账号名称"></el-input>
          </el-form-item>
          <el-form-item label="password" prop="password">
            <el-input v-model="form.password" placeholder="请输入密码" type="password"></el-input>
          </el-form-item>
          <el-form-item label="confirm" prop="password_confirm">
            <el-input v-model="form.password_confirm" placeholder="请重复确认密码" type="password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submit_form">submit</el-button>
            <router-link :to="{name:'Login'}">Login</router-link>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',

  data() {
    const checkName = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入姓名(英文)'));
      } else {
        const uPattern = /^[a-zA-Z0-9_-]{4,16}$/;
        if (!uPattern.test(value)) {
          callback(new Error('用户名格式不正确'));
        }
        callback();
      }
    };
    const checkEmail = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入email'));
      } else {
        const pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        if (!pattern.test(value)) {
          callback(new Error('email格式不正确'));
        }
        const data = this.form.email;
        let res;
        const path = 'http://172.16.41.49:5000/checkEmail';
        axios
          .post(path, {
            email: data,
          })
          .then((response) => {
            console.log(response);
            console.log(response.data);
            console.log(response.data === 'success');
            // if (response["data"] === "success") {
            //   callback(new Error("email已经被使用"));
            // }
            res = response.data === 'success';
            if (res) {
              alert('email已经被使用');
            }
          })
          .catch((error) => {
            console.log(error);
          });
        callback();
      }
    };
    const checkPassword = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else if (value.length <= 6) {
        callback(new Error('密码太短'));
      } else {
        callback();
      }
    };
    const checkPassword_2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请确认密码'));
      } else {
        if (value !== this.form.password) {
          callback(new Error('密码不一致'));
        }
        callback();
      }
    };
    return {
      form: {
        name: '',
        email: '',
        password: '',
        password_confirm: '',
      },
      rules: {
        name: [{ validator: checkName, trigger: 'blur' }],
        email: [{ validator: checkEmail, trigger: 'blur' }],
        password: [{ validator: checkPassword, trigger: 'blur' }],
        password_confirm: [{ validator: checkPassword_2, trigger: 'blur' }],
      },
      base_url: 'http://172.16.41.49:5000/',
    };
  },
  methods: {
    submit_form() {
      const path = `${this.base_url}register`;
      let success = false;
      axios
        .post(path, {
          form: this.form,
        })
        .then((response) => {
          console.log(response);
          if (response.data === 'success') {
            alert('success');
            success = true;
          } else {
            alter('error');
            success = false;
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
