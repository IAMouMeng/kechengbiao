-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2023-10-30 20:30:12
-- 服务器版本： 5.7.40-log
-- PHP 版本： 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `api_score`
--

-- --------------------------------------------------------

--
-- 表的结构 `assistant_courses`
--

CREATE TABLE `assistant_courses` (
  `id` int(11) NOT NULL,
  `username` varchar(32) DEFAULT NULL COMMENT '学号',
  `courses` json DEFAULT NULL COMMENT '课程表',
  `updatetime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `createtime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `assistant_exams`
--

CREATE TABLE `assistant_exams` (
  `id` int(11) NOT NULL,
  `username` varchar(32) DEFAULT NULL COMMENT '学号',
  `year` varchar(32) DEFAULT NULL COMMENT '学年',
  `semester` varchar(32) DEFAULT NULL COMMENT '学期',
  `exam_code` varchar(32) DEFAULT NULL COMMENT '学科代码',
  `exam_name` varchar(32) DEFAULT NULL COMMENT '学科名称',
  `exam_type` varchar(32) DEFAULT NULL COMMENT '学科类型',
  `exam_score` varchar(32) DEFAULT NULL COMMENT '学科分数',
  `exam_owner` varchar(32) DEFAULT NULL COMMENT '学科归属',
  `exam_makeup_score` varchar(32) DEFAULT NULL COMMENT '补考成绩',
  `exam_regrade_score` varchar(32) DEFAULT NULL COMMENT '重修成绩',
  `exam_credit_points` varchar(32) DEFAULT NULL COMMENT '学分',
  `exam_mark_minor` varchar(32) DEFAULT NULL COMMENT '辅修标识',
  `exam_gpa` varchar(32) DEFAULT NULL COMMENT '绩点',
  `updatetime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `createtime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `assistant_students`
--

CREATE TABLE `assistant_students` (
  `id` int(11) NOT NULL,
  `username` varchar(255) DEFAULT NULL COMMENT '学号',
  `name` varchar(32) DEFAULT NULL COMMENT '姓名',
  `institute` varchar(32) DEFAULT NULL COMMENT '学院',
  `profession` varchar(32) DEFAULT NULL COMMENT '专业',
  `classname` varchar(32) DEFAULT NULL COMMENT '班级',
  `avatar` varchar(255) DEFAULT 'https://static.lnsec.cn/20230930/avatar.png',
  `cookie` varchar(255) DEFAULT NULL,
  `courses_updatetime` datetime DEFAULT NULL,
  `exams_updatetime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `createtime` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转储表的索引
--

--
-- 表的索引 `assistant_courses`
--
ALTER TABLE `assistant_courses`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- 表的索引 `assistant_exams`
--
ALTER TABLE `assistant_exams`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD UNIQUE KEY `exam` (`username`,`year`,`semester`,`exam_code`) USING BTREE;

--
-- 表的索引 `assistant_students`
--
ALTER TABLE `assistant_students`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `username` (`username`) USING BTREE;

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `assistant_courses`
--
ALTER TABLE `assistant_courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `assistant_exams`
--
ALTER TABLE `assistant_exams`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `assistant_students`
--
ALTER TABLE `assistant_students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
