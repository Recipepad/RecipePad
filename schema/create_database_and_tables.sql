CREATE DATABASE `recipepad`;
CREATE TABLE `user_account` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `uid` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1007 DEFAULT CHARSET=latin1;
CREATE TABLE `user_profile` (
  `uid` int(11) unsigned NOT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `avatar_imgid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `recipe` (
  `rid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  `cover_imgid` varchar(45) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `ingredients` json DEFAULT NULL,
  `steps` json DEFAULT NULL,
  `tags` json DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_recipe` (
  `uid` int(11) unsigned NOT NULL,
  `rid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`uid`,`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_bookmark` (
  `uid` int(11) unsigned NOT NULL,
  `rid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`uid`,`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
