

/*Uncomment line 3 if you want to reset the database.

drop database FinalTake;
*/
create database FinalTake;
use FinalTake;

create table media(
	mediaID int not Null auto_increment,
    primary key(mediaID)
    );
    
create table Users(
	UserId int not null auto_increment,
    username varchar(50),
    pw varchar(50),
    email varchar(50),
    
    Primary key(USERID)
	);

create table Sessions(
	SessionID int not null auto_increment,
    SessionUser int not null,
    Primary Key (SessionID),
    Foreign key (SessionUser) references Users(UserID)
    );

create table Movies(
	movieID int not null auto_increment,
	mediaID int not null,
    
    title varchar(255) not null,
    yor int,
    tmdbID int, 
    picture varchar(255),
    decription varchar(255),
    
    primary key (movieID),
    Foreign Key (mediaID) references media(mediaID)
    );
    
create table Books(
	BookID int not null auto_increment,
    title varchar(255) not null,
	mediaID int not null,
    Author varchar(255),
    published int,
    ISBN int, 
    picture varchar(255),
    decription varchar(255),
	primary key (BookID),
    Foreign Key (mediaID) references media(mediaID)
    );
    
create table shows(
	showID int not null auto_increment,
    title varchar(255) not null,
	mediaID int not null,
    yor int,
    tvdbID int, 
    picture varchar(255),
    decription varchar(255),
	primary key (showID),
    Foreign Key (mediaID) references media(mediaID)
    );
    
create table games(
	gameID int not null auto_increment,
    mediaID int not null,
    title varchar(255) not null,
    yor int,
    rawgID int, 
    picture varchar(255),
    decription varchar(255),
    primary key (gameID),
    Foreign Key (mediaID) references media(mediaID)
    );
    

    
create table comments(
	commentID int not null auto_increment,
    mediaID int not null,
    userID int not null,
    commentText varchar(500),
    
    primary key (commentID),
    foreign key (mediaID) references media(mediaID),
    foreign key (userID) references users(userID)
    );
    
    
insert into media values(null);
insert into movies (mediaID, title) values (1, "Escape from New York");

insert into media values(null);
insert into Books (mediaID, title, Author) values(2, "Wizard of Earthsea", "Ursula K. LeGuin");

insert into media values(null);
insert into shows (mediaId, title) values (3, "Grim Adventures of Billy and Mandy");

insert into media values(null);
insert into games (mediaId, title) values (4, "Balatro");

insert into Users (username, pw, email) values ("grocha", "pw", "grocha2381@gmail.com");
insert into comments (mediaID, userID, commentText) values (4, 1, "This game is great");