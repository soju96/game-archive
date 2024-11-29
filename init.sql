-- init.sql

-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS flask_db;

-- 데이터베이스 사용
USE flask_db;

-- 기존 테이블 삭제 (초기화용)
DROP TABLE IF EXISTS Comment_table;
DROP TABLE IF EXISTS Answer_table;
DROP TABLE IF EXISTS Question_table;
DROP TABLE IF EXISTS GameSolution_table;
DROP TABLE IF EXISTS News_table;
DROP TABLE IF EXISTS Content_table;
DROP TABLE IF EXISTS User_table;

-- users 테이블 생성
USE flask_db;

-- 사용자 테이블 생성
CREATE TABLE User_table (
    user_id INT AUTO_INCREMENT PRIMARY KEY,      -- 사용자 고유 ID
    username VARCHAR(100) NOT NULL UNIQUE,        -- 사용자 이름 (로그인 ID)
    email VARCHAR(100) NOT NULL UNIQUE,          -- 이메일 주소
    password VARCHAR(255) NOT NULL,              -- 비밀번호 해시 값
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 계정 생성 시간
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,             -- 마지막 업데이트 시간
    last_login DATETIME                          -- 마지막 로그인 시간
);

-- 콘텐츠 테이블 생성
CREATE TABLE Content_table (
    content_id INT AUTO_INCREMENT PRIMARY KEY, -- 콘텐츠 고유 ID
    name VARCHAR(100) NOT NULL, -- 콘텐츠 이름
    description VARCHAR(200) NOT NULL -- 콘텐츠 설명
);

-- 댓글 테이블 생성
CREATE TABLE Comment_table (
    comment_id INT AUTO_INCREMENT PRIMARY KEY, -- 댓글 고유 ID
    content_id INT NOT NULL, -- 콘텐츠 ID (외래 키)
    user_id INT NOT NULL, -- 사용자 ID (외래 키)
    content TEXT NOT NULL, -- 댓글 내용
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- 댓글 작성 시간
    FOREIGN KEY (content_id) REFERENCES Content_table(content_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User_table(user_id) ON DELETE CASCADE
);

-- 질문 테이블 생성
CREATE TABLE Question_table (
    question_id INT AUTO_INCREMENT PRIMARY KEY, -- 질문 고유 ID
    user_id INT NOT NULL, -- 사용자 ID (외래 키)
    title VARCHAR(100) NOT NULL, -- 질문 제목
    content TEXT NOT NULL, -- 질문 내용
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- 질문 작성 시간
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL, -- 질문 업데이트 시간
    FOREIGN KEY (user_id) REFERENCES User_table(user_id) ON DELETE CASCADE
);

-- 답변 테이블 생성
CREATE TABLE Answer_table (
    answer_id INT AUTO_INCREMENT PRIMARY KEY, -- 답변 고유 ID
    question_id INT NOT NULL, -- 질문 ID (외래 키)
    user_id INT NOT NULL, -- 사용자 ID (외래 키)
    content TEXT NOT NULL, -- 답변 내용
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- 답변 작성 시간
    FOREIGN KEY (question_id) REFERENCES Question_table(question_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User_table(user_id) ON DELETE CASCADE
);

-- 게임 솔루션 테이블 생성
CREATE TABLE GameSolution_table (
    game_id INT AUTO_INCREMENT PRIMARY KEY, -- 게임 솔루션 고유 ID
    user_id INT NOT NULL, -- 사용자 ID (외래 키)
    game_title VARCHAR(100) NOT NULL, -- 게임 제목
    content TEXT NOT NULL, -- 솔루션 내용
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- 작성 시간
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL, -- 업데이트 시간
    FOREIGN KEY (user_id) REFERENCES User_table(user_id) ON DELETE CASCADE
);

-- 뉴스 테이블 생성
CREATE TABLE News_table (
    news_id INT AUTO_INCREMENT PRIMARY KEY, -- 뉴스 고유 ID
    news_title VARCHAR(100) NOT NULL, -- 뉴스 제목
    content TEXT NOT NULL, -- 뉴스 내용
    auth VARCHAR(100) NOT NULL, -- 작성자 이름 또는 권한 정보
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL -- 작성 시간
);


-- admin 사용자 비밀번호 설정 및 권한 부여 (MySQL 8.0 기본 인증 플러그인 사용)
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON flask_db.* TO 'admin'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;