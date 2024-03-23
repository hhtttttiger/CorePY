import threading
from datetime import datetime

class SnowflakeUtil:
    machine_id = 0
    datacenter_id = 0
    sequence = 0
    twepoch = 687888001020
    machine_id_bits = 5
    datacenter_id_bits = 5
    sequence_bits = 12
    max_machine_id = -1 ^ (-1 << machine_id_bits)
    max_datacenter_id = -1 ^ (-1 << datacenter_id_bits)
    sequence_mask = -1 ^ (-1 << sequence_bits)
    machine_id_shift = sequence_bits
    datacenter_id_shift = sequence_bits + machine_id_bits
    timestamp_left_shift = sequence_bits + machine_id_bits + datacenter_id_bits
    last_timestamp = -1
    sync_root = threading.Lock()

    @staticmethod
    def get_timestamp():
        return int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)

    @staticmethod
    def get_next_timestamp(last_timestamp):
        timestamp = SnowflakeUtil.get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = SnowflakeUtil.get_timestamp()
        return timestamp

    @staticmethod
    def generate_id(machine_id=None, datacenter_id=None):
        with SnowflakeUtil.sync_root:
            if machine_id is not None:
                if machine_id < 0 or machine_id > SnowflakeUtil.max_machine_id:
                    raise ValueError(f"MachineId must be between 0 and {SnowflakeUtil.max_machine_id}")
                SnowflakeUtil.machine_id = machine_id
            if datacenter_id is not None:
                if datacenter_id < 0 or datacenter_id > SnowflakeUtil.max_datacenter_id:
                    raise ValueError(f"DatacenterId must be between 0 and {SnowflakeUtil.max_datacenter_id}")
                SnowflakeUtil.datacenter_id = datacenter_id

            timestamp = SnowflakeUtil.get_timestamp()
            if timestamp < SnowflakeUtil.last_timestamp:
                timestamp = SnowflakeUtil.last_timestamp + 1
            if timestamp == SnowflakeUtil.last_timestamp:
                SnowflakeUtil.sequence = (SnowflakeUtil.sequence + 1) & SnowflakeUtil.sequence_mask
                if SnowflakeUtil.sequence == 0:
                    timestamp = SnowflakeUtil.get_next_timestamp(SnowflakeUtil.last_timestamp)
            else:
                SnowflakeUtil.sequence = 0

            SnowflakeUtil.last_timestamp = timestamp

            return ((timestamp - SnowflakeUtil.twepoch) << SnowflakeUtil.timestamp_left_shift) | \
                    (SnowflakeUtil.datacenter_id << SnowflakeUtil.datacenter_id_shift) | \
                    (SnowflakeUtil.machine_id << SnowflakeUtil.machine_id_shift) | \
                    SnowflakeUtil.sequence
