import os, sys, json, argparse, subprocess
import requests
import socket
import threading
import webbrowser
BMY_PATH_PROJECT = 'C:\\Users\\benme\\Desktop\\Projects'


def sparta_b5e0253c94(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f'Port {port} on {host} is open.')
        else:
            print(f'Port {port} on {host} is closed or unreachable.')


def sparta_1d36954957(port=9001) ->bool:
    """
    Check if spartaqube server is running
    """
    req = requests.get(f'http://localhost:{port}/heartbeat')
    res_dict = json.loads(req.text)
    if res_dict['res'] == 1:
        return True
    return False


def sparta_07ca586f10():
    return f'{BMY_PATH_PROJECT}\\spartaqube\\web\\venv\\Scripts\\activate.bat'


def sparta_f9b320dfdd(port):
    current_path = os.path.dirname(__file__)
    process = subprocess.Popen(
        f'{get_activate_cmd()} && python manage.py runserver {port} &',
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, cwd=
        current_path, env=os.environ.copy())
    while True:
        try:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
        except Exception as e:
            print(e)
            break


def sparta_3b84fd5154(port):
    server_thread = threading.Thread(target=start_django_application, args=
        (port,))
    server_thread.start()


def sparta_26cc4f9669():
    """
    npm run dev
    """
    current_path = os.path.dirname(__file__)
    cmd = 'npm run dev'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, cwd=current_path)
    stdout, stderr = process.communicate()
    print('npm run dev')
    print(stdout)
    print(stderr)


def sparta_d1de3351b4():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=str, help='Port', default=None)
    parser.add_argument('-npm', '--npm', type=str, help='Npm run dev',
        default=None)
    parser.add_argument('-mode', '--mode', type=str, help='Cypress mode',
        default=None)
    args = parser.parse_args()
    port_input = args.port
    npm_input = args.npm
    mode_input = args.mode
    if port_input is None:
        port = 9005
    else:
        port = int(port_input)
    os.environ['CYPRESS_TEST_PORT'] = str(port)
    os.environ['CYPRESS_TEST_APP'] = '1'
    if sparta_b5e0253c94('localhost', port):
        if not sparta_1d36954957(port):
            raise Exception(f'Spartaqube is not running on port {port}')
    else:
        sparta_3b84fd5154(port)
    if npm_input is not None:
        if str(npm_input).lower() == 'true':
            print('Call npm run dev')
            sparta_26cc4f9669()
    cmd_cypress = f'set CYPRESS_TEST_PORT={port} && npx cypress run --headed'
    is_reference_mode = False
    if mode_input is not None:
        if str(mode_input).lower() == 'reference':
            is_reference_mode = True
            cmd_cypress = (
                f'set CYPRESS_TEST_PORT={port} && npx cypress run --env mode=reference --headed'
                )
    print(f'Launch cypress now with cmd: {cmd_cypress}')
    current_path = os.path.dirname(__file__)
    process = subprocess.Popen(cmd_cypress, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_path, env=os.environ.copy()
        )
    stdout, stderr = process.communicate()
    print('cypress run:')
    print(stdout)
    print(stderr)
    if is_reference_mode:
        print('Open visual test on port http://localhost:6868')
        process = subprocess.Popen('node visual-test.ts &', shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=
            current_path, env=os.environ.copy())
        stdout, stderr = process.communicate()
        print('node visual test:')
        print(stdout)
        print(stderr)
        webbrowser.open('http://localhost:6868')
    else:
        print('--- End of tests ---')
        os._exit(0)


if __name__ == '__main__':
    sparta_d1de3351b4()

#END OF QUBE
