create extension if not exists "pgcrypto";

create table users (
    id uuid primary key default gen_random_uuid(),
    email text not null unique,
    username varchar(30) not null check (length(username) >= 2),
    created_at timestamptz not null default now()
);

insert into users (email, username) values
    ('kim@example.com',  '김철수'),
    ('lee@example.com',  '이영희'),
    ('park@example.com', '박민수'),
    ('choi@example.com', '최지은'),
    ('jung@example.com', '정하늘');