import requests
import os
import re
import logging
import argparse
from requests_html import HTMLSession
from typing import Callable, Optional
from random import randint
from common import print_and_log, logger
from models import available_services

import sys
MIN_PYTHON = (3, 7)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

def initial_setup():

    parser = argparse.ArgumentParser(description='Download a random 3D model')

    parser.add_argument('--independant', '-i', action='store_true',
                        help='Runs the script without asking for input from the user')
    parser.add_argument('--unlimited', '-u', action='store_false',
                        help='Runs the script over and over again to download many random prints')

    parser.add_argument('--service', '-s', default=None,
                        help='''Specifies which service to use, accepts either 'prusa' or 'thingiverse' ''')
    parser.add_argument('--filter', '-f', default=None,
                        help='''Filters the results based on the input''')
    parser.add_argument('--output', '-o', default=os.getcwd()+'\Downloads',
                        help='''Specifies a location to save the files to''')

    args = parser.parse_args()

    return args

def download_file(download_to, file_name, url, args_output):
        if url:
            file_path = os.path.join(f"{args_output}",f"{download_to.replace(' ', '_').strip()}")
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            response = requests.get(url)
            open(f'{file_path}/{file_name}', 'wb').write(response.content)
            return file_path

def pick_random_service():
    if len(available_services) <= 1:
        return available_services[list(available_services.keys())[0]]
    else:
        return available_services[list(available_services.keys())[randint(0,len(available_services)-1)]]

def main(session):
    args = initial_setup()
    
    while True:
        if args.service:
            if args.service in available_services:
                service = available_services[args.service.lower()]
            else:
                print_and_log(f"The service '{args.service}' does not exist")
                return
        else:
            service = pick_random_service()

        service_object = service(session, args.filter)

        print_and_log("Finding prints...")
        print()
        if args.independant:
            if service_object.find_random_print(200):
                print_and_log(f"Item found at: {service_object.item_url}")
                service_object.get_item_detail()
                print_and_log(f"\tName: {service_object.item_name}")
                print_and_log(f"\tUser: {service_object.item_user}")
                print()
                print_and_log("Getting files...")
                service_object.get_printable_files()
            else:
                print_and_log("No prints found")
        else:
            if service_object.find_random_print(200):
                print_and_log(f"Item found at: {service_object.item_url}")
            
                service_object.get_item_detail()
                print_and_log(f"\tName: {service_object.item_name}")
                print_and_log(f"\tUser: {service_object.item_user}")
                inp_continue = input("Do you want to continue? (Y/n)").lower()
                if inp_continue != 'n':
                    print()
                    print_and_log("Getting files...")
                    service_object.get_printable_files()
                else:
                    return

        print()
        if service_object.files_urls:
            download_to = os.path.join(re.sub('[^\w-]','_',service_object.item_user), re.sub('[^\w-]','_',service_object.item_name))
            if args.independant:
                print_and_log("Found the following files:")
                for file in service_object.files_urls:
                    print_and_log(f"\t{file}")
                print()
                for file in service_object.files_urls:
                    print_and_log(f"\tDownloading {file}")
                    download_file(download_to, file, service_object.files_urls[file], args.output)
            else:
                print_and_log("Found the following files:")
                for file in service_object.files_urls:
                    print_and_log(f"\t{file}")
                print()
                inp_download_all = input("Do you wish to download all? (Y/n)").lower()
                if inp_download_all != 'n':
                    for file in service_object.files_urls:
                        print_and_log(f"\tDownloading {file}")
                        download_file(download_to, file, service_object.files_urls[file], args.output)
                else:
                    for file in service_object.files_urls:
                        inp_download_ind = input(f"Do you want to download {file}? (Y/n)").lower()
                        if inp_download_ind != 'n':
                            print_and_log(f"\tDownloading {file}")
                            download_file(download_to, file, service_object.files_urls[file], args.output)
            
            print()
            print_and_log(f"Files downloaded to: {download_to}")
        else:
            print_and_log("No files found")
        
        if (args.unlimited):
            break



if __name__ == "__main__":
    try:
        with HTMLSession() as session:
            main(session)
    except Exception as error:
        print_and_log(f"{error}. Cannot guarentee files completed download.", level=logging.error)