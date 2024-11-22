
DROP TABLE dbo.Messages;
DROP TABLE dbo.Transactions;
DROP TABLE dbo.Products;
DROP TABLE dbo.Users;

CREATE TABLE Users (
    ID int IDENTITY(1, 1),
    Username varchar(64) UNIQUE,
    Email varchar(320) UNIQUE,
    Password varchar(128),

    PRIMARY KEY (ID)
)

CREATE TABLE Products (
	ID int IDENTITY(1, 1),
	Name varchar(100),
    Description varchar(1000),
	Price DECIMAL(10, 2),
	OwnerID int,

    PRIMARY KEY (ID),
	FOREIGN KEY (OwnerID) REFERENCES Users(ID)
)

-- Central table in star schema (the 'many' side)
CREATE TABLE Transactions (
    ID int IDENTITY(1, 1),
    ProductID int,
    BuyerID int

    PRIMARY KEY (ID),
    FOREIGN KEY (ProductID) REFERENCES Products(ID),
    FOREIGN KEY (BuyerID) REFERENCES Users(ID)
)

-- Central table in second star schema
CREATE TABLE Messages (
    ID int IDENTITY(1, 1),
    Title varchar(100),
    Content varchar(1000),
    FromUserID int,
    ToUserID int,

    PRIMARY KEY (ID),
    FOREIGN KEY (FromUserID) REFERENCES Users(ID),
    FOREIGN KEY (ToUserID) REFERENCES Users(ID),
)
