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
        
        /*************************
         CREATE AND REMOVE ACCOUNT
         *************************/
        @try {
            datahub_accountAccountServiceClient *client = [[datahub_accountAccountServiceClient alloc] initWithProtocol:protocol];
            
            // create
            [client create_account:@"ACCOUNT_NAME" email:@"ACCOUNT_EMAIL" password:@"ACCOUNT PASSWORD" app_id:@"APP_ID" app_token:@"APP_TOKEN"];
            
            // delete
            [client remove_account:@"ACCOUNT_NAME" app_id:@"APP_ID" app_token:@"APP_TOKEN"];
        }
        @catch (NSException *exception) {
            NSLog(@"Create/Delete: %@", exception);
        }
        
        
        /***********************
         CONNECT TO AND QUERY DB
         ***********************/
        @try {
            datahubDataHubClient *server = [[datahubDataHubClient alloc] initWithProtocol:protocol];
            
            datahubConnectionParams *conparams = [[datahubConnectionParams alloc] initWithClient_id:@"foo" seq_id:nil user:@"anantb" password:@"anant" repo_base:nil];
            
            datahubConnection *connection = [server open_connection:conparams];
            datahubResultSet *results = [server execute_sql:connection query:@"select * from test.demo" query_params:nil];
            
            NSLog(@"%@", results);
        }
        @catch (NSException *exception) {
            NSLog(@"Connect/Query Exception: %@", exception);
        }
       
        
    }
    return 0;
}
