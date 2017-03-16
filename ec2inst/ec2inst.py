#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import boto3
from collections import defaultdict


def colorize_str(s, color):
    if color == "green":
        output_str = "\033[32m" + s + "\033[0m"
    elif color == "red":
        output_str = "\033[31m" + s + "\033[0m"
    elif color == "yellow":
        output_str = "\033[33m" + s + "\033[0m"
    elif color == "blue":
        output_str = "\033[34m" + s + "\033[0m"
    else:
        output_str = s
    return output_str


def make_instance_list(response, columns):
    output = defaultdict(list)
    for instance_unit in response["Reservations"]:
        instance = defaultdict(lambda: "-", instance_unit["Instances"][0])

        if "Tags" in instance.keys():
            instance_name = instance["Tags"][0]["Value"]
            for tag in instance["Tags"]:
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]
        else:
            instance_name = "-"
        instance_id = instance["InstanceId"]
        instance_type = instance["InstanceType"]
        availability_zone = instance["Placement"]["AvailabilityZone"]
        instance_state = instance["State"]["Name"]
        public_dns_name = instance["PublicDnsName"]
        public_ip_address = instance["PublicIpAddress"]
        private_ip_address = instance["PrivateIpAddress"]
        key_name = instance["KeyName"]
        monitoring = instance["Monitoring"]["State"]
        launch_time = instance["LaunchTime"].strftime("%Y/%m/%d %H:%M:%S")
        security_group = ",".join([g["GroupName"]
                                   for g in instance["SecurityGroups"]])

        image_id = instance["ImageId"]
        instance_state_code = str(instance["State"]["Code"])

        for column in columns:
            output[column].append(eval(column))
    return output


def prettyprint_table(d, columns):
    output = []
    max_len = {}
    for k, v in d.items():
        max_len[k] = max([len(s) for s in v] + [len(k)])

    # header and boarder
    output_column = ""
    output_hr = ""
    for column in columns:
        output_column += column.ljust(max_len[column], " ") + "  "
        output_hr += "-" * max_len[column] + "  "
    output.append(output_column)
    output.append(output_hr)

    for i in range(0, len(d[columns[0]])):
        output_line = ""
        for column in columns:
            if column != "instance_state":
                output_line += d[column][i].ljust(max_len[column], " ") + "  "
            else:
                # http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html
                state = d[column][i].ljust(max_len[column], " ")
                if d[column][i] == "running":
                    output_line += colorize_str(state, "green")
                elif d[column][i] in ["stopped", "terminated"]:
                    output_line += colorize_str(state, "red")
                elif d[column][i] in ["pending", "stopping", "shutting-down"]:
                    output_line += colorize_str(state, "yellow")
                elif d[column][i] == "rebooting":
                    output_line += colorize_str(state, "blue")
                else:
                    output_line += output_line
        output.append(output_line)

    for o in output:
        print(o)


def main():
    column_name_list = [
        "instance_name",
        "instance_id",
        "instance_type",
        "availability_zone",
        "instance_state",
        "instance_state_code",
        "public_dns_name",
        "public_ip_address",
        "private_ip_address",
        "key_name",
        "monitoring",
        "launch_time",
        "security_group",
        "image_id",
    ]

    default_column_names = ["instance_id",
                            "instance_type",
                            "image_id",
                            "instance_name",
                            "public_ip_address",
                            "private_ip_address",
                            "instance_state",
                            ]

    # argparse
    parser = argparse.ArgumentParser(
        description="AWS EC2 instance console for CLI")
    parser.add_argument("-p", "--profile",
                        help="select profile_name in ~/.aws/credentials")
    parser.add_argument("-c", "--columns",
                        default=",".join(default_column_names),
                        help="columns to display:  " + ",".join(column_name_list))
    args = parser.parse_args()
    show_column_names = args.columns.split(",")

    # boto3 connection
    if args.profile:
        session = boto3.Session(profile_name=args.profile)
        aws_client = session.client("ec2")
    else:
        aws_client = boto3.client("ec2")
    response = aws_client.describe_instances()

    # output
    instance_list = make_instance_list(response, show_column_names)
    prettyprint_table(instance_list, show_column_names)


if __name__ == "__main__":
    main()
