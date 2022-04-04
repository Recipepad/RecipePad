CREATE DATABASE `recipepad`;
CREATE TABLE `user_account` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`uid`,`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_profile` (
  `uid` int(11) unsigned NOT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `avatar_imgid` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `recipes` (
  `rid` int(11) unsigned NOT NULL,
  `title` varchar(45) DEFAULT NULL,
  `cover_imgid` int(11) unsigned DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `ingredients` json DEFAULT NULL,
  `steps` json DEFAULT NULL,
  `tags` json DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_recipes` (
  `uid` int(11) unsigned NOT NULL,
  `rid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`uid`,`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_bookmark` (
  `uid` int(11) unsigned NOT NULL,
  `rid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`uid`,`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
