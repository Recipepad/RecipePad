CREATE TABLE `recipes` (
  `rid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  `cover_imgid` varchar(45) DEFAULT NULL,
  `description` varchar(300) DEFAULT NULL,
  `ingredients` json DEFAULT NULL,
  `steps` json DEFAULT NULL,
  `tags` json DEFAULT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
