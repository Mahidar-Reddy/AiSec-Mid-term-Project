#!/usr/bin/env python

import boto3
import numpy as np
import argparse
import ast
from sklearn.preprocessing import RobustScaler



def main():
 
    import json
    import ember
    
    from sklearn.preprocessing import RobustScaler
    rs = RobustScaler()
       
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--featureversion", type=int, default=2, help="EMBER feature version")
    parser.add_argument("binaries", metavar="BINARIES", type=str, nargs="+", help="PE files to classify")
    args = parser.parse_args()
    #opening the downloaded PE file
    testpe = open(args.binaries[0],'rb').read()
    #Feature extractor class of the ember project 
    extract = ember.PEFeatureExtractor() 
    data = extract.feature_vector(testpe) #vectorizing the extracted features
    scaled_data = rs.fit_transform([data])
    Xdata = np.reshape(scaled_data,(1, 2381))
    Xdata= Xdata.tolist()

    client = boto3.client('runtime.sagemaker',
				region_name='us-east-1',
                              	#enter ids from AWS CLI
				aws_access_key_id='ASIAUUVH5KUPA43FG5NS', 
				aws_secret_access_key='EbYC1kpcHb0Aaf14Ak/Q+tPwJJ0MknpRM/KxAgVK',
				aws_session_token='FwoGZXIvYXdzENr//////////wEaDLcMcJu9e0RaBgYJ8SK3AWq4sdHfbn3jN1rw3I4Fl5hGsgS+JTyzmiMAnDYTBztLPzsNDHyFbPCu2DvPjWiB3f2bGToHe4u5ehcnbhGmJ8Bp9qxyYQ16oB07RhjGd44cXrDCMMQZYbjDsT8fGzHrv+/d1cfYJ8xT9p4FK4j1C0PhGn/n4p6WmszrlsSa40UQd3xYkzR+c8bIOiADi/6I0mCDPOR/wAs793oS+d2eLTLsFHbSuigI2n0qTB+gcjZJQL9jugrItiicnqOLBjItO/k7IORqk76Z6dcnq17/Gy0lOaEvHgpTJB2RhXR9BmXpU25xc9kMD9NhyaHG')
    
    response = client.invoke_endpoint(EndpointName='sagemaker-tensorflow-serving-2021-10-15-00-27-55-675' ,Body=json.dumps(Xdata), ContentType='application/json')
    response_body = response['Body']
    out = response_body.read()
    astr = out.decode("UTF-8")
    out = ast.literal_eval(astr)
    print(out)

    #if out[0] >=0.5:
    #    print("Malicious")
    #else:
    #    print("Benign")
		
if __name__ == "__main__":
	main()
