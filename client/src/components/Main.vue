<template>
  <div>
    <!-- <img src="./assets/logo.png"> -->
    <el-container>
      <el-header>
        <el-row>
          <el-col :span="16">NLP标注平台</el-col>
          <el-col :span="4">Welcome,{{ name}}</el-col>
          <el-col :span="4">
            <el-button type="danger" @click="logout">Logout</el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-container>
        <el-aside width="10%">
          <el-menu :default-active="$route.path" router>
            <el-menu-item index="/Reading">
              <i class="el-icon-document"></i>
              <span slot="title">阅读理解</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Cookies from 'js-cookie';

export default {
  name: 'Main',
  data() {
    return {
      name: Cookies.get('name'),
    };
  },
  methods: {
    logout() {
      const ans = window.confirm('确定注销？');
      if (ans) {
        Cookies.remove('name');
        Cookies.remove('email');
        setTimeout(
          () => {
            this.$router.push('/Login');
          },
          500,
        );
      }
    },
  },
};
</script>
<style>
/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
.el-aside {
  background-color: #d3dce6;
  color: rgb(26, 25, 25);
  text-align: center;
  line-height: 200px;
}
.el-header {
  background-color: #545c64;
  color: rgb(250, 243, 243);
  text-align: left;
  line-height: 60px;
}
</style>

