from plexus.utils.console_client_api import PlexusUserApi
from plexus.nodes.message import Message
import json
# from config import  list_of_nodes

class StendControlCommandCreator:

    def __init__(self, client_addr, list_of_nodes, node_name):
        client_name = "client_{0}".format(client_addr)
        self.node_name = node_name
        self.stend_control_api = PlexusUserApi(endpoint=client_addr, name=client_name, list_of_nodes=list_of_nodes)
        addr_decoded_, decoded_resp_ = self.stend_control_api.get_full_node_info(node_name)
        self.decoded_resp_ = decoded_resp_


    def get_devices_names(self):
        devices = [device for device in self.decoded_resp_["data"]["devices"]]
        devices.insert(0,self.node_name)  # добавляем элемент на позицию 0
        return devices

    def get_commands(self, device_name):
        if device_name == self.node_name:
            return [command for command in self.decoded_resp_["data"]["system_commands"]]
        else:
            return [command for command in self.decoded_resp_["data"]["devices"][device_name]["commands"]]

    def get_arguments_str(self, device_name, command): # работает только для одного аргумента
        if device_name == self.node_name:
            if self.decoded_resp_["data"]["system_commands"][command]['input_kwargs'] == None:
                return "None"
            else:
                return "{0}\"{1}\": #{2}".format('{',str(list((self.decoded_resp_["data"]["system_commands"][command]['input_kwargs']).keys())[0]),'}')
        else:
            if self.decoded_resp_['data']['devices'][device_name]['commands'][command]['input_kwargs'] == None:
                return "None"
            else:
                return "{0}\"{1}\": #{2}".format('{',str(list((self.decoded_resp_['data']['devices'][device_name]['commands'][command]['input_kwargs']).keys())[0]),'}')

    def send_message(self, device, command, arguments):
        try:
            if device != None and command != None and arguments != None:
                if arguments == 'None' or arguments == None:
                    data = None
                else:
                    data = json.loads(arguments)
                message = Message(addr=self.node_name, device=device, command=command, data=data)
                node_answer_raw = self.stend_control_api.send_msg(message)
                node_addres, node_answer = Message.parse_zmq_msg(node_answer_raw)
                return str(node_answer)
        except:
            return 'send message error'


# {"channel": #}
# command_arguments_str = "{0}\"{1}\": #{2}".format('{',str(list((decoded_resp_['data']['devices'][device_dropdown_value]['commands'][command]['input_kwargs']).keys())[0]),'}')