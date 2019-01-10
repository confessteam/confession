



# 一起表白吧

## 用户表（user表）			

| 字段名   | 数据类型       | 描述   |      |
| -------- | -------------- | ------ | ---- |
| userName | vchar（30）    | 昵称   |      |
| phone    | vchar（11）    | 手机号 |      |
| password | varchar（256） | 密码   |      |
| icon     | varchar（256） | 头像   |      |
| sex      | varchar（5）   | 性别   |      |
| age      | integer        | 年龄   |      |
| id       | integer        | 用户id |      |
| province | varchar（64）  | 省     |      |
| city     | varchar（64）  | 市     |      |
| school   | varchar（256） | 学校   |      |
|          |                |        |      |

## 表白表（confess表）			

| 字段名   | 数据类型       | 描述     |
| -------- | -------------- | -------- |
| userID   | integer        | 用户id   |
| context  | text           | 表白内容 |
| id       | integer        | 表白id   |
| img1     | varchar（256） | 配图1    |
| img2     | varchar（256） | 配图2    |
| img3     | varchar（256） | 配图3    |
| userName | varchar(30)    | 昵称     |
| state    | varchar（50）  | 审核状态 |

## 点赞表（like）

| 字段名 | 数据类型 | 描述 |
| ------ | -------- | ---- |
| userID | VAR      |      |
|        |          |      |

