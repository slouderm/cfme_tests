
import pytest
import random
from cfme.fixtures import pytest_selenium as sel
from cfme.infrastructure.virtual_machines import Vm
from utils import testgen
from utils.conf import cfme_data
from utils.providers import setup_provider
from utils.randomness import generate_random_string
from utils.log import logger
from utils.ssh import SSHClient
from utils.wait import wait_for

# GLOBAL vars
random_vm_test = []    # use the same values(provider/vm) for all the quadicon tests


def pytest_generate_tests(metafunc):
    # Filter out providers without provisioning data or hosts defined
    argnames, argvalues, idlist = testgen.infra_providers(metafunc, 'provider_key')
    for i, argvalue_tuple in enumerate(argvalues):
        provider_data = cfme_data['management_systems'][
            argvalue_tuple[argnames.index('provider_key')]]
        if provider_data.get('type', False) != 'virtualcenter':
            continue

    if 'random_snpsht_mgt_vm' in metafunc.fixturenames:
        if random_vm_test:
            argnames, new_argvalues, new_idlist = random_vm_test
        else:
            single_index = random.choice(range(len(idlist)))
            new_idlist = [idlist[single_index]]
            new_argvalues = argvalues[single_index]
            argnames.append('random_snpsht_mgt_vm')
            new_argvalues.append('')
            new_argvalues = [new_argvalues]
            random_vm_test.append(argnames)
            random_vm_test.append(new_argvalues)
            random_vm_test.append(new_idlist)
    else:
        new_idlist = idlist
        new_argvalues = argvalues
    testgen.parametrize(metafunc, argnames, new_argvalues, ids=new_idlist, scope="module")


@pytest.fixture(scope="module")
def provider_init(provider_key):
    """cfme/infrastructure/provider.py provider object."""
    try:
        setup_provider(provider_key)
    except Exception as e:
        pytest.skip("Skipping,because it's not possible to set up this provider({})".format(str(e)))


@pytest.fixture(scope="module")
def vm_name():
    return "test_snpsht_" + generate_random_string()


@pytest.fixture(scope="module")
def test_vm(request, provider_init, provider_crud, provider_mgmt, vm_name):
    '''Fixture to provision appliance to the provider being tested if necessary'''
    vm = Vm(vm_name, provider_crud)

    if not provider_mgmt.does_vm_exist(vm_name):
        vm.create_on_provider()
    return vm


def new_snapshot(test_vm):
    new_snapshot = Vm.Snapshot(name="snpshot_" + generate_random_string(), description="snapshot",
                        memory=False, parent_vm=test_vm)
    return new_snapshot


@pytest.mark.usefixtures("random_snpsht_mgt_vm")
def test_snapshot_crud(test_vm, provider_key):
        snapshot = new_snapshot(test_vm)
        snapshot.create()
        snapshot.delete()


def test_delete_all_snapshots(test_vm, provider_key):
        snapshot1 = new_snapshot(test_vm)
        snapshot1.create()
        snapshot2 = new_snapshot(test_vm)
        snapshot2.create()
        snapshot2.delete_all()


def test_verify_revert_snapshot(test_vm, provider_key, soft_assert, register_event, request):
        snapshot1 = new_snapshot(test_vm)
        ip = snapshot1.vm.provider_crud.get_mgmt_system().get_ip_address(snapshot1.vm.name)
        print ip
        ssh_kwargs = {
            'username': 'root',
            'password': 'redhat',
            'hostname': ip
        }
        ssh = SSHClient(**ssh_kwargs)
        ssh.run_command('touch snapshot1.txt')
        snapshot1.create()
        ssh.run_command('touch snapshot2.txt')
        snapshot2 = new_snapshot(test_vm)
        snapshot2.create()
        snapshot1.revert_to()
        # Wait for the snapshot to become active
        logger.info('Waiting for vm %s to become active', snapshot1.name)
        wait_for(snapshot1.wait_for_snapshot_active, num_sec=300, delay=20, fail_func=sel.refresh)
        test_vm.wait_for_vm_state_change(desired_state=Vm.STATE_OFF, timeout=720)
        register_event(
            test_vm.provider_crud.get_yaml_data()['type'],
            "vm", test_vm.name, ["vm_power_on_req", "vm_power_on"])
        test_vm.power_control_from_cfme(option=Vm.POWER_ON, cancel=False)
        pytest.sel.force_navigate(
            'infrastructure_provider', context={'provider': test_vm.provider_crud})
        test_vm.wait_for_vm_state_change(desired_state=Vm.STATE_ON, timeout=900)
        soft_assert(test_vm.find_quadicon().state == 'currentstate-on')
        soft_assert(
            test_vm.provider_crud.get_mgmt_system().is_vm_running(test_vm.name), "vm not running")
        client = SSHClient(**ssh_kwargs)
        status, out = client.run_command('test -e snapshot2.txt')
        if status != 0:
            logger.info('Revert to snapshot %s successful', snapshot1.name)
        else:
            logger.info('Revert to snapshot %s Failed', snapshot1.name)
        request.addfinalizer(test_vm.delete_from_provider)
