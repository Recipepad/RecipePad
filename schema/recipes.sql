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