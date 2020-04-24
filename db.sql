--
-- Table structure for table `author`
--
 
 
CREATE TABLE `author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `password` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
);
 
--
-- Dumping data for table `author`
--
 
INSERT INTO `author` VALUES (1,'egoing',SHA2('egoing', 256));
INSERT INTO `author` VALUES (2,'duru', SHA2('duru', 256));
INSERT INTO `author` VALUES (3,'taeho',SHA2('taeho', 256));
INSERT INTO `author` VALUES (4,'sookbu ', SHA2('sookbun', 256));
 
--
-- Table structure for table `topic`
--
 
CREATE TABLE `content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `songtitle` varchar(100) NOT NULL,
  `lyrics` text,
  `created` datetime NOT NULL,
  `url` text,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
);
 
--
-- Dumping data for table `topic`
--
 
INSERT INTO `content` VALUES (1,'아기상어','아기상어 뚜르르뚜르','2018-01-01 12:10:11','<iframe width="560" height="315" src="https://www.youtube.com/embed/761ae_KDg_Q" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', 1);
INSERT INTO `content` VALUES (2,'찐이야','찐찐찐찐 찐이야 완전 찐이야','2018-01-03 13:01:10', '<iframe width="560" height="315" src="https://www.youtube.com/embed/64RV3mnRB3o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',1);