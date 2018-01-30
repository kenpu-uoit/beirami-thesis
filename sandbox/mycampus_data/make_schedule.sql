create sequence am_thesis.id;

create table am_thesis.schedule__base as 
select nextval('am_thesis.id') as id, *
from am_thesis.schedule;

alter table am_thesis.schedule__base
add primary key (id);

drop table am_thesis.schedule;

-- create table for tracking snapshots

create table if not exists am_thesis.system_snapshots (
    snapshotname varchar(100) primary key,
    tablename varchar(100),
    __t__ timestamp
)
