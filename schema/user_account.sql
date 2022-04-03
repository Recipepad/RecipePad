CREATE TABLE `user_account` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `uid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
