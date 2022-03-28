create database `musicfy_db`;

create table `user_tbl` (
    `uid` int not null auto_increment,
    `usertype` varchar(10) not null,
    `username` varchar(30) not null,
    `password` varchar(16) not null,
    `subscription` bool not null default 0,
    `uploaded` int not null default 0,
    `downloaded` int not null default 0,
    `profile_image` varchar(50) not null default 0,
    `image_id` varchar(50) not null default 0,
    primary key (uid)
);

create table `audio_tbl` (
    `aid` int not null auto_increment,
    `audio_name` varchar(50) not null,
    `uid` int not null, -- id of Artist / Uploader
    `audio_path` varchar(255) not null, -- Reason of not storing as BLOB: Performance overhead
    primary key (aid),
    foreign key (uid) references user_tbl(uid) on delete cascade
);

-- constraint Primary key = foreign+foreign/unique from other tables to form PK
create table `like_tbl` (
    `aid` int not null,
    `uid` int not null,
    `like_status` tinyint(1), -- 0 = dislike, 1 = like,  no react = delete
    foreign key (aid) references audio_tbl(aid) on delete cascade,
    foreign key (uid) references user_tbl(uid) on delete cascade,
    constraint PK_likes primary key (aid,uid)
);

create table `category_tbl` (
    `cid` int not null auto_increment,
    `category_name` varchar(50) not null,
    primary key (cid)
);

create table `song_in_category` (
    `cid` int not null,
    `aid` int not null,
    foreign key (cid) references category_tbl(cid) on delete cascade,
    foreign key (aid) references audio_tbl(aid) on delete cascade,
    constraint PK_sic primary key (cid,aid)
);

create table `playlist_tbl` (
    `pid` int not null auto_increment, -- Unique code for every playlist
    `uid` int not null,                -- Owner of playlist
    `playlist_name` varchar(50) not null,
    primary key (pid),
    foreign key (uid) references user_tbl(uid) on delete cascade
);

create table `song_in_playlist` (
    `pid` int not null,
    `aid` int not null,                -- Songs in the playlist
    foreign key (pid) references playlist_tbl(pid) on delete cascade,
    foreign key (aid) references audio_tbl(aid) on delete cascade,
    constraint PK_sip primary key (pid,aid)
);

/* NOT DECIDED TO IMPLEMENT YET

create table `album_tbl` (
    `album_id` int not null auto_increment,
    `uid` int not null,
    primary key (album_id),
    foreign key (uid) references user_tbl(uid)
);

create table `song_in_album` (
    `album_id` int not null,
    `aid` int not null,
    foreign key (album_id) references album_tbl(album_id),
    foreign key (aid) references audio_tbl(aid),
    constraint PK_sia primary key (album_id,aid)
);
*/

-- --------------------------------------------Below are sample data----------------------------------------------

insert into `user_tbl` (uid, usertype, username, password)
values ('1','admin','admin','admin'),
('2','artist','imartist','artist'),
('3','listener','imlistener','listener');

insert into `audio_tbl` (aid, audio_name, uid, audio_path)
values (1, 'Star Wars 3', 1, 'audio_files/StarWars3.wav'),
(2, 'Lone Sojounrer', 1, 'audio_files/Lone_Sojourner.mp3'),
(3, 'The Moon Song', 1, 'audio_files/The_Moon_Song.mp3'),
(4, '2113', 1, 'audio_files/two_one_one_three.mp3'),
(5, 'Letting Go', 1, 'audio_files/letting_go.mp3');

insert into `like_tbl` (aid, uid, like_status)
values (1,1,1),
(2,1,1),
(3,1,1),
(4,1,1),
(5,1,1);

insert into `category_tbl` (cid, category_name)
values (1,'Lofi'),
(2,'Hit-hop'),
(3,'Jazz'),
(4,'Meme'),
(5,'Game OST'),
(6,'acoustic');

insert into `song_in_category` (cid, aid)
values (1,5),
(4,4),
(3,5),
(4,1),
(5,2),
(6,3);

insert into `playlist_tbl` (pid, uid, playlist_name)
values (1,1, "Oh snap ACT 1st playlist"),
(2,1, "playlist satu"),
(3,1, "Playlist dua lipa"),
(4,2, "third playlist"),
(5,3, "playlist wu");

insert into `song_in_playlist` (pid, aid)
values (1,1),
(1,2),
(1,3),
(1,4),
(1,5),
(4,1),
(4,2),
(5,3),
(5,4),
(5,5);