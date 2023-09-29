#!/usr/bin/env python3

import pprint 
import sys

import salt.client

client = salt.client.LocalClient()

test_data ={
    'test_blobstore': {
        'inputs': [],
        'results': {
            'type': 'File'
        },
    },
    'test_s3_blobstore': {
        'inputs': [
            'store_type=s3',
            's3_bucket=nexus3',
            's3_accessKeyId=AKIAIOSFODNN7EXAMPLE',
            's3_secretAccessKey=wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY',
            's3_endpoint=http://minio:9000',
            's3_forcePathStyle=True'
        ],
        'results': {
            'type': 'S3'
        },
    },
}


def main():
    blobstores = []

    for name, values in test_data.items():
        # print(" Creating blobstore {}".format(name))
        try:
            create_blobstore(name, values)
            blobstores.append(name)
        except:
            print(" Failed creating blobstore {}".format(name))

    list_blobstores(len(blobstores))

    for name in blobstores:
        # print(" Deleting blobstore {}".format(name))
        delete_blobstore(name)

    # print(" Running blobstore states")
    blobstores_state()


def create_blobstore(name, values):
    list1 = [name]
    args = list1 + values['inputs']

    ret = client.cmd('test.minion', 'nexus3_blobstores.create', args)
    # print(ret)
    assert ret['test.minion']['blobstore'] != {},'blobstore is empty'
    assert ret['test.minion']['blobstore']['name'] == name,'blobstore {} not created'.format(name)
    assert ret['test.minion']['blobstore']['type'] == values['results']['type'],'wrong store type {} found'.format(values['results']['type'])


def delete_blobstore(blobstore):
    ret = client.cmd('test.minion', 'nexus3_blobstores.delete', ['name={}'.format(blobstore)])
    # print(ret)
    assert ret['test.minion']['comment'] == 'Deleted blobstore "{}"'.format(blobstore),'blobstore {} not deleted'.format(blobstore)


def list_blobstores(count):
    ret = client.cmd('test.minion', 'nexus3_blobstores.list_all')
    # print(ret)
    assert ret['test.minion']['blobstores'] != {},'data is empty'


def blobstores_state():
    pillar = {
        "nexus": {
            "blobstores": {
                "apt": [],
                "docker": [],
                "maven": [
                    {"quota_type": "spaceRemainingQuota"},
                    {"quota_limit": 1000000000}
                ],
                "s3blobstore": [
                    {"store_type": "s3"},
                    {"s3_bucket": "nexus3"},
                    {"s3_accessKeyId": "AKIAIOSFODNN7EXAMPLE"},
                    {"s3_secretAccessKey": "wJalrXUtnFEMIK7MDENGbPxRfiCYEXAMPLEKEY"},
                    {"s3_endpoint": "http://minio:9000"},
                    {"s3_forcePathStyle": True}
                ],
                "yum": []
            },
        }
    }

    pillar_update = {
        "nexus": {
            "blobstores": {
                "maven": [
                    {"quota_type": "spaceRemainingQuota"},
                    {"quota_limit": 2000000000}
                ],
            },
        }
    }
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(pillar)
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.blobstores', f'pillar={pillar}'])
    # pp.pprint(ret['test.minion'])
    validate_return(ret)

    # pp.pprint(pillar_update)
    ret = client.cmd('test.minion', 'state.apply', ['nexus3.blobstores', 'pillar={}'.format(pillar_update), 'test=True'])
    # pp.pprint(ret['test.minion'])

    # clean up
    for blobstore in pillar['nexus']['blobstores']:
        delete_blobstore(blobstore)


def validate_return(ret):
    pp = pprint.PrettyPrinter(indent=2)

    try:
        for key, value in ret['test.minion'].items():
            if value['result']:
                continue

            print("state failure occurred")
            print("state name: '{}'\nreturn value:").format(key)
            pp.pprint(value)
            sys.exit()

        # pp.pprint(ret)
    except Exception as e:
        print(e)
        pp.pprint(ret['test.minion'])


if __name__ == "__main__":
    main()
