import pickle

class FertilizerTransformer:
    """
    Clase para tomar los valores de distorsión de fertilizante y transformarlos a gramos
    """

    def __init__(self, regresor_file, poly_features_file):
        """Constructor de la clase FertilizerImputer.

        Args:
            - regresor: Regresor que transforma los valores de distorsión a gramos.
            - poly_features: Grado del polinomio a utilizar en la transformación de los datos.        
        """
        ##cargo el regresor con pickle. Usamos try para capturar el error FileNotFoundError
        try:
            with open(regresor_file, 'rb') as file:
                self._regresor = pickle.load(file)
            print("Regresor cargado con éxito.")
        except FileNotFoundError:
            print("El archivo no se encuentra en el directorio actual.")

        ##cargo las características polinómicas con pickle. Usamos try para capturar el error FileNotFoundError
        try:
            with open(poly_features_file, 'rb') as file:
                self._poly_features = pickle.load(file)
            print("Características polinómicas cargadas con éxito.")
        except FileNotFoundError:
            print("El archivo no se encuentra en el directorio actual.")
            
        self.fertilizer_grams = None ##cuando no se ha transformado ningún dato, se inicializa en None


    def transform(self, X):
        """Transforma los datos de distorsión de fertilizante a gramos.

        Params:
            - X: Es un array con los datos de distorsión de fertilizante. La forma de X es (n,1)

            Ejemplo: [12.  1. 12.  0.  0.  0.  0.  0.  0. 12.]

        Returns:
            - 0: Array con los valores de distorsión de fertilizante transformados a gramos.
        """

        X_poly = self._poly_features.fit_transform(X)
        self.fertilizer_grams = self._regresor.predict(X_poly)

        ##retorno con shape (n,)
        return self.fertilizer_grams.reshape(-1,)
    
if __name__ == "__main__":
    import os
    import pandas as pd
    import numpy as np
    from sarapy.preprocessing import TransformInputData
    from sarapy.mlProcessors import PlantinFMCreator
    import sarapy.utils.getRawOperations as getRawOperations
    tindata = TransformInputData.TransformInputData()

    ##cargo los archivos examples\2024-09-04\UPM001N\data.json y examples\2024-09-04\UPM001N\historical-data.json
    data_path = os.path.join(os.getcwd(), "examples\\2024-09-04\\UPM001N\\data.json")
    historical_data_path = os.path.join(os.getcwd(), "examples\\2024-09-04\\UPM001N\\historical-data.json")
    raw_data = pd.read_json(data_path, orient="records").to_dict(orient="records")
    raw_data2 = pd.read_json(historical_data_path, orient="records").to_dict(orient="records")

    raw_ops = np.array(getRawOperations.getRawOperations(raw_data, raw_data2))
    X = tindata.fit_transform(raw_ops) #transforma los datos de operaciones a un array de numpy
    
    from sarapy.mlProcessors import FertilizerFMCreator

    ftfmcreator = FertilizerFMCreator.FertilizerFMCreator()
    dst_ft = ftfmcreator.transform(X[:,2])
    ##convierto a int dst_ft
    dst_ft = dst_ft.astype(int)

    from sarapy.mlProcessors import FertilizerTransformer

    fertransformer = FertilizerTransformer.FertilizerTransformer(regresor_file='modelos\\regresor.pkl', poly_features_file='modelos\\poly_features.pkl')
    gramos = fertransformer.transform(dst_ft.reshape(-1,1))
    print(gramos[:10])