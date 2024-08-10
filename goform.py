import base64
import requests
import urllib.parse
import socket
from util import *

# this is the base class for inetracting with the HTTP goform functionality
class GoFormSetHttp:
    def __init__(self, id, **params):
        """
        Initializes a GoFormHttp object with an ID and a dictionary of parameters.

        :param id: The ID of the GoFormHttp object.
        :param params: Arbitrary keyword arguments representing the parameters.
        """
        self.id = id
        self.params = params

    def get_id(self):
        """
        Returns the ID of the GoFormHttp object.
        
        :return: The ID of the object.
        """
        return self.id

    def get_params(self):
        """
        Returns the parameters dictionary.
        
        :return: The parameters dictionary.
        """
        return self.params

    def set_param(self, key, value):
        """
        Sets a parameter in the parameters dictionary.
        
        :param key: The key of the parameter.
        :param value: The value of the parameter.
        """
        self.params[key] = value

    def get_param(self, key):
        """
        Gets a parameter value from the parameters dictionary by key.
        
        :param key: The key of the parameter.
        :return: The value of the parameter if key exists, else None.
        """
        return self.params.get(key)

    def remove_param(self, key):
        """
        Removes a parameter from the parameters dictionary by key.
        
        :param key: The key of the parameter to remove.
        """
        if key in self.params:
            del self.params[key]

    def __repr__(self):
        """
        Returns a string representation of the GoFormHttp object.
        
        :return: A string representation of the object.
        """
        return f"GoFormHttp(id={self.id}, params={self.params})"

    def __str__(self):
        """
        Returns a string with the goformId and all parameters.
        
        :return: A string with the goformId and all parameters.
        """
        params_str = "&".join(f"{key}={value}" for key, value in self.params.items())
        return f"goformId={self.id}&{params_str}"


"""
- Sets the "Language" paramater in the config (en/po/cn)
"""
class GOFORM_SET_WEB_LANGUAGE(GoFormSetHttp):
    def __init__(self, language):
        # Create and populate the params dictionary
        params = {
            "Language": language
        }

        super().__init__("SET_WEB_LANGUAGE", **params)


"""
- Sets the 'device mode': 0-user, 1-debug, 2-factory, 3-amt
"""
class GOFORM_SET_DEVICE_MODE(GoFormSetHttp):
    def __init__(self, debug_enable):
        # Create and populate the params dictionary
        params = {
            "debug_enable": debug_enable
        }

        super().__init__("SET_DEVICE_MODE", **params)


"""
- Performs login to the web UI, username is optional
- Sets the "user_ip_addr" to the IP address
- Sets the "loginfo" to "ok"
- Resets "psw_fail_num_str" to 5
- Sets save_login to 0/1
"""
class GOFORM_LOGIN(GoFormSetHttp):
    def __init__(self, password, save_login="", username=""):
        # Create and populate the params dictionary with username and password
        if username != "":
            params = {"username": username, "save_login": save_login, "password": base64.b64encode(password.encode()).decode()}
        else:
            params = {"save_login": save_login, "password": base64.b64encode(password.encode()).decode()}
        super().__init__("LOGIN", **params)


"""
- Logs out of the web UI
- Clears user_ip_addr in config
- Clears loginfo in config
"""
class GOFORM_LOGOUT(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary with username and password
        params = {}
        super().__init__("LOGOUT", **params)


"""
- Sets the "admin_Password" in the config to new password if the old password is correct
"""
class GOFORM_CHANGE_PASSWORD(GoFormSetHttp):
    def __init__(self, old_password, new_password):
        # Create and populate the params dictionary with username and password
        params = {
            "oldPassword": base64.b64encode(old_password.encode()).decode(), 
            "newPassword": base64.b64encode(new_password.encode()).decode()
        }
        super().__init__("CHANGE_PASSWORD", **params)


"""
- If oldPassword correct, sets "admin_Password" in cfg to newPassword, and "admin_user" in cfg to newUsername
"""
class GOFORM_CHANGE_ACCOUNT(GoFormSetHttp):
    def __init__(self, old_password, new_username, new_password):
        # Create and populate the params dictionary with username and password
        params = {
            "oldPassword": base64.b64encode(old_password.encode()).decode(), 
            "newPassword": base64.b64encode(new_password.encode()).decode(),
            "newUsername": base64.b64encode(new_username.encode()).decode()
        }
        super().__init__("CHANGE_ACCOUNT", **params)



## TODO NEEDS MORE ANALYSIS ITS MASSIVE
class GOFORM_QUICK_SETUP_EX(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary with username and password
        params = {
        }
        super().__init__("QUICK_SETUP_EX", **params)


"""
- Restore device to factory settings
"""
class GOFORM_RESTORE_FACTORY_SETTINGS(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary with username and password
        params = {}
        super().__init__("RESTORE_FACTORY_SETTINGS", **params)


"""
- Reboot the device
"""
class GOFORM_REBOOT_DEVICE(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("REBOOT_DEVICE", **params)

"""
- Turn off the device
"""
class GOFORM_TURN_OFF_DEVICE(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("TURN_OFF_DEVICE", **params)


"""
- Sets "mgmt_quicken_power_on" cfg value to 0/1
"""
class GOFORM_MGMT_CONTROL_POWER_ON_SPEED(GoFormSetHttp):
    def __init__(self, mgmt_quicken_power_on):
        # Create and populate the params dictionary
        params = {
            "mgmt_quicken_power_on" : mgmt_quicken_power_on
        }

        super().__init__("MGMT_CONTROL_POWER_ON_SPEED", **params)


"""
- Sets arbitrary config value, external_nv_name in config becomes external_nv_value
"""
class GOFORM_SET_EXTERNAL_NV(GoFormSetHttp):
    def __init__(self, external_nv_name, external_nv_value):
        # Create and populate the params dictionary
        params = {
            "external_nv_name": external_nv_name,
            "external_nv_value": external_nv_value
        }

        super().__init__("SET_EXTERNAL_NV", **params)


## TODO LOTS OF PARAMETERS
class GOFORM_SNTP(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("SNTP", **params)


"""
- Fetches smtp info, runtime, timestr, localtime
"""
class GOFORM_SNTP_Getdatastatic(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("SNTP_Getdatastatic", **params)

"""
- Runs system command for log stuff (log.sh script)
"""
class GOFORM_SYSLOG(GoFormSetHttp):
    def __init__(self, syslog_mode, syslog_flag):
        # Create and populate the params dictionary
        params = {
            "syslog_mode": syslog_mode,
            "syslog_flag": syslog_flag
        }

        super().__init__("SYSLOG", **params)


"""
- Sets the IMEI using AT+MODIMEI
- Seems to hit IPC (0x100a) in zte_mainctrl (MSG_CMD_WEB_IMEI_REQ), address 0xf250, calls "get_modem_info" with built AT command, which sends request to modem with 'send_req_and_wait' in libatutils.so
- ! AT command injection
"""
class GOFORM_CHANGE_IMEI(GoFormSetHttp):
    def __init__(self, imei):
        # Create and populate the params dictionary
        params = {
            "imei": imei
        }

        super().__init__("CHANGE_IMEI", **params)


"""
- ! Trivial strcat stack overflow here when parsing mac address
- ! AT command injection
- Builds AT command, sends to zte_mainctrl via IPC (0x100b), hits MSG_CMD_WEB_MAC_REQ handler
- Does same thing as GOFORM_CHANGE_IMEI and sends command to modem
"""
class GOFORM_CHANGE_MAC(GoFormSetHttp):
    def __init__(self, mac):
        # Create and populate the params dictionary
        params = {
            "mac": mac
        }

        super().__init__("CHANGE_MAC", **params)


"""
- Reads some stuff from config, checks against what we provide
- Writes stuff to config, and sends IPC (0x1524) to at_ctl (0x1e4d8)
- This loads "current_subrat_tmp", "str_num_rplmn_tmp", and "current_rat_tmp" from cfg
- Calls sub function which might do an AT command, decompilation might be broken here
- ? Maybe AT command injection
"""
class GOFORM_SET_NETWORK(GoFormSetHttp):
    def __init__(self, network_number, rat, subrat):
        # Create and populate the params dictionary
        params = {
            "NetworkNumber": network_number,
            "Rat": rat,
            "nSubrat": subrat
        }

        super().__init__("SET_NETWORK", **params)


"""
- Sets "dial_mode" and "roam_setting_option" to the config
- Does a software interrupt (0xdcf7ee), unsure if important
"""
class GOFORM_SET_CONNECTION_MODE(GoFormSetHttp):
    def __init__(self, connection_mode, roam_setting_option):
        # Create and populate the params dictionary
        params = {
            "ConnectionMode": connection_mode,
            "roam_setting_option": roam_setting_option
        }

        super().__init__("SET_CONNECTION_MODE", **params)


"""
NOT FINISHED
- Causes network connect or something
- Sends IPC to 0x159a (DUNNO WHERE THIS GOES)
"""
class GOFORM_CONNECT_NETWORK(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("CONNECT_NETWORK", **params)


"""
NOT FINISHED
- Causes network disconnect or something
- Sends IPC to 0x159c (DUNNO WHERE THIS GOES)
"""
class GOFORM_DISCONNECT_NETWORK(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("DISCONNECT_NETWORK", **params)


"""
- Reads some config stuff, writes some config stuff
- Sends IPC message to at_ctl (0x1523) calls function (0x1e340)
- Doesn't seem very interesting
"""
class GOFORM_SET_BEARER_PREFERENCE(GoFormSetHttp):
    def __init__(self, bearer_preference, pre_mode):
        # Create and populate the params dictionary
        params = {
            "BearerPreference": bearer_preference,
            "pre_mode": pre_mode
        }

        super().__init__("SET_BEARER_PREFERENCE", **params)

"""
- Similar to above, but sets "net_select_mode" to "manual_select"
"""
class GOFORM_SCAN_NETWORK(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("SCAN_NETWORK", **params)


"""
NOT FINISHED
- Sends IPC to 0x1542, I have no idea where this is
"""
class GOFORM_UNLOCK_NETWORK(GoFormSetHttp):
    def __init__(self, unlock_network_code):
        # Create and populate the params dictionary
        params = {
            "unlock_network_code": unlock_network_code
        }

        super().__init__("UNLOCK_NETWORK", **params)


"""
- Sets "actionLte", "uarfcnlte" and "cellParaIdlte" to what we give
- Sends 0x1527 IPC to at_ctl, which constructs an AT+ZLTELC AT command (which I assume sends to modem? only integers so boring)
"""
class GOFORM_LOCK_FREQUENCY(GoFormSetHttp):
    def __init__(self, action_lte, uarfcn_lte, cell_para_id_lte):
        # Create and populate the params dictionary
        params = {
            "actionlte": action_lte,
            "uarfcnlte": uarfcn_lte,
            "callParaIdlte": cell_para_id_lte
        }

        super().__init__("LOCK_FREQUENCY", **params)


## TODO HAS SUBHANDLERS
class GOFORM_APN_PROC_EX(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("APN_PROC_EX", **params)


class GOFORM_ENTER_PIN(GoFormSetHttp):
    def __init__(self, pin_number):
        # Create and populate the params dictionary
        params = {
            "PinNumber": pin_number
        }

        super().__init__("ENTER_PIN", **params)


class GOFORM_DISABLE_PIN(GoFormSetHttp):
    def __init__(self, old_pin_number):
        # Create and populate the params dictionary
        params = {
            "OldPinNumber": old_pin_number
        }

        super().__init__("DISABLE_PIN", **params)


class GOFORM_ENABLE_PIN(GoFormSetHttp):
    def __init__(self, old_pin_number, new_pin_number):
        # Create and populate the params dictionary
        params = {
            "OldPinNumber": old_pin_number,
            "NewPinNumber": new_pin_number
        }

        super().__init__("ENABLE_PIN", **params)

class GOFORM_ENTER_PUK(GoFormSetHttp):
    def __init__(self, puk_number, pin_number):
        # Create and populate the params dictionary
        params = {
            "PUKNumber": puk_number,
            "PinNumber": pin_number
        }

        super().__init__("ENTER_PUK", **params)


class GOFORM_AUTO_PIN(GoFormSetHttp):
    def __init__(self, auto_sim_pin, auto_sim_pin_code):
        # Create and populate the params dictionary
        params = {
            "auto_simpin": auto_sim_pin,
            "auto_simpin_code": auto_sim_pin_code
        }

        super().__init__("AUTO_PIN", **params)


## TODO HAS SUBHANDLERS
class GOFORM_DATA_LIMIT_SETTING(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("DATA_LIMIT_SETTING", **params)

## TODO HAS SUBHANDLERS
class GOFORM_FLOW_CALIBRATION_MANUAL(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("FLOW_CALIBRATION_MANUAL", **params)


class GOFORM_RESET_DATA_COUNTER(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("RESET_DATA_COUNTER", **params)


## TODO HAS SUBHANDLERS
class GOFORM_USSD_PROCESS(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("USSD_PROCESS", **params)


## TODO HAS SUBHANDLERS
class GOFORM_SET_WIFI_INFO(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("SET_WIFI_INFO", **params)


## TODO HAS SUBHANDLERS
class GOFORM_WIFI_MAC_FILTER(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("WIFI_MAC_FILTER", **params)


## TODO HAS SUBHANDLERS
class GOFORM_WIFI_WPS_SET(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("WIFI_WPS_SET", **params)


class GOFORM_SET_WIFI_SSID1_SETTINGS(GoFormSetHttp):
    def __init__(self, ssid, broadcast_ssid_enabled, max_access_num, security_mode, cipher, no_forwarding, show_qrcode_flag, security_shared_mode, passphrase):
        # Encode passphrase to Base64
        encoded_passphrase = base64.b64encode(passphrase.encode()).decode()

        # Create and populate the params dictionary
        params = {
            "ssid": ssid,
            "broadcastSsidEnabled": broadcast_ssid_enabled,
            "MAX_Access_num": max_access_num,
            "security_mode": security_mode,
            "cipher": cipher,
            "NoForwarding": no_forwarding,
            "show_qrcode_flag": show_qrcode_flag,
            "security_shared_mode": security_shared_mode,
            "passphrase": encoded_passphrase
        }

        super().__init__("SET_WIFI_SSID1_SETTINGS", **params)


class GOFORM_SET_WIFI_SSID2_SETTINGS(GoFormSetHttp):
    def __init__(self, m_ssid, m_hide_ssid, m_no_forwarding, m_max_access_num, m_show_qrcode_flag):
        # Encode passphrase to Base64
        encoded_passphrase = base64.b64encode(passphrase.encode()).decode()

        # Create and populate the params dictionary
        params = {
            "m_SSID": m_ssid,
            "m_HideSSID": m_hide_ssid,
            "m_NoForwarding": m_no_forwarding,
            "m_MAX_Access_num": m_max_access_num,
            "m_show_qrcode_flag": m_show_qrcode_flag
        }

        super().__init__("SET_WIFI_SSID2_SETTINGS", **params)


class GOFORM_SET_WIFI_SLEEP_INFO(GoFormSetHttp):
    def __init__(self, sys_idle_time_to_sleep):
        # Create and populate the params dictionary
        params = {
            "sysIdleTimeToSleep": sys_idle_time_to_sleep
        }

        super().__init__("SET_WIFI_SLEEP_INFO", **params)


class GOFORM_SAVE_TSW(GoFormSetHttp):
    def __init__(self, open_enable, close_enable, open_time, close_time):
        # Create and populate the params dictionary
        params = {
            "openEnable": open_enable,
            "closeEnable": close_enable,
            "openTime": open_time,
            "closeTime": close_time
        }

        super().__init__("SAVE_TSW", **params)


"""
- Sets some config stuff
- Calls IPC 0x400c which is in wifi_manager, writes a boring file
"""
class GOFORM_SET_WIFI_COVERAGE(GoFormSetHttp):
    def __init__(self, wifi_sta_connection):
        # Create and populate the params dictionary
        params = {
            "wifi_coverage": wifi_coverage
        }

        super().__init__("SET_WIFI_COVERAGE", **params)


class GOFORM_WIFI_STA_CONTROL(GoFormSetHttp):
    def __init__(self, wifi_sta_connection):
        # Create and populate the params dictionary
        params = {
            "wifi_sta_connection": wifi_sta_connection
        }

        super().__init__("WIFI_STA_CONTROL", **params)

## TODO IS COMPLICATED
class GOFORM_WIFI_SPOT_PROFILE_UPDATE(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("WIFI_SPOT_PROFILE_UPDATE", **params)


class GOFORM_WLAN_SET_STA_CON(GoFormSetHttp):
    def __init__(self, ex_ssid1, ex_authmode, ex_encrypt_type, ex_default_key_id, ex_wep_key, ex_wpapsk1, ex_wifi_profile, ex_mac):
        # Create and populate the params dictionary
        params = {
            "EX_SSID1": ex_ssid1,
            "EX_AuthMode": ex_authmode,
            "EX_EncrypType": ex_encrypt_type,
            "EX_DefaultKeyID": ex_default_key_id,
            "EX_WEPKEY": ex_wep_key,
            "EX_WPAPSK1": ex_wpapsk1,
            "EX_wifi_profile": ex_wifi_profile,
            "EX_mac": ex_mac
        }

        super().__init__("WLAN_SET_STA_CON", **params)


class GOFORM_WLAN_SET_STA_DISCON(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("WLAN_SET_STA_DISCON", **params)


class GOFORM_WLAN_SET_STA_REFRESH(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("WLAN_SET_STA_REFRESH", **params)


class GOFORM_DEL_IP_PORT_FILETER(GoFormSetHttp):
    def __init__(self, delete_id, delete_id_v6):
        # Create and populate the params dictionary
        params = {
            "delete_id": delete_id
        }

        super().__init__("DEL_IP_PORT_FILETER", **params)

## TODO HAS SUBHANDLERS
class GOFORM_ADD_IP_PORT_FILETER_V4V6(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("ADD_IP_PORT_FILETER_V4V6", **params)


class GOFORM_DEL_IP_PORT_FILETER_V4V6(GoFormSetHttp):
    def __init__(self, delete_id, delete_id_v6):
        # Create and populate the params dictionary
        params = {
            "delete_id": delete_id,
            "delete_id_v6": delete_id_v6
        }

        super().__init__("DEL_IP_PORT_FILETER_V4V6", **params)


class GOFORM_FW_FORWARD_ADD(GoFormSetHttp):
    def __init__(self, ip_address, port_start, port_end, protocol, comment):
        # Create and populate the params dictionary
        params = {
            "ipAddress": ip_address,
            "portStart": port_start,
            "portEnd": port_end,
            "protocol": protocol,
            "comment": comment,
        }

        super().__init__("FW_FORWARD_ADD", **params)


class GOFORM_FW_FORWARD_DEL(GoFormSetHttp):
    def __init__(self, delete_id):
        # Create and populate the params dictionary
        params = {
            "delete_id": delete_id
        }

        super().__init__("FW_FORWARD_DEL", **params)


## TODO HAS SUBHANDLERS
class GOFORM_ADD_PORT_MAP(GoFormSetHttp):
    def __init__(self):
        # Create and populate the params dictionary
        params = {}

        super().__init__("ADD_PORT_MAP", **params)


class GOFORM_DEL_PORT_MAP(GoFormSetHttp):
    def __init__(self, delete_id):
        # Create and populate the params dictionary
        params = {
            "delete_id": delete_id
        }

        super().__init__("DEL_PORT_MAP", **params)


class GOFORM_BASIC_SETTING(GoFormSetHttp):
    def __init__(self, port_filter_enabled, default_firewall_policy):
        # Create and populate the params dictionary
        params = {
            "portFilterEnabled": port_filter_enabled,
            "defaultFirewallPolicy": default_firewall_policy
        }

        super().__init__("BASIC_SETTING", **params)


"""
- Sets "PortForwardEnable" cfg value
- Sends IPC of 0x100d to zte_mainctrl, which enables loads of iptables stuff
"""
class GOFORM_VIRTUAL_SERVER(GoFormSetHttp):
    def __init__(self, port_forward_enable):
        # Create and populate the params dictionary
        params = {
            "PortForwardEnable": port_forward_enable
        }

        super().__init__("VIRTUAL_SERVER", **params)


"""
- Sets "RemoteManagement" and "WANPingFilter" cfg values
- Sends IPC of 0x100d to zte_mainctrl, which enables loads of iptables stuff
"""
class GOFORM_FW_SYS(GoFormSetHttp):
    def __init__(self, remote_management, wan_ping_filter):
        # Create and populate the params dictionary
        params = {
            "RemoteManagement": remote_management,
            "WANPingFilter": wan_ping_filter
        }

        super().__init__("FW_SYS", **params)


class GOFORM_DHCP_SETTING(GoFormSetHttp):
    def __init__(self, lan_ip, lan_net_mask, lan_dhcp_type, dhcp_start, dhcp_end, dhcp_dns, dhcp_lease):
        # Create and populate the params dictionary
        params = {
            "lanIp": lan_ip,
            "lanNetmask": lan_net_mask,
            "lanDhcpType": lan_dhcp_type,
            "dhcpStart": dhcp_start,
            "dhcpEnd": dhcp_end,
            "dhcpDns": dhcp_dns,
            "dhcpLease": dhcp_lease,
        }

        super().__init__("DHCP_SETTING", **params)

"""
- ! Command injection
"""
class GOFORM_STATIC_DHCP_SETTING(GoFormSetHttp):
    def __init__(self, mac_ip_list):
        # Create and populate the params dictionary
        params = {
            "mac_ip_list": mac_ip_list
        }

        super().__init__("STATIC_DHCP_SETTING", **params)


class GOFORM_STATIC_UPNP_SETTING(GoFormSetHttp):
    def __init__(self, upnp_setting_option):
        # Create and populate the params dictionary
        params = {
            "upnp_setting_option": upnp_setting_option
        }

        super().__init__("STATIC_UPNP_SETTING", **params)

"""
- ! Command injection
"""
class GOFORM_DMZ_SETTING(GoFormSetHttp):
    def __init__(self, dmz_enabled, dmz_ip_address):
        # Create and populate the params dictionary
        params = {
            "DMZEnabled": dmz_enabled,
            "DMZIPAddress": dmz_ip_address
        }

        super().__init__("DMZ_SETTING", **params)

"""
- ! Command injection
"""
class GOFORM_EDIT_HOSTNAME(GoFormSetHttp):
    def __init__(self, mac, hostname):
        # Create and populate the params dictionary
        params = {
            "mac": mac,
            "hostname": hostname
        }

        super().__init__("EDIT_HOSTNAME", **params)


class GOFORM_URL_FILTER_DELETE(GoFormSetHttp):
    def __init__(self, url_filter_delete_id):
        # Create and populate the params dictionary
        params = {
            "url_filter_delete_id": url_filter_delete_id
        }

        super().__init__("URL_FILTER_DELETE", **params)

"""
- ! Command injection
"""
class GOFORM_URL_FILTER_ADD(GoFormSetHttp):
    def __init__(self, add_url_filter):
        # Create and populate the params dictionary
        params = {
            "addURLFilter": add_url_filter
        }

        super().__init__("URL_FILTER_ADD", **params)


class GOFORM_SET_BIND_STATIC_ADDRESS(GoFormSetHttp):
    def __init__(self, mac_ip_status):
        # Create and populate the params dictionary
        params = {
            "mac_ip_status": mac_ip_status
        }

        super().__init__("SET_BIND_STATIC_ADDRESS", **params)

"""
- ! Command injection
"""
class GOFORM_BIND_STATIC_ADDRESS_ADD(GoFormSetHttp):
    def __init__(self, mac_address, ip_address):
        # Create and populate the params dictionary
        params = {
            "mac_address": mac_address,
            "ip_address": ip_address
        }

        super().__init__("BIND_STATIC_ADDRESS_ADD", **params)

"""
- ! Command injection
"""
class GOFORM_BIND_STATIC_ADDRESS_DEL(GoFormSetHttp):
    def __init__(self, mac_address):
        # Create and populate the params dictionary
        params = {
            "mac_address": mac_address
        }

        super().__init__("BIND_STATIC_ADDRESS_DEL", **params)

"""
- ! Command injection
"""
class GOFORM_ADD_DEVICE(GoFormSetHttp):
    def __init__(self, mac):
        # Create and populate the params dictionary
        params = {
            "mac": mac
        }

        super().__init__("ADD_DEVICE", **params)

"""
- ! Command injection
"""
class GOFORM_DEL_DEVICE(GoFormSetHttp):
    def __init__(self, mac):
        # Create and populate the params dictionary
        params = {
            "mac": mac
        }

        super().__init__("DEL_DEVICE", **params)


"""
- ! Command injection
"""
class GOFORM_ADD_WHITE_SITE(GoFormSetHttp):
    def __init__(self, name, site):
        # Create and populate the params dictionary
        params = {
            "name": name,
            "site": site,
        }

        super().__init__("ADD_WHITE_SITE", **params)


"""
- ! Command injection
"""
class GOFORM_REMOVE_WHITE_SITE(GoFormSetHttp):
    def __init__(self, ids):
        # Create and populate the params dictionary
        params = {
            "ids": ids
        }

        super().__init__("REMOVE_WHITE_SITE", **params)

"""
- Sets "time_limited" in cfg
- Sends 0x101a IPC to zte_mainctrl, which calls system but boring as decimals
"""
class GOFORM_SAVE_TIME_LIMITED(GoFormSetHttp):
    def __init__(self, time_limited):
        # Create and populate the params dictionary
        params = {
            "time_limited": time_limited
        }

        super().__init__("SAVE_TIME_LIMITED", **params)


class GOFORM_DDNS(GoFormSetHttp):
    def __init__(self, ddns_enable, ddns_mode, ddns_provider, ddns, ddns_hash_value, ddns_account, ddns_password):
        # Create and populate the params dictionary
        params = {
            "DDNS_Enable": ddns_enable,
            "DDNS_Mode": ddns_mode,
            "DDNSProvider": ddns_provider,
            "DDNS": ddns,
            "DDNS_Hash_Value": ddns_hash_value,
            "DDNSAccount": ddns_account,
            "DDNSPassword": ddns_password
        }

        super().__init__("DDNS", **params)


"""
- Sets "blc_wan_mode" in config, then restarts
"""
class GOFORM_OPERATION_MODE(GoFormSetHttp):
    def __init__(self, op_mode):
        # Create and populate the params dictionary
        params = {
            "opMode": op_mode
        }

        super().__init__("OPERATION_MODE", **params)


class GOFORM_WAN_GATEWAYMODE_PPPOE(GoFormSetHttp):
    def __init__(self, pppoe_username, pppoe_password, action_link, dial_mode):
        # Create and populate the params dictionary
        params = {
            "pppoe_username": pppoe_username,
            "pppoe_password": pppoe_password,
            "action_link": action_link,
            "dial_mode": dial_mode
        }

        super().__init__("WAN_GATEWAYMODE_PPPOE", **params)


class GOFORM_WAN_GATEWAYMODE_DHCP(GoFormSetHttp):
    def __init__(self, action_link, dial_mode):
        # Create and populate the params dictionary
        params = {
            "action_link": action_link,
            "dial_mode": dial_mode
        }

        super().__init__("WAN_GATEWAYMODE_DHCP", **params)


class GOFORM_WAN_GATEWAYMODE_STATIC(GoFormSetHttp):
    def __init__(self, static_wan_ipaddr, static_wan_netmask, static_wan_gateway, static_wan_primary_dns, static_wan_secondary_dns, action_link, dial_mode):
        # Create and populate the params dictionary
        params = {
            "static_wan_ipaddr": static_wan_ipaddr,
            "static_wan_netmask": static_wan_netmask,
            "static_wan_gateway": static_wan_gateway,
            "static_wan_primary_dns": static_wan_primary_dns,
            "static_wan_secondary_dns": static_wan_secondary_dns,
            "action_link": action_link,
            "dial_mode": dial_mode
        }

        super().__init__("WAN_GATEWAYMODE_STATIC", **params)


class GOFORM_WAN_GATEWAYMODE_AUTO(GoFormSetHttp):
    def __init__(self, pppoe_username, pppoe_password, action_link, dial_mode):
        # Create and populate the params dictionary
        params = {
            "pppoe_username": pppoe_username,
            "pppoe_password": pppoe_password,
            "action_link": action_link,
            "dial_mode": dial_mode
        }

        super().__init__("WAN_GATEWAYMODE_AUTO", **params)


"""
- ! Path traversal
"""
class GOFORM_HTTPSHARE_ENTERFOLD(GoFormSetHttp):
    def __init__(self, path_sd_card, index):
        # Create and populate the params dictionary
        params = {
            "path_SD_CARD": path_sd_card,
            "indexPage": index
        }

        super().__init__("HTTPSHARE_ENTERFOLD", **params)

"""
- ! Path traversal
"""
class GOFORM_HTTPSHARE_NEW(GoFormSetHttp):
    def __init__(self, path_sd_card, path_sd_card_time, path_sd_card_time_unix):
        # Create and populate the params dictionary
        params = {
            "path_SD_CARD": path_sd_card,
            "path_SD_CARD_time": path_sd_card_time,
            "path_SD_CARD_time_unix": path_sd_card_time_unix
        }

        super().__init__("HTTPSHARE_NEW", **params)

"""
- ! Path traversal
"""
class GOFORM_HTTPSHARE_DEL(GoFormSetHttp):
    def __init__(self, path_SD_CARD, name_SD_CARD):
        # Create and populate the params dictionary
        params = {
            "path_SD_CARD": path_SD_CARD,
            "name_SD_CARD": name_SD_CARD,
        }

        super().__init__("HTTPSHARE_DEL", **params)


class GOFORM_HTTPSHARE_AUTH_SET(GoFormSetHttp):
    def __init__(self, http_share_wr_auth, http_share_file, http_share_status):
        # Create and populate the params dictionary
        params = {
            "HTTP_SHARE_WR_AUTH": http_share_wr_auth,
            "HTTP_SHARE_FILE": http_share_file,
            "HTTP_SHARE_STATUS": http_share_status,
        }

        super().__init__("HTTPSHARE_MODE_SET", **params)


class GOFORM_HTTPSHARE_MODE_SET(GoFormSetHttp):
    def __init__(self, mode_set):
        # Create and populate the params dictionary
        params = {
            "mode_set": mode_set
        }

        super().__init__("HTTPSHARE_MODE_SET", **params)

"""
- ! Path traversal
"""
class GOFORM_HTTPSHARE_FILE_RENAME(GoFormSetHttp):
    def __init__(self, old_name, new_name):
        # Create and populate the params dictionary
        params = {
            "OLD_NAME_SD_CARD": old_name,
            "NEW_NAME_SD_CARD": new_name
        }

        super().__init__("HTTPSHARE_FILE_RENAME", **params)

"""
- ! Path traversal
"""
class GOFORM_HTTPSHARE_CHECK_FILE(GoFormSetHttp):
    def __init__(self, path_sd_card):
        # Create and populate the params dictionary
        params = {
            "path_SD_CARD": path_sd_card
        }

        super().__init__("HTTPSHARE_CHECK_FILE", **params)


## TODO HAS SUBHANDLERS
class GOFORM_PBM_CONTACT_ADD(GoFormSetHttp):
    def __init__(self, path_sd_card):
        # Create and populate the params dictionary
        params = {}

        super().__init__("PBM_CONTACT_ADD", **params)

## TODO HAS SUBHANDLERS
class GOFORM_PBM_CONTACT_DEL(GoFormSetHttp):
    def __init__(self, path_sd_card):
        # Create and populate the params dictionary
        params = {}

        super().__init__("PBM_CONTACT_DEL", **params)


class GOFORM_SET_MESSAGE_CENTER(GoFormSetHttp):
    def __init__(self, message_center, save_location, save_time, status_save, sendfail_retry, outdate_delete, default_store):
        # Create and populate the params dictionary
        params = {
            "MessageCenter": message_center,
            "save_location": save_location,
            "save_time": save_time,
            "status_save": status_save,
            "sendfail_retry": sendfail_retry,
            "outdate_delete": outdate_delete,
            "default_store": default_store,
        }

        super().__init__("SET_MESSAGE_CENTER", **params)


"""
- ! Crash
"""
class GOFORM_DELETE_SMS(GoFormSetHttp):
    def __init__(self, msg_id):
        # Create and populate the params dictionary
        params = {
            "msg_id": msg_id
        }

        super().__init__("DELETE_SMS", **params)


class GOFORM_ALL_DELETE_SMS(GoFormSetHttp):
    def __init__(self, which_page):
        # Create and populate the params dictionary
        params = {
            "which_page": which_page
        }

        super().__init__("ALL_DELETE_SMS", **params)


"""
- ! Crash
"""
class GOFORM_MOVE_TO_SIM(GoFormSetHttp):
    def __init__(self, msg_id):
        # Create and populate the params dictionary
        params = {
            "msg_id": msg_id
        }

        super().__init__("MOVE_TO_SIM", **params)


class GOFORM_SAVE_SMS(GoFormSetHttp):
    def __init__(self, location, tags, sms_message, sms_number, index, encode_type, sms_time, draft_group_id):
        # Create and populate the params dictionary
        params = {
            "location": number,
            "tags": tags,
            "SMSMessage": sms_message,
            "SMSNumber": sms_number,
            "Index": index,
            "encode_type": encode_type,
            "sms_time": sms_time,
            "draft_group_id": draft_group_id,
        }

        super().__init__("SAVE_SMS", **params)


class GOFORM_SEND_SMS(GoFormSetHttp):
    def __init__(self, number, message_body, msg_id, encode_type, sms_time):
        # Create and populate the params dictionary
        params = {
            "Number": number,
            "MessageBody": message_body,
            "ID": msg_id,
            "encode_type": encode_type,
            "sms_time": sms_time,
        }

        super().__init__("SEND_SMS", **params)


class GOFORM_SET_MSG_READ(GoFormSetHttp):
    def __init__(self, msg_id, tag):
        # Create and populate the params dictionary
        params = {
            "msg_id": msg_id,
            "tag": tag
        }

        super().__init__("SET_MSG_READ", **params)


class GOFORM_IF_UPGRADE(GoFormSetHttp):
    def __init__(self, select_op):
        # Create and populate the params dictionary
        params = {
            "select_op": select_op
        }

        super().__init__("IF_UPGRADE", **params)


class GOFORM_SetUpgAutoSetting(GoFormSetHttp):
    def __init__(self, upg_mode, upg_roam_permission):
        # Create and populate the params dictionary
        params = {
            "UpgMode": upg_mode,
            "UpgRoamPermission": upg_roam_permission
        }

        super().__init__("SetUpgAutoSetting", **params)


"""
- Writes config values if provided
- Sends IPC (0x101f) to zte_mainctrl, calls 0xa828
- This function builds a command which goes into system with stuff we control
- ! Command injection as we control stuff
"""
class GOFORM_PINT_DIAGNOSTICS_START(GoFormSetHttp):
    def __init__(self, ping_diag_addr, ping_repetition_count, ping_time_out, ping_data_size, ping_diag_interface):
        # Create and populate the params dictionary
        params = {
            "ping_diag_addr": ping_diag_addr,
            "ping_repetition_count": ping_repetition_count,
            "ping_time_out": ping_time_out,
            "ping_data_size": ping_data_size,
            "ping_diag_interface": ping_diag_interface
        }

        super().__init__("PINT_DIAGNOSTICS_START", **params)


"""
- Runs "killall ping" with system()
"""
class GOFORM_PINT_DIAGNOSTICS_STOP(GoFormSetHttp):
    def __init__(self, path_sd_card):
        # Create and populate the params dictionary
        params = {}

        super().__init__("PINT_DIAGNOSTICS_STOP", **params)


## WTF does this do?
class GOFORM_SET_SAMPLE(GoFormSetHttp):
    def __init__(self, path_sd_card):
        # Create and populate the params dictionary
        params = {}

        super().__init__("SET_SAMPLE", **params)


def goform_set(command, ip, cookie):
    url = f"http://{ip}/goform/goform_set_cmd_process"
    
    # Encode the command
    data = urllib.parse.quote(str(command), safe='=&')

    # Calculate the correct Content-Length
    content_length = str(len(data))
    
    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Content-Length": content_length,
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

    info(f"Sending data: {data}")

    response = requests.post(url, headers=headers, data=data)
    info(f"Status Code: {response.status_code}")
    info(f"Response Body: {response.text}\n")

    return response.text

def goform_login(command, ip):
    url = f"http://{ip}/goform/goform_set_cmd_process"

    # Encode the command
    data = urllib.parse.quote(str(command), safe='=&')

    # Calculate the correct Content-Length
    content_length = str(len(data))

    headers = {
        "Host": ip,
        "Connection": "keep-alive",
        "Content-Length": content_length,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en",
        "Origin": f"http://{ip}",
        "Referer": f"http://{ip}/index.html",
        "Accept-Encoding": "gzip, deflate"
    }

    info(f"Sending data: {data}")

    response = requests.post(url, headers=headers, data=data)
    info(f"Status Code: {response.status_code}")
    info(f"Response Body: {response.text}\n")

    # Get the cookie from the response
    if 'Set-Cookie' in response.headers:
        cookie = response.headers['Set-Cookie'].split(';')[0]
    else:
        cookie = None
        bad("No Set-Cookie header found in the response.")

    return cookie  # Return the cookie

## new router stuff

"""
- Performs login to the web UI, username is optional
- Sets the "user_ip_addr" to the IP address
- Sets the "loginfo" to "ok"
- Resets "psw_fail_num_str" to 5
- Sets save_login to 0/1
"""
class GOFORM_LOGIN_NEW(GoFormSetHttp):
    def __init__(self, username, password):
        # Create and populate the params dictionary with username and password
        params = {"password": base64.b64encode((username + '\n' +  password).encode()).decode()}
        super().__init__("LOGIN", **params)

class GOFORM_SET_DEVICE_MODE(GoFormSetHttp):
    def __init__(self, mode):
        # Create and populate the params dictionary with username and password
        params = {"debug_enable": mode}
        super().__init__("SET_DEVICE_MODE", **params)


class GOFORM_ADD_PORT_MAP_NEW(GoFormSetHttp):
    def __init__(self, port_map_enabled, from_port, ip_address, to_port, protocol, comment):
        # Create and populate the params dictionary
        params = {
            "portMapEnabled": port_map_enabled,
            "fromPort": from_port,
            "ip_address": ip_address,
            "toPort": to_port,
            "protocol": protocol,
            "comment": comment
        }

        super().__init__("ADD_PORT_MAP", **params)

class GOFORM_ADD_IP_PORT_FILETER(GoFormSetHttp):
    def __init__(self, mac_address, dip_address, sip_address, dFromPort, dToPort, sFromPort, sToPort, action, protocol, comment):
        # Create and populate the params dictionary
        params = {
            "mac_address": mac_address,
            "dip_address": dip_address,
            "sip_address": sip_address,
            "dFromPort": dFromPort,
            "dToPort": dToPort,
            "sFromPort": sFromPort,
            "sToPort": sToPort,
            "action": action,
            "protocol": protocol,
            "comment": comment
        }

        super().__init__("ADD_IP_PORT_FILETER", **params)
