from django.utils.deprecation import MiddlewareMixin


class SetRemoteAddrFromForwardedFor(MiddlewareMixin):
    """
    代理服务器也支持获取用户IP
    """
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError as err:
            pass
        else:
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip
