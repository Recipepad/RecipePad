CREATE TABLE `user_bookmark` (
  `uid` int(11) unsigned NOT NULL,
  `rid` int(11) unsigned NOT NULL,
  PRIMARY KEY (`uid`,`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
