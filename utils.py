from urllib.parse import urlparse, urljoin

# 检查 url 是否安全
def is_safe_url(target,request):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc