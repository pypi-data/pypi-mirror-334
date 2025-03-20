# SARAPY

Library for processing SARAPICO project metadata of _AMG SA_.

#### Version 1.3.0

- Se agrega funcionalidad para estimar la cantidad de gramos de fertilizante en base al nivel de distorsión de fertilizante arrojado por la electrónica. Se implementa mlProcessor.FertlizerFMCreator y mlProcessor.FertilizerTransformer. Además se modifican las clases OpsProcessor y TransformToOutputData para poder usar estas nuevas clases.

#### Version 1.2.6

- Se agrega línea dentro de clase OpsProcessor.

#### Version 1.1.6

- Se modifica PlantinClassifier para mejorar el NO conteo de plantines en OSP.

#### Version 1.1.5

- Se quita print de función update.

#### Version 1.1.4

- Se implementa actualización de operaciones con bandera MODE en 1. Se hacen operaciones de plantin iguales a 0 para todas las operaciones con MODE = 1.

#### Version 1.1.3

- Se modifica GeoProcessor para no tener problemas con valores de latitud y longitud fuera de rangos.

#### Version 1.1.2

- Se modifica TimeSeriesProcessor.transform() para poder usar la modificación realizada en 1.1.1.

#### Version 1.1.1

- Se modifica TimeSeriesProcessor.compute_ratio_dCdP() dado que la versión de vectorize al parecer no funcionaba correctamente en ciertos casos.

#### Version 1.1.0

Versión 1.1 estable para trabajarse en servidor.

- Se implementa nueva estrategia para la clasificación de plantines.


#### Version 1.0.1

- Se agrega *__init.py__* dentro del mpdulo _utils_.

#### Version 1.0.0

- Se crean clases TransformInputData y TransformToOuputData dentro del módulo proprocessing. Se crean utils.

#### Version 0.4.9

- Se cierra la versión 0.4.8 y se crea la versión 0.4.9 para actualizar repositorio, diagrama de clases a esta versión y la Licencia de uso.

#### Version 0.4.8

- Se importa pandas en OpsProcessor.py ya que no estaba.

#### Version 0.4.7

- Se agregan modificaciòn en método OpsProcessor.transformInputData() y se agrega OpsProcessor.transformToOutputData().

#### Version 0.4.6

- Se agrega función OpsProcessor.transformInputData() para convertir la lista de diccionarios entregadas por el decoder a un array de strings necesarios para procesar y clasificar los datos.

#### Version 0.4.5

- Se modifica clase PlantinClassifier para que ahora tome un clasificador y lo use para clasificar operaciones.
- Se modifica OpsProcessor para poder obtener clasificaciones (y no matrices de características de plantin como se venía probando).

#### Version 0.4.4

- Se modifica fit() de PlantinFMCreator.

#### Version 0.4.3

- Se agrega fit() dentro de transform() de PlantinFMCreator.

#### Version 0.4.2

- Se agrega \*\*kwargs en OpsProcessor, PlantinClassifier y PlantinFMCreator para poder setear los atributos de PlantinFMCreator desde las clases que lo usen.

#### Version 0.4.1

- Se corrigen problemas de importaciones circulares.

#### Version 0.4.0

- Se implementa _OpsProcessor_.
- Se implementa _PlanntinClassifier_.
- Se corrige salida de _transform()_ y _fit_transform()_ de GeoProcessor.
- Se mueve PlantinFMCreator a mlProcessors
- Se cambia nombre de TLMSensorDataCreator a TLMSensorDataProcessor
