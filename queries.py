CREATE_TABLE_USERS = """
create table if not exists public.users (
	id serial PRIMARY KEY,
	username varchar(50) unique not null,
	password varchar(255) not null,
	email_address varchar(50) unique not null,
	created_at timestamp not null
);
"""
