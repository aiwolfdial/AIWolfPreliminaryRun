import time
from sshtunnel import SSHTunnelForwarder
import util
from connection import TCPClient

if __name__ == "__main__":
	config_path = "./res/config.ini"
	inifile = util.check_config(config_path=config_path)
	inifile.read(config_path,"UTF-8")
	config = util.read_ssh_config(ssh_config_path=inifile.get("ssh","ssh_config_path"), ssh_host_name=inifile.get("ssh","host_name"))

	# hold bind ports
	port_list = []
	for remote_foward in config["remoteforward"]:
		parts = remote_foward.split()
		remote_port = parts[0]
		port_list.append(remote_port)
	
	allow_agent = None
	host_pkey_directories = None

	if inifile.getboolean("ssh","use_ssh_agent"):
		allow_agent = True
	else:
		host_pkey_directories = config["IdentityFile"]

	# make ssh tunnel
	server = SSHTunnelForwarder(
		config["hostname"],
		ssh_username=config["user"],
		local_bind_address=(inifile.get("tcp-client","host"),inifile.getint("tcp-client","port")),
		remote_bind_address=("localhost",10001),
		allow_agent=allow_agent,
		host_pkey_directories = host_pkey_directories,
	)

	server.start()
	
	try:
		client = TCPClient(inifile=inifile)
		client.connect()

		time.sleep(1)

		# send bind ports
		client.send(message=" ".join(port_list))
	except:
		print("ERROR")

	client.close()

	server.stop()
	server.close()