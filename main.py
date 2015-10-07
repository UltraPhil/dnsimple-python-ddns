import shelve

from dnsimple import DNSimple
from publicip import PublicIP

target_domain_name = 'TARGET_DOMAIN'
target_record_name = 'TARGET_RECORD'

# Shelve is used to compare last IP address with current (i.e. detect changes)
last_ip_file = 'last-ip.shelve'
last_ip_key = 'last_ip'

# Shelve is used to store and retrieve last used IP address, for convenience.
shelf = shelve.open(last_ip_file)


def find_record(records_collection, requested_record):
    '''
    Find a specific records in a collection of records retrieve from DNSimple.
    :param records_collection: the records retrieved from DNSimple
    :param requested_record: the request record.
    :return:
    '''
    for rec in records_collection:
        r = rec['record']
        if r['name'] == requested_record:
            return r
    raise Exception('record %s not found.' % requested_record)


def get_current_ip_address():
    '''
    Returns current public IP address.  Uses 2 different providers (although the class is shipped with 4 providers)
    to make a double-check, so a provider is not able to trick you in using an IP address that is not yours.
    Refer to the PublicIP module for available providers.

    :return: Your current IP address in a string.
    '''
    ip = PublicIP()
    ip_provider1 = ip.get_ip(ip.strategies['ip.42.pl'])
    ip_provider2 = ip.get_ip(ip.strategies['httpbin.org'])
    if ip_provider1 != ip_provider2:
        raise Exception("IP error: %s does not match %s" % (ip_provider1, ip_provider2))
    return ip_provider1


def unshelve_previous_ip_address():
    '''
    Retrieve the latest known IP address, using Python's Shelve.
    :return: last known IP address in string, or None if there is no previous IP address.
    '''
    global shelf
    last_ip = shelf[last_ip_key] if last_ip_key in shelf else None
    return last_ip


def shelve_current_ip_address(ip):
    '''
    Stores current IP address in a file using Python's Shelve.
    :param ip: the current IP address to be stored in the file.
    '''
    global shelf
    shelf[last_ip_key] = ip
    shelf.close()


if __name__ == '__main__':
    # Retrieve current IP address
    current_ip = get_current_ip_address()
    previous_ip = unshelve_previous_ip_address()  # retrieve last known IP address

    # handle IP change.
    if current_ip == previous_ip:
        raise Exception("IP did not change since last update.")
    else:
        shelve_current_ip_address(current_ip)  # store current IP address

    # Fetch domain records using DNSimple API
    dns = DNSimple()
    records = dns.records(target_domain_name)
    target_record = find_record(records, target_record_name)
    new_record_data = {'content': current_ip}  # could also contain time to live, etc.

    print "Updating dom %s, rec %s with content: %s" % (target_record['domain_id'], target_record['id'], current_ip)
    dns.update_record(target_record['domain_id'], target_record['id'], new_record_data)
