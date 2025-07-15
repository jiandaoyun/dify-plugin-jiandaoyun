from test.getenv import get_apikey
from utils.httpclient import APIRequestTool

# Test for widget tool in Jiandaoyun API
def test_widget():
    httpClient = APIRequestTool(base_url="https://api.jiandaoyun.com/api/",
                                token=get_apikey())
    # data = httpClient.create("v5/app/entry/widget/list", data={
    #     "app_id": "686c7bf22c8e537d9bbc61ff",
    #     "entry_id": "686c7bf64f481d0f0cb1bd8c"
    # })
    # https://api.jiandaoyun.com/api/v5/app/entry/widget/list
    # https://api.jiandaoyun.com/api/v5/app/entry/widget/list
    # print(data)
    data = httpClient.create("v5/app/entry/data/list", data={
        "app_id": "686c7bf22c8e537d9bbc61ff",
        "entry_id": "686c7bf64f481d0f0cb1bd8c",
        "data_id": None,
        "fields": None,
        "filter": {},
        "limit": 1000
    })["data"]
    print("data2",data)

if __name__ == '__main__':
    test_widget()