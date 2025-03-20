# coding=utf-8

import requests

from fastapi import APIRouter, Request


router = APIRouter(
    tags=['default'],
    responses={
        404: dict(description='Not found'),
    },
)


@router.get('/')
async def default(request: Request):
    templates = request.app.jinja_templates
    return templates.TemplateResponse(
        'page.html', dict(request=request, main='default/main.js')
    )


@router.get('/ping')
async def ping_pong(request: Request):
    url = 'https://qifu-api.baidubce.com/ip/geo/v1/district'
    params = {
        'ip': request.state.real_ip,
    }
    response = requests.get(url, params=params)
    result = response.json()

    info = {
        'accuracy': result['data']['accuracy'],
        'continent': result['data']['continent'],
        'country': result['data']['country'],
        'province': result['data']['prov'],
        'city': result['data']['city'],
        'district': result['data']['district'],
        'zipcode': result['data']['zipcode'],
        'areacode': result['data']['areacode'],
        'timezone': result['data']['timezone'],
        'lat': result['data']['lat'],
        'lng': result['data']['lng'],
        'radius': result['data']['radius'],
        'owner': result['data']['owner'],
        'isp': result['data']['isp'],
    }

    return dict(
        ip=request.state.real_ip,
        agent=request.headers.get('user-agent'),
        **info
    )
