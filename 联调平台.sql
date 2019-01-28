-- 用户表

UES serice;

CREATE TABLE account
 (
  id  INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  user VARCHAR(50) NOT NULL DEFAULT "",
  pwd VARCHAR(100) NOT NULL DEFAULT "",
  nick_name  VARCHAR(11) not null DEFAULT ""
)
engine myisam charset UTF8;