Use user_auth;
CREATE TABLE users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);
select * from users;
INSERT INTO users (username, password) VALUES ('admin', 'password123');
ALTER TABLE users ADD COLUMN email VARCHAR(255) NOT NULL UNIQUE;