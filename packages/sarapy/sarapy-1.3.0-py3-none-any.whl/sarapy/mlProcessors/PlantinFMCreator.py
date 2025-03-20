###Documentación en https://github.com/lucasbaldezzari/sarapy/blob/main/docs/Docs.md
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sarapy.dataProcessing import TLMSensorDataProcessor, TimeSeriesProcessor, GeoProcessor

class PlantinFMCreator(BaseEstimator, TransformerMixin):
    """La clase FMCreator se encarga de crear la Feature Matrix (FM) a partir de los datos de telemetría. Se utilizan las clases TLMSensorDataExtractor, TimeSeriesProcessor y GeoProcessor para realizar las transformaciones necesarias.
    
    Versión 0.1.0
    
    En esta versión la matriz de características está formada por las siguientes variables
    
    - DST_PT: Distorsión de plantín
    - deltaO: delta operación
    - ratio_dCdP: Ratio entre el delta de caminata y delta de pico abierto
    - distances: Distancias entre operaciones
    """
    
    def __init__(self, imputeDistances = True, distanciaMedia:float = 1.8,
                 umbral_precision:float = 0.3, dist_mismo_lugar = 0.0, max_dist = 100,
                 umbral_ratio_dCdP:float = 0.5, deltaO_medio = 4):
        """Inicializa la clase FMCreator.
        
        Args:
            - imputeDistances: Si es True, se imputan las distancias entre operaciones. Si es False, no se imputan las distancias.
            - distanciaMedia: Distancia media entre operaciones.
            - umbral_precision: Umbral para considerar que dos operaciones son el mismo lugar.
            - umbral_ratio_dCdP: Umbral para el ratio entre el delta de caminata y el delta de pico abierto.
            - deltaO_medio: delta de operación medio entre operaciones.
        """
        
        self.is_fitted = False
        self.imputeDistances = imputeDistances
        self.distanciaMedia = distanciaMedia
        self.umbral_precision = umbral_precision
        self.dist_mismo_lugar = dist_mismo_lugar
        self.max_dist = max_dist
        self.umbral_ratio_dCdP = umbral_ratio_dCdP
        self.deltaO_medio = deltaO_medio
        
        ##creamos un diccionario para saber la posición de cada dato dentro del array devuelto por transform()
        self._dataPositions = {"DST_PT": 0, "deltaO": 2, "ratio_dCdP": 3, "distances": 4}
        
    def fit(self, X: np.array, y=None)-> np.array:
        """Fittea el objeto
        
        Params:
            - X: Es un array con los datos provenientes (strings) de la base de datos histórica. La forma de X es (n,5)Las columnas de X son,
                - 0: tlm_spbb son los datos de telemetría.
                - 1: date_oprc son los datos de fecha y hora de operación.
                - 2: latitud de la operación
                - 3: longitud de la operación
                - 4: precision del GPS
        """
        self.is_fitted = True
        
    def transform(self, X: np.array, y = None):
        """Transforma los datos de X en la matriz de características.
        
        Params:
            - X: Es un array con los datos provenientes (strings) de la base de datos histórica. La forma de X es (n,5)Las columnas de X son,
                - 0: tlm_spbb son los datos de telemetría.
                - 1: date_oprc son los datos de fecha y hora de operación.
                - 2: latitud de la operación
                - 3: longitud de la operación
                - 4: precision del GPS
                
        Returns:
                - 0: feature_matrix: (deltaO, ratio_dCdP, distances)
                - 1: dst_pt
                - 2: inest_pt
        """
        
        if not self.is_fitted:
            raise RuntimeError("El modelo no ha sido fitteado.")
        
        ##instanciamos los objetos
        tlmDataExtractor = TLMSensorDataProcessor.TLMSensorDataProcessor()
        timeProcessor = TimeSeriesProcessor.TimeSeriesProcessor()
        geoprocessor = GeoProcessor.GeoProcessor()
        
        tlm_spbb = X[:,0] #datos de telemería
        date_oprc = X[:,1].astype(int) #datos de fecha y hora de operación
        lats = X[:,2].astype(float) #latitudes de las operaciones
        longs = X[:,3].astype(float) #longitudes de las operaciones  
        # precitions = X[:,4].astype(float) #precision del GPS   
        
##***** OBTENEMOS LOS DATOS PARA FITEAR LOS OBJETOS Y ASÍ PROCESAR LA FM *****
        ##obtengo las posiciones de los datos de tlmDataExtractor y timeProcessor
        self._tlmdeDP = tlmDataExtractor.dataPositions #posiciones de los datos transformados de tlmDataExtractor
        self._tpDP = timeProcessor.dataPositions #posiciones de los datos transformados de timeProcessor
        
        ##fitteamos tlmse con los datos de telemetría
        self._tlmExtracted = tlmDataExtractor.fit_transform(tlm_spbb)
        
        ##fitteamos timeProcessor con los datos de fecha y hora de operación y los TIMEAC
        timeData = np.hstack((date_oprc.reshape(-1,1),self._tlmExtracted[:,self._tlmdeDP["TIMEAC"]].reshape(-1, 1)))
        self._timeDeltas = timeProcessor.fit_transform(timeData)
        
        ##fitteamos geoprocessor con las latitudes y longitudes
        ##genero un array de puntos de la forma (n,2)
        points = np.hstack((lats.reshape(-1,1),longs.reshape(-1,1)))
        self._distances = geoprocessor.fit_transform(points)

        self.dst_pt = self._tlmExtracted[:,self._tlmdeDP["DSTRPT"]]
        self.inest_pt = self._tlmExtracted[:,self._tlmdeDP["INESTPT"]]
        
        ##armamos la feature matrix
        self.featureMatrix = np.vstack((self._timeDeltas[:,self._tpDP["deltaO"]],
                                        self._timeDeltas[:,self._tpDP["ratio_dCdP"]],
                                        self._distances)).T
        
        return self.featureMatrix, self.dst_pt, self.inest_pt

    def fit_transform(self, X: np.array, y=None):
        """Fittea y transforma los datos de X en la matriz de características.
        
        Params:
            - X: Es un array con los datos provenientes (strings) de la base de datos histórica. La forma de X es (n,5)Las columnas de X son,
                - 0: tlm_spbb son los datos de telemetría.
                - 1: date_oprc son los datos de fecha y hora de operación.
                - 2: latitud de la operación
                - 3: longitud de la operación
                - 4: precision del GPS
                
        Returns:
                - 0: feature_matrix: (deltaO, ratio_dCdP, distances)
                - 1: dst_pt
                - 2: inest_pt
        """
        self.fit(X)
        return self.transform(X)
    
    @property
    def tlmExtracted(self):
        """Devuelve los datos de telemetría extraídos."""
        return self._tlmExtracted
    
    @property
    def tlmdeDP(self):
        """Devuelve el diccionario con la posición de los datos dentro del array devuelto por transform()."""
        return self._tlmdeDP

    @property
    def timeDeltas(self):
        """Devuelve los datos de tiempo extraídos."""
        return self._timeDeltas
    
    @property
    def distances(self):
        """Devuelve las distancias entre operaciones."""
        return self._distances
    
    @property
    def dataPositions(self):
        """Devuelve el diccionario con la posición de los datos dentro del array devuelto por transform()."""
        return self._dataPositions
    
        
if __name__ == "__main__":
    import os
    import pandas as pd
    import numpy as np
    from sarapy.preprocessing import TransformInputData
    from sarapy.mlProcessors import PlantinFMCreator
    import sarapy.utils.getRawOperations as getRawOperations

    fmcreator = PlantinFMCreator.PlantinFMCreator(imputeDistances=False)
    tindata = TransformInputData.TransformInputData()

    ##cargo los archivos examples\2024-09-04\UPM001N\data.json y examples\2024-09-04\UPM001N\historical-data.json
    data_path = os.path.join(os.getcwd(), "examples\\2024-09-04\\UPM001N\\data.json")
    historical_data_path = os.path.join(os.getcwd(), "examples\\2024-09-04\\UPM001N\\historical-data.json")
    raw_data = pd.read_json(data_path, orient="records").to_dict(orient="records")
    raw_data2 = pd.read_json(historical_data_path, orient="records").to_dict(orient="records")

    raw_ops = np.array(getRawOperations.getRawOperations(raw_data, raw_data2))
    X = tindata.fit_transform(raw_ops)

    fm, dst_pt, inest_pt = fmcreator.fit_transform(X[:,2:])  
