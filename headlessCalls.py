import json
import time
import subprocess as sub

def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

class TeamsClient:
    """ contains info
    """
    def __init__(self, id, pw, number):
        self.id = id
        self.pw = pw
        self.number = number

    def display_data(self):
        print(f"client: id={self.id}, pw={self.pw}, number={self.number}")


class HeadLessCall:
    def __init__(self, clients, duration):
        self.power_shell = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
        shell_script = ".\\SipTesterClient.ps1"
        self.call_cmd = f"{shell_script} -TeamsOutUsername {clients[0].id} -TeamsOutPassword '{clients[0].pw}' -TeamsInUsername {clients[1].id} -TeamsInPassword '{clients[1].pw}' -DestinationNumber {clients[1].number}"
        self.call_options = "-MediaValidationFrequencyMinutes 1 -TestTimeoutInSeconds 300 -UseUserCredentials"
        self.call_duration = f"-CallDurationMinutes {duration}"
        self.simring = f"-TeamsInSimulringUsername {clients[2].id} -TeamsInSimulringPassword '{clients[2].pw}' -TeamsInSimulringIncomingNumber {clients[2].number}"
        self.escalation = f"-TeamsInEscalationUsername {clients[2].id} -TeamsInEscalationPassword '{clients[2].pw}' -TeamsInEscalationIncomingNumber {clients[2].number}"
        self.transfer = f"-TeamsInTransferTargetUsername {clients[2].id} -TeamsInTransferTargetPassword '{clients[2].pw}' -TeamsInTransferTargetIncomingNumber {clients[2].number}"

    def execute_script(self, cmd, debug):
        shell_cmd = [self.power_shell]
        shell_cmd.append(cmd)
        ret = sub.run(shell_cmd, shell=True, capture_output=True, text=True, timeout=500)
        if debug > 0:
            print(f"ret.returncode = {ret.returncode}\n\n")
            print(f"ret.stdout = {ret.stdout}\n\n")
            print(f"ret.stderr = {ret.stderr}\n\n")
            print(f"ret.args = {ret.args}\n\n")
            print(f"ret.check_returncode = {ret.check_returncode}\n\n")

        if ret.stdout.rfind("True") > -1:
            return 'Passed'
        else:
            #local_file = f"{log_location}/{test_name}-iteration{iteration}.log"
            #print(local_file)
            #dut.download_file(rest_host, cookies, "locallogfile", "webui.log", local_file)
            #print(ret.stdout)
            #print("\n\n\n\nStart")
            lines = ret.stdout.split('\n\n')
            for line in lines:
                if line.find("failed") > - 1:
                    #print(line)
                    break
            #print("End\n\n\n\n")
            #print(ret.stderr)
            #failed_cases = failed_cases + 1
            failure_reason = f"Failed\n{line}\n"
            #print(failure_reason)
            return failure_reason

    def basic_call(self, debug):
        cammand = f"{self.call_cmd} {self.call_duration} {self.call_options}"
        if debug > 0:
            print(cammand)
        status = self.execute_script(cammand, debug)
        return status

    def simring_call(self, debug):
        # Simultaneous Ring
        cammand = f"{self.call_cmd} {self.simring} {self.call_duration} {self.call_options}"
        if debug > 0:
            print(cammand)
        status = self.execute_script(cammand, debug)
        return status
    def esclation_call(self, debug):
        cammand = f"{self.call_cmd} {self.escalation} {self.call_duration} {self.call_options}"
        if debug > 0:
            print(cammand)
        status = self.execute_script(cammand, debug)
        return status

    def consulttransfer_call(self, debug):
        #Consultative Transfer
        cammand = f"{self.call_cmd} {self.transfer} {self.call_duration} {self.call_options}"
        if debug > 0:
            print(cammand)
        status = self.execute_script(cammand, debug)
        #test_result = f'Consultative Transfer:\t{status}\n\n'
        #result_file.write(test_result)
        #print(test_result)
        return status


# Read Test Info
"""
data = read_json("./TeamsHeadlessTest.JSON")
test_cycles = data['CYCLES']
duration = data['CALL-DURATION']
#print(f"test_cycles={test_cycles}, duration={duration}")
"""

# Read DUT config
"""
log_location = data['LOG-LOCATION']
configs = data['CONFIGS']
log_location = "C:\\Users\\mahmood-aslami\\Downloads\\DevTeamsHeadLess\\logs"
print(f"rest_host={rest_host}, rest_user={rest_user}, rest_pw={rest_pw}, log_location={log_location}")
"""
"""
        for file in os.scandir(log_location):
        os.remove(file.path)
        result_file = open('TeamsTestResults.txt', 'w')
        test_cycle = f"Starting Teams headless test cycle {cycle}\n"
        print(test_cycle)
        test_result = f'Basic call:\t\t{status}\n'
        result_file.write(test_result)
        result_file.write(test_cycle)
        test_result = f'Simultaneous Ring:\t{status}\n'
        result_file.write(test_result)
        test_result = f'Media Escalation:\t{status}\n'
        result_file.write(test_result)
        test_result = f'Consultative Transfer:\t{status}\n\n'
        result_file.write(test_result)
        result_summary = f'Summary: Passed={passed_cases} Failed={failed_cases}\n\n'
        result_file.write(result_summary)
        result_file.close()

"""

def headless_calls(test, duration, cycles, debug):
    
    failed_cases = 0
    passed_cases = 0

    # Read Teams Clients Info
    data = read_json("./TeamsHeadlessClients.JSON")
    clients = data['CLIENTS']
   
   # Create Teams clients
    client_list = []
    for i in range(3):
        client_list.append(TeamsClient(clients[i]['ID'], clients[i]['PASSWORD'], clients[i]['NUMBER']))
        if debug:
            client_list[i].display_data()
    
    # Create HeadlessCall object
    call = HeadLessCall(client_list, duration)

    # Make requested calls
    for cycle in range(1, cycles+1):
        test_cycle = f"Starting Teams headless test cycle {cycle}\n"
        print(test_cycle)
        if test & 1: # Basic call
            status = call.basic_call(debug)
            if status == 'Passed':
                passed_cases = passed_cases + 1
            else:
                failed_cases = failed_cases + 1
        if test & 2: # Simultaneous Ring
            status = call.simring_call(debug)
            if status == 'Passed':
                passed_cases = passed_cases + 1
            else:
                failed_cases = failed_cases + 1
        if test & 4: # Media Escalation
            status = call.esclation_call(debug)
            if status == 'Passed':
                passed_cases = passed_cases + 1
            else:
                failed_cases = failed_cases + 1
        if test & 8: # Consultative Transfer
            status = call.consulttransfer_call(debug)
            if status == 'Passed':
                passed_cases = passed_cases + 1
            else:
                failed_cases = failed_cases + 1
        if exit_event.is_set():
            break;

    summary = f'Summary: Passed={passed_cases} Failed={failed_cases}\n\n'

        