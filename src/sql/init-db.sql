drop table if exists tl;
create table tl(
    -- original attributes
    r_id int not null,
    c    text,

    -- timeline attributes
    op_id serial primary key,
    deleted boolean default false,

    -- signatures
    sig numeric(400)
);
