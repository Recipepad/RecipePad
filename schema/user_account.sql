CREATE TABLE `user_account` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `uid` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`uid`),
UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1007 DEFAULT CHARSET=latin1;
