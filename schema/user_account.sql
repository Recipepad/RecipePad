CREATE TABLE `user_account` (
  `Username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `UID` int(10) unsigned NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `UID_UNIQUE` (`UID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
