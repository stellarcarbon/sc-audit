import datetime as dt
import zoneinfo

from sc_audit.sources.sink_invocations import SinkInvocation


gmt_zoneinfo = zoneinfo.ZoneInfo(key='GMT')

def get_items() -> list[SinkInvocation]:
    return [
        SinkInvocation(
        id=1,
        toid=188328285796925850,
        ledger=43848596,
        timestamp=dt.datetime(2022, 12, 3, 15, 33, 35, tzinfo=gmt_zoneinfo),
        contract_id='CAVS7HEUNFCMOW6DC7EBY7J6HNFJ5JJ7LV4H7RPUC6V5QO5OMS7AQLD5',
        function_name='sink_carbon',
        invoking_account='GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL',
        tx_hash='2f55d7e30d801908fc72f5f11cbf44b264fca73f6386117ebc6274f356affa71',
        funder='GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL',
        recipient='GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y',
        amount=1000000,
        project_id='VCS1360',
        memo_text='one',
        processed_at=dt.datetime(2025, 8, 24, 12, 28, 23, 38732, tzinfo=gmt_zoneinfo),
        schema_name='carbon_sink_v1',
        successful=True,
        created_at=dt.datetime(2025, 8, 24, 12, 28, 23, 38732, tzinfo=gmt_zoneinfo)
    ),
    SinkInvocation(
        id=2,
        toid=188915296156604069,
        ledger=43985272,
        timestamp=dt.datetime(2022, 12, 12, 20, 50, 40, tzinfo=gmt_zoneinfo),
        contract_id='CAVS7HEUNFCMOW6DC7EBY7J6HNFJ5JJ7LV4H7RPUC6V5QO5OMS7AQLD5',
        function_name='sink_carbon',
        invoking_account='GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL',
        tx_hash='1b2aed0644c8fab9abff84aee78e7f0b92b09a8cf9bd2c1a17e71964c768a805',
        funder='GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL',
        recipient='GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y',
        amount=3330000,
        project_id='VCS1360',
        memo_text='two',
        processed_at=dt.datetime(2025, 8, 24, 12, 29, 59, 73393, tzinfo=gmt_zoneinfo),
        schema_name='carbon_sink_v1',
        successful=True,
        created_at=dt.datetime(2025, 8, 24, 12, 29, 59, 73393, tzinfo=gmt_zoneinfo)
    ),
    SinkInvocation(
        id=3,
        toid=2209834166299873287,
        ledger=348855824,
        timestamp=dt.datetime(2025, 8, 24, 12, 30, 32, tzinfo=gmt_zoneinfo),
        contract_id='CAVS7HEUNFCMOW6DC7EBY7J6HNFJ5JJ7LV4H7RPUC6V5QO5OMS7AQLD5',
        function_name='sink_carbon',
        invoking_account='GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL',
        tx_hash='e7d68ab7c57e38e2e103b81926db97731eb9ca861de5282eaf1bcc97e1605deb',
        funder='GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL',
        recipient='GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y',
        amount=4444444,
        project_id='VCS1360',
        memo_text='tri',
        processed_at=dt.datetime(2025, 8, 24, 12, 30, 34, 920249, tzinfo=gmt_zoneinfo),
        schema_name='carbon_sink_v1',
        successful=True,
        created_at=dt.datetime(2025, 8, 24, 12, 30, 34, 920249, tzinfo=gmt_zoneinfo)
    ),
]
