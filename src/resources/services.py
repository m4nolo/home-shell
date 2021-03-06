__author__ = 'alisonbento'

import flask_restful
import hsres
import src.resstatus as _status

from src.dao.servicedao import ServiceDAO
from src.lib.service_caller import call_service


class ListServicesResource(hsres.HomeShellResource):

    def get(self, appliance_id):

        dao = ServiceDAO(self.get_dbc())

        services = dao.list("appliance_id = ?", (appliance_id,))

        if len(services) > 0:
            self.set_status(_status.STATUS_OK)
            all_services = []
            for service in services:
                all_services.append(service.to_array())

            self.add_content('services', all_services)

        else:
            self.set_status(_status.STATUS_GENERAL_ERROR)

        return self.end()


class ServiceResource(hsres.HomeShellResource):

    def get(self, appliance_id, service_id):

        dao = ServiceDAO(self.get_dbc())

        if service_id.isdigit():
            service = dao.get(service_id, "appliance_id = " + str(appliance_id))
        else:
            services = dao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
            if len(services) > 0:
                service = services[0]
            else:
                service = None

        if service is None:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()

        self.set_status(_status.STATUS_OK)
        self.add_content('service', service.to_array())

        return self.end()

    def post(self, appliance_id, service_id):
        return call_service(self, appliance_id, service_id, flask_restful.request.form)
        # servicedao = ServiceDAO(self.get_dbc())
        #
        # if service_id.isdigit():
        #     service = servicedao.get(service_id, "appliance_id = " + str(appliance_id))
        # else:
        #     services = servicedao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
        #     if len(services) > 0:
        #         service = services[0]
        #     else:
        #         service = None
        #
        # if service is None:
        #     self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
        #     return self.end()
        # else:
        #     paramdao = ParamDAO(self.get_dbc())
        #     params = paramdao.select("service_id = ?", (service.id,))
        #
        #     all_params_with_values = []
        #     for param in params:
        #         p_value = flask_restful.request.form[param.name]
        #         if p_value is not None:
        #             all_params_with_values.append(param.name + '=' + p_value)
        #
        #     if len(all_params_with_values) > 0:
        #         param_string = '&'.join(all_params_with_values)
        #         param_string = '?' + param_string
        #     else:
        #         param_string = ''
        #
        #     appliancedao = ApplianceDAO(self.get_dbc())
        #     appliance = appliancedao.get(appliance_id)
        #     # address = 'http://' + appliance.address + '/services/' + service.name + '/' + param_string
        #     address = 'http://' + appliance.address + '/services/' + service.name + param_string
        #
        #     try:
        #         r = requests.get(address)
        #
        #         if r.status_code == '404':
        #             self.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
        #         elif r.status_code:
        #             print(r.text)
        #             # Update status
        #             updater = StatusUpdater(self.get_dbc())
        #             appjson = r.json()
        #             fullappliance = updater.updateStatus(appliance, appjson)
        #             self.set_status(_status.STATUS_OK)
        #             self.add_content('appliance', fullappliance.to_array())
        #
        #     except requests.ConnectionError:
        #         self.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
        #         self.get_dbc().rollback()
        #
        #
        # return self.end()
