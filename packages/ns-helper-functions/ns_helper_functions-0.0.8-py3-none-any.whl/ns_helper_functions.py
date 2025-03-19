import pandas as pd
import openpyxl
import nornir
import pynautobot

def push_output_to_gitlab(file_to_push_to_git_list,BRANCH="main"):

    import requests
    import base64
    from datetime import datetime
    import os
    from rich.console import Console

    console = Console()

    # from dotenv import load_dotenv

    now = datetime.now().strftime("%d-%m-%Y_%H.%M.%S")

    # load_dotenv()

    GITLAB_TOKEN = os.environ['GITLAB_TOKEN']
    PROJECT_ID = os.environ['PROJECT_ID']
    git_output_root_directory = os.environ['git_output_root_directory']

    if all(v is not None for v in [GITLAB_TOKEN, PROJECT_ID, git_output_root_directory]):

        for file in file_to_push_to_git_list:

            # This is obviously a very stupid workaround and not at all reusable, but it works for now
            # test1[len(test2)+1:]

            with open(file, "rb") as f:
                content = base64.b64encode(f.read()).decode()

            relative_file_location = file[len(f"{os.getcwd()}/_OUTPUT/"):]
            FILE_PATH = f"{git_output_root_directory}/{relative_file_location}"

            url = f"https://git.space.gr/api/v4/projects/{PROJECT_ID}/repository/files/{FILE_PATH.replace('/', '%2F')}"
            headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
            data = {
                "branch": BRANCH,
                "commit_message": f"Adding file via API at {now}",
                "content": content
            }

            response = requests.post(url, headers=headers, data=data)
            # print(response.json())
    else:
        console.print("No GITLAB_TOKEN, PROJECT_ID, or git_output_root_directory found in environment variables, skipping push to Gitlab")

    return None


def create_menu() -> dict:
    """
    Creates and configures a menu using argparse to handle command line arguments.

    Configures arguments for inventory source, Nautobot URL, token, filter parameters,
    Vault URL, token, and mode. Populates arguments from environment variables if not provided.

    Returns:
        dict: A dictionary containing the configuration parameters
    """
    import argparse
    import os
    import json

    ReturnDict = {}

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--inventory_source",
        "-i",
        help="Source of the inventory. Valid options are nautobot, excel or nornir",
        type=str,
        choices=["excel", "nornir", "nautobot"],
        required=False,
    )

    parser.add_argument(
        "--nautobot_url", 
        help="Nautobot url, for example http://localhost:8080", 
        type=str, 
        required=False
    )
    parser.add_argument(
        "--nautobot_token", 
        help="Nautobot token", 
        type=str, 
        required=False
    )
    
    parser.add_argument(
        "--nautobot_filter_parameters_string", 
        "-q", 
        help="Nautobot query filter (in json format)", 
        type=str, 
        required=False
    )
    
    parser.add_argument(
        "--vault_url", 
        help="Hashicorp vault url, for example http://localhost:8200", 
        type=str, 
        required=False
    )

    parser.add_argument(
        "--vault_token", 
        help="Hashicorp vault token", 
        type=str, 
        required=False
    )

    parser.add_argument(
        "--mode",
        help="Valid choices are dry_run, apply",
        type=str,
        choices=["dry_run", "apply"],
        required=False,
    )

    args = parser.parse_args()

    if not args.inventory_source:
        args.inventory_source = get_inventory_source()
    ReturnDict.update({"inventory_source": args.inventory_source})

    if args.inventory_source == "nautobot":
        if not args.nautobot_url:
            if os.environ.get('nautobot_url'):
                args.nautobot_url = os.environ.get('nautobot_url')
            else:
                args.nautobot_url = get_nautobot_url()
        ReturnDict.update({"nautobot_url": args.nautobot_url})

        if not args.nautobot_token:
            if os.environ.get('nautobot_token'):
                args.nautobot_token = os.environ.get('nautobot_token')
            else:
                args.nautobot_token = get_nautobot_token()
        ReturnDict.update({"nautobot_token": args.nautobot_token})

        if not args.nautobot_filter_parameters_string:
            if os.environ.get('nautobot_filter_parameters_string'):
                nautobot_filter_parameters_string = os.environ.get('nautobot_filter_parameters_string')
                nautobot_filter_parameters = json.loads(args.nautobot_filter_parameters_string)
            else:
                nautobot_filter_parameters = get_nautobot_query_filter_string()
            ReturnDict.update({"nautobot_filter_parameters": nautobot_filter_parameters})
        ReturnDict.update({"nautobot_filter_parameters": nautobot_filter_parameters})
                
        if not args.vault_url:
            if os.environ.get('vault_url'):
                args.vault_url = os.environ.get('vault_url')
            else:
                args.vault_url = get_vault_url()
        ReturnDict.update({"vault_url": args.vault_url})

        if not args.vault_token:
            if os.environ.get('vault_token'):
                args.vault_token = os.environ.get('vault_token')
            else:
                args.vault_token = get_vault_token()
        ReturnDict.update({"vault_token": args.vault_token})

        if not args.mode:
            args.mode = get_dry_run()
            ReturnDict.update({"mode": args.mode})


    return ReturnDict


def frame(text: str, style_character: str = '*') -> None:
    """
    Prints the given text in a framed box.

    Args:
        text (str): The text to be framed
        style_character (str, optional): The character used for the frame. Defaults to '*'
    """
    line_len = []
    for line in text.split('\r\n'):
        line_len.append(len(line))
    max_len = max(line_len)
    frame_line = style_character * (max_len + 4)
    print(frame_line)
    for line in text.split('\r\n'):
        print(style_character+line.center(max_len+2)+style_character)
    print(frame_line)


def create_default_files_and_directories(files: list = [{"name" : ".env", "content" : ["nautobot_url", "vault_url", "nautobot_token", "vault_token", "nautobot_query_filter"]}], directories: list = ["_OUTPUT", "parameters"]) -> None:    
    """
    Creates default files and directories if they don't exist.

    Args:
        files (list, optional): List of file names to create. Defaults to [".env"]
        directories (list, optional): List of directory names to create. Defaults to ["_OUTPUT", "parameters"]
    """
    import os

    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)

    for file in files:
        file_name = file["name"]
        if not os.path.isfile(file_name):
            if "content" in file:
                if file["content"]:
                    env_parameters = file["content"]
                    with open(file_name, 'w') as f:
                        for parameter in env_parameters:
                            f.write(f"{parameter}=\n")
                        f.write("\n")
            else:
                open(file_name, 'a').close()

    return None



def get_col_widths(dataframe: pd.DataFrame) -> list:
    """
    Calculates the maximum column widths for a DataFrame.

    The width for each column is determined by the maximum length of either the column name or any value in the column.
    Minimum column width is set to 12 characters.

    Args:
        dataframe (pandas.DataFrame): The DataFrame for which to calculate column widths

    Returns:
        list: A list of integers representing the maximum width for each column
    """
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    ColumnLengthList = [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
    for index,length in enumerate(ColumnLengthList):
        if length < 12:
            ColumnLengthList[index] = 12

    return ColumnLengthList


def chunks(l: list, n: int) -> list:
    """
    Yields successive n-sized chunks from a list.

    Args:
        l (list): The list to split into chunks
        n (int): Size of each chunk

    Yields:
        list: A chunk of size n from the list
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def create_key_parameter_menu(folder: str, extension: str) -> str:
    """
    Creates a menu for selecting a file with a specific extension from a given folder.

    Args:
        folder (str): The folder to search in
        extension (str): The file extension to look for

    Returns:
        str: The name of the selected file
    """
    import os

    KEYS = [f for f in os.listdir(folder) if f.endswith(extension)]
    KEYS.sort()     
    print("The following Excel files were detected in your parameters file.\n")
    i=0
    for KEY in KEYS:
        i=i+1
        print(f"[{str(i)}]:", (KEY))
    while True:
        KEY = input("\r\nPlease input the number of the file you would like to use: ")

        if str(KEY).isdigit():
            KEY = int(KEY)
        if (KEY in set(range(1, len(KEYS)+1))):
            break
        else:
            print("Your entry is not valid. Please try again.\r\n")
            continue

    workbookname = KEYS[KEY-1]
    return workbookname


def get_workbook(default_folder: str) -> tuple:
    """
    Prompts the user for an Excel workbook folder and loads the workbook.

    Args:
        default_folder (str): The default folder to use if no input is provided

    Returns:
        tuple: A tuple containing the loaded workbook, workbook name, and workbook folder
    """
    import openpyxl 
    import os

    forbiden_chars = ["<", ">", ":", "\"", "\\", "|", '?', "*"]
    extension = 'xlsx'
    while True:
        workbookfolder_raw = input(f"\nPlease enter the name of the excel workbook folder, press . to use the current folder or press enter to use the default {default_folder} folder: ")
        if workbookfolder_raw.strip() == "":
            workbookfolder = default_folder
            break
        elif any(i in workbookfolder_raw.strip() for i in forbiden_chars):
            print("\r\nThe folder name contains forbidden characters")
            continue
        elif not os.path.exists(workbookfolder_raw.strip()):
            print("\r\nThe folder you provided does not exist")
            continue
        else:
            workbookfolder = workbookfolder_raw.strip()
            break

    if workbookfolder == ".":
        print("\r\nYou have chosen the current folder as your workbook folder.")
    else:
        print("\r\nYou have chosen the" , workbookfolder , "folder as your workbook folder.")
    print()

    workbookname = create_key_parameter_menu(workbookfolder, extension)
    
    workbookpath = workbookfolder+"/"+workbookname
    workbook = openpyxl.load_workbook(workbookpath, data_only=True)

    return workbook, workbookname, workbookfolder


def get_device_worksheet(workbook: openpyxl.Workbook) -> str:
    """
    Prompts the user to select a worksheet from the given workbook.

    Args:
        workbook (openpyxl.Workbook): The workbook containing worksheets

    Returns:
        str: The name of the selected worksheet
    """
    worksheets = []
    print("\r\nYour workbook contains the following worksheets:\r\n")
    
    for worksheet in workbook.worksheets:
        worksheets.append(worksheet.title)
    i=0
    for worksheet in worksheets:
        i=i+1
        print(f"[{str(i)}]:", (worksheet))
    
    while True:
        deviceworksheet_number = input(f"\r\nPlease input the number of the device worksheet: ")
    
        if str(deviceworksheet_number).isdigit():
            deviceworksheet_number = int(deviceworksheet_number)
        if (deviceworksheet_number not in set(range(1, len(worksheets)+1))) or (not str(deviceworksheet_number).isdigit()):
            print("Your entry is not valid. Please try again.\r\n")
            continue
        deviceworksheet_name = worksheets[int(deviceworksheet_number)-1]
        if deviceworksheet_name not in workbook.sheetnames:
            print("The provided excel workbook does not include a worksheet named:" , deviceworksheet_name)
            continue
        else:
            break
            
    return deviceworksheet_name


def get_hostname(task: nornir.core.Task) -> str:
    """
    Retrieves the hostname from a network device using Netmiko.

    Args:
        task (nornir.core.Task): The Nornir task object

    Returns:
        str: The hostname of the device
    """
    task.host.open_connection("netmiko", None)
    conn = task.host.connections["netmiko"].connection
    hostname = conn.find_prompt()
    return hostname


def get_hostname_ftd(task: nornir.core.Task) -> str:
    """
    Retrieves the hostname from a Cisco FTD device using Netmiko.

    Args:
        task (nornir.core.Task): The Nornir task object

    Returns:
        str: The hostname of the device
    """
    task.host.open_connection("netmiko", None)
    conn = task.host.connections["netmiko"].connection
    conn.send_command("system support diagnostic-cli", expect_string="#", read_timeout=15, auto_find_prompt=False)
    hostname = conn.find_prompt()
    return hostname


def get_hostname_asa(task: nornir.core.Task) -> str:
    """
    Retrieves the hostname from a Cisco ASA device using Netmiko.

    Args:
        task (nornir.core.Task): The Nornir task object

    Returns:
        str: The hostname of the device
    """
    task.host.open_connection("netmiko", None)
    conn = task.host.connections["netmiko"].connection
    hostname = conn.find_prompt()
    return hostname


def get_credentials() -> tuple:
    """
    Prompts the user for username and password.

    Returns:
        tuple: A tuple containing the username and password
    """
    from getpass import getpass

    username = input(
        "\r\nPlease enter your Username or press enter to use excel Username: ")
    password = getpass(
        "\r\nPlease enter your password or press enter to use excel password: ")
    DICT = dict()

    return username, password


def get_nr_from_excel_or_NB_choice() -> int:
    """
    Presents a menu for the user to choose between getting inventory data from Excel or Nautobot.

    Returns:
        int: 1 if Excel is chosen, 2 if Nautobot is chosen
    """
    from rich.console import Console
    console = Console()

    nr_from_excel_or_NB_choice = 0
    while nr_from_excel_or_NB_choice != 1 or nr_from_excel_or_NB_choice != 2:
        console.print(
            "\r\n[1] Get inventory data from Excel\r\n[2] Get inventory data from Nautobot \r\n")
        nr_from_excel_or_NB_choice = input(
            "Please input 1 to get inventory data from Excel or 2 to get inventory data from Nautobot: ")
        if nr_from_excel_or_NB_choice == "1":
            console.print("\nYou have chosen to get inventory data from Excel")
            break
        elif nr_from_excel_or_NB_choice == "2":
            console.print("\nYou have chosen to get inventory data from Nautobot")
            break
        else:
            console.print("\nNot a Valid Choice. Try again")

    return nr_from_excel_or_NB_choice


def get_credentials_from_NB_or_stdin() -> int:
    """
    Presents a menu for the user to choose between getting credentials from Nautobot or from standard input.

    Returns:
        int: 1 if Nautobot is chosen, 2 if standard input is chosen
    """
    from rich.console import Console
    console = Console()

    credentials_from_NB_or_stdin = 0
    while credentials_from_NB_or_stdin not in [1,2]:
        console.print(
            "\r\n[1] Get credentials from from Nautobot\r\n[2] Get credentials from stdin \r\n")
        credentials_from_NB_or_stdin = input(
            "Please input 1 to get credentials from Nautobot or 2 to get credentials from stdin: ")
        if credentials_from_NB_or_stdin == "1":
            console.print("\nYou have chosen to get credentials from Nautobot")
            break
        elif credentials_from_NB_or_stdin == "2":
            console.print("\nYou have chosen to get credentials from stdin")
            break
        else:
            console.print("\nNot a Valid Choice. Try again")

    return credentials_from_NB_or_stdin


def get_nautobot_data() -> dict:
    """
    Retrieves Nautobot URL, token, and query filter from environment variables or user input.

    Returns:
        dict: A dictionary containing Nautobot connection details
    """
    import os
    from getpass import getpass
    from rich.console import Console

    console = Console()

    if "nautobot_url" in os.environ:
        console.print(f"nautobot_url [red bold]found[/red bold] in environment variables.")
        nautobot_url = os.environ.get('nautobot_url')
    else:
        nautobot_url = input(f"Please input the nautobot URL, for example http://localhost:8080: ")

    if "nautobot_token" in os.environ:
        console.print(f"nautobot_token [red bold]found[/red bold] in environment variables.")
        nautobot_token = os.environ.get('nautobot_token')
    else:
        nautobot_token = getpass(f"Please input your Nautobot authentication token: ")

    if "nautobot_query_filter" in os.environ:
        console.print(f"nautobot_query_filter [red bold]found[/red bold] in environment variables.")
        nautobot_query_filter = os.environ.get('nautobot_query_filter')
    else:
        nautobot_query_filter = input(f"Please input your Nautobot query filter, or leave blank: ")

    nautobot_data = {
        "nautobot_url" : nautobot_url,
        "nautobot_token" : nautobot_token,
        "nautobot_query_filter" : nautobot_query_filter
    }

    return nautobot_data


def init_nautobot(url: str, token: str) -> pynautobot.api:
    """
    Initializes a connection to the Nautobot API.

    Args:
        url (str): Nautobot server URL
        token (str): Nautobot authentication token

    Returns:
        pynautobot.api: The initialized Nautobot API object
    """
    import pynautobot 

    nautobot = pynautobot.api(
        url=url,
        token=token,
    )

    return nautobot


def get_hc_secrets_group_parameters_dict(nr: nornir.core.Nornir, nautobot: pynautobot.api) -> dict:
    """
    Retrieves secrets group parameters from Nautobot for all devices in the inventory.

    Args:
        nr (nornir.core.Nornir): The Nornir object
        nautobot (pynautobot.api): The Nautobot API object

    Returns:
        dict: A dictionary containing secrets group parameters organized by group name
    """
    secrets_group_name_set = set()
    for host in nr.inventory.dict()['hosts']:
        if nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']:
            secrets_group_name_set.add(nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']['name'])

    hc_secrets_group_parameters_dict = {}
    for secrets_group_name in secrets_group_name_set:
        secrets_group_credentials_list = nautobot.extras.secrets_groups.get(
            secrets_group_name
        ).secrets
        for secret_group in secrets_group_credentials_list:
            secret_provider = secret_group.secret.provider
            secret_name = secret_group.secret.name
            secret_type = secret_group.secret_type
            if secret_provider == "hashicorp-vault":
                hc_secret_group_parameters = secret_group["secret"]["parameters"]
                if not secrets_group_name in hc_secrets_group_parameters_dict:
                    hc_secrets_group_parameters_dict.update(
                        {
                            secrets_group_name: {
                                secret_type: {
                                    "secret_parameters": hc_secret_group_parameters,
                                    "secret_name": secret_name,
                                }
                            }
                        }
                    )
                else:
                    hc_secrets_group_parameters_dict[secrets_group_name].update(
                        {
                            secret_type: {
                                "secret_parameters": hc_secret_group_parameters,
                                "secret_name": secret_name,
                            }
                        }
                    )
    return hc_secrets_group_parameters_dict


def get_credentials_from_HCKV(HCKV_TOKEN: str, HCKV_URL: str, hc_secrets_group_parameters_dict: dict) -> dict:
    """
    Retrieves credentials from Hashicorp Key Vault (HCKV) based on secrets group parameters.

    Args:
        HCKV_TOKEN (str): HCKV authentication token
        HCKV_URL (str): HCKV server URL
        hc_secrets_group_parameters_dict (dict): Dictionary containing secrets group parameters

    Returns:
        dict: A dictionary containing credentials organized by secrets group name
    """
    import requests

    HCKV_headers = {
        "X-Vault-Token": HCKV_TOKEN
    }

    secret_group_name_credentials_dict = {}
    for secret_group_name, secret_group_credential_type_dict in hc_secrets_group_parameters_dict.items():
        for secret_group_credential_type, secret_group_credential_type_parameters in secret_group_credential_type_dict.items():
            path = secret_group_credential_type_parameters['secret_parameters']['path']
            mount_point = secret_group_credential_type_parameters['secret_parameters']['mount_point']
            path = secret_group_credential_type_parameters['secret_parameters']['path']
            response = requests.get(f'{HCKV_URL}/v1/{mount_point}/data/{path}', headers=HCKV_headers).json()
            if secret_group_name not in secret_group_name_credentials_dict:
                secret_group_credential_type_value = response['data']['data'][secret_group_credential_type]
                secret_group_name_credentials_dict.update({secret_group_name : {secret_group_credential_type : secret_group_credential_type_value}})
            else:
                secret_group_credential_type_value = response['data']['data'][secret_group_credential_type]
                secret_group_name_credentials_dict[secret_group_name].update({secret_group_credential_type : secret_group_credential_type_value})


    return secret_group_name_credentials_dict


def get_HCKV_data() -> dict:
    """
    Retrieves Hashicorp Key Vault (HCKV) URL and token from environment variables or user input.

    Returns:
        dict: A dictionary containing HCKV connection details
    """
    import os
    from getpass import getpass
    from rich.console import Console

    console = Console()

    env_vars = ['vault_url', 'vault_token']
    if all(e in os.environ for e in env_vars):
        console.print(f"Vault environment variables [red bold]found[/red bold], getting vault url and token.")
        HCKV_URL = os.environ.get('vault_url')
        HCKV_TOKEN = os.environ.get('vault_token')
    else:
        while True:
            HCKV_URL = input(f"Please input the Hashicorp Key vault URL, for example http://localhost:8200: ")
            HCKV_TOKEN = getpass(f"Please input your Hashicorp Key vault authentication token: ")
            break

    HCKV_data = {
        "HCKV_URL" : HCKV_URL,
        "HCKV_TOKEN" : HCKV_TOKEN,
    }

    return HCKV_data


def get_nr_from_NB() -> tuple:
    """
    Initializes Nornir with inventory data from Nautobot.

    Configures Nornir with Nautobot inventory and handles credential retrieval from either Nautobot or standard input.

    Returns:
        tuple: A tuple containing the Nautobot API object and the Nornir object
    """
    from nornir import InitNornir
    import json

    nautobot_data = get_nautobot_data()
    nautobot_url = nautobot_data['nautobot_url']
    nautobot_token = nautobot_data['nautobot_token']
    filter_parameters_string = nautobot_data['nautobot_query_filter']
    filter_parameters = json.loads(filter_parameters_string)
    query_filter_list = []
    for filter_key, filter_value in filter_parameters.items():
        query_filter_list.append(f"{filter_key} : \"{filter_value}\"")
    query_filter = ", ".join(query_filter_list)

    nautobot = init_nautobot(nautobot_url,nautobot_token)
    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 50,
            },
        },
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": nautobot_url,
                "nautobot_token": nautobot_token.split(" ")[-1],
                "filter_parameters": filter_parameters,
            },
        },
    )

    credentials_from_NB_or_stdin = get_credentials_from_NB_or_stdin()
    
    if credentials_from_NB_or_stdin == "1":
        HCKV_data = get_HCKV_data()
        HCKV_URL = HCKV_data["HCKV_URL"]
        HCKV_TOKEN = HCKV_data["HCKV_TOKEN"]

        hc_secrets_group_parameters_dict = get_hc_secrets_group_parameters_dict(nr,nautobot)
        secret_group_name_credentials_dict = get_credentials_from_HCKV(HCKV_TOKEN,HCKV_URL,hc_secrets_group_parameters_dict)

        for host in nr.inventory.dict()['hosts']:
            if nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']:
                secrets_group_name = nr.inventory.dict()['hosts'][host]['data']['pynautobot_dictionary']['secrets_group']['name']
                nr.inventory.hosts[host].username = secret_group_name_credentials_dict[secrets_group_name]['username']
                nr.inventory.hosts[host].password = secret_group_name_credentials_dict[secrets_group_name]['password']

    elif credentials_from_NB_or_stdin == "2":
        username, password = get_credentials()

        for host in nr.inventory.dict()['hosts']:
            nr.inventory.hosts[host].username = username
            nr.inventory.hosts[host].password = password

    return nautobot, nr


def get_nr_from_excel() -> tuple:
    """
    Initializes Nornir with inventory data from an Excel file.

    Prompts the user for workbook selection and configures Nornir with Excel inventory.

    Returns:
        tuple: A tuple containing the Nornir object, workbook, workbook name, workbook folder, device worksheet name, and workbook path
    """
    from nornir import InitNornir
    import os

    if not os.path.exists("parameters"):
        os.mkdir("parameters")

    default_folder = "parameters"
    workbook, workbookname, workbookfolder = get_workbook(default_folder)
    deviceworksheet = get_device_worksheet(workbook)
    workbookpath = (f"{workbookfolder}/{workbookname}")

    nr = InitNornir(
        logging={"enabled": False},
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 50
            }
        },
        inventory={
            "plugin": "ExcelInventory",
            "options":
            {
                "excel_file": workbookpath,
                "excel_sheet": deviceworksheet

            }
        })

    username, password = get_credentials()


    for host in nr.inventory.dict()['hosts']:
        if username:
            nr.inventory.hosts[host].username = username
        if password:
            nr.inventory.hosts[host].password = password

    return nr, workbook, workbookname, workbookfolder, deviceworksheet, workbookpath
