###Documentación en https://github.com/lucasbaldezzari/sarapy/blob/main/docs/Docs.md

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class TransformInputData(BaseEstimator, TransformerMixin):
    """
    Clase para transformar los datos de entrada a un formato utilizable para procesar las operaciones.
    """

    def __init__(self):
        """
        Constructor de la clase TransformInputData.
        
        Args:
            - features_list: Lista con los nombres de las columnas a extraer de los datos recibidos de cada operación.
        """
        self.is_fitted = False
        self.positions = {"id_db_h":0,
                          "ID_NPDP":1,
                          "TLM_NPDP":2,
                          "date_oprc":3,
                          "latitud":4,
                          "longitud":5,
                          "Precision":6,
                          "FR":7,
                          "id_db_dw":8}

    def fit(self, X:np.array, y = None):
        """
        Fittea el objeto
        """
        self.is_fitted = True  

        self.newSample = np.array([[d["id_db_h"],
                                    d["ID_NPDP"],
                                    ''.join([bin(byte)[2:].zfill(8) for byte in d["TLM_NPDP"]]),
                                    int(d["date_oprc"].timestamp()),
                                    d["Latitud"],
                                    d["Longitud"],
                                    d["Precision"],
                                    d["FR"],
                                    d["id_db_dw"]] for d in X])   
              
        return self
    
    def transform(self, X:np.array):
        """
        Transforma los datos de entrada a un formato utilizable para procesar las operaciones.
        
        Args:
            data: Es una lista de diccionario. Cada diccionario tiene los siguientes keys.
                     
            Ejemplo:
            
            {
                "id_db_h":1, #int
                "ID_NPDP":"XXAA123", #string
                "FR": 1, #int
                "TLM_NPDP": b'\xfc\x01\t\t\x00\x00\x00\x98', #bytes
                "date_oprc":datetime.datetime(2024, 2, 16, 21, 2, 2, tzinfo=tzutc()),#datetime
                "Latitud":-32.145564789, #float
                "Longitud":-55.145564789, #float
                "Precision": 1000,
                "id_db_dw": 1 #int
            }
            
        NOTA: Los diccionarios de la lista tienen más datos, pero no se usan ahora.
        
        Returns:
            Retorna un array de strings con la siguiente estructura
            - 0: id_db_h
            - 1: ID_NPDP
            - 2: TLM_NPDP
            - 3: date_oprc
            - 4: latitud
            - 5: longitud
            - 6: Precision
            - 7: FR
            - 8: id_db_dw
    """
        ##chequeamos si se ha llamado a fit(). Sino, se arroja un error
        if not self.is_fitted:
            raise ValueError("TransformInputData no ha sido fitteado. Llame a fit() previamente.")
        
        return self.newSample
    
    def fit_transform(self, X:np.array, y=None):
        self.fit(X)
        return self.transform(X)
    
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import os
    from sarapy.utils.getRawOperations import getRawOperations

    # features=["id_db_h","ID_NPDP","TLM_NPDP","date_oprc","latitud","longitud","Precision","FR","id_db_dw",
    #           "INESTPT","INESTFT"]
    
    transform_input_data = TransformInputData()

    #cargo "examples\\2024-05-30\\UPM007N\\data.json"
    data = pd.read_json("examples\\2024-05-30\\UPM007N\\data.json").to_dict(orient="records")
    historical_data = pd.read_json("examples\\2024-05-30\\UPM007N\\historical-data.json").to_dict(orient="records")

    ppk_results = getRawOperations(data,historical_data)

    X = np.array(ppk_results)
    print(transform_input_data.fit_transform(X))
