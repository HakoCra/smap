from django.test import TestCase, Client
from smap_app.smap.models import Sumari, Tag


class TagViewTest(TestCase):

    def create_data(self, data):
        for sumari in data:
            message = sumari["message"]
            name = sumari["name"]
            lat = sumari["lat"]
            lng = sumari["lng"]
            new_sumari = Sumari(name=name, message=message, lat=lat, lng=lng)
            new_sumari.save()
            for tagname in sumari["tags"]:
                tag = Tag.get_or_create(tagname)
                new_sumari.tags.add(tag)
                new_sumari.save()

    def test_get_all_tag_view(self):
        data = [
            {
                "tags": {
                    "meshi",
                    "ramen"
                },
                "name": "山岡屋",
                "message": "山岡屋うまい",
                "lat": 41.773809,
                "lng": 140.726467,
            },
            {
                "tags": {
                    "meshi",
                    "sushi"
                },
                "name": "すしろー",
                "message": "すしうまい",
                "lat": 41.773809,
                "lng": 140.726467,
            }
        ]
        self.create_data(data)
        client = Client()
        response = client.get('/tag')
        self.assertSetEqual({sumari for sumari in response.json()}, {"meshi", "ramen", "sushi"})
