def get_ip():
    """ 获取公网ip

    Returns:
        str: 公网ip
    """
    import requests
    response = requests.get('https://ipinfo.io/ip')
    if response.status_code == 200:
        return response.text
    else:
        return "0.0.0.0"
    
def get_user_id(request):
    """ 获取会话用户id

    Returns:
        str: 公网ip
    """
    current_user = request.state.current_user
    userId = current_user["userId"]
    return userId

if __name__ == '__main__':
    print(get_ip())
    
    
    