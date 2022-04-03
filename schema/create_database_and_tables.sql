CREATE DATABASE `recipepad`;
CREATE TABLE `user_account` (
  `Username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `UID` int(10) unsigned NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `UID_UNIQUE` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_profile` (
  `UID` int(11) NOT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `avatar_imgID` int(11) DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `recipes` (
  `RID` int(11) NOT NULL,
  `title` varchar(45) DEFAULT NULL,
  `cover_imgID` int(11) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `ingredients` json DEFAULT NULL,
  `steps` json DEFAULT NULL,
  `tags` json DEFAULT NULL,
  PRIMARY KEY (`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_recipes` (
  `UID` int(11) NOT NULL,
  `RID` int(11) NOT NULL,
  PRIMARY KEY (`UID`,`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `user_bookmark` (
  `UID` int(11) NOT NULL,
  `RID` int(11) NOT NULL,
  PRIMARY KEY (`UID`,`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;