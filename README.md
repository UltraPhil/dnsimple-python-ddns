# dnsimple-python-ddns
Python script to update a record on DNSIMPLE when your public IP changes.  Kinda emulates a DDNS (i.e. no-ip)

## known limitation
You currently cannot use a _domain API token_, you need to use your _account API token_

### Usage
- enter your email address and account API token in the .dnsimple file.
- Edit the main.py script and replace dummy values with your target domain name and domain record to be updated.
- Run the script twice: first time should update the target record, second time should yield an exception (ip didn't change)