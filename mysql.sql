CREATE DATABASE `musicfy_db`;

CREATE TABLE `user_tbl` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `usertype` varchar(10) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(16) NOT NULL,
  `subscription` tinyint(1) NOT NULL DEFAULT '0',
  `uploaded` int NOT NULL DEFAULT '0',
  `downloaded` int NOT NULL DEFAULT '0',
  `profile_image` varchar(50) NOT NULL DEFAULT '0',
  `image_id` varchar(50) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`)
);

CREATE TABLE `audio_tbl` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `audio_name` varchar(50) NOT NULL,
  `uid` int NOT NULL,
  `audio_path` varchar(255) NOT NULL,
  `song_id` varchar(100) NOT NULL,
  PRIMARY KEY (`aid`),
  KEY `uid` (`uid`),
  CONSTRAINT `audio_tbl_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user_tbl` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `category_tbl` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  PRIMARY KEY (`cid`)
);

CREATE TABLE `like_tbl` (
  `aid` int NOT NULL,
  `uid` int NOT NULL,
  `like_status` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`aid`,`uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `like_tbl_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `audio_tbl` (`aid`) ON DELETE CASCADE,
  CONSTRAINT `like_tbl_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `user_tbl` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `playlist_tbl` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `uid` int NOT NULL,
  `playlist_name` varchar(50) NOT NULL,
  PRIMARY KEY (`pid`),
  KEY `uid` (`uid`),
  CONSTRAINT `playlist_tbl_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user_tbl` (`uid`) ON DELETE CASCADE
);

CREATE TABLE `song_in_category` (
  `cid` int NOT NULL,
  `aid` int NOT NULL,
  PRIMARY KEY (`cid`,`aid`),
  KEY `aid` (`aid`),
  CONSTRAINT `song_in_category_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `category_tbl` (`cid`) ON DELETE CASCADE,
  CONSTRAINT `song_in_category_ibfk_2` FOREIGN KEY (`aid`) REFERENCES `audio_tbl` (`aid`) ON DELETE CASCADE
);

CREATE TABLE `song_in_playlist` (
  `pid` int NOT NULL,
  `aid` int NOT NULL,
  PRIMARY KEY (`pid`,`aid`),
  KEY `aid` (`aid`),
  CONSTRAINT `song_in_playlist_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `playlist_tbl` (`pid`) ON DELETE CASCADE,
  CONSTRAINT `song_in_playlist_ibfk_2` FOREIGN KEY (`aid`) REFERENCES `audio_tbl` (`aid`) ON DELETE CASCADE
);

INSERT INTO `category_tbl` (`cid`, `category_name`) VALUES 
(1,'Lofi'),
(2,'Hit-hop'),
(3,'Jazz'),
(4,'Meme'),
(5,'Game OST'),
(6,'acoustic');

INSERT INTO `user_tbl` (`uid`, `username`, `password`, `usertype`,`subscription`, `uploaded`, `downloaded`, `profile_image`, `image_id`) VALUES 
-- Admin
(1,'admin','admin','admin',1,0,0,'0','0'),
-- Artist
(2,'artist','artist123','artist',1,3,0,'0','0'),
(3,'James','james123','artist',1,2,0,'0','0'),
(4,'Ali','ali123','artist',1,4,0,'0','0'),
(5,'Simon','simon123','artist',0,3,0,'0','0'),
(6,'Linda','linda123','artist',0,1,0,'0','0'),
-- Listener
(7,'listener','imlistener1','listener',1,0,0,'3.jpg','1-pT9_4GJ19k-l9lTXLhaL0NUfHTYQh2t'),
(8,'Rando','rando123','listener',0,0,0,'3.jpg','1-pT9_4GJ19k-l9lTXLhaL0NUfHTYQh2t');


INSERT INTO `audio_tbl` (`aid`, `audio_name`, `uid`, `audio_path`, `song_id`) VALUES 
(1,'Star Wars 3',2,'audio_files/StarWars3.wav','1gg8Ao-zQLk0f2EflrYihQMQ3VLQsvhWn'),
(2,'Lone Sojounrer',2,'audio_files/Lone_Sojourner.mp3','1pCjZSko_mwa29MXWUxskBXhY_9y5YpGd'),
(3,'The Moon Song',2,'audio_files/The_Moon_Song.mp3','14nLSp4Q2IpLfQHrNlMyoBOZSnJamlc1Z'),
(4,'Two one one three 2113',3,'audio_files/two_one_one_three.mp3','1BrOAd5FSxpbnv9AjMM6BtFe2v5WDlJrZ'),
(5,'Letting Go',3,'audio_files/letting_go.mp3','1aeGtfQxMSFjGKXopUgv8WCiB9ICGAZpV'),
(6,'bossa uh',4,'audio_files/bossa uh - potsu.mp3','1fE-0WyB0JZ6in7oOSmitCIj9f5oHSDkH'),
(7,'Stay Strapped',4,'audio_files/Stay Strapped - MC Virgins & Yung Nugget.mp3','1jU9XNVE767uSYqldf5QlNuWY9D5Nwdq-'),
(8,'Someone Special',4,'audio_files/Someone Special - tomatoism.mp3','1i78Lssp9fGxwM-hoavG9JgVc8X7cn8WT'),
(9,'Make You Mine',4,'audio_files/Make You Mine - PUBLIC.mp3','1hg0sFVU9F_GTh5spJz-ILqpTkHbpc3nC'),
(10,'just friends',5,'audio_files/just friends - potsu.mp3','1pQSSMe2Bh0uAnJwm1xUCFeUz0NXJLZal'),
(11,'comethru',5,'audio_files/comethru - Jeremy Zucker.mp3','1MLkxnh8NA0RilVHQvPawYAUcGtjj2sQb'),
(12,'deep coma',5,'audio_files/deep coma - haruno.mp3','1J9c1c1E4-D2p4AOWRuUzDYKVLRgMouk9'),
(13,'Better Now (Slowed)',6,'audio_files/Better now -post malone (slowed + reverb).mp3','1eBKE2hDtHA8xlcNaVAFx3FOZzCYTlDZb');



INSERT INTO `song_in_category` (`aid`,`cid`) VALUES 
(1,4),
(2,5),
(3,6),
(4,4),
(4,2),
(5,3),
(5,1),
(6,3),
(6,1),
(7,4),
(7,2),
(8,2),
(9,2),
(10,1),
(10,3),
(11,2),
(12,2),
(12,1),
(12,6),
(13,1),
(13,2);


INSERT INTO `like_tbl` (`aid`, `uid`, `like_status`) VALUES 
(1,1,1),
(1,2,1),
(1,3,1),
(1,4,1),
(1,6,1),
(1,7,1),
(2,4,1),
(3,1,1),
(4,1,1),
(5,1,1);

INSERT INTO `playlist_tbl` (`pid`, `uid`, `playlist_name`) VALUES 
(1,2,'Artist Playlist'),
(2,3,'James Pick'),
(3,4,'Disco'),
(4,5,'Good Stuff'),
(5,7,'Amazing Songs');

INSERT INTO `song_in_playlist` (`pid`, `aid`) VALUES 
(1,1),
(1,3),
(1,8),
(1,12),
(2,12),
(2,8),
(2,13),
(2,7),
(2,3),
(3,12),
(3,8),
(3,13),
(3,7),
(3,3),
(4,11),
(4,10),
(4,9),
(4,2),
(4,4),
(4,5),
(4,1),
(5,3),
(5,6),
(5,5),
(5,4),
(5,2);

