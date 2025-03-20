import click
import argparse
import os
import subprocess
import signal

import itertools
import threading
import time
import sys

from .general import sync_policies, sync_profiles_from_tar, check_cinc_installed, check_saf_installed
from .static import static_analysis
from .vm import run_stig_over_ssh
from .runtime import runtime_analysis, saf_convert_output
from .inputs import collect_inputs, runtime_get_image_digest, get_runtime_cluster
from .provision import install_cinc, install_train_plugin
from .generate import generate_input_file
from .review import validate_file, create_output_rollup
from anchorestig import __version__

@click.group()
def main():
    pass


@click.command()
@click.option('--username', '-u', help='Username for private registry')
@click.option('--password', '-p', help="Password for private registry")
@click.option('--url', '-r', help="URL for private registry")
@click.option('--aws-bucket', '-b', help="S3 upload. Specify bucket name")
@click.option('--account', '-a', help="Anchore STIG UI account. Required for S3 upload")
@click.option('--insecure', '-s', is_flag=True, default=False, help="Allow insecure registries or registries with custom certs")
@click.option('--profile', '-l', default="auto", help="Specify profile to run. Can be the name of an existing profile or the path to a custom profile")
@click.option('--input-file', '-i', help="Specify the path to a custom input file to run with a profile.")
@click.option('--sync', '-y', is_flag=True, default=False, help="Sync policies from Anchore")
@click.option('--sync-from-file', '-t', help="Sync policies from tar file provided by Anchore. Provide the path to the tar file.")
@click.argument('image')
def static(username, password, url, insecure, image, aws_bucket, account, profile, input_file, sync, sync_from_file):
    """Run static analysis"""
    if sync:
        sync_policies()
        print("Policies successfully downloaded.")
    if sync_from_file:
        sync_profiles_from_tar(sync_from_file)
        print("Policies successfully updated.")
    check_cinc_installed()
    check_saf_installed()
    if not input_file:
        input_file = "default"
    done = False
    def animate():
        print('Running STIG')
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\r' + c)
            sys.stdout.flush
            time.sleep(0.1)
        sys.stdout.write('\rDone!     ')
    t = threading.Thread(target=animate)
    t.start()
    aws = aws_bucket
    static_analysis(username, password, url, insecure, image, aws, account, profile, input_file)
    done = True

@click.command()
@click.option("--image", "-i", help="Specify profile to use. Available options are ubuntu-20.04, ubuntu-22.04, ubi8, ubi9, postgres9, apache-tomcat9, crunchy-postgresql, jboss, jre7, mongodb, nginx")
@click.option("--pod", "-p", help="Any running pod running an image that runs one of the specififed profile's software")
@click.option("--container", "-c", help="Container in the pod to run against")
@click.option("--outfile", "-o", help="Output file name. Only JSON output filetype is supported (include the '.json' extension with the output file name in CLI)")
@click.option("--namespace", "-n", help="Namespace the pod is located in")
@click.option("--usecontext", "-u", help="Specify the kubernetes context to use")
@click.option("--aws-bucket", "-b", help="Specify the S3 bucket to upload results to. Omit to skip upload")
@click.option("--account", "-a", help="Specify the Anchore STIG UI account to associate the S3 upload with. Omit to skip upload")
@click.option('--interactive', '-t', is_flag=True, default=False, help="Run in interactive mode")
@click.option('--input-file', '-f', help="Specify the path to a custom input file to run with a profile.")
@click.option('--sync', '-s', is_flag=True, default=False, help="Sync policies from Anchore")
@click.option('--sync-from-file', '-y', help="Sync policies from tar file provided by Anchore. Provide the path to the tar file.")
def runtime(image, pod, container, outfile, namespace, usecontext, aws_bucket, account, interactive, input_file, sync, sync_from_file):
    """Run runtime analysis"""
    print("Runtime Analysis")
    aws = aws_bucket
    if not aws:
        aws = "skip_upload"
    if not account:
        account = "skip_upload"
    if sync:
        sync_policies()
        print("Policies successfully downloaded.")
        if not interactive or not pod or not container:
            return
    if sync_from_file:
        sync_profiles_from_tar(sync_from_file)
        print("Policies successfully updated.")
        if not interactive or not pod or not container:
            return
    check_saf_installed()
    if interactive == True:
        input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name = collect_inputs()
        input_outfile = f"{input_outfile.rsplit('.', 1)[0]}/{input_outfile}"
        runtime_analysis(input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name)
    else:
        input_image_digest, input_image_name = runtime_get_image_digest(pod, namespace, container)
        input_cluster = get_runtime_cluster(usecontext)
        input_image, input_pod, input_container, input_namespace, input_usecontext, input_outfile, input_aws_s3_bucket_upload, input_account = image, pod, container, namespace, usecontext, outfile, aws, account
        input_outfile = f"{input_outfile.rsplit('.', 1)[0]}/{input_outfile}"
        runtime_analysis(input_image, input_pod, input_container, input_namespace, input_usecontext, input_cluster, input_outfile, input_aws_s3_bucket_upload, input_account, input_image_digest, input_image_name)
    saf_convert_output(input_outfile)

@click.command()
@click.option('--user', '-u', help='Username for SSH Host', required=True)
@click.option('--password', '-p', default="usekey", help="Password for SSH Host")
@click.option('--key', '-k', default="nokey", help="PEM Key path for SSH Host")
@click.option('--host', '-h', help='Username for SSH Host', required=True)
@click.option('--profile', '-l', default="indeterminate", help="Specify profile to run. Can be the name of an existing profile or the path to a custom profile. Existing profile are Available options are ubuntu2004, ubuntu2204, ubi8, ubi9, postgres9, apache-tomcat9, crunchy-postgresql, jboss, jre7, mongodb, nginx", required=True)
@click.option('--input-file', '-i', help="Specify the path to a custom input file to run with a profile.")
def vm(user, password, key, host, profile, input_file):
    """Run vm analysis"""
    if not input_file:
        input_file = "default"
    done = False
    def animate():
        print('Running STIG')
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\r' + c)
            sys.stdout.flush
            time.sleep(0.1)
        sys.stdout.write('\rDone!     ')
    t = threading.Thread(target=animate)
    t.start()
    run_stig_over_ssh(profile, input_file, host, user, password, key)
    done = True

@click.command()
@click.option('--install', '-i', is_flag=True, default=False, help="Install the necessary version of CINC")
@click.option("--privileged", "-s", is_flag=True, default=False, help="Install CINC with sudo.")
@click.option("--plugin", "-p", is_flag=True, default=False, help="Install the CINC Train K8S Plugin")
def provision(install, privileged, plugin):
    """Install required tools - Please note this tool is experimental. Refer to documentation for instructions about installing required tooling."""
    if install:
        install_cinc(privileged)
    if plugin:
        install_train_plugin()

@click.command()
@click.argument('profile_name', required=False)
def generate(profile_name):
    """Generate an example inputs file. Note: the generated file will be the default file used if no input file is specified."""
    profile_list = """
    Profile name required. Please specify one of the following as an argument.
    Available profile names:
    apache-tomcat9
    crunchy-postgresql
    jboss
    jre7
    mongodb
    nginx
    postgres9
    ubi8
    ubi9
    ubuntu2004
    ubuntu2204
    """
    available_profiles = ["apache-tomcat9", "crunchy-postgresql", "jboss", "jre7", "mongodb", "nginx", "postgres9", "ubi8", "ubi9", "ubuntu2004", "ubuntu2204"]
    if not profile_name:
        print(profile_list)
    elif profile_name not in available_profiles:
        print(profile_list)
    else:
        generate_input_file(profile_name)

@click.command()
@click.argument('output_file_path', required=True)
def review(output_file_path):
    """Generates an in-terminal rollup of a STIG result file"""
    valid_file = validate_file(output_file_path)
    if not valid_file:
        print("Input file is not valid, please try again.")
        exit()
    else:
        create_output_rollup(output_file_path)

@click.command()
def version():
    """Print the current version of Anchore STIG"""
    print(__version__)

main.add_command(static)
main.add_command(runtime)
main.add_command(provision)
main.add_command(vm)
main.add_command(generate)
main.add_command(version)
main.add_command(review)

if __name__ == '__main__':
    main()
