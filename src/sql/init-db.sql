drop table if exists tl;
create table tl(
    op_id serial primary key,
    r_id int not null,
    c    text,
    deleted boolean default false
);
