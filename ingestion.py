import requests
import pandas as pd
import boto3
import io

# 1. Collect data from the API
# In the tutorial, dummy API data is collected [1]
api_url = "https://jsonplaceholder.typicode.com/posts" 
response = requests.get(api_url)
data = response.json() # Convert API response to JSON [1]
print(data)


# 2. Process data using Pandas
# Convert the JSON data into a DataFrame [2]
df = pd.DataFrame(data)

# 3. Prepare data for S3 (using a String Buffer)
# Instead of saving a local file, we use io.StringIO as an interface [3], [2]
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False) # Convert DataFrame to CSV format [2], [4]

# 4. Upload to AWS S3
# Initialize the Boto3 S3 client to connect with AWS services [5], [2]
s3_client = boto3.client('s3')

bucket_name = 'landing-zone-api-data' # Mentioned as 'Landing Zone' in the source [4]
file_path = 'landing-zone/post_data.csv'

# Upload the CSV data from the buffer to the specified S3 bucket [6]
s3_client.put_object(
    Bucket=bucket_name,
    Key=file_path,
    Body=csv_buffer.getvalue() # Getting the string value from the buffer [6]
)

print("File successfully uploaded to S3!")