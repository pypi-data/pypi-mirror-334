import requests

def api_request(api_key, method, **kwargs):
    url = 'https://modkey.space/api/v1/action'
    data = {
        'method': method,
        'api_key': api_key,
    }
    data.update(kwargs)

    try:
        response = requests.post(url, data=data)
        if response.ok:
            result = response.json()
            print(result)  # Выводим полный ответ для отладки
            if result.get('status'):
                return True, result.get('data', {})  # Гарантируем, что data — словарь
            else:
                return False, result.get('message', 'Error without message')
        else:
            print(response.text)
            return False, 'Server error'
    except requests.RequestException as e:
        print(e)
        return False, f'Request failed: {str(e)}'


def create_key(api_key, days, devices, key_type):
    status, data = api_request(
        api_key=api_key,
        method='create-key',
        days=days,
        devices=devices,
        type=key_type
    )
    if status:
        return data.get("key")  
    return None


def edit_key_status(api_key, key, new_status):
    status, data = api_request(
        api_key=api_key,
        method='edit-key-status',
        key=key,
        status_type=new_status  # Изменил type → status_type
    )
    if status:
        return data.get("new_status")
    return None


def edit_key_max_devices(api_key, key, new_max_devices):
    status, data = api_request(
        api_key=api_key,
        method='edit-key-max-devices',
        key=key,
        new_max_devices=new_max_devices
    )
    if status:
        return data.get("new_max_devices")
    return None


def edit_user_key(api_key, key, new_user_key):
    status, data = api_request(
        api_key=api_key,
        method='edit-user-key',
        key=key,
        new_user_key=new_user_key
    )
    if status:
        return data.get("new_user_key")
    return None
