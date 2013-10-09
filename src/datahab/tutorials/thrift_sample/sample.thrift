namespace py datahub.tutorials.thrift_sample

enum Sex {
  MALE,
  FEMALE
}

struct Department {
  1: i32 id,
  2: string name,
}

struct Faculty {
  1: i32 id,
  2: string name,
  3: Sex sex,
  4: Department dept,
  5: string office
}
