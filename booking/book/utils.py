import requests

def get_location_from_ip(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json')
    data = response.json()
    return data['region'], data['country']

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
