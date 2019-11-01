import configparser
import random

from fabric import task
from patchwork.files import append, exists

config = configparser.ConfigParser()
config.read('config.ini')


@task
def deploy(connection):
    site_folder = '/home/{}/sites/{}'.format(connection.user, connection.host)
    source_folder = site_folder + '/source'
    # create_directory_structure_if_necessary
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        connection.run('mkdir -p {}/{}'.format(site_folder, subfolder))
    # add ssh key to github
    if not exists(connection, '~/.ssh/id_rsa.pub'):
        connection.run('ssh-keygen -t rsa -b 4096 -C "{}"'.format(config['github']['Email']))
    connection.run(
        ('curl -u "{username}:{password}" '
         '--data "{{\\"title\\":\\"{host}\\",\\"key\\":\\"`cat ~/.ssh/id_rsa.pub`\\"}}" '
         'https://api.github.com/user/keys').format(
             username=config['github']['Username'],
             password=config['github']['Password'],
             host=connection.host)
    )
    connection.run('ssh-keyscan github.com >> ~/.ssh/known_hosts')
    # get_latest_source
    if exists(connection, source_folder + '/.git'):
        connection.run('cd {} && git fetch'.format(source_folder))
    else:
        connection.run('git clone {} {}'.format(config['github']['Repo'], source_folder))
    current_commit = connection.local('git log -n 1 --format=%H')
    connection.run('cd {} && git reset --hard {}'.format(source_folder, current_commit.stdout))
    #  update_settings
    settings_path = source_folder + '/superlists/settings.py'
    connection.run('sed "s/DEBUG = True/DEBUG=False/" {}'.format(settings_path))
    connection.run('sed "s/ALLOWED_HOSTS = .+$/ALLOWED_HOSTS = [{}]/" {}'.format(connection.host, settings_path))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(connection, secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(connection, secret_key_file, 'SECRET_KEY = "{}"'.format(key))
    append(connection, settings_path, '\nfrom .secret_key import SECRET_KEY')
    #  update_virtualenv
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(connection, virtualenv_folder + '/bin/pip'):
        connection.run('virtualenv --python=python3 {}'.format(virtualenv_folder))
    connection.run('{}/bin/pip install -r {}/requirements.txt'.format(virtualenv_folder, source_folder))
    #  update_static_files
    connection.run('cd {} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(source_folder))
    #  update_database
    connection.run('cd {} && ../virtualenv/bin/python3 manage.py migrate --noinput'.format(source_folder))
    # start nginx
    connection.run('sudo apt-get install -y nginx')
    connection.run(
        'cd {} && sed "s/SITENAME/mm.mmflow.online/g" deploy_tools/nginx.template.conf '.format(source_folder)
        + '| sudo tee /etc/nginx/sites-available/mm.mmflow.online')
    if not exists(connection, '/etc/nginx/sites-enabled/mm.mmflow.online'):
        connection.run('sudo ln -s /etc/nginx/sites-available/mm.mmflow.online '.format(source_folder)
                       + '/etc/nginx/sites-enabled/mm.mmflow.online')
    connection.run('sudo service nginx start')
    connection.run('sudo service nginx reload')
    # start gunicorn
    connection.run(
        'cd {} && sed "s/SITENAME/mm.mmflow.online/g" '.format(source_folder)
        + 'deploy_tools/gunicorn-systemd.template.service | '
        + 'sudo tee /lib/systemd/system/gunicorn-mm.mmflow.online.service')
    connection.run('sudo systemctl restart gunicorn-mm.mmflow.online')
