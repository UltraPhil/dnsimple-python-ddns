try:
    from publicip import PublicIP, IPGetStrategy, Ip42pl, Ipify, HttpBin, JsonIP
except ImportError:
    from publicip.publicip import PublicIP, IPGetStrategy, Ip42pl, Ipify, HttpBin, JsonIP
