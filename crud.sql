drop table if exists contents;

create table contents (
    id integer primary key autoincrement,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp,
    title text not null,
    body text not null
);
