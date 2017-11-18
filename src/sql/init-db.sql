drop table if exists TL;
create table TL (
    op_id serial primary key,
    r_id int not null,
    c    text,
    deleted boolean default false
);
