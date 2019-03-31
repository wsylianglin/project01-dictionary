电子词典项目
    功能说明：
        1、用户可以登陆和注册，
            1）登陆需要用户名和密码
            2）注册要求用户必须填写用户名和密码其他内容自定
            3）用户名不能重复
        2、用户的数据要求保存在数据库中数据结构自定
        3、能够满足多个用户同时登陆操作的需求
        4、功能分为用户端和客户端，客户端发起请求，服务端处理请求。
        用户启动客户端即进入一级界面
            登陆   注册   退出
        5、用户登陆后进入二级界面
            查单词  查看历史记录 退出
            查单词：输入单词显示单词的意思，可以循环查询输入##表示退出
            查看历史记录：查看当前用户的历史查词记录
            name  word  time
            退出：退出到一级界面相当于注销

        1、确定技术点
            1）什么并发，什么套接字 什么数据库
            文件处理还是数据库查询？如果是数据库查询如何将单词存入数据库
            2）建立数据表
            建立几个表 每个表结构，表关系
            用户表(user_id,user_name(unique key),user_age,user_pwd)
            单词表(w_id,w_name,w_explain)
            历史表：history(u_name,w_name,time)
            3）搭建通信框架
            4）分析几个功能，如何封装，每个功能的具体实现内容

项目分析
服务器： 登陆 注册 查词 历史记录

客户端：打印界面 发出请求 接受反馈 打印结果

技术点：并发 sys.fock
      套接字 tcp
      数据库 mysql
      查词  文本
工作流程： 创建数据库，存储数据 -->搭建通信框架，建立并发关系---->实现具体的功能封装

1.创建数据库存储数据
dic
user： id name password
hist： id name word time
words：id word interpret

create table user(
    U_id int primary key auto_increment,
    u_name varchar(32) NOT NULL,
    u_password varchar(20) default '000000'
    )default chartset=utf8;
create table hist(
    w_id int primary key auto_increment,
    u_name varchar(32),
    w_name varchar(32) NOT NULL,
    w_time varchar(64)
    )default charset=utf8;
create table words(
    id int primary key auto_increment,
    w_name varchar(32) NOT NULL,
    interpret text NOT NULL
    )default charset=utf8;

2、搭建通信框架
    服务器：创建套接字--->创建父子进程--->子进程等待处理客户端请求
          父进程继续接受下一个客户端连接
    客户端：创建套接字-->发起连接请求--->一级界面-->请求(登陆，注册，退出)
          登陆成功-->进入二级界面-->请求(查词，历史记录)



