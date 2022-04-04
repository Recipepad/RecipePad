CREATE TABLE `user_account` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `uid` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`uid`,`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=latin1;
