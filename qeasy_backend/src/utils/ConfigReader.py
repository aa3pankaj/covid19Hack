import logging,json

class ConfigReader(object):
    def __init__(self, cmdConfig, confFile):
        self.cmdConfig = cmdConfig
        self.confFile = confFile
        self.setValues()

    def setValues(self):
        try:
            self.cmdConfig.readfp(open(self.confFile))
            self.ipv4, self.ipv6, self.port = self.cmdConfig.get('HostDetails', 'ListenIpv4'), \
                self.cmdConfig.get('HostDetails', 'ListenIpv6'), \
                int(self.cmdConfig.get('HostDetails', 'ListenPort'))
            self.serverMib = self.cmdConfig.get('General', 'server-mib')
            self.severMibNew = self.cmdConfig.get('General', 'server-mib-new')
            self.snmpMib = self.cmdConfig.get('General', 'snmpv2-mib')
            self.defaultsnmpObj = self.cmdConfig.get('General', 'snmpTrapOID')
            self.authKey = self.cmdConfig.get('General', 'authKey')
            self.privKey = self.cmdConfig.get('General', 'privKey')
            self.securityEngineId = self.cmdConfig.get(
                'General', 'securityEngineId')
            self.comArea = self.cmdConfig.get('General', 'communityArea')
            self.comName = self.cmdConfig.get('General', 'communityName')
            self.desMD5 = self.cmdConfig.get('General', 'desMD5')
            self.nonMD5 = self.cmdConfig.get('General', 'nonMD5')
            self.aesSha = self.cmdConfig.get('General', 'aesSha')
            self.relayType = self.cmdConfig.get('General', 'relayType')
            self.mastIpv4, self.mastIpv6, self.mastPort = self.cmdConfig.get('MasterDetails', 'ListenIpv4'), \
                self.cmdConfig.get('MasterDetails', 'ListenIpv6'), \
                (self.cmdConfig.get('MasterDetails', 'ListenPort'))
            self.host = self.cmdConfig.get('MYSQL', 'HOST')
            self.userName = self.cmdConfig.get('MYSQL', 'USERNAME')
            self.password = self.cmdConfig.get('MYSQL', 'PASSWORD')
            self.webHookPort = int(self.cmdConfig.get('WEBHOOK', 'port'))
            self.webHookLog = self.cmdConfig.get('WEBHOOK', 'log')
            self.apiPort = int(self.cmdConfig.get('API', 'port'))
            self.apiLog = self.cmdConfig.get('API', 'log')
            self.log = self.cmdConfig.get("General", "log")
            self.logLevel = self.cmdConfig.get("General", "loglevel")
            self.ssl_ca = self.cmdConfig.get("General","ssl_ca")
            self.ssl_cert = self.cmdConfig.get("General","ssl_cert")
            self.ssl_key = self.cmdConfig.get("General","ssl_key")
            self.notifications_flag = self.cmdConfig.get("General","notifications_flag")
            #self.accesskey = self.cmdConfig.get('AwsCredentials','ACCESS_KEY')
            #self.secretkey = self.cmdConfig.get('AwsCredentials', 'SECRET_KEY')
            self.bucketname = self.cmdConfig.get('AwsCredentials', 'BUCKET_NAME')
            self.trapFileEtLoc = self.cmdConfig.get('General', 'trapFileEtLoc')

            self.switchApiLog = self.cmdConfig.get('SWITCH_API', 'log')
            self.switchApiPort = int(self.cmdConfig.get('SWITCH_API', 'port'))
            self.licensing_agent_port = self.cmdConfig.get("Licensing", "licensing_agent_port")
            self.licensing_agent_domain = self.cmdConfig.get("Licensing", "licensing_agent_domain")
            self.license_verifier_api = self.cmdConfig.get("Licensing", "license_verifier_api")
            self.trap_receiver_license_check_interval_in_sec = int(self.cmdConfig.get("Licensing","trap_receiver_license_check_interval_in_sec"))
            self.polling_traps_license_check_interval_in_sec = int(self.cmdConfig.get("Licensing","polling_traps_license_check_interval_in_sec"))
            self.switch_ui_license_check_interval_in_sec = int(self.cmdConfig.get("Licensing","switch_ui_license_check_interval_in_sec"))
            self.api_server_license_check_interval_in_sec = int(self.cmdConfig.get("Licensing","api_server_license_check_interval_in_sec"))

        except Exception as error:

            raise ValueError(ErrorCodes.ERR_CONFIG_FILE_READING_ERROR.value + str(error))

    def setAWSCredentials(self, credentials_file):
        try:
            data = json.load(open(credentials_file))
            self.accesskey = data["ACCESS_KEY"]
            self.secretkey = data["SECRET_KEY"]
        except Exception as err:
            logging.error(str(err))
