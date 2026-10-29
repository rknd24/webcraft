-- 下書きで本番はモデル

CREATE TABLE users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL
);

CREATE TABLE category (
    category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);

CREATE TABLE question (
    que_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id INT NOT NULL REFERENCES category (category_id),
    que_statement TEXT NOT NULL,
    que_explanation TEXT NOT NULL
);