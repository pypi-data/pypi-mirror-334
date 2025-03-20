from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from pytest import fixture, mark, raises

from ..src.validation import *


@dataclass
class ClassWithValidation(ValidationClass):
    intVar: int = 0
    intOptVar: Optional[int] = None
    posIntVar: int = 0
    posIntOptVar: Optional[int] = None
    strVar: str = ''
    strOptVar: Optional[str] = None
    dtVar: datetime = datetime.now()
    dtOptVar: Optional[datetime] = None
    floatVar: float = 0.0
    floatOptVar: Optional[float] = None
    boolVar: bool = False
    boolOptVar: Optional[bool] = None
    tupleVar: tuple = ()
    listVar: list = field(default_factory= list)
    dictVar: dict = field(default_factory= dict)

    def validate_intVar(self, value: Any) -> int:
        return self.validateInt(value)

    def validate_intOptVar(self, value: Any) -> Optional[int]:
        return self.validateOptInt(value)

    def validate_posIntVar(self, value: Any) -> int:
        return self.validatePositiveInt(value)

    def validate_posIntOptVar(self, value: Any) -> Optional[int]:
        return self.validateOptPositiveInt(value)

    def validate_strVar(self, value: Any) -> str:
        return self.validateStr(value)

    def validate_strOptVar(self, value: Any) -> Optional[str]:
        return self.validateOptStr(value)

    def validate_dtVar(self, value: Any) -> datetime:
        return self.validateDatetime(value)

    def validate_dtOptVar(self, value: Any) -> Optional[datetime]:
        return self.validateOptDatetime(value)

    def validate_floatVar(self, value: Any) -> float:
        return self.validateFloat(value)

    def validate_floatOptVar(self, value: Any) -> Optional[float]:
        return self.validateOptFloat(value)

    def validate_boolVar(self, value: Any) -> bool:
        return self.validateBool(value)

    def validate_boolOptVar(self, value: Any) -> Optional[bool]:
        return self.validateOptBool(value)

    def validate_tupleVar(self, value: Any) -> tuple:
        return self.validateTuple(value)

    def validate_listVar(self, value: Any) -> list:
        return self.validateList(value)

    def validate_dictVar(self, value: Any) -> list:
        return self.validateDict(value)

@fixture
def validationObj() -> ClassWithValidation:
    return ClassWithValidation()

class TestValidation:
    @mark.parametrize('inValue, outValue', [
        (1, 1),
        (1.4, 1),
        (-1, -1),
        ('1', 1),
        ('-1', -1),
    ])
    def test_int(self, validationObj: ClassWithValidation, inValue: Any, outValue: int) -> None:
        validationObj.intVar = inValue
        assert validationObj.intVar == outValue
        assert type(validationObj.intVar) == type(outValue)

    @mark.parametrize('inValue', [
        None,
        'a',
    ])
    def test_intErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.intVar = inValue

    @mark.parametrize('inValue, outValue', [
        (1, 1),
        (1.4, 1),
        (-1, -1),
        ('1', 1),
        ('-1', -1),
        (None, None),
    ])
    def test_intOpt(self, validationObj: ClassWithValidation, inValue: Any, outValue: Optional[int]) -> None:
        validationObj.intOptVar = inValue
        assert validationObj.intOptVar == outValue
        assert type(validationObj.intOptVar) == type(outValue)

    @mark.parametrize('inValue', [
        'a',
    ])
    def test_intOptErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.intOptVar = inValue

    @mark.parametrize('inValue, outValue', [
        (1, 1),
        (1.4, 1),
        ('1', 1),
    ])
    def test_posInt(self, validationObj: ClassWithValidation, inValue: Any, outValue: int) -> None:
        validationObj.posIntVar = inValue
        assert validationObj.posIntVar == outValue
        assert type(validationObj.posIntVar) == type(outValue)

    @mark.parametrize('inValue', [
        None,
        'a',
        -1,
        '-1',
    ])
    def test_posIntErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.posIntVar = inValue

    @mark.parametrize('inValue, outValue', [
        (1, 1),
        (1.4, 1),
        ('1', 1),
        (None, None),
    ])
    def test_posIntOpt(self, validationObj: ClassWithValidation, inValue: Any, outValue: Optional[int]) -> None:
        validationObj.posIntOptVar = inValue
        assert validationObj.posIntOptVar == outValue
        assert type(validationObj.posIntOptVar) == type(outValue)

    @mark.parametrize('inValue', [
        'a',
        -1,
        '-1',
    ])
    def test_posIntOptErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.posIntOptVar = inValue

    @mark.parametrize('inValue, outValue', [
        ('a', 'a'),
        (1, '1'),
        (None, 'None'),
    ])
    def test_str(self, validationObj: ClassWithValidation, inValue: Any, outValue: str) -> None:
        validationObj.strVar = inValue
        assert validationObj.strVar == outValue
        assert type(validationObj.strVar) == type(outValue)

    @mark.parametrize('inValue', [
    ])
    def test_strErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.strVar = inValue

    @mark.parametrize('inValue, outValue', [
        ('a', 'a'),
        (1, '1'),
        (None, None),
    ])
    def test_strOpt(self, validationObj: ClassWithValidation, inValue: Any, outValue: Optional[str]) -> None:
        validationObj.strOptVar = inValue
        assert validationObj.strOptVar == outValue
        assert type(validationObj.strOptVar) == type(outValue)

    @mark.parametrize('inValue', [
    ])
    def test_strOptErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.strOptVar = inValue

    @mark.parametrize('inValue, outValue', [
        (datetime(2000, 2, 1, 12, 15, 30, 123000), datetime(2000, 2, 1, 12, 15, 30, 123000)),
        ('2000-02-01 12:15:30.123', datetime(2000, 2, 1, 12, 15, 30, 123000)),
        ('2000-02-01 12:15:30', datetime(2000, 2, 1, 12, 15, 30)),
        ('2000-02-01T12:15:30.123', datetime(2000, 2, 1, 12, 15, 30, 123000)),
        ('2000-02-01T12:15:30.123Z', datetime(2000, 2, 1, 12, 15, 30, 123000)),
    ])
    def test_dt(self, validationObj: ClassWithValidation, inValue: Any, outValue: datetime) -> None:
        validationObj.dtVar = inValue
        assert validationObj.dtVar == outValue
        assert type(validationObj.dtVar) == type(outValue)

    @mark.parametrize('inValue', [
        '1',
        'a',
        None,
    ])
    def test_dtErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.dtVar = inValue

    @mark.parametrize('inValue, outValue', [
        (datetime(2000, 2, 1, 12, 15, 30, 123000), datetime(2000, 2, 1, 12, 15, 30, 123000)),
        ('2000-02-01 12:15:30.123', datetime(2000, 2, 1, 12, 15, 30, 123000)),
        ('2000-02-01 12:15:30', datetime(2000, 2, 1, 12, 15, 30)),
        ('2000-02-01T12:15:30.123', datetime(2000, 2, 1, 12, 15, 30, 123000)),
        ('2000-02-01T12:15:30.123Z', datetime(2000, 2, 1, 12, 15, 30, 123000)),
        (None, None)
    ])
    def test_dtOpt(self, validationObj: ClassWithValidation, inValue: Any, outValue: Optional[datetime]) -> None:
        validationObj.dtOptVar = inValue
        assert validationObj.dtOptVar == outValue
        assert type(validationObj.dtOptVar) == type(outValue)

    @mark.parametrize('inValue', [
        '1',
        'a',
    ])
    def test_dtErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.dtOptVar = inValue

    @mark.parametrize('inValue, outValue', [
        (1, 1.0),
        (1.4, 1.4),
        (-1, -1.0),
        ('1.5', 1.5),
        ('-1.7', -1.7),
    ])
    def test_float(self, validationObj: ClassWithValidation, inValue: Any, outValue: float) -> None:
        validationObj.floatVar = inValue
        assert validationObj.floatVar == outValue
        assert type(validationObj.floatVar) == type(outValue)

    @mark.parametrize('inValue', [
        None,
        'a',
    ])
    def test_floatErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.floatVar = inValue

    @mark.parametrize('inValue, outValue', [
        (1, 1.0),
        (1.4, 1.4),
        (-1, -1.0),
        ('1.5', 1.5),
        ('-1.7', -1.7),
        (None, None),
    ])
    def test_floatOpt(self, validationObj: ClassWithValidation, inValue: Any, outValue: Optional[float]) -> None:
        validationObj.floatOptVar = inValue
        assert validationObj.floatOptVar == outValue
        assert type(validationObj.floatOptVar) == type(outValue)

    @mark.parametrize('inValue', [
        'a',
    ])
    def test_floatOptErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.floatOptVar = inValue

    @mark.parametrize('inValue, outValue', [
        (True, True),
        (1, True),
        (0, False),
        ('true', True),
        ('TRUE', True),
        ('false', False),
        ('FALSE', False),
    ])
    def test_bool(self, validationObj: ClassWithValidation, inValue: Any, outValue: bool) -> None:
        validationObj.boolVar = inValue
        assert validationObj.boolVar == outValue
        assert type(validationObj.boolVar) == type(outValue)

    @mark.parametrize('inValue', [
        None,
        'a',
        5,
    ])
    def test_boolErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.boolVar = inValue

    @mark.parametrize('inValue, outValue', [
        (True, True),
        (1, True),
        (0, False),
        ('true', True),
        ('TRUE', True),
        ('false', False),
        ('FALSE', False),
        (None, None),
    ])
    def test_boolOpt(self, validationObj: ClassWithValidation, inValue: Any, outValue: Optional[bool]) -> None:
        validationObj.boolOptVar = inValue
        assert validationObj.boolOptVar == outValue
        assert type(validationObj.boolOptVar) == type(outValue)

    @mark.parametrize('inValue', [
        'a',
        5,
    ])
    def test_boolOptErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.boolOptVar = inValue

    @mark.parametrize('inValue, outValue', [
        ((1, 2), (1, 2)),
        ([1, 2], (1, 2)),
        ('abc', ('a', 'b', 'c')),
    ])
    def test_tuple(self, validationObj: ClassWithValidation, inValue: Any, outValue: tuple) -> None:
        validationObj.tupleVar = inValue
        assert validationObj.tupleVar == outValue
        assert type(validationObj.tupleVar) == type(outValue)

    @mark.parametrize('inValue', [
        5,
        None,
    ])
    def test_tupleErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.tupleVar = inValue

    @mark.parametrize('inValue, types, outValue', [
        ((1, 2), (int), (1, 2)),
        ([1, 4, 2.1, 'a'], (int, float, str), (1, 4, 2.1, 'a')),
    ])
    def test_tupleWithTypes(self,
                            validationObj: ClassWithValidation,
                            inValue: Any,
                            types: Iterable,
                            outValue: tuple) -> None:
        def validate_tupleWithTypesVar(value: Any) -> tuple:
            return ValidationClass.validateTuple(value, types)
        validationObj.validate_tupleWithTypesVar = validate_tupleWithTypesVar
        validationObj.tupleWithTypesVar = inValue
        assert validationObj.tupleWithTypesVar == outValue
        assert type(validationObj.tupleWithTypesVar) == type(outValue)

    @mark.parametrize('inValue, types', [
        ((1, 2), (float)),
        ([1, 4, 2.1, 'a'], (int, str)),
    ])
    def test_tupleWithTypesErrors(self,
                                  validationObj: ClassWithValidation,
                                  inValue: Any,
                                  types: Iterable) -> None:
        def validate_tupleWithTypesVar(value: Any) -> tuple:
            return ValidationClass.validateTuple(value, types)
        validationObj.validate_tupleWithTypesVar = validate_tupleWithTypesVar
        with raises(TypeError):
            validationObj.tupleWithTypesVar = inValue

    @mark.parametrize('inValue, outValue', [
        ((1, 2), [1, 2]),
        ([1, 2], [1, 2]),
        ('abc', ['a', 'b', 'c']),
    ])
    def test_list(self, validationObj: ClassWithValidation, inValue: Any, outValue: list) -> None:
        validationObj.listVar = inValue
        assert validationObj.listVar == outValue
        assert type(validationObj.listVar) == type(outValue)

    @mark.parametrize('inValue', [
        5,
        None,
    ])
    def test_listErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.listVar = inValue

    @mark.parametrize('inValue, types, outValue', [
        ((1, 2), (int), [1, 2]),
        ([1, 4, 2.1, 'a'], (int, float, str), [1, 4, 2.1, 'a']),
    ])
    def test_listWithTypes(self,
                           validationObj: ClassWithValidation,
                           inValue: Any,
                           types: Iterable,
                           outValue: list) -> None:
        def validate_listWithTypesVar(value: Any) -> list:
            return ValidationClass.validateList(value, types)
        validationObj.validate_listWithTypesVar = validate_listWithTypesVar
        validationObj.listWithTypesVar = inValue
        assert validationObj.listWithTypesVar == outValue
        assert type(validationObj.listWithTypesVar) == type(outValue)

    @mark.parametrize('inValue, types', [
        ((1, 2), (float)),
        ([1, 4, 2.1, 'a'], (int, str)),
    ])
    def test_listWithTypesErrors(self,
                                  validationObj: ClassWithValidation,
                                  inValue: Any,
                                  types: Iterable) -> None:
        def validate_listWithTypesVar(value: Any) -> list:
            return ValidationClass.validateList(value, types)
        validationObj.validate_listWithTypesVar = validate_listWithTypesVar
        with raises(TypeError):
            validationObj.listWithTypesVar = inValue




    @mark.parametrize('inValue, outValue', [
        ({'a': 1, 'b': 2}, {'a': 1, 'b': 2}),
        ([('a', 1), ('b', 2)], {'a': 1, 'b': 2}),
        ((('a', 1), ('b', 2)), {'a': 1, 'b': 2})
    ])
    def test_dict(self, validationObj: ClassWithValidation, inValue: Any, outValue: dict) -> None:
        validationObj.dictVar = inValue
        assert validationObj.dictVar == outValue
        assert type(validationObj.dictVar) == type(outValue)

    @mark.parametrize('inValue', [
        5,
        None,
        (1, 'a'),
        'abcd'
    ])
    def test_dictErrors(self, validationObj: ClassWithValidation, inValue: Any) -> None:
        with raises(TypeError):
            validationObj.dictVar = inValue

    @mark.parametrize('inValue, types, outValue', [
        ({'a': 1, 'b': 2}, (int), {'a': 1, 'b': 2}),
        ({'a': 1.2, 'b': 2}, (int, float), {'a': 1.2, 'b': 2}),
        ([('a', 'a'), ('b', 2)], (int, str), {'a': 'a', 'b': 2}),
    ])
    def test_dictWithTypes(self,
                           validationObj: ClassWithValidation,
                           inValue: Any,
                           types: Iterable,
                           outValue: dict) -> None:
        def validate_dictWithTypesVar(value: Any) -> dict:
            return ValidationClass.validateDict(value, types)
        validationObj.validate_dictWithTypesVar = validate_dictWithTypesVar
        validationObj.dictWithTypesVar = inValue
        assert validationObj.dictWithTypesVar == outValue
        assert type(validationObj.dictWithTypesVar) == type(outValue)

    @mark.parametrize('inValue, types', [
        ({'a': 1.2, 'b': 2}, (int)),
        ([('a', 'a'), ('b', 2)], (str)),
    ])
    def test_dictWithTypesErrors(self,
                                  validationObj: ClassWithValidation,
                                  inValue: Any,
                                  types: Iterable) -> None:
        def validate_dictWithTypesVar(value: Any) -> dict:
            return ValidationClass.validateDict(value, types)
        validationObj.validate_dictWithTypesVar = validate_dictWithTypesVar
        with raises(TypeError):
            validationObj.dictWithTypesVar = inValue
