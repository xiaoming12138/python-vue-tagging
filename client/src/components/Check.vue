<template>
  <div>
    <h2>段落内容</h2>
    <el-row>
      <el-col :span="24">
        <el-card class="box-card">
          <div>{{mongo_data['context']}}</div>
        </el-card>
      </el-col>
    </el-row>
    <h2>问题&答案</h2>
    <el-card v-for="(data,index) in mongo_data['question_answer']" :key="data">
      <el-row gutter="20">
        <el-col :span="15">
          <el-row>
            <el-col :span="1">
              <h4>{{index+1}}</h4>
            </el-col>
            <el-col :span="23">
              <el-input v-model="data['question']" placeholder="请输入问题"></el-input>
              <el-input
                v-model="data['answer']"
                placeholder="答案"
                :disabled="true"
                class="answer_input"
              ></el-input>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="2">
          <el-select v-model="data['is_impossible']" placeholder="请选择">
            <el-option value="false" label="正例"></el-option>
            <el-option value="true" label="负例"></el-option>
          </el-select>
        </el-col>
        <el-col :span="1"></el-col>
        <el-col :span="1"></el-col>
        <el-col :span="5"></el-col>
      </el-row>
    </el-card>
  </div>
</template>
<script>
import axios from 'axios';
import Cookie from 'js-cookie';

export default {
  name: 'Check',
  data() {
    return {
      user: { name: Cookie.get('name'), email: Cookie.get('email') },
      base_url: 'http://172.16.41.49:5000/',
      mongo_data: '',
    };
  },
  methods: {
    get_mongo_data() {
      const path = `${this.base_url}get_context_to_check`;
      console.log(path);
      axios
        .get(path)
        .then((res) => {
          this.mongo_data = res.data;
          console.log(this.mongo_data);
          console.log(res);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.get_mongo_data();
  },
};
</script>
