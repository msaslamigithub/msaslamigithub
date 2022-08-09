import time
import json
import requests as req
#import headlessCalls as hl

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

class Dut:
    def __init__(self, host, user, pw):
        self.rest_host = host
        self.rest_user = user
        self.rest_pw = pw
        return
    """
    def __init__(self):
        data = read_json("./DUTConfig.JSON")
        self.rest_host = data['HOST']
        self.rest_user = data['USER']
        self.rest_pw = data['PASSWORD']
        return
    """
    def display_data(self):
        print(f"REST: host={self.rest_host}, user={self.rest_user}, pw={self.rest_pw}")
    
    def login(self, debug):
        rest_endpoint = f"https://{self.rest_host}/rest"
        login = f"{rest_endpoint}/login/"
        credentials = {}
        credentials['Username'] = self.rest_user
        credentials['Password'] = self.rest_pw
        if debug:
            print(credentials)

        self.session = req.post(login, data=credentials, verify=False)
        if self.session.status_code == 200:
            return True
        else: 
            return False

    def logout(self, debug):
        rest_endpoint = f"https://{self.rest_host}/rest"
        logout = f"{rest_endpoint}/logout"
        if debug:
            print(logout)

        resp = req.post(logout, verify=False, cookies=self.session.cookies)
        if resp.status_code != 200:
            print(resp.text)



    def reboot_sbc(self, host, debug):
        rest_endpoint = f"https://{host}/rest"
        rest_request = f"{rest_endpoint}/system?action=reboot"
        if debug:
            print(rest_request)
        resp = req.post(rest_request, verify=False, cookies=self.session.cookies)
        time.sleep(2)
        if resp.status_code != 200:
            print(resp.text)
        return

    def ha_role(self, host, debug):
        rest_request = f"https://{host}/rest/ha"
        if debug:
            print(rest_request)
        resp = req.get(rest_request, verify=False, cookies=self.session.cookies)
        time.sleep(2)
        print(resp.text)
        if resp.status_code != 200:
            print(resp.text)
        return


    def rotate_log(self, cookies):    
        rest_endpoint = f"https://{self.rest_host}/rest"
        rest_request = f"{rest_endpoint}/systemlog?action=rotate"
        #print(rest_request)
        resp = req.post(rest_request, verify=False, cookies=self.session.cookies)
        time.sleep(2)
        if resp.status_code != 200:
            print(resp.text)
        return

   
    def download_file(file_type, remote_file, local_file):    
        rest_endpoint = f"https://{host}/rest"
        rest_request = f"{rest_endpoint}/{file_type}/{remote_file}?action=download"
        #print(rest_request)
        resp = req.post(rest_request, verify=False, cookies=self.session.cookies)
        time.sleep(1)
        if resp.status_code == 200:
            fLog = open(local_file, 'w')
            time.sleep(1)
            fLog.write(resp.text)
            time.sleep(1)
            fLog.close()
        else:
            print(resp.text)
        return


"""
def set_route_media_list(configs, host, cookies, media_profile_id, config_list_index, iteration):
    num_configs = len(configs)
    config_sufex = iteration % num_configs + 1
    config_index = f"CONFIG{config_sufex}-MEDIALISTS"
    config = configs[config_index]
    codecs = config[config_list_index]['VOICEFAXPROFILEID']
    #print(f"iteration={iteration}, num_configs={num_configs}, config_index={config_index}, codecs={codecs}")
    rest_endpoint = f"https://{host}/rest"
    rest_req = f"{rest_endpoint}/medialistprofile/{media_profile_id}"
    codec_profiles = {}
    codec_profiles['VoiceFaxProfileID'] = codecs
    resp = req.post(rest_req, codec_profiles, verify=False, cookies=cookies)
    if resp.status_code != 200:
        print(resp.text)
        Resource - routingentry
        https://192.168.0.111/rest/routingtable/{identifier}/routingentry/{identifier}
        MediaSelection
"""

def reboot_dut(wait, repeat, debug):
    data = read_json("./DUTConfig.JSON")
    dut = Dut(data['HA-HOST1'], data['USER'], data['PASSWORD'])
    if debug:
        dut.display_data()

    for n in range(repeat):
        login = dut.login(debug)
        if login == True:
            dut.ha_role(data['HA-HOST1'], debug)
            #dut.reboot_sbc(debug)
            dut.logout(debug)
            time.sleep(wait)
        else:
            print(f"REST login to {data['HOST']}, user={data['USER']}, pw={data['PASSWORD']} failed")
    
  