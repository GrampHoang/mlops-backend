import pymongo

import argparse

# py InsertDeployedModel.py --modelListName model1,model2,model3 --versionList 123,456,126 --image image123

parser = argparse.ArgumentParser()

parser.add_argument("--modelListName", help="Add model name list, ex: model1,model2,model3")
parser.add_argument("--versionList", help="Add version list, ex: 123,456,126")
parser.add_argument("--image", help="Add image name")
args = parser.parse_args()

client = pymongo.MongoClient(
    "mongodb+srv://haicauancarem:tiachop1@cluster0.dd88nyj.mongodb.net/?retryWrites=true&w=majority", 
    connectTimeoutMS=300000)
mydb = client["MLOpsData"]
mycol = mydb["image"]

modelListName = args.modelListName
versionList = args.versionList
image = args.image

x = mycol.insert_one({"image": image, "versionList": versionList, "modelListName": modelListName})


