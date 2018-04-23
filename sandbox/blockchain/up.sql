create table if not exists timeline (
    tx_id int,
    row_id int,
    deleted boolean,
    data text,
    primary key (tx_id, row_id)
);

create table if not exists entities (
    ent_id int primary key,
    pubkey text
);

create table if not exists signatures (
    tx_id int,
    hash text,
    sig  text,
    pubkey text,
    primary key (tx_id)
);

