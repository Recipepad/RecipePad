CREATE TABLE `user_account` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`uid`,`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
