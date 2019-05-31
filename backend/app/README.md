## 数据库设计
### 博物馆信息
#### 段落信息
```json
{
title:"",
title_md5:"",
index:"",//所属段落位置
context:"",//段落内容
is_labled:"",
is_used:"",
user_name:"",
user_email:"",
question_answer:[
    {
        question:"",
        answer:"",
        start_postion:""
    },
],
version:""
}
```

#### 文章总体
```json
{
    title:"",
    title_md5:"",

}
```
#### 用户账号

```json
{
    user_name:"",
    user_email:"",//unique
    password_md5:"",
}
```