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

#import "Thrift.h"
#import "TBinaryProtocol.h"
#import "THTTPClient.h"
#import "TTransport.h"


int main(int argc, const char * argv[]) {
    @autoreleasepool {
        
        /**********
         HTTP SETUP
         **********/
        NSURL *url = [NSURL URLWithString:@"http://datahub.csail.mit.edu/service"]; // chose you server
        
        // Talk to a server via HTTP, using a binary protocol
        THTTPClient *transport = [[THTTPClient alloc] initWithURL:url];
        
        TBinaryProtocol *protocol = [[TBinaryProtocol alloc]
                                     initWithTransport:transport
                                     strictRead:YES
                                     strictWrite:YES];
        
        
        /********************************************************
         CONNECT TO AND QUERY DB USING YOUR USERNAME AND PASSWORD
         ********************************************************/
        // This will initially thrown an exception.
        // You will need to create a username, password,
        // repository, and table to query.
        @try {
            
            NSLog(@"\n\nTrying to query a user's table...");
            
            // create a client
            datahubDataHubClient *client = [[datahubDataHubClient alloc] initWithProtocol:protocol];
            
            // create connection parameters
            // login with a username and password
            datahubConnectionParams *conparams = [[datahubConnectionParams alloc] initWithClient_id:nil seq_id:nil user:@"YOUR USERNAME" password:@"YOUR PASSWORD" app_id:nil app_token:nil repo_base:nil];
            
            // If a user has authorized your application, you can also connect to their repo by leaving user and password as nil and adding your app_id, app_token, and repo_base variables.
            // They can authorize your account at https://datahub.csail.mit.edu/permissions/apps/allow_access/APP_ID/REPO_NAME
            // datahubConnectionParams *conparams = [[datahubConnectionParams alloc] initWithClient_id:nil seq_id:nil user:@"YOUR USERNAME" password:nil app_id:@"APP ID" app_token:@"APP_TOKEN" repo_base:nil];
            
            
            // open a connection
            datahubConnection *connection = [client open_connection:conparams];
            
            // get the result set
            datahubResultSet *results = [client execute_sql:connection query:@"select * from REPO_NAME.TABLE_NAME" query_params:nil];

            // make sure and close the connection
            [client close_connection:connection];
            
            NSLog(@"%@", results);
        }
        @catch (NSException *exception) {
            NSLog(@"Connect/Query Exception: %@", exception);
        }
       
        
    }
    return 0;
}
