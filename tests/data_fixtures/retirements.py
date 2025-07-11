import datetime

from sc_audit.db_schema.retirement import Retirement

def get_retirements_whole_and_round_up():
    retirements = [
        Retirement(certificate_id=143471, vcu_amount=1, serial_number='8040-449402275-449402275-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2021, 11, 21), retirement_beneficiary='GAVF6ZB7Z7FKCWM5HEY2OV4ENPK3OSSHMFTVR4HHSBFHKW36U3FUH2CB', retirement_details='stellarcarbon.io 61d4ff5516b7098bbc2219d244e7f29a039c32735e1c16d1c05d66a0739727d9', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=152309, vcu_amount=1, serial_number='8040-449402276-449402276-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 9, 18), retirement_beneficiary='GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y via stellarcarbon.io', retirement_details='stellarcarbon.io 63f55c3ff92b239ecdb774c336cb91e896a3e4906a81cbeb23a60f20563c198f', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=152312, vcu_amount=1, serial_number='8040-449402277-449402277-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 12, 3), retirement_beneficiary='GBAQIUT26BTMG652R5RI5HM22UZ7KDHVM3VPZ4NXUZGR7FVN5KUP4TSA via stellarcarbon.io', retirement_details='stellarcarbon.io 40def47032e4ab8fc7f06b817ca58f354ee0ba590ac318377856e8658e512771', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=187116, vcu_amount=1, serial_number='8040-449402278-449402278-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 12, 3), retirement_beneficiary='GDL4YOQH5VH7EUYSW45QZNEBI5377WACZICSF3A7KL7AOGI5BSB54GTC via stellarcarbon.io', retirement_details='stellarcarbon.io 5af83162a018c92d669fe317dda1e5659bfb3a041a14bc4efa176fb382799a13', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=187117, vcu_amount=1, serial_number='8040-449402279-449402279-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 12, 3), retirement_beneficiary='GBIH7Z3SMZUX62JPLLDTHA3QEVMRCGUCUQVCFFRJTEGCKB4MV4NGU7BE via stellarcarbon.io', retirement_details='stellarcarbon.io c2f0ed42774091e1249f11af93d56be53af1aa24bc397d36f2fcbb0907475fb4', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=187118, vcu_amount=1, serial_number='8040-449402280-449402280-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 12, 3), retirement_beneficiary='GBIH7Z3SMZUX62JPLLDTHA3QEVMRCGUCUQVCFFRJTEGCKB4MV4NGU7BE via stellarcarbon.io', retirement_details='stellarcarbon.io 2827d90abd658986345f4c20cb68f1f29af128bccaa0d8743ce0248732a2b4fc', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=187119, vcu_amount=1, serial_number='8040-449402281-449402281-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 12, 12), retirement_beneficiary='GBBKODANH3RROGGDHDC6FLGY2P4Y2GKT53ULPW75ATCRJRGUKQIO7S7Z via stellarcarbon.io', retirement_details='stellarcarbon.io 0bb7cbdf0ccd7f3679009b69c1d323948236e312825920510b90cd6ee07383d5', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=187861, vcu_amount=1, serial_number='8040-449402282-449402282-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2022, 12, 17), retirement_beneficiary='GBN4VSSXH4C32W37GK54UXAXZPXK4QGKJFA62K5CJXPOXEKXPQJABD4T via stellarcarbon.io', retirement_details='stellarcarbon.io 7d982a3b39f1cf9ff80e08ad1a503561dd68d12336f2a04b5855f539c1e83fcf', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=188439, vcu_amount=9, serial_number='8040-449402283-449402291-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2023, 5, 7), retirement_beneficiary='GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y via stellarcarbon.io', retirement_details='stellarcarbon.io d58b08d1cbc27fe931752e4cfcbdfdcfc057b0bf1bd312b05a41c298b7c54f7e 263f997b4a2326df41ec2b346d79cbca4c06d2d72cff381620d39ca3ebe552f4 6854d5fc7690776dddba92fd0754e9f69ce7f5a3d3180373bc77d359d8e83d9f 063d8428b79a080eee39f5a8a39e4e199d43dbfe529a0b402ede160bb997b816 a36ffd373d153cf2e8fda674f5c9da9115d0322c29e1bad6a6c0b96030c09ed6 48d69bb7691c02df2ed5e79a89b7a89f5ae944409dc0450e59cefd5636d3cfc9 2ec3bb8fa3975ee46aa61ed14912c7c26d68e04fe293d388e3579807ec53282e', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=203703, vcu_amount=1, serial_number='8040-449402292-449402292-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2023, 5, 7), retirement_beneficiary='GBBKODANH3RROGGDHDC6FLGY2P4Y2GKT53ULPW75ATCRJRGUKQIO7S7Z via stellarcarbon.io', retirement_details='stellarcarbon.io 9f3c6b2107711b7b273c6decad32a7f71bacaf1dd141a047849c9afd1723fc9b', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259), 
        Retirement(certificate_id=203704, vcu_amount=5, serial_number='8040-449402293-449402297-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2023, 6, 14), retirement_beneficiary='GDZTF5ELO5GIJVYYJS4QDN5UMTROJFLYQIG4ACPXWYGLC7VMHCEGIXKX via stellarcarbon.io', retirement_details='stellarcarbon.io f4bdee046a289d32933a8bae36fa272bfde3acce6d0c68c412be1534249c9134 ce0f7783a87ee385216ba9d797ce69d951abba31a02cb25fb83659fc7a7371b0', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259)
    ]
    return retirements


def get_retirements_with_round_down_and_community():
    retirements = get_retirements_whole_and_round_up()[:-1]
    assert len(retirements) == 10, "need to update slice on the preceding line"
    round_down = Retirement(certificate_id=203704, vcu_amount=3, serial_number='8040-449402293-449402295-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2023, 6, 14), retirement_beneficiary='GAXLLGNPEMRUMSLHO3QLYDWZCNPQMBDCWYNLVDPR32ABYWDWQO6YXHSL via stellarcarbon.io', retirement_details='stellarcarbon.io 20dbafdc604fc1a48eafc4ce0df2b6151dfa5a5241c307f811a99ce4ddf2fb7f', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259)
    community = Retirement(certificate_id=203705, vcu_amount=2, serial_number='8040-449402296-449402297-VCU-042-MER-PE-14-1360-01072013-30062014-1', retirement_date=datetime.date(2023, 6, 14), retirement_beneficiary='The Stellarcarbon Community', retirement_details='stellarcarbon.io 20dbafdc604fc1a48eafc4ce0df2b6151dfa5a5241c307f811a99ce4ddf2fb7f f4bdee046a289d32933a8bae36fa272bfde3acce6d0c68c412be1534249c9134', vcs_project_id=1360, issuance_date=datetime.date(2020, 3, 20), instrument_type='VCU', vintage_start=datetime.date(2013, 7, 1), vintage_end=datetime.date(2014, 6, 30), total_vintage_quantity=97259)
    return retirements + [round_down, community]


search_response = """
    {
        "totalCount": 11,
        "countExceeded": false,
        "@count": 11,
        "value": [
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402275-449402275-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2021-11-21",
                "retirementBeneficiary": "GAVF6ZB7Z7FKCWM5HEY2OV4ENPK3OSSHMFTVR4HHSBFHKW36U3FUH2CB",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 61d4ff5516b7098bbc2219d244e7f29a039c32735e1c16d1c05d66a0739727d9",
                "inputTypes": null,
                "holdingIdentifier": "143471"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402276-449402276-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-09-18",
                "retirementBeneficiary": "GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 63f55c3ff92b239ecdb774c336cb91e896a3e4906a81cbeb23a60f20563c198f",
                "inputTypes": null,
                "holdingIdentifier": "152309"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402277-449402277-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-12-03",
                "retirementBeneficiary": "GBAQIUT26BTMG652R5RI5HM22UZ7KDHVM3VPZ4NXUZGR7FVN5KUP4TSA via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 40def47032e4ab8fc7f06b817ca58f354ee0ba590ac318377856e8658e512771",
                "inputTypes": null,
                "holdingIdentifier": "152312"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402278-449402278-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-12-03",
                "retirementBeneficiary": "GDL4YOQH5VH7EUYSW45QZNEBI5377WACZICSF3A7KL7AOGI5BSB54GTC via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 5af83162a018c92d669fe317dda1e5659bfb3a041a14bc4efa176fb382799a13",
                "inputTypes": null,
                "holdingIdentifier": "187116"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402279-449402279-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-12-03",
                "retirementBeneficiary": "GBIH7Z3SMZUX62JPLLDTHA3QEVMRCGUCUQVCFFRJTEGCKB4MV4NGU7BE via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io c2f0ed42774091e1249f11af93d56be53af1aa24bc397d36f2fcbb0907475fb4",
                "inputTypes": null,
                "holdingIdentifier": "187117"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402280-449402280-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-12-03",
                "retirementBeneficiary": "GBIH7Z3SMZUX62JPLLDTHA3QEVMRCGUCUQVCFFRJTEGCKB4MV4NGU7BE via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 2827d90abd658986345f4c20cb68f1f29af128bccaa0d8743ce0248732a2b4fc",
                "inputTypes": null,
                "holdingIdentifier": "187118"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402281-449402281-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-12-12",
                "retirementBeneficiary": "GBBKODANH3RROGGDHDC6FLGY2P4Y2GKT53ULPW75ATCRJRGUKQIO7S7Z via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 0bb7cbdf0ccd7f3679009b69c1d323948236e312825920510b90cd6ee07383d5",
                "inputTypes": null,
                "holdingIdentifier": "187119"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402282-449402282-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2022-12-17",
                "retirementBeneficiary": "GBN4VSSXH4C32W37GK54UXAXZPXK4QGKJFA62K5CJXPOXEKXPQJABD4T via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 7d982a3b39f1cf9ff80e08ad1a503561dd68d12336f2a04b5855f539c1e83fcf",
                "inputTypes": null,
                "holdingIdentifier": "187861"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 9,
                "serialNumbers": "8040-449402283-449402291-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2023-05-07",
                "retirementBeneficiary": "GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io d58b08d1cbc27fe931752e4cfcbdfdcfc057b0bf1bd312b05a41c298b7c54f7e 263f997b4a2326df41ec2b346d79cbca4c06d2d72cff381620d39ca3ebe552f4 6854d5fc7690776dddba92fd0754e9f69ce7f5a3d3180373bc77d359d8e83d9f 063d8428b79a080eee39f5a8a39e4e199d43dbfe529a0b402ede160bb997b816 a36ffd373d153cf2e8fda674f5c9da9115d0322c29e1bad6a6c0b96030c09ed6 48d69bb7691c02df2ed5e79a89b7a89f5ae944409dc0450e59cefd5636d3cfc9 2ec3bb8fa3975ee46aa61ed14912c7c26d68e04fe293d388e3579807ec53282e",
                "inputTypes": null,
                "holdingIdentifier": "188439"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 1,
                "serialNumbers": "8040-449402292-449402292-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2023-05-07",
                "retirementBeneficiary": "GBBKODANH3RROGGDHDC6FLGY2P4Y2GKT53ULPW75ATCRJRGUKQIO7S7Z via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io 9f3c6b2107711b7b273c6decad32a7f71bacaf1dd141a047849c9afd1723fc9b",
                "inputTypes": null,
                "holdingIdentifier": "203703"
            },
            {
                "issuanceDate": "2020-03-20",
                "programObjectives": null,
                "instrumentType": "VCU",
                "vintageStart": "2013-07-01",
                "vintageEnd": "2014-06-30",
                "reportingPeriodStart": "2013-07-01",
                "reportingPeriodEnd": "2014-06-30",
                "resourceIdentifier": "1360",
                "resourceName": "Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region",
                "region": "Latin America",
                "country": "Peru",
                "protocolCategory": "Agriculture Forestry and Other Land Use",
                "protocol": "VM0015",
                "totalVintageQuantity": 97259,
                "quantity": 5,
                "serialNumbers": "8040-449402293-449402297-VCU-042-MER-PE-14-1360-01072013-30062014-1",
                "additionalCertifications": "CCB-Gold",
                "retiredCancelled": true,
                "retireOrCancelDate": "2023-06-14",
                "retirementBeneficiary": "GDZTF5ELO5GIJVYYJS4QDN5UMTROJFLYQIG4ACPXWYGLC7VMHCEGIXKX via stellarcarbon.io",
                "retirementReason": "Retirement for Person or Organization",
                "retirementDetails": "stellarcarbon.io f4bdee046a289d32933a8bae36fa272bfde3acce6d0c68c412be1534249c9134 ce0f7783a87ee385216ba9d797ce69d951abba31a02cb25fb83659fc7a7371b0",
                "inputTypes": null,
                "holdingIdentifier": "203704"
            }
        ]
    }
"""
