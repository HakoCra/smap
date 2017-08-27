import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Tag, Sumari


def home(request):
    return render(request, 'smap/home.html')


@csrf_exempt
def smari(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        try:
            name = data["name"]
            message = data["message"]
            lat = data["position"]["lat"]
            lng = data["position"]["lng"]
            tags = data["tags"]
        except KeyError as e:
            return JsonResponse({"status": str(e)})

        try:
            new_sumari = Sumari(name=name, message=message, lat=lat, lng=lng)
            new_sumari.save()
            for tagname in tags.split(','):
                tag = Tag.get_or_create(tagname)
                new_sumari.tags.add(tag)
            new_sumari.save()

        except Exception as e:
            return JsonResponse({"status": str(e)})
        return JsonResponse({"status": "ok"})

    elif request.method == 'GET':
        tags = request.GET.get('tags', None)
        if not tags:
            json_objs = [sumari.to_json() for sumari in Sumari.objects.all()]
            return JsonResponse(json_objs, safe=False)

        tags = tags.split(",")
        sumari_list = Sumari.search_with_tags(tags=tags, to_json=True)
        return JsonResponse(sumari_list, safe=False)


@csrf_exempt
def update_sumari(request, id):
    if request.method == "GET":
        sumari = Sumari.objects.get(pk=id)
        return JsonResponse(sumari.to_json())

    elif request.method == "PUT":
        sumari = Sumari.objects.get(pk=id)
        data = json.loads(request.body.decode("utf-8"))
        for key in data.keys():
            if key == "tags":
                sumari.tags.clear()
                if ',' in data[key]:
                    sumari.tags.add([Tag.get_or_create(tag) for tag in data[key].split(',')])
                else:
                    sumari.tags.add(Tag.get_or_create(data[key]))
            elif key == "name":
                sumari.name = data[key]
            elif key == "message":
                sumari.message = data[key]
        sumari.save()
        return JsonResponse(sumari.to_json())


@csrf_exempt
def good(request, id):
    if request.method == "POST":
        sumari = Sumari.objects.get(pk=id)
        sumari.good += 1
        sumari.save()
        return JsonResponse(sumari.to_json(), safe=False)


def tag(request):
    if request.method == "GET":
        tag_list = [tag.name for tag in Tag.objects.all()]
        return JsonResponse(tag_list, safe=False)


def hakodate_mock(reqest):
    return JsonResponse({"": ""})
