import os
import errno
import paramiko
import configparser

def check_config(config_path:str) -> configparser.ConfigParser:

    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
    
    return configparser.ConfigParser()

def read_ssh_config(ssh_config_path:str, ssh_host_name:str) -> paramiko.SSHConfigDict:
        config_file = os.path.expanduser(ssh_config_path)
        ssh_config = paramiko.SSHConfig()
        ssh_config.parse(open(config_file, 'r'))

        return ssh_config.lookup(ssh_host_name)