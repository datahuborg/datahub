create table versions (
 v_id SERIAL primary key,
 name varchar(100) NOT NULL CHECK (name <> ''),
 ts timestamp default  current_timestamp,
 user_id varchar(100),
 msg varchar(240) 
);

create table version_parent (
  child_id integer references versions(v_id),
  parent_id integer references versions(v_id)
);

create table query_log (
  log_id SERIAL primary key,
  v_id integer references versions(v_id),
  ts timestamp default  current_timestamp,
  queries json
);

create table versioned_table (
  real_name varchar(110) primary key,
  display_name varchar(100),
  v_id integer references versions(v_id),
  copy_on_write boolean default false,
  ts timestamp default current_timestamp
);

create table versioned_table_parent (
  child_table varchar(110) references versioned_table(real_name),
  parent_table varchar(110) references versioned_table(real_name)
);

create table table_metadata (
  rid integer,
  deleted boolean default false,
  table_rn varchar(110) references versioned_table(real_name)
);

create table user_head (
  user_id varchar(100),
  repo varchar(100),
  head_version integer references versions(v_id),
  constraint head primary key(user_id, repo)
);