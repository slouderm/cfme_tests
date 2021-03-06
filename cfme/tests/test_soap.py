#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pytest
from random import choice

from utils import testgen
from utils.miq_soap import MiqVM, set_client
from utils.randomness import generate_random_string


@pytest.mark.usefixtures("setup_infrastructure_providers")
class TestSoapBasicInteraction(object):
    def test_connectivity(self, soap_client):
        assert soap_client.service.EVMPing(), "Could not do EVMPing()!"

    def test_evm_host_list(self, soap_client):
        assert isinstance(soap_client.service.EVMHostList(), list)

    def test_evm_vm_list(self, soap_client):
        assert isinstance(soap_client.service.EVMVmList("*"), list)

    def test_evm_cluster_list(self, soap_client):
        assert isinstance(soap_client.service.EVMClusterList(), list)

    def test_evm_resource_pool_list(self, soap_client):
        assert isinstance(soap_client.service.EVMResourcePoolList(), list)

    def test_evm_datastore_list(self, soap_client):
        assert isinstance(soap_client.service.EVMDatastoreList(), list)

    def test_get_ems_list(self, soap_client):
        assert isinstance(soap_client.service.GetEmsList(), list)

    def test_version(self, soap_client):
        assert isinstance(soap_client.service.Version(), list)

    @pytest.mark.bugzilla(1096768)
    def test_get_hosts_from_ems(self, soap_client):
        for ems in soap_client.service.GetEmsList():
            assert isinstance(soap_client.service.EVMGetHosts(ems.guid), list)

    def test_get_host(self, soap_client):
        for host in soap_client.service.EVMHostList():
            get_host = soap_client.service.EVMGetHost(host.guid)
            assert get_host.guid == host.guid
            assert get_host.name == host.name

    @pytest.mark.bugzilla(1096768)
    def test_get_clusters_from_ems(self, soap_client):
        for ems in soap_client.service.GetEmsList():
            assert isinstance(soap_client.service.EVMGetClusters(ems.guid), list)

    @pytest.mark.bugzilla(1096708)
    def test_get_cluster(self, soap_client):
        for cluster in soap_client.service.EVMClusterList():
            get_cluster = soap_client.service.EVMGetCluster(cluster.id)
            assert get_cluster.id == cluster.id
            assert get_cluster.name == cluster.name

    @pytest.mark.bugzilla(1096768)
    def test_get_resource_pools_from_ems(self, soap_client):
        for ems in soap_client.service.GetEmsList():
            assert isinstance(soap_client.service.EVMGetResourcePools(ems.guid), list)

    @pytest.mark.bugzilla(1096708)
    def test_get_resource_pool(self, soap_client):
        for resource_pool in soap_client.service.EVMResourcePoolList():
            get_resource_pool = soap_client.service.EVMGetResourcePool(resource_pool.id)
            assert get_resource_pool.id == resource_pool.id
            assert get_resource_pool.name == resource_pool.name

    @pytest.mark.bugzilla(1096768)
    def test_get_datastores_from_ems(self, soap_client):
        for ems in soap_client.service.GetEmsList():
            assert isinstance(soap_client.service.EVMGetDatastores(ems.guid), list)

    @pytest.mark.bugzilla(1096708)
    def test_get_datastore(self, soap_client):
        for datastore in soap_client.service.EVMDatastoreList():
            get_datastore = soap_client.service.EVMGetDatastore(datastore.id)
            assert get_datastore.id == datastore.id
            assert get_datastore.name == datastore.name

    @pytest.mark.bugzilla(1096768)
    def test_get_vms_from_host(self, soap_client):
        host = choice(soap_client.service.EVMHostList())
        vms = soap_client.service.EVMGetVms(host.guid)
        assert isinstance(vms, list)
        for vm in vms:
            get_vm = soap_client.service.EVMGetVm(vm.guid)
            assert get_vm.guid == vm.guid
            assert get_vm.name == vm.name

    def test_get_host_list(self, soap_client):
        ems = choice(soap_client.service.GetEmsList())
        assert isinstance(soap_client.service.GetHostList(ems.guid), list)

    def test_get_cluster_list(self, soap_client):
        ems = choice(soap_client.service.GetEmsList())
        assert isinstance(soap_client.service.GetClusterList(ems.guid), list)

    def test_get_resource_pool_list(self, soap_client):
        ems = choice(soap_client.service.GetEmsList())
        assert isinstance(soap_client.service.GetResourcePoolList(ems.guid), list)

    def test_get_datastore_list(self, soap_client):
        ems = choice(soap_client.service.GetEmsList())
        assert isinstance(soap_client.service.GetDatastoreList(ems.guid), list)

    def test_get_vm_list(self, soap_client):
        host = choice(soap_client.service.EVMHostList())
        assert isinstance(soap_client.service.GetVmList(host.guid), list)

    def test_find_ems_by_guid(self, soap_client):
        ems = choice(soap_client.service.GetEmsList())
        get_ems = soap_client.service.FindEmsByGuid(ems.guid)
        assert get_ems.guid == ems.guid
        assert get_ems.name == ems.name

    def test_find_host_by_guid(self, soap_client):
        host = choice(soap_client.service.EVMHostList())
        get_host = soap_client.service.FindHostByGuid(host.guid)
        assert get_host.guid == host.guid
        assert get_host.name == host.name
        assert isinstance(soap_client.service.FindHostsByGuid(host.guid), list)

    def test_find_cluster_by_id(self, soap_client):
        cluster = choice(soap_client.service.EVMClusterList())
        get_cluster = soap_client.service.FindClusterById(cluster.id)
        assert get_cluster.id == cluster.id
        assert get_cluster.name == cluster.name
        assert isinstance(soap_client.service.FindClustersById(cluster.id), list)

    def test_find_datastore_by_id(self, soap_client):
        datastore = choice(soap_client.service.EVMDatastoreList())
        get_datastore = soap_client.service.FindDatastoreById(datastore.id)
        assert get_datastore.id == datastore.id
        assert get_datastore.name == datastore.name
        assert isinstance(soap_client.service.FindDatastoresById(datastore.id), list)

    def test_find_resource_pool_by_id(self, soap_client):
        resource_pool = choice(soap_client.service.EVMResourcePoolList())
        get_resource_pool = soap_client.service.FindResourcePoolById(resource_pool.id)
        assert get_resource_pool.id == resource_pool.id
        assert get_resource_pool.name == resource_pool.name
        assert isinstance(soap_client.service.FindResourcePoolsById(resource_pool.id), list)

    # Goes through hosts because EVMVmList does not work at all.
    def test_find_vm_by_guid(self, soap_client):
        vm = choice(soap_client.service.EVMVmList("*"))
        get_vm = soap_client.service.FindVmByGuid(vm.guid)
        assert get_vm.guid == vm.guid
        assert get_vm.name == vm.name
        assert isinstance(soap_client.service.FindVmsByGuid(vm.guid), list)

    # Goes through hosts because EVMVmList does not work at all.
    def test_evm_vm_software(self, soap_client):
        vm = choice(soap_client.service.EVMVmList("*"))
        assert isinstance(soap_client.service.EVMVmSoftware(vm.guid), list)

    # Goes through hosts because EVMVmList does not work at all.
    def test_evm_vm_accounts(self, soap_client):
        vm = choice(soap_client.service.EVMVmList("*"))
        assert isinstance(soap_client.service.EVMVmAccounts(vm.guid), list)

    def test_ems_tagging(self, soap_client):
        ems = choice(soap_client.service.GetEmsList())
        # Prepare (find the opposite tag if already tagged)
        cc = "001"
        for tag in soap_client.service.EmsGetTags(ems.guid):
            if tag.category == "cc":
                if tag.tag_name == cc:
                    cc = "002"
                break
        # Tag!
        soap_client.service.EmsSetTag(ems.guid, "cc", cc)
        for tag in soap_client.service.EmsGetTags(ems.guid):
            if tag.category == "cc" and tag.tag_name == cc:
                break
        else:
            pytest.fail("Could not find tags for Ems {}".format(ems.name))

    def test_cluster_tagging(self, soap_client):
        cluster = choice(soap_client.service.EVMClusterList())
        # Prepare (find the opposite tag if already tagged)
        cc = "001"
        for tag in soap_client.service.ClusterGetTags(cluster.id):
            if tag.category == "cc":
                if tag.tag_name == cc:
                    cc = "002"
                break
        # Tag!
        soap_client.service.ClusterSetTag(cluster.id, "cc", cc)
        for tag in soap_client.service.ClusterGetTags(cluster.id):
            if tag.category == "cc" and tag.tag_name == cc:
                break
        else:
            pytest.fail("Could not find tags for cluster {}".format(cluster.name))

    def test_datastore_tagging(self, soap_client):
        datastore = choice(soap_client.service.EVMDatastoreList())
        # Prepare (find the opposite tag if already tagged)
        cc = "001"
        for tag in soap_client.service.DatastoreGetTags(datastore.id):
            if tag.category == "cc":
                if tag.tag_name == cc:
                    cc = "002"
                break
        # Tag!
        soap_client.service.DatastoreSetTag(datastore.id, "cc", cc)
        for tag in soap_client.service.DatastoreGetTags(datastore.id):
            if tag.category == "cc" and tag.tag_name == cc:
                break
        else:
            pytest.fail("Could not find tags for datastore {}".format(datastore.name))

    def test_host_tagging(self, soap_client):
        host = choice(soap_client.service.EVMHostList())
        # Prepare (find the opposite tag if already tagged)
        cc = "001"
        for tag in soap_client.service.HostGetTags(host.guid):
            if tag.category == "cc":
                if tag.tag_name == cc:
                    cc = "002"
                break
        # Tag!
        soap_client.service.HostSetTag(host.guid, "cc", cc)
        for tag in soap_client.service.HostGetTags(host.guid):
            if tag.category == "cc" and tag.tag_name == cc:
                break
        else:
            pytest.fail("Could not find tags for host {}".format(host.name))

    def test_resource_pool_tagging(self, soap_client):
        pool = choice(soap_client.service.EVMResourcePoolList())
        # Prepare (find the opposite tag if already tagged)
        cc = "001"
        for tag in soap_client.service.ResourcePoolGetTags(pool.id):
            if tag.category == "cc":
                if tag.tag_name == cc:
                    cc = "002"
                break
        # Tag!
        soap_client.service.ResourcePoolSetTag(pool.id, "cc", cc)
        for tag in soap_client.service.ResourcePoolGetTags(pool.id):
            if tag.category == "cc" and tag.tag_name == cc:
                break
        else:
            pytest.fail("Could not find tags for pool {}".format(pool.name))

    def test_vm_tagging(self, soap_client):
        vm = choice(soap_client.service.EVMVmList("*"))
        # Prepare (find the opposite tag if already tagged)
        cc = "001"
        for tag in soap_client.service.VmGetTags(vm.guid):
            if tag.category == "cc":
                if tag.tag_name == cc:
                    cc = "002"
                break
        # Tag!
        soap_client.service.VmSetTag(vm.guid, "cc", cc)
        for tag in soap_client.service.VmGetTags(vm.guid):
            if tag.category == "cc" and tag.tag_name == cc:
                break
        else:
            pytest.fail("Could not find tags for vm {}".format(vm.name))

    # These are here as a placeholder to know what is not tested ...
    def test_EVM_delete_vm_by_name(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_smart_start(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_smart_stop(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_smart_suspend(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_get_policy(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_event_list(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_condition_list(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_action_list(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_policy_list(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_vm_rsop(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_assign_policy(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_unassign_policy(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_add_lifecycle_event(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_provision_request(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_provision_request_ex(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_host_provision_request(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_vm_scan_by_property(self, soap_client):
        pytest.skip("Not tested yet")

    def test_EVM_vm_event_by_property(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetEmsByList(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetHostsByList(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetClustersByList(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetDatastoresByList(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetResourcePoolsByList(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetVmsByList(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetVmsByTag(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetTemplatesByTag(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetClustersByTag(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetResourcePoolsByTag(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetDatastoresByTag(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmAddCustomAttributeByFields(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmAddCustomAttribute(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmAddCustomAttributes(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmDeleteCustomAttribute(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmDeleteCustomAttributes(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmProvisionRequest(self, soap_client):
        pytest.skip("Not tested yet")

    def test_VmSetOwner(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetVmProvisionRequest(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetVmProvisionTask(self, soap_client):
        pytest.skip("Not tested yet")

    def test_CreateAutomationRequest(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetAutomationRequest(self, soap_client):
        pytest.skip("Not tested yet")

    def test_GetAutomationTask(self, soap_client):
        pytest.skip("Not tested yet")


pytest_generate_tests = testgen.generate(
    testgen.infra_providers,
    "small_template",
    scope="module"
)


@pytest.mark.bugzilla(
    1118831, unskip={1118831: lambda appliance_version: appliance_version < "5.3"})
@pytest.mark.fixtureconf(server_roles="+automate")
@pytest.mark.usefixtures("setup_infrastructure_providers", "server_roles")
def test_provision_via_soap(
        request, soap_client, provider_key, provider_data, provider_mgmt, small_template):
    vm_name = "test_soap_provision_{}".format(generate_random_string())
    vlan = provider_data.get("provisioning", {}).get("vlan", None)

    def _cleanup():
        try:
            if provider_mgmt.does_vm_exist(vm_name):
                provider_mgmt.delete_vm(vm_name)
        except:
            pass

    request.addfinalizer(_cleanup)
    set_client(soap_client)
    vm = MiqVM.provision_from_template(small_template, vm_name, vlan=vlan, wait_min=10,)
    if vm.is_powered_on:
        vm.power_off()
    vm.power_on()
    assert vm.is_powered_on
    vm.power_off()
    assert vm.is_powered_off
