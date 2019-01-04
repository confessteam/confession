# 一起表白吧

## 用户表（user表）			

| 字段名   | 数据类型       | 描述   |
| -------- | -------------- | ------ |
| u_name   | vchar（30）    | 昵称   |
| phone    | vchar（11）    | 手机号 |
| password | varchar（11）  | 密码   |
| icon     | varchar（256） | 头像   |
| sex      | varchar（5）   | 性别   |
| age      | integer        | 年龄   |
| id       | integer        | 用户id |

## 表白表（confess表）			

| 字段名  | 数据类型       | 描述     |
| ------- | -------------- | -------- |
| u_id    | integer        | 用户id   |
| context | text           | 表白内容 |
| id      | integer        | 表白id   |
| img1    | varchar（256） | 配图1    |
| img2    | varchar（256） | 配图2    |
| img3    | varchar（256） | 配图3    |