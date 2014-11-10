__author__ = 'alisonbento'

import basedao
from src.entities.hsstatus import HomeShellStatus


class StatusDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_appliance_status', 'status_id')

    def convert_row_to_object(self, entity_row):
        status = HomeShellStatus()

        status.id = entity_row['status_id']
        status.name = entity_row['status_key']
        status.value = entity_row['status_value']

        return status