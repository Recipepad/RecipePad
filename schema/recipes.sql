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
