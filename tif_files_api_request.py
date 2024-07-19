from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import tarfile
import io
import os
import shutil


# folder path for tiff images
f_path = '/Users/chesterfrancisco/Desktop/Copernicus_OAuth'

#  folder path to where the SAFE folder structure will be created
base_safe_path = '/Users/chesterfrancisco/Desktop/Copernicus_OAuth'

# Your client credentials
client_id = 'sh-0fd33afc-662c-411f-a51a-65bd2d06dba3'
client_secret = 'RzvGQJm9Yw0EdjLttLp0WCnlRgFNVicA'

"""
The next two variables  values can be found in the Copernicus API Dashboard
1. create an account and sign into Dashboard
2. create an OAuth client 
3. copy client and oauth key into this file
"""
# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)


# token url from copernics API 
url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'

# Get token for the session
token = oauth.fetch_token(token_url= url,client_secret=client_secret, include_client_id=True)

# All requests using this session will have an access token automatically added
resp = oauth.get("https://sh.dataspace.copernicus.eu/configuration/v1/wms/instances")

# you can print the response to see sign in data if needed
#print(resp.content)

"""
an evalscript defines how the satellite data shall be processed by Sentinel Hub and what values the service shall return
It is required for any process or request made to the Copernicus API

You can modify the evalscript to find specific values in the return 
"""

evalscript = """
//VERSION=3
function setup() {
  return {
    input: [
      {
        bands: [
          "B02",
          "B03",
          "B04",
          "AOT",
          "SCL",
          "SNW",
          "CLD",
          "sunAzimuthAngles",
          "sunZenithAngles",
          "viewAzimuthMean",
          "viewZenithMean",
        ],
      },
    ],
    output: [
      { id: "TrueColor", bands: 3, sampleType: SampleType.FLOAT32 },
      { id: "AOT", bands: 1, sampleType: SampleType.UINT16 },
      { id: "SCL", bands: 1, sampleType: SampleType.UINT8 },
      { id: "SNW", bands: 1, sampleType: SampleType.UINT8 },
      { id: "CLD", bands: 1, sampleType: SampleType.UINT8 },
      { id: "SAA", bands: 1, sampleType: SampleType.FLOAT32 },
      { id: "SZA", bands: 1, sampleType: SampleType.FLOAT32 },
      { id: "VAM", bands: 1, sampleType: SampleType.FLOAT32 },
      { id: "VZM", bands: 1, sampleType: SampleType.FLOAT32 },
    ],
  }
}

function evaluatePixel(sample) {
  var truecolor = [sample.B04, sample.B03, sample.B02]
  var aot = [sample.AOT]
  var scl = [sample.SCL]
  var snw = [sample.SNW]
  var cld = [sample.CLD]
  var saa = [sample.sunAzimuthAngles]
  var sza = [sample.sunZenithAngles]
  var vam = [sample.viewAzimuthMean]
  var vzm = [sample.viewZenithMean]

  return {
    TrueColor: truecolor,
    AOT: aot,
    SCL: scl,
    SNW: snw,
    CLD: cld,
    SAA: saa,
    SZA: sza,
    VAM: vam,
    VZM: vzm,
  }
}
"""


#This is the request for all of the tiff files that will be returned from the Copernicus API
request = {
    "input": {
        "bounds": {
            "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            "bbox": [
                13.822174072265625,
                45.85080395917834,
                14.55963134765625,
                46.29191774991382,
            ],
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2022-10-01T00:00:00Z",
                        "to": "2022-10-31T00:00:00Z",
                    }
                },
            }
        ],
    },
    "output": {
        "width": 512,
        "height": 512,
        "responses": [
            {
                "identifier": "TrueColor",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "AOT",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "SCL",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "SNW",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "CLD",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "SAA",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "SZA",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "VAM",
                "format": {"type": "image/tiff"},
            },
            {
                "identifier": "VZM",
                "format": {"type": "image/tiff"},
            },
        ],
    },
    "evalscript": evalscript,
}

# This is the process api url needed for the oauth post request
url = "https://sh.dataspace.copernicus.eu/api/v1/process"

# posting request and headers whihc retrieves the tiff files
response = oauth.post(url, json=request, headers={"Accept": "application/tar"})

# content returned will form of bytes
print(response.content)

"""
The next few lines of code will extract the tar file and display the tiff image
"""
# Assume raw_tar_data contains the raw tar data as bytes
raw_tar_data = response.content # Replace with your actual raw tar data

# # Use io.BytesIO to handle the raw tar data in memory
tar_data = io.BytesIO(raw_tar_data)

# Open the tar file for writing
with open('output.tar', 'wb') as output_file:
    output_file.write(tar_data.getvalue())

# Alternatively, you can directly work with tarfile module if you need to extract files
# with tarfile.open(fileobj=tar_data, mode='r:*') as tar:
#     tar.extractall(path='/Users/chesterfrancisco/Desktop/Copernicus_OAuth')  # Specify your output directory

# # Confirm the file was created successfully
print("Tar file created successfully.")

# choose any tif image you'd like to be displayed
image = Image.open('CLD.tif')
image.show()

"""
This creates a SAFE folder structure necessary for the format of QGIS
"""

# Step 1: Define paths
base_safe_path = f'{base_safe_path}/copernicus'
granule_path = os.path.join(base_safe_path, 'GRANULE', 'L1C_T32TQM_A011214_20210525T104625')
img_data_path = os.path.join(granule_path, 'IMG_DATA')
aux_data_path = os.path.join(granule_path, 'AUX_DATA')
qi_data_path = os.path.join(granule_path, 'QI_DATA')
datastrip_path = os.path.join(base_safe_path, 'DATASTRIP')

# Step 2: Create directories
os.makedirs(img_data_path, exist_ok=True)
os.makedirs(aux_data_path, exist_ok=True)
os.makedirs(qi_data_path, exist_ok=True)
os.makedirs(datastrip_path, exist_ok=True)

# Update with actual paths of tif file locations
tiff_files = [f'{f_path}/VZM.tif', f'{f_path}/CLD.tif', f'{f_path}/SAA.tif', f'{f_path}/SCL.tif', f'{f_path}/SNW.tif',
              f'{f_path}/SZA.tif', f'{f_path}/TrueColor.tif', f'{f_path}/VAM.tif', f'{f_path}/AOT.tif']  

# Step 3: Copy TIFF files to IMG_DATA
for tiff in tiff_files:
    shutil.copy(tiff, img_data_path)


# metadata_content can be updated with your own metadata content
# Step 4: Create metadata files
metadata_content = """<?xml version="1.0" encoding="UTF-8"?>
<metadata>
    <name>Example</name>
    <description>This is an example metadata file.</description>
</metadata>
"""

"""
creates and joins the folders created above into the necessary SAFE folder structure
The next three files are very important to a SAFE structure

- manifest.safe is the metadata file that is required for the SAFE folder structure
- MTD_TL.xml is the metadata file for the granule
- DS_MTD.xml is the metadata file for the datastrip
"""
with open(os.path.join(base_safe_path, 'manifest.safe'), 'w') as f:
    f.write(metadata_content)

with open(os.path.join(granule_path, 'MTD_TL.xml'), 'w') as f:
    f.write(metadata_content)

with open(os.path.join(datastrip_path, 'DS_MTD.xml'), 'w') as f:
    f.write(metadata_content)

# Step 5: Compress the SAFE folder into a .tar.gz archive
shutil.make_archive('SAFE_FOLDER', 'gztar', base_safe_path)




