# Created by Thibault and Javier
# Requierments: pip3 install "fastapi[all]" pyasn
# run with uvicorn fastAPI:app --reload

#todo: ad parameter for non-local queries saying I know it might leak data and trigger iocs
#todo: add tranco list top 10k
import asyncio
import ipaddress
import operator
import socket
from functools import reduce
import requests

from fastapi import FastAPI
import pyasn
from typing import Optional

app = FastAPI()
####################################################################
# INIT VARS
###################################################################
VT_API_KEY = ""
####################################################################
# INIT OBJECTS
####################################################################
asndb = pyasn.pyasn('/home/azo/.asn_data/asn_numbers.ipasn', as_names_file='/home/azo/.asn_data/asnames.json',)
tor_ips = set()
for line in open("/home/azo/.asn_data/exit-addresses"):
    if "ExitAddress" in line:
        _, ip, _ = line.split(" ", 2)
        tor_ips.add(ip)
vt_session = requests.Session()
vt_session.headers = {'X-Apikey': VT_API_KEY}
###################################################################

@app.get("/fast")
async def get_all_fast(ip: str ):
    if ipaddress.ip_address(ip).is_private:
        return {"ip": ip, "type": ipaddress.ip_address(ip).is_private}
    return reduce(operator.or_, await asyncio.gather(get_is_private(ip), get_is_tor_exit(ip), get_asn(ip)))

@app.get("/fast/get_as")
async def get_asn(ip: str, as_networks: Optional[bool]=False ):
    asn_number, network = asndb.lookup(ip)
    if as_networks:
        return {"ip": ip, "asn_number":asn_number, "network":network, "as name": asndb.get_as_name(asn_number), "as_networks" : asndb.get_as_prefixes(asn_number)}
    return {"ip": ip, "asn_number":asn_number, "network":network, "as name": asndb.get_as_name(asn_number)}

@app.get("/fast/get_ip_type")
async def get_is_private(ip: str):
    return {"ip": ip, "type": ipaddress.ip_address(ip).is_private}

@app.get("/fast/get_is_tor_exit")
async def get_is_tor_exit(ip: str ):
    return {"ip": ip, "tor_exit_node": (ip in tor_ips)}

@app.get("/slow/reverse_dns")
async def get_reverse_dns(ip: str ):
    return {"ip": ip, "dns": socket.gethostbyaddr(ip)[0]}

@app.get("/slow/sha256/vt")
async def get_vt_results(hash:str):
    url = "https://www.virustotal.com/api/v3/monitor_partner/hashes/"+hash+"/items"
    return {hash: vt_session.get(url).json()}

@app.get("/")
async def root():
    return {"message": "go to /docs and RTFM"}



# #download asn_data:
# pyasn_util_download.py --latestv46
# pyasn_util_convert.py --single <Downloaded RIB File> <ipasn_db_file_name>
# pyasn_util_asnames.py > asname.json
# wget https://check.torproject.org/exit-addresses
