//
//  main.m
//  DataHub-Example
//
//  Created by Albert Carter on 12/3/14.
//  Copyright (c) 2014 CSAIL Big Data Initiative. All rights reserved.
//

#import <Foundation/Foundation.h>

#import "datahub.h"
#import "account.h"
#import "THTTPClient.h"
#import "TBinaryProtocol.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        // insert code here...
        NSLog(@"Hello, World!");
        
        NSURL *url = [NSURL URLWithString:@"http://datahub.csail.mit.edu/service"];
        
        // Talk to a server via HTTP, using a binary protocol
        THTTPClient *transport = [[THTTPClient alloc] initWithURL:url];
        TBinaryProtocol *protocol = [[TBinaryProtocol alloc]
                                     initWithTransport:transport
                                     strictRead:YES
                                     strictWrite:YES];
        
        DataHubClient *server = [[DataHubClient alloc] initWithProtocol:protocol];
        
        ConnectionParams *conparams = [[ConnectionParams alloc] initWithClient_id:@"foo" seq_id:nil user:@"anantb" password:@"anant" repo_base:nil];
        
        Connection *connection = [server open_connection:conparams];
        
        ResultSet *results =  [server execute_sql:connection query:@"select * from test.demo" query_params:nil];
        
        NSLog(@"%@", results);
        
    }
    return 0;
}
