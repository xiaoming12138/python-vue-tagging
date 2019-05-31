<template>
  <div>
    <el-row gutter="20">
      <el-col :span="12">
        <el-input v-model="user.name" placeholder="请输入姓名" style></el-input>
      </el-col>
      <el-col :span="12">
        <el-input v-model="user.email" placeholder="请输入邮箱"></el-input>
      </el-col>
    </el-row>

    <h2>段落内容</h2>
    <el-row>
      <el-col :span="24">
        <el-card class="box-card">
          <div @click="put_answer">{{mongo_data.context}}</div>
        </el-card>
      </el-col>
    </el-row>
    <h2>问题&答案</h2>
    <el-row>
      <el-col :span="24">
        <el-card>
          <div class="panel-body" style="height: 500px; overflow-y:scroll">
            <div style="border: 1px  #000000; width: 90%; margin: 0 auto;" id="input_item">
              <el-card v-for="(data,index) in data_list" :key="data">
                <el-row @click.native="change_index(index)">
                  <el-col :span="3">
                    <h3>
                      <span style="background:gray;text-align: center;color: white">{{index+1}}.</span>
                    </h3>
                  </el-col>
                  <el-col :span="18">
                    <el-input
                      v-model="data.question"
                      @focus="change_index(index)"
                      placeholder="请输入问题"
                    ></el-input>
                    <!-- <el-card v-model="data.answer"></el-card> -->
                    <el-input
                      v-model="data.answer"
                      placeholder="答案"
                      :disabled="true"
                      class="answer_input"
                    ></el-input>
                    <el-radio-group v-model="data.is_impossible" @change="change_index(index)">
                      <el-radio-button label="true">正例</el-radio-button>
                      <el-radio-button label="false">负例</el-radio-button>
                    </el-radio-group>
                  </el-col>
                  <el-col :span="1" :offset="1">
                    <li
                      class="el-icon-info"
                      style="font-size:40px;align-content:center;color: gray"
                    ></li>
                  </el-col>
                </el-row>
              </el-card>
            </div>
            <div style="width:90% ;text-align:center">
              <el-button v-on:click="add" type="warning" icon="el-icon-circle-plus" round>添加问题</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="3" :offset="9">
        <el-button type="primary" @click="put_question_ans">确定</el-button>
      </el-col>
      <el-col :span="3">
        <router-link to="/">
          <el-button type="danger">退出</el-button>
        </router-link>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

export default {
  name: 'Reading',
  data() {
    return {
      user: { name: Cookies.get('name'), email: Cookies.get('email') },
      msg: 'Reading',
      focus_index: 0,
      data_list: [],
      data_item: {
        question: '',
        answer: '',
        start: -1,
        is_impossible: -1,
        is_checked: -1,
        checked_answer: -1,
        reason: -1,
      },
      init_data_list_len: 6,
      mongo_data: '',
      base_url: 'http://172.16.41.49:5000/',
    };
  },
  methods: {
    init_data_list() {
      for (let i = 0; i < this.init_data_list_len; i++) {
        this.data_list.push(JSON.parse(JSON.stringify(this.data_item)));
      }
    },
    add() {
      this.data_list.push(JSON.parse(JSON.stringify(this.data_item)));
      console.log(JSON.parse(JSON.stringify(this.data_item)));
    },
    change_index(num) {
      this.focus_index = num;
      console.log(this.focus_index);
    },
    get_selected() {
      const selection = window.getSelection();
      console.log(selection);
      console.log(window.getSelection().toString());
      console.log(window.getSelection().baseOffset);
      console.log(window.getSelection().focusOffset);
      return {
        text: selection.toString(),
        start: selection.baseOffset,
        end: selection.focusOffset,
      };
    },
    put_answer() {
      const data = this.get_selected();
      console.log(data);
      this.data_list[this.focus_index].answer = data.text;
      this.data_list[this.focus_index].start = data.start;
    },
    get_mongodata() {
      const path = `${this.base_url}context_v2`;
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
    get_reload() {
      this.focus_index = 0;
      this.data_list = [];
      this.init_data_list();
      this.get_mongodata();
    },
    put_question_ans() {
      const path = `${this.base_url}put_question_ans_v2`;
      let data;
      let index;
        console.log(this.data_list);
        if (this.user.name == '' || this.user.email == '') {
        this.$confirm('个人信息还没填写', '警告', {
          confirmButtonText: 'confirm',
          cancelButtonText: 'cancel',
          type: 'warning',
        })
          .then(() => {})
          .catch(() => {});
        return;
      }
      for (let i = 0; i < this.data_list.length; i++) {
        data = this.data_list[i];
        console.log(this.data_list[i]);
        if (
          data.question === '' ||
          data.answer === '' ||
          data.is_impossible === -1
        ) {
          this.$confirm(`${(i + 1).toString()}位置还没填写`, '警告', {
            confirmButtonText: 'confirm',
            cancelButtonText: 'cancel',
            type: 'warning',
          })
            .then(() => {})
            .catch(() => {});
          return;
        }
        this.data_list[i].is_impossible =
          data.is_impossible === 'true';
      }
        console.log(this.data_list);
        // axios
      //   .post(path, {
      //     user: this.user,
      //     mongo_data: this.mongo_data,
      //     labels: this.data_list,
      //   })
      //   .then((response) => {
      //     console.log(response);
      //   })
      //   .then(this.get_reload())
      //   .catch((error) => {
      //     console.log(error);
      //   });
    },
  },
  created() {
    // this.$confirm("这是一段说明", "说明", {
    //   confirmButtonText: "confirm",
    //   cancelButtonText: "cancel",
    //   type: "warning"
    // })
    //   .then(() => {})
    //   .catch(() => {});
    this.init_data_list();
    this.get_mongodata();
  },
};
</script>

<style scoped>
.el-row {
  margin: 20px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.el-input {
  margin-bottom: 10px;
}

.el-button {
  margin-top: 20px;
  /* align-content: center; */
  /* text-align: center; */
}
/* .answer_input {
  color: red;
} */
</style>
