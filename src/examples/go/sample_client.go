package main

/**
 * Sample Go Client for DataHub
 *
 * @author: Anant Bhardwaj
 * @date: 03/23/2014
 */

import "fmt"
import "datahub"
import "git.apache.org/thrift.git/lib/go/thrift"

func main() {
  user, password := "anantb", "anant"
  con_params := datahub.ConnectionParams {
      User: user,
      Password: password}
  
  protocolFactory := thrift.NewTBinaryProtocolFactoryDefault()
  //transport, err := thrift.NewTHttpClient("http://datahub.csail.mit.edu/service")
  transport, err := thrift.NewTSocket("datahub.csail.mit.edu:9000")

  if err != nil {
    fmt.Println(err)
    return
  }

  client := datahub.NewDataHubClientFactory(transport, protocolFactory)

  transport.Open()
  defer transport.Close()

  // open connection
  con, exception, err := client.OpenConnection(&con_params)
  
  if exception != nil {
    fmt.Println(exception)
    return
  }

  // execute sql
  res, exception, err := client.ExecuteSql(
      con, "SELECT * FROM anantb.test.demo", nil)  
  
  if exception != nil {
    fmt.Println(exception)
    return
  }
  print_result_set(res)
}

func print_result_set(res *datahub.ResultSet) {
  // print fields
  if res != nil && res.FieldNames != nil {
    for _, field_name := range res.FieldNames {
      fmt.Printf("%s\t", field_name)
    }
  }

  fmt.Println()

  // print tuples
  if res != nil && res.Tuples != nil {
    for _, tuple := range res.Tuples {
      for _, cell := range tuple.Cells {
        fmt.Printf("%s\t", cell)
      }
      fmt.Println()
    }
  }

  fmt.Println()
}
