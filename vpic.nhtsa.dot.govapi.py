import pandas as pd
import requests

#### opening the csv file that contains sets of nhtsa codes and saving to 'df' variable
df = pd.read_csv("002_AUTO_VIN_test.csv")
# print(df.head(100))

### extracting only the column with 50 codes per row
Auto_Vin_sets = df["Auto_Vin_MERGE"]

# going for each row of sets
for set_ in Auto_Vin_sets:
    print(f"Set to download: {set_}")

    url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/"

    payload = f"DATA={set_}&format=JSON"
    headers = {
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "upgrade-insecure-requests": "1",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "cache-control": "no-cache",
        "postman-token": "13d1b9fc-5bf4-43be-713c-fdacb81ff18d",
    }
    try:
        ### making requests with Post method, and giving data and headers parameters
        response = requests.request("POST", url, data=payload, headers=headers)
        # print(response.text)

        ### saving content to JSON format, since data are in JSON
        content = response.json()

        # getting only data within 'Results' key parameter
        results = content["Results"]
        # print(results)

        ### inserting data to pandas dataframe
        df = pd.DataFrame(results)

        print(df.head())

        ### saving/converting dataframe data to CSV format.
        df.to_csv("output.csv", index=False, mode="a")
    except Exception as e:
        print(e)

### removing duplicate header rows...
df2 = pd.read_csv("output.csv")
print(f"Rows, Columns: {df2.shape}")
df3 = df2.drop(df2[df2["ABS"] == "ABS"].index)
df3.to_csv("output2.csv", index=False)
print(f"Rows, Columns: {df3.shape} after removing dups.")
