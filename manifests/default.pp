node default {
  include postgresql
  
  class { 'postgresql::server': }

  postgresql::server::db { 'datahub':
    user     => 'postgres',
    password => postgresql_password('postgres', 'postgres'),
  }
}
