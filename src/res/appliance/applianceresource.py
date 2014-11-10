__author__ = 'alisonbento'

import flask
import flask_restful

import src.res.connector as connector
import src.dao.fullappliancedao as fullappliancedao
import src.answer.answer as hs_answer
import src.hsstatus as _status


class ApplianceResource(flask_restful.Resource):

    def get(self, appliance_id):

        connection = connector.getcon()
        dao = fullappliancedao.FullApplianceDAO(connection)

        appliance = dao.get(appliance_id)

        reply = hs_answer.Answer()
        if appliance is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
            reply.add_content('appliance', {})
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('appliance', appliance.to_array())

        connection.close()
        return flask.jsonify(reply.to_array())