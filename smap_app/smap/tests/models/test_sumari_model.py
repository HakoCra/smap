from django.test import TestCase

from smap_app.smap.models import Sumari, Tag


class SumariModelTest(TestCase):

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


    def test_search_sumaris_by_tag(self):
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
            },
            {
                "tags": {
                    "sushi"
                },
                "name": "すしろー",
                "message": "回転寿司うまい",
                "lat": 41.773809,
                "lng": 140.726467,

            },
            {
                "tags": {
                    "sushi"
                },
                "name": "すしろー",
                "message": "うまい",
                "lat": 41.773809,
                "lng": 140.726467,

            }
        ]
        self.create_data(data)

        self.assertEqual(len(Sumari.objects.filter(tags__name__in=["meshi"])), 2)
        self.assertEqual(len(Sumari.objects.filter(tags__name__in=["ramen"])), 1)
        self.assertEqual(len(Sumari.objects.filter(tags__name__in=["sushi"])), 3)
        self.assertEqual(len(Sumari.objects.filter(tags__name__in=["ramen", "sushi"])), 4)

    def test_search_with_tags_not_exist(self):
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
            },
            {
                "tags": {
                    "sushi"
                },
                "name": "すしろー",
                "message": "回転寿司うまい",
                "lat": 41.773809,
                "lng": 140.726467,

            },
            {
                "tags": {
                    "sushi"
                },
                "name": "すしろー",
                "message": "うまい",
                "lat": 41.773809,
                "lng": 140.726467,

            }
        ]
        self.create_data(data)

        self.assertEqual(len(Sumari.objects.filter(tags__name__in=["USA"])), 0)
        self.assertEqual(len(Sumari.objects.filter(tags__name__in=["---", "0000"])), 0)

    def test_to_json(self):
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
            }
        ]
        self.create_data(data)
        sumari = Sumari.objects.filter(tags__name__in=["meshi"])[0]
        obj = sumari.to_json()
        self.assertSetEqual(set(obj["tags"]), {"meshi", "ramen"})
        self.assertEqual(obj["name"], "山岡屋")
        self.assertEqual(obj["message"], "山岡屋うまい")
        self.assertEqual(obj["position"]["lat"], 41.773809)
        self.assertEqual(obj["position"]["lng"], 140.726467)

    def test_search_and_get_as_json(self):
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
        json_objs = Sumari.search_with_tags(tags=["meshi"], to_json=True)
        self.assertSetEqual({sumari["name"] for sumari in json_objs}, {"山岡屋", "すしろー"})
        self.assertEqual(len([sumari["id"] for sumari in json_objs]), 2)

    def test_search_with_tags_not_exist_and_get_as_json(self):
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
        json_objs = Sumari.search_with_tags(tags=["tokyo"], to_json=True)
        self.assertEqual(json_objs, [])

    def test_json_include_good(self):
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
        json_obj = Sumari.search_with_tags(tags=["sushi"], to_json=True)[0]
        self.assertEqual(type(json_obj["good"]), int)