"""Urls for nautobot_dns_records."""

from django.urls import path

from nautobot_dns_records.views import (
    addressrecord,
    txtrecord,
    locrecord,
    cnamerecord,
    ptrrecord,
    sshfprecord,
    device_tab,
    srvrecord,
    ipaddress_tab,
)

urlpatterns = [
    # Address Record
    path("address_record/", addressrecord.AddressRecordsListView.as_view(), name="addressrecord_list"),
    path("address_record/add/", addressrecord.AddressRecordEditView.as_view(), name="addressrecord_add"),
    path("address_record/<uuid:pk>/", addressrecord.AddressRecordView.as_view(), name="addressrecord"),
    path("address_record/<uuid:pk>/edit/", addressrecord.AddressRecordEditView.as_view(), name="addressrecord_edit"),
    path(
        "address_record/<uuid:pk>/delete/", addressrecord.AddressRecordDeleteView.as_view(), name="addressrecord_delete"
    ),
    # TXT Record
    path("txt_record/", txtrecord.TxtRecordsListView.as_view(), name="txtrecord_list"),
    path("txt_record/add/", txtrecord.TxtRecordEditView.as_view(), name="txtrecord_add"),
    path("txt_record/<uuid:pk>/", txtrecord.TxtRecordView.as_view(), name="txtrecord"),
    path("txt_record/<uuid:pk>/edit/", txtrecord.TxtRecordEditView.as_view(), name="txtrecord_edit"),
    path("txt_record/<uuid:pk>/delete/", txtrecord.TxtRecordDeleteView.as_view(), name="txtrecord_delete"),
    # LOC Record
    path("loc_record/", locrecord.LocRecordsListView.as_view(), name="locrecord_list"),
    path("loc_record/add/", locrecord.LocRecordEditView.as_view(), name="locrecord_add"),
    path("loc_record/<uuid:pk>/", locrecord.LocRecordView.as_view(), name="locrecord"),
    path("loc_record/<uuid:pk>/edit/", locrecord.LocRecordEditView.as_view(), name="locrecord_edit"),
    path("loc_record/<uuid:pk>/delet/", locrecord.LocRecordDeleteView.as_view(), name="locrecord_delete"),
    # CNAME Record
    path("cname_record/", cnamerecord.CnameRecordsListView.as_view(), name="cnamerecord_list"),
    path("cname_record/add/", cnamerecord.CnameRecordEditView.as_view(), name="cnamerecord_add"),
    path("cname_record/<uuid:pk>/", cnamerecord.CnameRecordView.as_view(), name="cnamerecord"),
    path("cname_record/<uuid:pk>/edit/", cnamerecord.CnameRecordEditView.as_view(), name="cnamerecord_edit"),
    path("cname_record/<uuid:pk>/delete/", cnamerecord.CnameRecordDeleteView.as_view(), name="cnamerecord_delete"),
    # PTR Record
    path("ptr_record/", ptrrecord.PtrRecordsListView.as_view(), name="ptrrecord_list"),
    path("ptr_record/add/", ptrrecord.PtrRecordEditView.as_view(), name="ptrrecord_add"),
    path("ptr_record/<uuid:pk>/", ptrrecord.PtrRecordView.as_view(), name="ptrrecord"),
    path("ptr_record/<uuid:pk>/edit/", ptrrecord.PtrRecordEditView.as_view(), name="ptrrecord_edit"),
    path("ptr_record/<uuid:pk>/delete/", ptrrecord.PtrRecordDeleteView.as_view(), name="ptrrecord_delete"),
    # SSHFP Record
    path("sshfp_record/", sshfprecord.SshfpRecordsListView.as_view(), name="sshfprecord_list"),
    path("sshfp_record/add/", sshfprecord.SshfpRecordEditView.as_view(), name="sshfprecord_add"),
    path("sshfp_record/<uuid:pk>/", sshfprecord.SshfpRecordView.as_view(), name="sshfprecord"),
    path("sshfp_record/<uuid:pk>/edit/", sshfprecord.SshfpRecordEditView.as_view(), name="sshfprecord_edit"),
    path("sshfp_record/<uuid:pk>/delete/", sshfprecord.SshfpRecordDeleteView.as_view(), name="sshfprecord_delete"),
    # SRV Record
    path("srv_record/", srvrecord.SrvRecordsListView.as_view(), name="srvrecord_list"),
    path("srvfp_record/add/", srvrecord.SrvRecordEditView.as_view(), name="srvrecord_add"),
    path("srvfp_record/<uuid:pk>/", srvrecord.SrvRecordView.as_view(), name="srvrecord"),
    path("srvfp_record/<uuid:pk>/edit/", srvrecord.SrvRecordEditView.as_view(), name="srvrecord_edit"),
    path("srvfp_record/<uuid:pk>/delete/", srvrecord.SrvRecordDeleteView.as_view(), name="srvrecord_delete"),
    # Custom Tabs
    path("devices/<uuid:pk>/records/", device_tab.DeviceRecordsTab.as_view(), name="device_records_tab"),
    path("ip-addresses/<uuid:pk>/records/", ipaddress_tab.IpAddressRecordsTab.as_view(), name="address_records_tab"),
]
