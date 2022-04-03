CREATE TABLE `user_profile` (
  `UID` int(11) NOT NULL,
  `nickname` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `avatar_imgID` int(11) DEFAULT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
