
from plexus.utils.console_client_api import PlexusUserApi
from plexus.nodes.message import Message


###############################
if __name__ == "__main__":
        list_of_nodes1 = [
                {"name": "node1", "address": "tcp://10.9.0.23:5566"},
                {"name": "node2", "address": "tcp://10.9.0.12:5567"}
                ]
        client_addr = "tcp://10.9.0.1:5565"         # мой адресс
        stend_control = PlexusUserApi(endpoint=client_addr, name="client", list_of_nodes=list_of_nodes1)
        # message = stend_control.user_input_parse(
            # addr="tcp://10.9.0.12:5567", node="node2", device="node2", command="info", raw_args="{0}\"{1}\": 10{2}".format("{", "arg", "}")
        # )
        # res = stend_control.send_msg(message)
        res = stend_control.get_full_node_info("node2")
        # message = Message(addr="node2", device ='node2', command='info')
        addr_decoded_, decoded_resp_ = Message.parse_zmq_msg(res)
        print(addr_decoded_, decoded_resp_)