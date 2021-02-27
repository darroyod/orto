from requests import Session
import datetime


class ResponseException(Exception):
    pass


class LoginException(Exception):
    pass


class SessionException(Exception):
    pass


class NoResponseException(Exception):
    pass


class SelectContractException(Exception):
    pass


class Iber:

    __domain = "https://www.i-de.es"
    __login_url = __domain + "/consumidores/rest/loginNew/login"
    __watthourmeter_url = __domain + "/consumidores/rest/escenarioNew/obtenerMedicionOnline/24"
    __icp_status_url = __domain + "/consumidores/rest/rearmeICP/consultarEstado"
    __contracts_url = __domain + "/consumidores/rest/cto/listaCtos/"
    __contract_detail_url = __domain + "/consumidores/rest/detalleCto/detalle/"
    __contract_selection_url = __domain + "/consumidores/rest/cto/seleccion/"
    __downloadCSV_url = __domain + "/consumidores/rest/consumoNew/exportarACSVPeriodoConsumo/"
    __dailyData_url = __domain + "/consumidores/rest/consumoNew/obtenerDatosConsumo/"
    __getPowerDateLimits_url = __domain + "/consumidores/rest/consumoNew/obtenerLimitesFechasPotencia/"
    __getMaxPower_url = __domain + "/consumidores/rest/consumoNew/obtenerPotenciasMaximas/"
    
    __headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        'accept': "application/json; charset=utf-8",
        'content-type': "application/json; charset=utf-8",
        'cache-control': "no-cache"
    }

    def __init__(self):
        """Iber class __init__ method."""
        self.__session = None

    def login(self, user, password):
        """Creates session with your credentials"""
        self.__session = Session()
        login_data = "[\"{}\",\"{}\",null,\"Windows 10\",\"PC\",\"Firefox 85.0\",\"0\",\"\",\"s\"]".format(user, password)
        response = self.__session.request("POST", self.__login_url, data=login_data, headers=self.__headers)
        if response.status_code != 200:
            self.__session = None
            raise ResponseException("Response error, code: {}".format(response.status_code))
        json_response = response.json()
        if json_response["success"] != "true":
            self.__session = None
            raise LoginException("Login error, bad login")

    def __check_session(self):
        if not self.__session:
            raise SessionException("Session required, use login() method to obtain a session")

    def watthourmeter(self,mode):
        """Returns your current power consumption."""
        """If mode is normal then we will return the measure. If mode is debuig then we will return the whole response"""
        """The whole response has these fields:
        valLecturaContador
        codSolicitudTGT
        valInterruptor
        valMagnitud
        valEstado"""
        self.__check_session()
        response = self.__session.request("GET", self.__watthourmeter_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException
        if mode == "normal":
            json_response = response.json()
            return json_response['valMagnitud']
        elif mode == "debug":
            return response.json()


    def icpstatus(self,mode):
        """Returns the status of your ICP."""
        """If mode is normal then we will return the measure. If mode is debuig then we will return the whole response"""
        self.__check_session()
        response = self.__session.request("POST", self.__icp_status_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException
        if mode == "normal":
            json_response = response.json()
            if json_response["icp"] == "trueConectado":
                return True
            else:
                return False
        elif mode == "debug":
            return response.json()

    def contracts(self):
        self.__check_session()
        response = self.__session.request("GET", self.__contracts_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        if json_response["success"]:
            return json_response["contratos"]

    def contract(self):
        self.__check_session()
        response = self.__session.request("GET", self.__contract_detail_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException
        return response.json()

    def contractselect(self, id):
        self.__check_session()
        response = self.__session.request("GET", self.__contract_selection_url + id, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        if not json_response["success"]:
            raise SelectContractException

    def getCsv(self,myDate):
        self.__check_session()
        """myDate parameter must has this format: DD-MM-YYYYHH:mm:ss. Example: 16-04-202000:00:00 -> April, 16th of 2020 at 00:00:00"""        
        try:
            datetime.datetime.strptime(myDate, '%d-%m-%Y%H:%M:%S')
        except ValueError:
            raise ResponseException("Incorrect data format, should be like 16-04-202000:00:00")

        myURL = self.__downloadCSV_url + "fechaInicio/" + myDate + "/frecuencia/horas/tipo/horaria/"
        response = self.__session.request("GET", myURL, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException        
        return response.content

    def getDailyData(self,myDate):
        self.__check_session()
        """myDate parameter must has this format: DD-MM-YYYYHH:mm:ss. Example: 16-04-202000:00:00 -> April, 16th of 2020 at 00:00:00"""
        try:
            datetime.datetime.strptime(myDate, '%d-%m-%Y%H:%M:%S')
        except ValueError:
            raise ResponseException("Incorrect data format, should be like 16-04-202000:00:00")

        myURL = self.__dailyData_url + "fechaInicio/" + myDate + "/colectivo/USU/frecuencia/horas/acumular/false"
        response = self.__session.request("GET", myURL, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException        
        return response.json()

    def getPowerDateLimits(self):
        self.__check_session()
        """myDate parameter must has this format: DD-MM-YYYYHH:mm:ss. Example: 16-04-202000:00:00 -> April, 16th of 2020 at 00:00:00"""    

        myURL = self.__getPowerDateLimits_url
        response = self.__session.request("GET", myURL, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException        
        return response.json()


    def getMaxPower(self,myDate):
        self.__check_session()
        """myDate parameter must has this format: DD-MM-YYYYHH:mm:ss. Example: 16-04-202000:00:00 -> April, 16th of 2020 at 00:00:00"""
        try:
            datetime.datetime.strptime(myDate, '%d-%m-%Y%H:%M:%S')
        except ValueError:
            raise ResponseException("Incorrect data format, should be like 16-04-202000:00:00")

        myURL = self.__getMaxPower_url + myDate
        response = self.__session.request("GET", myURL, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException
        if not response.text:
            raise NoResponseException        
        return response.json()
