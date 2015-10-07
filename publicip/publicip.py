class IPGetStrategy(object):
    def get_ip(self):
        pass


class Ip42pl(IPGetStrategy):
    def get_ip(self):
        from urllib2 import urlopen
        return urlopen('http://ip.42.pl/raw').read()


class JsonIP(IPGetStrategy):
    def get_ip(self):
        from json import load
        from urllib2 import urlopen
        return load(urlopen('http://jsonip.com'))['ip']


class HttpBin(IPGetStrategy):
    def get_ip(self):
        from json import load
        from urllib2 import urlopen
        return load(urlopen('http://httpbin.org/ip'))['origin']


class Ipify(IPGetStrategy):
    def get_ip(self):
        from json import load
        from urllib2 import urlopen
        return load(urlopen('https://api.ipify.org/?format=json'))['ip']


class PublicIP(object):
    '''
    http://stackoverflow.com/a/9481595/2236500
    '''
    strategies = {
        'ip.42.pl': Ip42pl,
        'jsonip.com': JsonIP,
        'httpbin.org': HttpBin,
        'ipify.org': Ipify,
    }

    def __init__(self):
        pass

    def get_ip(self, strategy_name):
        ip_fetcher = strategy_name()
        return ip_fetcher.get_ip()


if __name__ == "__main__":
    ip = PublicIP()
    ip.get_ip(ip.strategies['ip.42.pl'])
