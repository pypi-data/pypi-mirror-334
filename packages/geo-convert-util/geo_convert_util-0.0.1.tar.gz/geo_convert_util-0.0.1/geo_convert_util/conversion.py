
class Conversion:

    @staticmethod
    def ha_to_alqpta(ha: float) -> float:
        return ha / 2.42
    
    @staticmethod
    def ha_to_m2(ha: float) -> float:
        return ha * 10000
    
    @staticmethod
    def m2_to_alqpta(m2: float) -> float:
        return m2 / 24200
    
    @staticmethod
    def m2_to_ha(m2: float) -> float:
        return m2 / 10000
    
    @staticmethod
    def alqpta_to_ha(alqpta: float) -> float:
        return alqpta * 2.42
    
    @staticmethod
    def alqpta_to_m2(alqpta: float) -> float:
        return alqpta * 24200
    
