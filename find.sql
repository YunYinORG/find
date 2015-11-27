 /*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2015/11/7 11:16:30                           */
/*==============================================================*/


drop table if exists record;
drop table if exists user;

/*==============================================================*/
/* Table: record                                                   */
/*==============================================================*/
create table record
(
   id                int not null auto_increment,
   find_id           int not null,
   lost_id           int not null,
   time              timestamp not null default CURRENT_TIMESTAMP,
   status            tinyint not null default 0,
   way               int,
   token             char(32),
   primary key (id)
);


/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   id                int not null auto_increment,
   yyid              bigint,
   number            char(10) not null,
   school            tinyint,
   name              varchar(10) not null,
   phone             char(16),
   type              tinyint,#标记用户类型0临时用户，-1无账号用户(失主)，云印用户
   blocked				tinyint	not null default 0,
   status            tinyint default 1,
   primary key (id),
   CONSTRAINT UNIQUE_CARD UNIQUE (school,number),#卡号唯一
   UNIQUE(phone),#手机号唯一
   UNIQUE(yyid)
);

alter table record add constraint FK_lost_user foreign key (lost_id)
      references user (id) on delete restrict on update restrict;

alter table record add constraint FK_find_user foreign key (find_id)
      references user (id) on delete restrict on update restrict;