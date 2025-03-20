# GeoConvertUtil

 #### Equivalência das medidas:

 |Descrição|Abreviação|Equivalência|
 |--|--|--|
 |Alqueires Paulista|Alq.Pta.|1,00|
 |Hectares|Ha|2,4200|
 |Metros Quadrados|m²|24.200,00|

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install geoutil

```bash

    pip install geo_convert_util

```

## Usage

```python

from geo_convert_util import Conversion

result = Conversion.ha_to_alqpta(ha)
result = Conversion.ha_to_m2(ha)
result = Conversion.m2_to_alqpta(m2)
result = Conversion.m2_to_ha(m2)
result = Conversion.alqpta_to_ha(alq)
result = Conversion.alqpta_to_m2(alq)

```

## Author
Paulo Sergio de Campos Filho


## License
[MIT](https://choosealicense.com/licenses/mit/)