CREATE TABLE users (
    id INT PRIMARY KEY,
    address VARCHAR(44) NOT NULL UNIQUE
);

CREATE TABLE currency (
    user_id INT REFERENCES users(id),
    address VARCHAR(44) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    PRIMARY KEY (user_id, address)
);

CREATE INDEX user_address ON users(address);
