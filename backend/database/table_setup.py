TABLE_SETUP_QUERY="""

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
	Name text,
    Description text,
	Price decimal,
	OwnerID int,

    PRIMARY KEY (ID),
	FOREIGN KEY (OwnerID) REFERENCES Users(ID)
)

-- Central table in star schema (the 'many' side)
CREATE TABLE Transactions (
    ID int IDENTITY(1, 1),
    ProductID int,
    BuyerID int,
    SellerID int,

    PRIMARY KEY (ID),
    FOREIGN KEY (ProductID) REFERENCES Products(ID),
    FOREIGN KEY (BuyerID) REFERENCES Users(ID),
    FOREIGN KEY (SellerID) REFERENCES Users(ID)
)

-- Central table in second star schema
CREATE TABLE Messages (
    ID int IDENTITY(1, 1),
    Title text,
    Content text,
    FromUserID int,
    ToUserID int,

    PRIMARY KEY (ID),
    FOREIGN KEY (FromUserID) REFERENCES Users(ID),
    FOREIGN KEY (ToUserID) REFERENCES Users(ID),
)

"""