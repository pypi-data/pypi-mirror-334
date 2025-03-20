from dataclasses import dataclass
from units_converter.base import Unit, ConverstionFactor
@dataclass
class Ion:
    name: str
    charge: int
    molar_mass: float
    @property
    def equivalent_weight(self) -> float:
        return self.molar_mass / abs(self.charge)

class IonConcentration(Unit):
    ions = {
        "na": Ion(name="na", charge=1, molar_mass=22.99),
        "cl": Ion(name="cl", charge=-1, molar_mass=35.45),
        "ca": Ion(name="ca", charge=2, molar_mass=40.08),
        "mg": Ion(name="mg", charge=2, molar_mass=24.31),
        "so4": Ion(name="so4", charge=-2, molar_mass=96.06),
        "hco3": Ion(name="hco3", charge=-1, molar_mass=61.02),
        "fe": Ion(name="fe", charge=2, molar_mass=55.85),
        "mn": Ion(name="mn", charge=2, molar_mass=54.94),
        "zn": Ion(name="zn", charge=2, molar_mass=65.39),
        "cu": Ion(name="cu", charge=2, molar_mass=63.55),
        "pb": Ion(name="pb", charge=2, molar_mass=207.2),
        "cr": Ion(name="cr", charge=3, molar_mass=52.00),
        "ni": Ion(name="ni", charge=2, molar_mass=58.69),
        "al": Ion(name="al", charge=3, molar_mass=26.98),
        "alk": Ion(name="alk", charge=-1, molar_mass=61.02),
        "hrd": Ion(name="hrd", charge=2, molar_mass=40),
        "po4": Ion(name="po4", charge=-3, molar_mass=94.97),
        "sio2": Ion(name="sio2", charge=-2, molar_mass=60.08),
    }
    default_unit = "caco3"
    _conversion_factors = {
        "caco3": ConverstionFactor(1, 0),
        "ppm": ConverstionFactor(1, 0),
        "meq": ConverstionFactor(1,0),
        'mmol': ConverstionFactor(1,0),
    }
    def __init__(self, ion: str, value: float, unit: str) -> None:
        self._set_ion(ion)
        self._value = self._to_internal(value, unit)

    def _set_ion(self, ion):
        self._ion = self.ions[ion]
        self._conversion_factors = {
            "caco3": ConverstionFactor(1, 0),
            "ppm": ConverstionFactor(50/self._ion.equivalent_weight, 0),
            "meq": ConverstionFactor(50, 0),
            'mmol': ConverstionFactor(50/self._ion.molar_mass, 0),
        }
    def __add__(self, other: "IonConcentration") -> "IonConcentration":
        if self._ion.name != other._ion.name:
            raise ValueError(f"Cannot add ions with different names: {self._ion.name} and {other._ion.name}")
        return IonConcentration(self._ion.name, self._value + other._value, self.default_unit)
    
    def __sub__(self, other: "IonConcentration") -> "IonConcentration":
        if self._ion.name != other._ion.name:
            raise ValueError(f"Cannot subtract ions with different names: {self._ion.name} and {other._ion.name}")
        return IonConcentration(self._ion.name, self._value - other._value, self.default_unit)
    
    def __mul__(self, other: float | int) -> "IonConcentration":
        return IonConcentration(self._ion.name, self._value * other, self.default_unit)
    
    def __truediv__(self, other: float | int) -> "IonConcentration":
        return IonConcentration(self.ion.name, self._value / other, self.default_unit)

        

    
    
    

    

