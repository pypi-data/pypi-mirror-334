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
        "Na": Ion(name="Na", charge=1, molar_mass=22.99),
        "Cl": Ion(name="Cl", charge=-1, molar_mass=35.45),
        "Ca": Ion(name="Ca", charge=2, molar_mass=40.08),
        "Mg": Ion(name="Mg", charge=2, molar_mass=24.31),
        "SO4": Ion(name="SO4", charge=-2, molar_mass=96.06),
        "HCO3": Ion(name="HCO3", charge=-1, molar_mass=61.02),
        "Cl": Ion(name="Cl", charge=-1, molar_mass=35.45),
        "Fe": Ion(name="Fe", charge=2, molar_mass=55.85),
        "Mn": Ion(name="Mn", charge=2, molar_mass=54.94),
        "Zn": Ion(name="Zn", charge=2, molar_mass=65.39),
        "Cu": Ion(name="Cu", charge=2, molar_mass=63.55),
        "Pb": Ion(name="Pb", charge=2, molar_mass=207.2),
        "Cr": Ion(name="Cr", charge=3, molar_mass=52.00),
        "Ni": Ion(name="Ni", charge=2, molar_mass=58.69),
        "Al": Ion(name="Al", charge=3, molar_mass=26.98),
        "Alk": Ion(name="Alk", charge=-1, molar_mass=61.02),
        "Hrd": Ion(name="Hrd", charge=2, molar_mass=40),
        "PO4": Ion(name="PO4", charge=-3, molar_mass=94.97),
    }
    default_unit = "caco3"
    _conversion_factors = {
        "caco3": ConverstionFactor(1, 0),
        "ppm": ConverstionFactor(1, 0),
        "meq": ConverstionFactor(1,0)
    }
    def __init__(self, ion: str, value: float, unit: str) -> None:
        self._set_ion(ion)
        self._value = self._to_internal(value, unit)

    def _set_ion(self, ion):
        self._ion = self.ions[ion]
        self._conversion_factors = {
            "caco3": ConverstionFactor(1, 0),
            "ppm": ConverstionFactor(50/self._ion.equivalent_weight, 0),
            "meq": ConverstionFactor(50, 0)
        }
    def __add__(self, other: "IonConcentration") -> "IonConcentration":
        if self.ion.name != other.ion.name:
            raise ValueError(f"Cannot add ions with different names: {self.ion.name} and {other.ion.name}")
        return IonConcentration(self.ion.name, self._value + other._value, self.default_unit)
    
    def __sub__(self, other: "IonConcentration") -> "IonConcentration":
        if self.ion.name != other.ion.name:
            raise ValueError(f"Cannot subtract ions with different names: {self.ion.name} and {other.ion.name}")
        return IonConcentration(self.ion.name, self._value - other._value, self.default_unit)
    
    def __mul__(self, other: float | int) -> "IonConcentration":
        return IonConcentration(self.ion.name, self._value * other, self.default_unit)
    
    def __truediv__(self, other: float | int) -> "IonConcentration":
        return IonConcentration(self.ion.name, self._value / other, self.default_unit)

        

    
    
    

    

