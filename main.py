from sanic import Sanic
from sanic.response import json

app = Sanic("theCommonAndDataService")


# check status

@app.get("/status")
def get_status(request):
    return json({"server": "ON"})



# add views
from classviews.geography_views import CountryView

app.add_route(CountryView.as_view(), "/geography/country/")








if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10001, dev=True)
