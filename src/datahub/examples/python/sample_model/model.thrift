struct Faculty {
  1: optional i32 id,
  2: optional string name,
}

struct Course {
  1: optional i32 id,
  2: optional string name,
  3: optional Faculty faculty,
}

