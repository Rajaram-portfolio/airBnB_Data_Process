import json
import pandas as pd
import numpy as np
from datetime import date
import boto3
from io import StringIO

s3_client = boto3.client('s3')
today_date = str(date.today())
target_s3 = 'airbnbbooking-records'
target_file ="airbnbbooking_"+today_date+".csv"


def lambda_handler(event, context):
    try:
        #print(event)
        message =  json.loads(event[0]['body'])
        #print(message)
        df = pd.DataFrame(message)
        #print(df)
        #convert the object to datetime datatype
        df['startDate'] = pd.to_datetime(df['startDate']) 
        df['endDate'] = pd.to_datetime(df['endDate'])
        #Finding the difference between endate and start date of booking
        df['datediff'] = round((df['endDate'] - df['startDate'])/np.timedelta64(1,"D"),0).astype(int)
        #filtering the rows with date difference greater than 1 day
        print(df)
        result_df = df.loc[df['datediff'] > 1]
        print(result_df)
        result_df = result_df.drop(['datediff'], axis=1)
        df1=result_df.to_json()
        s3_client.put_object(Body=df1, Bucket=target_s3, Key=target_file)
        print("File has been uploaded successfully!!!")
    except Exception as e:
        return{
            'Error message' : str(e)
            
        }
    