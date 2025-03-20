from typing import *
import asyncio
import logging
import os
import traceback
import sys
import json
import datetime
import re
import copy
import pytz
from copy import deepcopy

from .config import NODEENV, dateTimeFormatInitial, dateFormatInitial, timeFormatInitial
from .JON_default import cleanField, JONDefaultSchema, defaultMapError, ConvertStringToInitialType, isObject, isDatetimeFormat, getDate, isDate, isString, isNumber, isBoolean, convertToBoolean
from .utils import getLang


log = logging.getLogger(__name__)

def checkIfCorrectTypeSchema(value: any):
    return (
        type(value) is String or
        isinstance(type(value), String) or
        issubclass(type(value), String) or
        type(value) is Number or
        isinstance(type(value), Number) or
        issubclass(type(value), Number) or
        type(value) is Boolean or
        isinstance(type(value), Boolean) or
        issubclass(type(value), Boolean) or
        type(value) is Date or
        isinstance(type(value), Date) or
        issubclass(type(value), Date) or
        type(value) is Enum or
        isinstance(type(value), Enum) or
        issubclass(type(value), Enum) or
        type(value) is ChosenType or
        isinstance(type(value), ChosenType) or
        issubclass(type(value), ChosenType) or
        type(value) is Object or
        isinstance(type(value), Object) or
        issubclass(type(value), Object) or
        type(value) is Array or
        isinstance(type(value), Array) or
        issubclass(type(value), Array) or
        type(value) is AnyType or
        isinstance(type(value), AnyType) or
        issubclass(type(value), AnyType)
    )
def convertInCorrectSchemaType(value: any):
    return value if(checkIfCorrectTypeSchema(value)) else None
def isCorrectType(
    value: any,
):
    return (
        type(value) in (list, tuple, dict, int, str, float, bool) or
        type(value) is datetime.datetime or
        type(value) is datetime.date or
        type(value) is datetime.time
    )


class Array(JONDefaultSchema):
    _maxValue: str = None
    _minValue: str = None
    _lessValue: str = None
    _greaterValue: str = None
    _lengthValue: str = None
    _types: list = []
    
    _ARRAY__RULE = None
    _ARRAY__TYPE__RULE = None
    _ARRAY__MIN__RULE = None
    _ARRAY__MAX__RULE = None
    _ARRAY__LESS__RULE = None
    _ARRAY__GREATER__RULE = None
    _ARRAY__LENGTH__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.array()

    def array(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    type(value) in (list, tuple) or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas un tableau".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not an array".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Array | array - rule - valueInitial:: ", valueInitial)
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__RULE = rule
        return self
    def types(self, *values):
        labelSTR = json.dumps(f"{self.get_label()}")
        def checker1Action():
            if not(type(values) in (list, tuple) and len(values) > 0):
                def rule(valueInitial):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un ou plusieurs types invalides pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has one or more invalid types for analysis".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                self.addRule(rule)
                self._ARRAY__TYPE__RULE = rule
                return self
        checker1 = checker1Action()
        if checker1 is not None:
            return self
        def checker2Action():
            datasTA = []
            if len(values) > 0:
                for indexTypeArray, typeArray in enumerate(values):
                    if not(
                        type(typeArray) is Number or
                        isinstance(type(typeArray), Number) or
                        type(typeArray) is String or
                        isinstance(type(typeArray), String) or
                        type(typeArray) is Boolean or
                        isinstance(type(typeArray), Boolean) or
                        type(typeArray) is Date or
                        isinstance(type(typeArray), Date) or
                        type(typeArray) is Enum or
                        isinstance(type(typeArray), Enum) or
                        type(typeArray) is NotEnum or
                        isinstance(type(typeArray), NotEnum) or
                        type(typeArray) is Object or
                        isinstance(type(typeArray), Object) or
                        type(typeArray) is Array or
                        isinstance(type(typeArray), Array) or
                        type(typeArray) is ChosenType or
                        isinstance(type(typeArray), ChosenType) or
                        type(typeArray) is AnyType or
                        isinstance(type(typeArray), AnyType)
                    ):
                        def rule(valueInitial):
                            return {
                                'valid': False,
                                'value': None,
                                'error': Exception({
                                    'fr': f"{labelSTR} a un ou plusieurs types invalides ({cleanField(typeArray)}) pour analyse",
                                    'en': f"{labelSTR} has one or more invalid types ({cleanField(typeArray)}) for analysis",
                                }[self.get_lang()])
                            }
                        self.addRule(rule)
                        self._ARRAY__TYPE__RULE = rule
                        datasTA = None
                        break
                    datasTA.append(typeArray)
            return datasTA
        typesArray = []
        checker2 = checker2Action()
        if not(type(checker2) in (list, tuple)):
            return self
        typesArray = checker2
        if NODEENV == 'debug':
            print("[jon -> JON_sup.py] Array | types - rule - typesArray:: ", typesArray)
        def compareArrayValueWithTypes(indexVal, val):
            try:
                validation = {
                    'valid': True,
                    'data': val,
                    'error': None
                } if val is None else None
                errorValidation = None
                if val is not None:
                    for indexTypeArray, typeArray in enumerate(typesArray):
                        schemaTypeArray = typeArray.label(f"{self.get_label()}[{indexVal}]")
                        validationVal = schemaTypeArray.validate(val)
                        validationVal['error_rule'] = schemaTypeArray._errorRule
                        if NODEENV == 'debug':
                            print("[jon -> JON_sup.py] Array | types - rule - compareArrayValueWithTypes - indexVal:: ", indexVal)
                            print("[jon -> JON_sup.py] Array | types - rule - compareArrayValueWithTypes - val:: ", val)
                            print("[jon -> JON_sup.py] Array | types - rule - compareArrayValueWithTypes - validationVal:: ", validationVal)
                        if validationVal['valid'] == True:
                            validation = validationVal
                            errorValidation = None
                            break
                        else:
                            if errorValidation is None:
                                errorValidation = validationVal
                if errorValidation is not None:
                    validation = errorValidation
                if validation is None:
                    validation = {
                        'valid': True,
                        'data': val,
                        'error': None
                    }
                return validation
            except Exception as err:
                stack = traceback.format_exc()
                log.error(stack)
                return {
                    'data': None,
                    'valid': False,
                    'error': str(stack),
                }
        def compareArrayWithTypes(valueInitial):
            try:
                if not(type(valueInitial) in (list, tuple) or valueInitial is None):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un type invalide pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has an invalid type for analyse".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                successValidationDatas = []
                successValidation = {
                    'data': valueInitial,
                    'valid': True,
                    'error': None,
                }
                errorValidation = None
                if valueInitial is not None:
                    for indexVal, val in enumerate(valueInitial):
                        valIsTrue = False
                        validationVal = compareArrayValueWithTypes(indexVal = indexVal, val = val)
                        if NODEENV == 'debug':
                            print("[jon -> JON_sup.py] Array | types - rule - compareArrayWithTypes - val:: ", val)
                            print("[jon -> JON_sup.py] Array | types - rule - compareArrayWithTypes - validationVal:: ", validationVal)
                        if validationVal['valid'] == True:
                            successValidation = validationVal
                            successValidationDatas.append(validationVal['data'])
                            errorValidation = None
                        if not(validationVal['valid'] == True) and errorValidation is None:
                            successValidation = None
                            successValidationDatas = None
                            errorValidation = validationVal
                            break
                if errorValidation is not None:
                    return errorValidation
                return {
                    'data': successValidationDatas if valueInitial is not None else None,
                    'valid': successValidation['valid'],
                    'error': successValidation['error'],
                }
            except Exception as err:
                stack = traceback.format_exc()
                log.error(stack)
                return {
                    'data': None,
                    'valid': False,
                    'error': str(stack),
                }


        if NODEENV == 'debug':
            print("[jon -> JON_sup.py] Array | types - rule - typesArray:: ", typesArray)
        def rule(valueInitial):
            typeArrayCmps = None
            validationFinal = compareArrayWithTypes(valueInitial = valueInitial)
            def sanitizeFunct(value: any) -> str:
                return validationFinal['data']
            def ruleFunct(value):
                return validationFinal['valid']
            def errorFunct(value):
                return validationFinal['error']
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Array | types - rule - valueInitial:: ", valueInitial)
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__TYPE__RULE = rule
        return self

    def min(self, minValue: int):
        self._minValue = minValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) in (list, tuple) and
                        len(value) >= minValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._maxValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être compris entre {min} et {max}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                            'en': "the size of {label} must be between {min} and {max}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être au minimum {min}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                            'en': "the size of {label} must be at least {min}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__MIN__RULE = rule
        return self
    def max(self, maxValue: int):
        self._maxValue = maxValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) in (list, tuple) and
                        len(value) <= maxValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._minValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être compris entre {min} et {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = maxValue,
                            ),
                            'en': "the size of {label} must be between {min} and {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = maxValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être au maximum {max}".format(
                                label = labelSTR,
                                max = maxValue,
                            ),
                            'en': "the size of {label} must be maximum {max}".format(
                                label = labelSTR,
                                max = maxValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__MAX__RULE = rule
        return self
    def less(self, lessValue: int):
        self._lessValue = lessValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) in (list, tuple) and
                        len(value) < lessValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._greaterValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être inférieure à {less} et superieure à {greater}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "the size of {label} must be less than {less} and greater than {greater}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être inferieure à {less}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "the size of {label} must be less than {less}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__LESS__RULE = rule
        return self
    def greater(self, greaterValue: int):
        self._greaterValue = greaterValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) in (list, tuple) and
                        len(value) > greaterValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._lessValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être inférieure à {less} et superieure à {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = greaterValue,
                            ),
                            'en': "the size of {label} must be less than {less} and greater than {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = greaterValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être supérieur à {greater}".format(
                                label = labelSTR,
                                greater = greaterValue,
                            ),
                            'en': "the size of {label} must be greater than {greater}".format(
                                label = labelSTR,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__GREATER__RULE = rule
        return self
    def length(self, lengthValue: int):
        self._lengthValue = lengthValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) in (list, tuple) and
                        len(value) == lengthValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être égale à {length}".format(
                            label = labelSTR,
                            length = lengthValue,
                        ),
                        'en': "the size of {label} must be equal to {length}".format(
                            label = labelSTR,
                            length = self._lengthValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__LENGTH__RULE = rule
        return self

    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.arrayValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ArrayString | arrayValidation - ruleData (For Array):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ArrayString | arrayValidation - ruleData (For Primary):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ArrayString | arrayValidation - ruleDataF:: ", ruleDataF)
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Array | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def arrayValidation(self, value):
        try:
            ruleDataF = None

            if self._ARRAY__RULE is not None:
                ruleData = self._ARRAY__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__RULE"
                    if NODEENV == 'debug':
                        print("[jon -> JON_sup.py] Array | arrayValidation - ruleData:: ", ruleData)
                        print("[jon -> JON_sup.py] Array | arrayValidation - self._errorRule:: ", self._errorRule)
                    return ruleDataF
            if self._ARRAY__MIN__RULE is not None:
                ruleData = self._ARRAY__MIN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__MIN__RULE"
                    return ruleDataF
            if self._ARRAY__MAX__RULE is not None:
                ruleData = self._ARRAY__MAX__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__MAX__RULE"
                    return ruleDataF
            if self._ARRAY__LESS__RULE is not None:
                ruleData = self._ARRAY__LESS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__LESS__RULE"
                    return ruleDataF
            if self._ARRAY__GREATER__RULE is not None:
                ruleData = self._ARRAY__GREATER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__GREATER__RULE"
                    return ruleDataF
            if self._ARRAY__LENGTH__RULE is not None:
                ruleData = self._ARRAY__LENGTH__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__LENGTH__RULE"
                    return ruleDataF
            if self._ARRAY__TYPE__RULE is not None:
                ruleData = self._ARRAY__TYPE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ARRAY__TYPE__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
class Object(JONDefaultSchema):
    _struct: dict = {}
    _primaryStruct: bool = False
    _maxValue: str = None
    _minValue: str = None
    _lessValue: str = None
    _greaterValue: str = None
    _lengthValue: str = None

    _struct: dict = None
    _primaryStruct: bool = False
    
    _oldValueForStruct = None
    
    _OBJECT__RULE = None
    _OBJECT__STRUCT__RULE = None
    _OBJECT__PRIMARY_STRUCT__RULE = None
    _OBJECT__TYPES_VALUES__RULE = None
    _OBJECT__CONTAINS_KEYS__RULE = None
    _OBJECT__NO_CONTAINS_KEYS__RULE = None
    _OBJECT__REGEXP_CONTAINS_KEYS__RULE = None
    _OBJECT__REGEXP_NO_CONTAINS_KEYS__RULE = None
    _OBJECT__MIN__RULE = None
    _OBJECT__MAX__RULE = None
    _OBJECT__LESS__RULE = None
    _OBJECT__GREATER__RULE = None
    _OBJECT__LENGTH__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.object()

    def object(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> any:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    type(value) == dict or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas un objet".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not an object".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Object | object - rule - valueInitial:: ", valueInitial)
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__RULE = rule
        return self
    def structAction(self, values: dict):
        labelSTR = json.dumps(f"{self.get_label()}")
        def checker1Action():
            if not(type(values) == dict and len(tuple(values.keys())) > 0):
                def rule(valueInitial):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un ou plusieurs types invalides pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has one or more invalid types for analysis".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                self.addRule(rule)
                self._OBJECT__STRUCT__RULE = rule
                return self
        checker1 = checker1Action()
        if checker1 is not None:
            return self
        def checker2Action():
            datasTO = {}
            if len(tuple(values.keys())) > 0:
                for keyTypeObject, typeObject in values.items():
                    if not(
                        type(typeObject) is Number or
                        isinstance(type(typeObject), Number) or
                        type(typeObject) is String or
                        isinstance(type(typeObject), String) or
                        type(typeObject) is Boolean or
                        isinstance(type(typeObject), Boolean) or
                        type(typeObject) is Date or
                        isinstance(type(typeObject), Date) or
                        type(typeObject) is Enum or
                        isinstance(type(typeObject), Enum) or
                        type(typeObject) is NotEnum or
                        isinstance(type(typeObject), NotEnum) or
                        type(typeObject) is Object or
                        isinstance(type(typeObject), Object) or
                        type(typeObject) is Array or
                        isinstance(type(typeObject), Array) or
                        type(typeObject) is ChosenType or
                        isinstance(type(typeObject), ChosenType) or
                        type(typeObject) is AnyType or
                        isinstance(type(typeObject), AnyType)
                    ):
                        def rule(valueInitial):
                            return {
                                'valid': False,
                                'value': None,
                                'error': Exception({
                                    'fr': f"L'attribut '{keyTypeObject}' de l'element {labelSTR} a un type invalide ({cleanField(typeObject)}) pour analyse",
                                    'en': f"The '{keyTypeObject}' attribute of the {labelSTR} element has an invalid type ({cleanField(typeObject)}) for analysis.",
                                }[self.get_lang()])
                            }
                        self.addRule(rule)
                        self._OBJECT__STRUCT__RULE = rule
                        datasTO = None
                        break
                    datasTO[keyTypeObject] = typeObject
            return datasTO
        typesObject = {}
        checker2 = checker2Action()
        if not(type(checker2) == dict):
            return self
        typesObject = checker2
        self._struct = typesObject
        if NODEENV == 'debug':
            print("[jon -> JON_sup.py] Object | struct - rule - typesObject:: ", typesObject)
        def compareObject(valueInitial):
            try:
                valueInitialClone = {
                    **valueInitial
                } if type(valueInitial) == dict else valueInitial
                if not(type(valueInitial) == dict or valueInitial is None):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un type invalide pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has an invalid type for analyse".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                successValidationDatas = {}
                successValidation = {
                    'data': valueInitial,
                    'valid': True,
                    'error': None,
                }
                errorValidation = None
                if valueInitial is not None:
                    if NODEENV == 'debug':
                        print("[jon -> JON_sup.py] Object | struct - rule - compareObject - typesObject:: ", typesObject)
                    for keyTypeObject, typeObject in typesObject.items():
                        schemaTypeObject = typeObject.label(f"{self.get_label()}['{keyTypeObject}']")

                        valueInitialTarget = valueInitial[keyTypeObject] if keyTypeObject in tuple(valueInitial.keys()) else None
                        validationVal = schemaTypeObject.validate(valueInitialTarget)
                        if NODEENV == 'debug' and not(validationVal['valid'] == True):
                            print("[jon -> JON_sup.py] Object | struct - rule - compareObject - keyTypeObject:: ", keyTypeObject)
                            print("[jon -> JON_sup.py] Object | struct - rule - compareObject - valueInitialTarget:: ", valueInitialTarget)
                        if NODEENV == 'debug':
                            print("[jon -> JON_sup.py] Object | struct - rule - compareObject - validationVal:: ", validationVal)
                            print("[jon -> JON_sup.py] Object | struct - rule - compareObject - schemaTypeObject:: ", schemaTypeObject)
                        validationVal['error_rule'] = schemaTypeObject._errorRule
                        if validationVal['valid'] == True:
                            successValidation = validationVal
                            successValidationDatas[keyTypeObject] = validationVal['data']
                            errorValidation = None
                        if not(validationVal['valid']):
                            successValidation = None
                            successValidationDatas = None
                            errorValidation = validationVal
                            break
                if errorValidation is not None:
                    return errorValidation
                if NODEENV == 'debug':
                    print("[jon -> JON_sup.py] Object | struct - rule - compareObject - valueInitialClone:: ", valueInitialClone)
                    print("[jon -> JON_sup.py] Object | struct - rule - compareObject - self._primaryStruct:: ", self._primaryStruct)
                    print("[jon -> JON_sup.py] Object | struct - rule - compareObject - successValidationDatas:: ", successValidationDatas)
                    print("[jon -> JON_sup.py] Object | struct - rule - compareObject - len(tuple(valueInitialClone.keys())):: ", len(tuple(valueInitialClone.keys())))
                    print("[jon -> JON_sup.py] Object | struct - rule - compareObject - len(tuple(successValidationDatas.keys())):: ", len(tuple(successValidationDatas.keys())))
                if self._primaryStruct == True and not(
                    valueInitial is None or (
                        valueInitial is not None and
                        len(tuple(valueInitialClone.keys())) == len(tuple(successValidationDatas.keys()))
                    )
                ):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} doit avoir le même nombre d'attributs que la structure de validation".format(
                                label = labelSTR,
                            ),
                            'en': "{label} must have the same number of attributes as the validation structure".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                    
                return {
                    'data': successValidationDatas if valueInitial is not None else None,
                    'valid': successValidation['valid'],
                    'error': successValidation['error'],
                }
            except Exception as err:
                stack = traceback.format_exc()
                log.error(stack)
                return {
                    'data': None,
                    'valid': False,
                    'error': str(stack),
                }

        def rule(valueInitial):
            validationFinal = compareObject(valueInitial = valueInitial)
            def sanitizeFunct(value: any) -> any:
                return validationFinal['data']
            def ruleFunct(value):
                return validationFinal['valid']
            def errorFunct(value):
                return validationFinal['error']
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Object | struct - rule - valueInitial:: ", valueInitial)
                print("[jon -> JON_sup.py] Object | struct - rule - validationFinal:: ", validationFinal)
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        if self._primaryStruct:
            self._OBJECT__PRIMARY_STRUCT__RULE = rule
        else:
            self._OBJECT__STRUCT__RULE = rule
        return self
    def struct(self, values: dict):
        self._primaryStruct = False
        return self.structAction(values=values)
    def primaryStruct(self, values: dict):
        self._primaryStruct = True
        return self.structAction(values=values)
    def getStruct(self,):
        return self._struct
    
    def typesValues(self, *values):
        labelSTR = json.dumps(f"{self.get_label()}")
        def checker1Action():
            if not(type(values) in (list, tuple) and len(values) > 0):
                def rule(valueInitial):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un ou plusieurs typesValues invalides pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has one or more invalid typesValues for analysis".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                self.addRule(rule)
                self._OBJECT__TYPES_VALUES__RULE = rule
                return self
        checker1 = checker1Action()
        if checker1 is not None:
            return self
        def checker2Action():
            datasTA = []
            if len(values) > 0:
                for indexTypeObject, typeObject in enumerate(values):
                    if not(
                        type(typeObject) is Number or
                        isinstance(type(typeObject), Number) or
                        type(typeObject) is String or
                        isinstance(type(typeObject), String) or
                        type(typeObject) is Boolean or
                        isinstance(type(typeObject), Boolean) or
                        type(typeObject) is Date or
                        isinstance(type(typeObject), Date) or
                        type(typeObject) is Enum or
                        isinstance(type(typeObject), Enum) or
                        type(typeObject) is NotEnum or
                        isinstance(type(typeObject), NotEnum) or
                        type(typeObject) is Object or
                        isinstance(type(typeObject), Object) or
                        type(typeObject) is Array or
                        isinstance(type(typeObject), Array) or
                        type(typeObject) is ChosenType or
                        isinstance(type(typeObject), ChosenType) or
                        type(typeObject) is AnyType or
                        isinstance(type(typeObject), AnyType)
                    ):
                        def rule(valueInitial):
                            return {
                                'valid': False,
                                'value': None,
                                'error': Exception({
                                    'fr': f"{labelSTR} a un ou plusieurs typesValues invalides ({cleanField(typeObject)}) pour analyse",
                                    'en': f"{labelSTR} has one or more invalid typesValues ({cleanField(typeObject)}) for analysis",
                                }[self.get_lang()])
                            }
                        self.addRule(rule)
                        self._OBJECT__TYPES_VALUES__RULE = rule
                        datasTA = None
                        break
                    datasTA.append(typeObject)
            return datasTA
        typesObject = []
        checker2 = checker2Action()
        if not(type(checker2) in (list, tuple)):
            return self
        typesObject = checker2
        if NODEENV == 'debug':
            print("[jon -> JON_sup.py] Object | typesValues - rule - typesObject:: ", typesObject)
        def compareObjectValueWithTypes(keyVal, val):
            try:
                validation = {
                    'valid': True,
                    'data': val,
                    'error': None
                }
                errorValidation = None
                for indexTypeObject, typeObject in enumerate(typesObject):
                    schemaTypeObject = typeObject.label(f"{self.get_label()}['{keyVal}']")
                    validationVal = schemaTypeObject.validate(val)
                    validationVal['error_rule'] = schemaTypeObject._errorRule
                    if NODEENV == 'debug':
                        print("[jon -> JON_sup.py] Object | typesValues - rule - compareObjectValueWithTypes - val:: ", val)
                        print("[jon -> JON_sup.py] Object | typesValues - rule - compareObjectValueWithTypes - typeObject:: ", typeObject)
                        print("[jon -> JON_sup.py] Object | typesValues - rule - compareObjectValueWithTypes - validationVal:: ", validationVal)
                    if validationVal['valid'] == True:
                        validation = validationVal
                        errorValidation = None
                        break
                    if not(validationVal['valid'] == True) and errorValidation is None:
                        errorValidation = validationVal
                        validation = None
                if errorValidation is not None:
                    validation = errorValidation
                return validation
            except Exception as err:
                stack = traceback.format_exc()
                log.error(stack)
                return {
                    'data': None,
                    'valid': False,
                    'error': str(stack),
                }
        def compareObjectWithTypes(valueInitial):
            try:
                if not(type(valueInitial) == dict or valueInitial is None):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un type invalide pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has an invalid type for analyse".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                successValidationDatas = {}
                successValidation = {
                    'data': valueInitial,
                    'valid': True,
                    'error': None,
                }
                errorValidation = None
                if valueInitial is not None:
                    for keyVal, val in valueInitial.items():
                        validationVal = compareObjectValueWithTypes(keyVal = keyVal, val = val)
                        if NODEENV == 'debug':
                            print("[jon -> JON_sup.py] Object | typesValues - rule - compareObjectWithTypes - validationVal:: ", validationVal)
                        if validationVal['valid'] == True:
                            successValidation = validationVal
                            successValidationDatas[keyVal] = validationVal['data']
                            errorValidation = None
                        if not(validationVal['valid']):
                            successValidation = None
                            successValidationDatas = None
                            errorValidation = validationVal
                            break
                if errorValidation is not None:
                    return errorValidation
                return {
                    'data': successValidationDatas if valueInitial is not None else None,
                    'valid': successValidation['valid'],
                    'error': successValidation['error'],
                }
            except Exception as err:
                stack = traceback.format_exc()
                log.error(stack)
                return {
                    'data': None,
                    'valid': False,
                    'error': str(stack),
                }


        if NODEENV == 'debug':
            print("[jon -> JON_sup.py] Object | typesValues - rule - typesObject:: ", typesObject)
        def rule(valueInitial):
            validationFinal = compareObjectWithTypes(valueInitial = valueInitial)
            def sanitizeFunct(value: any) -> str:
                return validationFinal['data']
            def ruleFunct(value):
                return validationFinal['valid']
            def errorFunct(value):
                return validationFinal['error']
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Object | typesValues - rule - valueInitial:: ", valueInitial)
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__TYPES_VALUES__RULE = rule
        return self

    def containsKeys(self, keys = [], strict = False):
        strict = strict if type(strict) == bool else False
        keys = keys if type(keys) in (list, tuple) else []
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and (
                            (
                                strict == False and
                                len([key for key in keys if (
                                    key in tuple(value.keys())
                                )]) > 0
                            ) or 
                            (
                                strict == True and
                                len([key for key in keys if (
                                    key in tuple(value.keys())
                                )]) == len(keys)
                            )
                        )
                    )
                )
            def errorFunct(value):
                invalidKeys = [key for key in keys if not(
                    key in tuple(value.keys())
                )]
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(self.get_label())
                    if(not(len(keys) > 0)):
                        err = Exception({
                            'fr': "{label} ne possede aucune clé à verifier pour la validation".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has no key to check for validation".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    elif(invalidKeys is not None and len(invalidKeys) > 0):
                        err = Exception({
                            'fr': "{label} possède une ou plusieurs clés indefinis: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: '"{0}"'.format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                            'en': "{label} has one or more undefined keys: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: "'{0}'".format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} est d'un type invalide".format(
                                label = labelSTR,
                            ),
                            'en': "{label} is of an invalid type".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__CONTAINS_KEYS__RULE = rule
        return self
    def noContainsKeys(self, keys = [], strict = False):
        strict = strict if type(strict) == bool else False
        keys = keys if type(keys) in (list, tuple) else []
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and (
                            (
                                strict == False and
                                len([key for key in keys if not(
                                    key in tuple(value.keys())
                                )]) > 0
                            ) or 
                            (
                                strict == True and
                                len([key for key in keys if not(
                                    key in tuple(value.keys())
                                )]) >= len(keys)
                            )
                        )
                    )
                )
            def errorFunct(value):
                invalidKeys = [key for key in keys if (
                    key in tuple(value.keys())
                )]
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(self.get_label())
                    if(not(len(keys) > 0)):
                        err = Exception({
                            'fr': "{label} ne possede aucune clé à verifier pour la validation".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has no key to check for validation".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    elif(invalidKeys is not None and len(invalidKeys) > 0):
                        err = Exception({
                            'fr': "{label} possède une ou plusieurs clés definis: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: '"{0}"'.format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                            'en': "{label} has one or more defined keys: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: "'{0}'".format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} est d'un type invalide".format(
                                label = labelSTR,
                            ),
                            'en': "{label} is of an invalid type".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__NO_CONTAINS_KEYS__RULE = rule
        return self

    def regExpContainsKeys(self, ruleValue: str, flag: re.RegexFlag = None, strict: bool = False):
        strict = strict if type(strict) == bool else False
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and (
                            (
                                strict == False and
                                len([keyValue for keyValue, value in value.items() if (
                                    String(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) > 0
                            ) or 
                            (
                                strict == True and
                                len([keyValue for keyValue, value in value.items() if (
                                    String(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) >= len(tuple(value.keys()))
                            )
                        )
                    )
                )
            def errorFunct(value):
                invalidKeys = [keyValue for keyValue, value in value.items() if not(
                    String(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                )]
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(self.get_label())
                    if(not(len(list(value.keys())) > 0)):
                        err = Exception({
                            'fr': "{label} ne possede aucune clé à verifier pour la validation".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has no key to check for validation".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    elif(invalidKeys is not None and len(invalidKeys) > 0):
                        err = Exception({
                            'fr': "{label} possède une ou plusieurs clés au format invalide: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: '"{0}"'.format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                            'en': "{label} has one or more invalidly formatted keys: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: "'{0}'".format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} est d'un type invalide".format(
                                label = labelSTR,
                            ),
                            'en': "{label} is of an invalid type".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__REGEXP_CONTAINS_KEYS__RULE = rule
        return self
    def regExpNoContainsKeys(self, ruleValue: str, flag: re.RegexFlag = None, strict: bool = False):
        strict = strict if type(strict) == bool else False
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and (
                            (
                                strict == False and
                                len([keyValue for keyValue, value in value.items() if not(
                                    String(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) > 0
                            ) or 
                            (
                                strict == True and
                                len([keyValue for keyValue, value in value.items() if not(
                                    String(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) >= len(tuple(value.keys()))
                            )
                        )
                    )
                )
            def errorFunct(value):
                invalidKeys = [keyValue for keyValue, value in value.items() if (
                    String(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                )]
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(self.get_label())
                    if(not(len(list(value.keys())) > 0)):
                        err = Exception({
                            'fr': "{label} ne possede aucune clé à verifier pour la validation".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has no key to check for validation".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    elif(invalidKeys is not None and len(invalidKeys) > 0):
                        err = Exception({
                            'fr': "{label} ne possède pas des clés au format: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: '"{0}"'.format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                            'en': "{label} does not have keys in: {attrs}".format(
                                label = labelSTR,
                                attrs = ', '.join(list(
                                    map(
                                        lambda key: "'{0}'".format(key),
                                        invalidKeys
                                    )
                                )),
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} est d'un type invalide".format(
                                label = labelSTR,
                            ),
                            'en': "{label} is of an invalid type".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__REGEXP_NO_CONTAINS_KEYS__RULE = rule
        return self
    
    def min(self, minValue: int):
        self._minValue = minValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and
                        len(value.keys()) >= minValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._maxValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être compris entre {min} et {max}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                            'en': "the size of {label} must be between {min} and {max}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être au minimum {min}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                            'en': "the size of {label} must be at least {min}".format(
                                label = labelSTR,
                                min = minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__MIN__RULE = rule
        return self
    def max(self, maxValue: int):
        self._maxValue = maxValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and
                        len(value.keys()) <= maxValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._minValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être compris entre {min} et {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = maxValue,
                            ),
                            'en': "the size of {label} must be between {min} and {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = maxValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être au maximum {max}".format(
                                label = labelSTR,
                                max = maxValue,
                            ),
                            'en': "the size of {label} must be maximum {max}".format(
                                label = labelSTR,
                                max = maxValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__MAX__RULE = rule
        return self
    def less(self, lessValue: int):
        self._lessValue = lessValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and
                        len(value.keys()) > lessValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._greaterValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être inférieure à {less} et superieure à {greater}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "the size of {label} must be less than {less} and greater than {greater}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être inferieure à {less}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "the size of {label} must be less than {less}".format(
                                label = labelSTR,
                                less = lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__LESS__RULE = rule
        return self
    def greater(self, greaterValue: int):
        self._greaterValue = greaterValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and
                        len(value.keys()) < greaterValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._lessValue is not None
                    ):
                        err = Exception({
                            'fr': "la taille de {label} doit être inférieure à {less} et superieure à {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = greaterValue,
                            ),
                            'en': "the size of {label} must be less than {less} and greater than {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = greaterValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "la taille de {label} doit être supérieur à {greater}".format(
                                label = labelSTR,
                                greater = greaterValue,
                            ),
                            'en': "the size of {label} must be greater than {greater}".format(
                                label = labelSTR,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__GREATER__RULE = rule
        return self
    def length(self, lengthValue: int):
        self._lengthValue = lengthValue
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        type(value) == dict and
                        len(value.keys()) == lengthValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être égale à {length}".format(
                            label = labelSTR,
                            length = lengthValue,
                        ),
                        'en': "the size of {label} must be equal to {length}".format(
                            label = labelSTR,
                            length = self._lengthValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__LENGTH__RULE = rule
        return self

    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.objectValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ObjectString | objectValidation - ruleData (For String):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ObjectString | objectValidation - ruleData (For Primary):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ObjectString | objectValidation - ruleDataF:: ", ruleDataF)
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Object | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def objectValidation(self, value):
        try:
            ruleDataF = None

            if self._OBJECT__RULE is not None:
                ruleData = self._OBJECT__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__RULE"
                    return ruleDataF
            if self._OBJECT__STRUCT__RULE is not None:
                ruleData = self._OBJECT__STRUCT__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__STRUCT__RULE"
                    return ruleDataF
            if self._OBJECT__PRIMARY_STRUCT__RULE is not None:
                ruleData = self._OBJECT__PRIMARY_STRUCT__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__PRIMARY_STRUCT__RULE"
                    return ruleDataF
            if self._OBJECT__TYPES_VALUES__RULE is not None:
                ruleData = self._OBJECT__TYPES_VALUES__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__TYPES_VALUES__RULE"
                    return ruleDataF
            if self._OBJECT__CONTAINS_KEYS__RULE is not None:
                ruleData = self._OBJECT__CONTAINS_KEYS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__CONTAINS_KEYS__RULE"
                    return ruleDataF
            if self._OBJECT__NO_CONTAINS_KEYS__RULE is not None:
                ruleData = self._OBJECT__NO_CONTAINS_KEYS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__NO_CONTAINS_KEYS__RULE"
                    return ruleDataF
            if self._OBJECT__REGEXP_CONTAINS_KEYS__RULE is not None:
                ruleData = self._OBJECT__REGEXP_CONTAINS_KEYS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__REGEXP_CONTAINS_KEYS__RULE"
                    return ruleDataF
            if self._OBJECT__REGEXP_NO_CONTAINS_KEYS__RULE is not None:
                ruleData = self._OBJECT__REGEXP_NO_CONTAINS_KEYS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__REGEXP_NO_CONTAINS_KEYS__RULE"
                    return ruleDataF
            if self._OBJECT__MIN__RULE is not None:
                ruleData = self._OBJECT__MIN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__MIN__RULE"
                    return ruleDataF
            if self._OBJECT__MAX__RULE is not None:
                ruleData = self._OBJECT__MAX__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__MAX__RULE"
                    return ruleDataF
            if self._OBJECT__LESS__RULE is not None:
                ruleData = self._OBJECT__LESS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__LESS__RULE"
                    return ruleDataF
            if self._OBJECT__GREATER__RULE is not None:
                ruleData = self._OBJECT__GREATER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__GREATER__RULE"
                    return ruleDataF
            if self._OBJECT__LENGTH__RULE is not None:
                ruleData = self._OBJECT__LENGTH__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "OBJECT__LENGTH__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp

class ChosenType(JONDefaultSchema):
    _types = []
    _invalid_types = []

    _CHOSEN_TYPE__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def chosenTypes(self):
        def compareElementWithTypes(valueInitial):
            try:
                validation = {
                    'valid': True,
                    'data': valueInitial,
                    'error': None
                }
                errorIndex = None
                errorValidation = None
                for indexCEWT, typeCEWT in enumerate(self._types):
                    if NODEENV == 'debug':
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - self._types[{indexCEWT}] - valueInitial:: ", valueInitial)
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - self._types[{indexCEWT}] - typeCEWT:: ", typeCEWT)
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - self._types[{indexCEWT}] - typeCEWT._default:: ", typeCEWT._default)
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - self._types[{indexCEWT}] - self._default:: ", self._default)
                    schemaTypeArray = typeCEWT.label(self.get_label())
                    valueForVV = valueInitial
                    if valueInitial is None:
                        if typeCEWT._default is not None:
                            valueForVV = typeCEWT._default
                        else:
                            valueForVV = self._default
                    validationVal = schemaTypeArray.validate(valueForVV)
                    if NODEENV == 'debug':
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - self._types[{indexCEWT}] - valueForVV:: ", valueForVV)
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - self._types[{indexCEWT}] - validationVal:: ", validationVal)
                    validationVal['error_rule'] = schemaTypeArray._errorRule
                    if validationVal['valid'] == True:
                        validation = validationVal
                        errorValidation = None
                        break
                    if not(validationVal['valid'] == True) and errorValidation is None:
                        errorIndex = indexCEWT
                        errorValidation = validationVal
                if errorValidation is not None and not(validation['valid'] == True):
                    if NODEENV == 'debug':
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - errorIndex:: ", errorIndex)
                        print(f"[jon -> JON_sup.py] ChosenType | chosenTypes - compareElementWithTypes - errorValidation:: ", errorValidation)
                    validation = errorValidation
                return validation
            except Exception as err:
                stack = traceback.format_exc()
                log.error(stack)
                return {
                    'data': None,
                    'valid': False,
                    'error': str(stack),
                }
        def rule(valueInitial):
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ChosenType | chosenTypes - rule - self._types:: ", self._types)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ChosenType | chosenTypes - rule - valueInitial:: ", valueInitial)
            validationFinal = compareElementWithTypes(valueInitial = valueInitial)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ChosenType | chosenTypes - rule - validationFinal:: ", validationFinal)
            def sanitizeFunct(value: any) -> str:
                return validationFinal['data']
            def ruleFunct(value):
                return validationFinal['valid']
            def errorFunct(value):
                return validationFinal['error']
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ChosenType | chosenTypes - rule - valueInitial:: ", valueInitial)
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._CHOSEN_TYPE__RULE = rule
        return self
    def choices(self, *types: list):
        labelSTR = json.dumps(f"{self.get_label()}")
        def checker1Action():
            if not(type(types) in (list, tuple) and len(types) > 0):
                def rule(valueInitial):
                    return {
                        'valid': False,
                        'value': None,
                        'error': Exception({
                            'fr': "{label} a un ou plusieurs types invalides pour analyse".format(
                                label = labelSTR,
                            ),
                            'en': "{label} has one or more invalid types for analysis".format(
                                label = labelSTR,
                            ),
                        }[self.get_lang()])
                    }
                self.addRule(rule)
                self._CHOSEN_TYPE__RULE = rule
                return self
        checker1 = checker1Action()
        if checker1 is not None:
            return self
        def checker2Action():
            datasTA = []
            if len(types) > 0:
                for indexTypeCT, typeCT in enumerate(types):
                    if not(
                        type(typeCT) is Number or
                        isinstance(type(typeCT), Number) or
                        type(typeCT) is String or
                        isinstance(type(typeCT), String) or
                        type(typeCT) is Boolean or
                        isinstance(type(typeCT), Boolean) or
                        type(typeCT) is Date or
                        isinstance(type(typeCT), Date) or
                        type(typeCT) is Enum or
                        isinstance(type(typeCT), Enum) or
                        type(typeCT) is NotEnum or
                        isinstance(type(typeCT), NotEnum) or
                        type(typeCT) is Object or
                        isinstance(type(typeCT), Object) or
                        type(typeCT) is Array or
                        isinstance(type(typeCT), Array) or
                        type(typeCT) is ChosenType or
                        isinstance(type(typeCT), ChosenType) or
                        type(typeCT) is AnyType or
                        isinstance(type(typeCT), AnyType)
                    ):
                        def rule(valueInitial):
                            return {
                                'valid': False,
                                'value': None,
                                'error': Exception({
                                    'fr': f"{labelSTR} a un ou plusieurs types invalides ({cleanField(typeCT)}) pour analyse",
                                    'en': f"{labelSTR} has one or more invalid types ({cleanField(typeCT)}) for analysis",
                                }[self.get_lang()])
                            }
                        self.addRule(rule)
                        self._CHOSEN_TYPE__RULE = rule
                        datasTA = None
                        break
                    
                    dataTA = typeCT.label(self.get_label())
                    if dataTA._default is None:
                        dataTA = dataTA.default(self._default)
                    datasTA.append(dataTA)
            return datasTA
        self._types = []
        checker2 = checker2Action()
        if not(type(checker2) in (list, tuple)):
            return self
        self._types = checker2
        if NODEENV == 'debug':
            print(f"[jon -> JON_sup.py] ChosenType | chosenTypesChoices - self._types:: ", self._types)

        return self.chosenTypes()
    
    def types(self,):
        return self._types
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.chosenTypesValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] ChosenType | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def chosenTypesValidation(self, value):
        try:
            ruleDataF = None

            if self._CHOSEN_TYPE__RULE is not None:
                ruleData = self._CHOSEN_TYPE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CHOSEN_TYPES__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp

class Enum(JONDefaultSchema):
    _choices: any = []

    _ENUM__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def enum(self):
        def rule(valueInitial):
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Enum | enum - self._choices:: ", self._choices)
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    len([choice == value for indexChoice, choice in enumerate(self._choices) if (
                        choice == value
                    )]) > 0 or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est ne correspond à aucune de ses valeurs ({vals})".format(
                            label = labelSTR,
                            vals= " ou ".join([f"\"{choice}\"" for indexChoice, choice in enumerate(self._choices)]),
                        ),
                        'en': "{label} does not correspond to any of its values ({vals})".format(
                            label = labelSTR,
                            vals= " or ".join([f"\"{choice}\"" for indexChoice, choice in enumerate(self._choices)]),
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ENUM__RULE = rule
        return self
    def choices(self, *values: list):
        self._choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self.enum()
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.enumValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Enum | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def enumValidation(self, value):
        try:
            ruleDataF = None

            if self._ENUM__RULE is not None:
                ruleData = self._ENUM__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ENUM__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
class NotEnum(JONDefaultSchema):
    _choices: any = []

    _NOT_ENUM__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def notEnum(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    not(len([choice == value for indexChoice, choice in enumerate(self._choices) if not(
                        choice == value
                    )]) > 0) or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est ne doit pas correspondre à une de ses valeurs ({vals})".format(
                            label = labelSTR,
                            vals= " ou ".join([f"\"{choice}\"" for indexChoice, choice in enumerate(self._choices)]),
                        ),
                        'en': "{label} est must not correspond to one of its values ({vals})".format(
                            label = labelSTR,
                            vals= " or ".join([f"\"{choice}\"" for indexChoice, choice in enumerate(self._choices)]),
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NOT_ENUM__RULE = rule
        return self
    def choices(self, *values: list):
        self._choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self.notEnum()
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.notEnumValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] NotEnum | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def notEnumValidation(self, value):
        try:
            ruleDataF = None

            if self._NOT_ENUM__RULE is not None:
                ruleData = self._NOT_ENUM__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NOT_ENUM__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    
class Date(JONDefaultSchema):
    _timezone: any = pytz.UTC
    _format: str = None
    _dateFormat: str = dateFormatInitial
    _timeFormat: str = timeFormatInitial
    _maxValue: any = None
    _minValue: any = None
    _lessValue: any = None
    _greaterValue: any = None
    _equalValue: any = None
    
    _DATE__RULE = None
    _DATE__MIN__RULE = None
    _DATE__MAX__RULE = None
    _DATE__LESS__RULE = None
    _DATE__GREATER__RULE = None
    _DATE__EQUAL_TO__RULE = None
    _DATE__TO_DATE__RULE = None
    _DATE__TO_TIME__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.date()

    def date(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(value is not None):
                    if(self._format is None):
                        self.changeFormat(dateTimeFormatInitial)
                            
                    if(isDate(value, typeValue="string", dateFormat=self._format)):
                        value = datetime.datetime.strptime(value, self._format)

                    if(self._timezone is not None):
                        value = value.astimezone(self._timezone)

                    if type(value) == str:
                        value = datetime.datetime.strptime(value, self._format)

                return value
            def ruleFunct(value):
                return (
                    isDate(value, dateFormat = self._format) or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une date".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a date".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__RULE = rule
        return self
    def min(self, minValue: any):
        if(getDate(minValue, dateFormat = self._format, timezone = self._timezone) is not None):
            self._minValue = getDate(minValue, dateFormat = self._format, timezone = self._timezone)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or (
                        isDate(value) and
                        value >= minValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._maxValue is not None
                    ):
                        err = Exception({
                            'fr': "{label} doit être compris entre {min} et {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = self._maxValue,
                            ),
                            'en': "{label} must be between {min} and {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} doit être au minimum {min}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = self._maxValue,
                            ),
                            'en': "{label} must be at least {min}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__MIN__RULE = rule
        return self
    def max(self, maxValue: any):
        if(getDate(maxValue, dateFormat = self._format, timezone = self._timezone) is not None):
            self._maxValue = getDate(maxValue, dateFormat = self._format, timezone = self._timezone)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or (
                        isDate(value) and
                        value <= maxValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._minValue is not None
                    ):
                        err = Exception({
                            'fr': "{label} doit être compris entre {min} et {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = self._maxValue,
                            ),
                            'en': "{label} must be between {min} and {max}".format(
                                label = labelSTR,
                                min = self._minValue,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} doit être au maximum {max}".format(
                                label = labelSTR,
                                max = self._maxValue,
                            ),
                            'en': "{label} must be maximum {max}".format(
                                label = labelSTR,
                                max = self._maxValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__MAX__RULE = rule
        return self
    def less(self, lessValue: any):
        if(getDate(lessValue, dateFormat = self._format, timezone = self._timezone) is not None):
            self._lessValue = getDate(lessValue, dateFormat = self._format, timezone = self._timezone)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or (
                        isDate(value) and
                        value >= lessValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._greaterValue is not None
                    ):
                        err = Exception({
                            'fr': "{label} doit être inférieure à {less} et superieure à {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "{label} must be less than {less} and greater than {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} doit être inferieure à {less}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "{label} must be less than {less}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__LESS__RULE = rule
        return self
    def greater(self, greatedValue: any):
        if(getDate(greatedValue, dateFormat = self._format, timezone = self._timezone) is not None):
            self._greatedValue = getDate(greatedValue, dateFormat = self._format, timezone = self._timezone)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or (
                        isDate(value) and
                        value <= greatedValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    if(
                        self._lessValue is not None
                    ):
                        err = Exception({
                            'fr': "{label} doit être inférieure à {less} et superieure à {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = self._greaterValue,
                            ),
                            'en': "{label} must be less than {less} and greater than {greater}".format(
                                label = labelSTR,
                                less = self._lessValue,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    else:
                        err = Exception({
                            'fr': "{label} doit être supérieur à {greater}".format(
                                label = labelSTR,
                                greater = self._greaterValue,
                            ),
                            'en': "{label} must be greater than {greater}".format(
                                label = labelSTR,
                                greater = self._greaterValue,
                            ),
                        }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__GREATER__RULE = rule
        return self
    def equalTo(self, equalValue: int):
        if(getDate(equalValue, dateFormat = self._format, timezone = self._timezone) is not None):
            self._equalValue = getDate(equalValue, dateFormat = self._format, timezone = self._timezone)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or (
                        isDate(value) and
                        value == equalValue
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} doit être égale à {length}".format(
                            label = labelSTR,
                            length = self._equalValue,
                        ),
                        'en': "{label} must be equal to {length}".format(
                            label = labelSTR,
                            length = self._equalValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__EQUAL_TO__RULE = rule
        return self
    def toDate(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or 
                    isDate(value)
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est d'un type \"Date\" invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid \"Date\" type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__TO_DATE__RULE = rule
        return self
    def toTime(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    isDate(value, typeValue = 'null') or 
                    isDate(value)
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est d'un type \"Date\" invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid \"Date\" type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__TO_TIME__RULE = rule
        return self
    
    def changeFormat(self,
        newFormat: str
    ):
        if (
            type(newFormat) == str and
            len(newFormat) > 0
        ):
            self._format = newFormat

        return self
    def changeTimezone(self,
        newTimezone: any
    ):
        if (
            newTimezone is not None
        ):
            self._timezone = newTimezone

        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.dateValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    error=Exception({
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()]),
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def dateValidation(self, value):
        try:
            ruleDataF = None

            if self._DATE__RULE is not None:
                ruleData = self._DATE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__RULE"
                    return ruleDataF
            if self._DATE__MIN__RULE is not None:
                ruleData = self._DATE__MIN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__MIN__RULE"
                    return ruleDataF
            if self._DATE__MAX__RULE is not None:
                ruleData = self._DATE__MAX__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__MAX__RULE"
                    return ruleDataF
            if self._DATE__LESS__RULE is not None:
                ruleData = self._DATE__LESS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__LESS__RULE"
                    return ruleDataF
            if self._DATE__GREATER__RULE is not None:
                ruleData = self._DATE__GREATER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__GREATER__RULE"
                    return ruleDataF
            if self._DATE__EQUAL_TO__RULE is not None:
                ruleData = self._DATE__EQUAL_TO__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__EQUAL_TO__RULE"
                    return ruleDataF
            if self._DATE__TO_DATE__RULE is not None:
                ruleData = self._DATE__TO_DATE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__TO_DATE__RULE"
                    return ruleDataF
            if self._DATE__TO_TIME__RULE is not None:
                ruleData = self._DATE__TO_TIME__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "DATE__TO_TIME__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Date | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    
class Boolean(JONDefaultSchema):
    _trueValues: list = ['true', 't', '1', 1, True]
    _falseValues: list = ['false', 'f', '0', 0, False]

    _BOOLEAN__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.boolean()

    def boolean(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value) == True):
                    return convertToBoolean(value)
            def ruleFunct(value):
                return isBoolean(value, (self._trueValues + self._falseValues), False)
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas un booléen".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a Boolean".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._BOOLEAN__RULE = rule
        return self
    def required(self, isRequired: bool = True):
        isRequired = isRequired if type(isRequired) == bool else True
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    value is not None or
                    type(value) == bool
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est requis".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is required".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        if isRequired:
            self._PRIMARY__REQUIRED__RULE = rule
        else:
            self._PRIMARY__REQUIRED__RULE = None
        return self
    
    def trueValues(self, valueInitial: list):
        values = valueInitial if type(valueInitial) in (list, tuple) else []
        if(len(values) > 0):
            self._trueValues = values
        return self
    def falseValues(self, valueInitial: list):
        values = valueInitial if type(valueInitial) in (list, tuple) else []
        if(len(values) > 0):
            self._falseValues = values
        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.booleanValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def booleanValidation(self, value):
        try:
            ruleDataF = None

            if self._BOOLEAN__RULE is not None:
                ruleData = self._BOOLEAN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "BOOLEAN__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Boolean | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp


class Number(JONDefaultSchema):
    _NUMBER__RULE = None
    _NUMBER__MIN__RULE = None
    _NUMBER__MAX__RULE = None
    _NUMBER__LESS__RULE = None
    _NUMBER__GREATER__RULE = None
    _NUMBER__NEGATIVE__RULE = None
    _NUMBER__POSITIVE__RULE = None
    _NUMBER__SIGNED__RULE = None
    _NUMBER__INTEGER__RULE = None
    _NUMBER__DECIMAL__RULE = None
    _NUMBER__MULTIPLE__RULE = None
    _NUMBER__TCP_PORT__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.number()

    def number(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    if (
                        value is not None and
                        isNumber(value) == True and
                        not(float(value).is_integer())
                    ):
                        return float(value)
                    elif (
                        value is not None and
                        isNumber(value) == True and
                        float(value).is_integer()
                    ):
                        return int(value)
            def ruleFunct(value):
                return (
                    isNumber(value) or
                    value is None 
                )
            def errorFunct(value):
                
                if NODEENV == 'debug':
                    print(f"[jon -> JON_sup.py] Number | number - errorFunct - value:: '{value}'")
                    print("""[jon -> JON_sup.py] Number | number - errorFunct - type(value):: """, type(value))
                    print("""[jon -> JON_sup.py] Number | number - errorFunct - ruleFunct(value):: """, ruleFunct(value))
                    print("""[jon -> JON_sup.py] Number | number - errorFunct - isNumber(value):: """, isNumber(value))
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas un nombre".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__RULE = rule
        return self
    def min(self, minValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        type(minValue) in (int, float) and
                        value >= minValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} doit être au minimum {min}".format(
                            label = labelSTR,
                            min = minValue,
                        ),
                        'en': "{label} must be at least {min}".format(
                            label = labelSTR,
                            min = minValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__MIN__RULE = rule
        return self
    def max(self, maxValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        type(maxValue) in (int, float) and
                        value <= maxValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} doit être au maximum {max}".format(
                            label = labelSTR,
                            max = maxValue,
                        ),
                        'en': "{label} must be maximum {max}".format(
                            label = labelSTR,
                            max = maxValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__MAX__RULE = rule
        return self
    def less(self, lessValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        type(lessValue) in (int, float) and
                        value > lessValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} doit être inferieure à {less}".format(
                            label = labelSTR,
                            less = lessValue,
                        ),
                        'en': "{label} must be less than {less}".format(
                            label = labelSTR,
                            less = lessValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__LESS__RULE = rule
        return self
    def greater(self, greaterValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        type(greaterValue) in (int, float) and
                        value < greaterValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} doit être supérieur à {greater}".format(
                            label = labelSTR,
                            greater = greaterValue,
                        ),
                        'en': "{label} must be greater than {greater}".format(
                            label = labelSTR,
                            greater = self._greaterValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__GREATER__RULE = rule
        return self
    def negative(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        value <= 0
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être un nombre negatif".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a negative number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__NEGATIVE__RULE = rule
        return self
    def positive(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        value >= 0
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être un nombre positif".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a positive number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__POSITIVE__RULE = rule
        return self
    def signed(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and (
                            value > 0 or
                            value < 0
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être soit un nombre négatif soit un nombre positif".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be either a negative number or a positive number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__SIGNED__RULE = rule
        return self
    def integer(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in (int, float)
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être un nombre entier valide".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a valid integer number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__INTEGER__RULE = rule
        return self
    def decimal(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in (float, int)
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être un nombre décimal valide".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a valid decimal number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__DECIMAL__RULE = rule
        return self
    def multiple(self, nber: float):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in (int, float) and
                        type(nber) in [int, float] and
                        value % nber == 0
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être un multiple de {nber}".format(
                            label = labelSTR,
                            nber = nber,
                        ),
                        "en": "{label} must be a multiple of {nber}".format(
                            label = labelSTR,
                            nber = nber,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__MULTIPLE__RULE = rule
        return self
    def TCPPort(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        isNumber(value) and
                        type(value) in [int, float] and
                        (
                            value > 9 and
                            value <= 99999
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        "fr": "{label} doit être au format d'un port TCP".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be in the format of a TCP port".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__TCP_PORT__RULE = rule
        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.numberValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] Number | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def numberValidation(self, value):
        try:
            ruleDataF = None

            if self._NUMBER__RULE is not None:
                ruleData = self._NUMBER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__RULE"
                    return ruleDataF
            if self._NUMBER__MIN__RULE is not None:
                ruleData = self._NUMBER__MIN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__MIN__RULE"
                    return ruleDataF
            if self._NUMBER__MAX__RULE is not None:
                ruleData = self._NUMBER__MAX__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__MAX__RULE"
                    return ruleDataF
            if self._NUMBER__LESS__RULE is not None:
                ruleData = self._NUMBER__LESS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__LESS__RULE"
                    return ruleDataF
            if self._NUMBER__GREATER__RULE is not None:
                ruleData = self._NUMBER__GREATER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__GREATER__RULE"
                    return ruleDataF
            if self._NUMBER__NEGATIVE__RULE is not None:
                ruleData = self._NUMBER__NEGATIVE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__NEGATIVE__RULE"
                    return ruleDataF
            if self._NUMBER__POSITIVE__RULE is not None:
                ruleData = self._NUMBER__POSITIVE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__POSITIVE__RULE"
                    return ruleDataF
            if self._NUMBER__SIGNED__RULE is not None:
                ruleData = self._NUMBER__SIGNED__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__SIGNED__RULE"
                    return ruleDataF
            if self._NUMBER__INTEGER__RULE is not None:
                ruleData = self._NUMBER__INTEGER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__INTEGER__RULE"
                    return ruleDataF
            if self._NUMBER__DECIMAL__RULE is not None:
                ruleData = self._NUMBER__DECIMAL__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__DECIMAL__RULE"
                    return ruleDataF
            if self._NUMBER__MULTIPLE__RULE is not None:
                ruleData = self._NUMBER__MULTIPLE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__MULTIPLE__RULE"
                    return ruleDataF
            if self._NUMBER__TCP_PORT__RULE is not None:
                ruleData = self._NUMBER__TCP_PORT__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "NUMBER__TCP_PORT__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp

class String(JONDefaultSchema):
    _maxValue: str = None
    _minValue: str = None
    _lessValue: str = None
    _greaterValue: str = None
    _lengthValue: str = None
    _format: str = None
    _dateFormat: str = '%Y/%m/%d'
    _timeFormat: str = '%H:%M:%S:%f'
    _enum_choices: any = []
    _not_enum_choices: any = []

    _STRING__RULE = None
    _STRING__MIN__RULE = None
    _STRING__MAX__RULE = None
    _STRING__LESS__RULE = None
    _STRING__GREATER__RULE = None
    _STRING__LENGTH__RULE = None
    _STRING__REGEXP__RULE = None
    _STRING__ALPHANUM__RULE = None
    _STRING__BASE64__RULE = None
    _STRING__LOWERCASE__RULE = None
    _STRING__UPPERCASE__RULE = None
    _STRING__CAPITALIZE__RULE = None
    _STRING__UC_FIRST__RULE = None
    _STRING__CREDIT_CARD__RULE = None
    _STRING__DATAURI__RULE = None
    _STRING__DOMAIN__RULE = None
    _STRING__URL__RULE = None
    _STRING__HOSTNAME__RULE = None
    _STRING__IP_ADDRESS__RULE = None
    _STRING__EMAIL__RULE = None
    _STRING__GUID__RULE = None
    _STRING__HEXA__RULE = None
    _STRING__BINARY__RULE = None
    _STRING__DATE__RULE = None
    _STRING__IDENTIFIER__RULE = None
    
    _STRING__ENUM__RULE = None
    _STRING__NOT_ENUM__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.string()

    def string(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value) == True):
                    if(value is not None):
                        if(self._format is None):
                            if (
                                isString(value, typeValue = "datetime")
                            ):
                                self.changeFormat(dateTimeFormatInitial)
                            elif (
                                isString(value, typeValue = "date")
                            ):
                                self.changeFormat(self._dateFormat)
                            elif (
                                isString(value, typeValue = "time")
                            ):
                                self.changeFormat(self._timeFormat)

                        if (
                            isString(value, typeValue = "other")
                        ):
                            return str(value)
                        elif (
                            isString(value, typeValue = "datetime") or
                            isString(value, typeValue = "date") or
                            isString(value, typeValue = "time")
                        ):
                            return value.strftime(self._format)
                    else:
                        return None
            def ruleFunct(value):
                return (
                    type(value) in [str, int, float, bool] or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
                return None
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__RULE = rule
        return self
    def min(self, minValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        len(value) >= minValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être au minimum {min}".format(
                            label = labelSTR,
                            min = minValue,
                        ),
                        'en': "the size of {label} must be at least {min}".format(
                            label = labelSTR,
                            min = minValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__MIN__RULE = rule
        return self
    def max(self, maxValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        len(value) <= maxValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être au maximum {max}".format(
                            label = labelSTR,
                            max = maxValue,
                        ),
                        'en': "the size of {label} must be maximum {max}".format(
                            label = labelSTR,
                            max = maxValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__MAX__RULE = rule
        return self
    def less(self, lessValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        len(value) > lessValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être inferieure à {less}".format(
                            label = labelSTR,
                            less = lessValue,
                            greater = self._greaterValue,
                        ),
                        'en': "the size of {label} must be less than {less}".format(
                            label = labelSTR,
                            less = lessValue,
                            greater = self._greaterValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__LESS__RULE = rule
        return self
    def greater(self, greaterValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        len(value) < greaterValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être supérieur à {greater}".format(
                            label = labelSTR,
                            greater = greaterValue,
                        ),
                        'en': "the size of {label} must be greater than {greater}".format(
                            label = labelSTR,
                            greater = self._greaterValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__GREATER__RULE = rule
        return self
    def length(self, lengthValue: int):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        len(value) == lengthValue
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "la taille de {label} doit être égale à {length}".format(
                            label = labelSTR,
                            length = lengthValue,
                        ),
                        'en': "the size of {label} must be equal to {length}".format(
                            label = labelSTR,
                            length = self._lengthValue,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__LENGTH__RULE = rule
        return self
    def regexp(self, ruleValue: str, flag: re.RegexFlag = None):
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} ne respecte pas la rêgle appliquée".format(
                            label = labelSTR,
                        ),
                        'en': "{label} does not respect the ruleFunct applied".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__REGEXP__RULE = rule
        return self
    def alphanum(self):
        ruleValue: str = r"^([\w\s])+$"
        flag: re.RegexFlag = re.MULTILINE
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères alphanumeriques".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string of alphanumeric characters".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__ALPHANUM__RULE = rule
        return self
    def base64(self, paddingRequired: bool = True, urlSafe: bool = True):
        paddingRequired = paddingRequired if type(paddingRequired) == bool else True
        urlSafe = urlSafe if type(urlSafe) == bool else True
        
        nbr1 = '=' if paddingRequired else '(={0,1})'
        nbr2 = '(\-{1})' if urlSafe else '(+{1})'
        nbr3 = '(_{1})' if urlSafe else '(\\{1})'

        ruleValue: str = r"^(?:[A-Za-z0-9" + nbr2 + "/]{4})*(?:[A-Za-z0-9" + nbr2 + "/]{2}==|[A-Za-z0-9" + nbr2 + "/]{3}" + nbr1 + "|[A-Za-z0-9" + nbr2 + "/]{4})$"
        flag: re.RegexFlag = (re.MULTILINE)

        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères de type base64".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a base64 string".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__BASE64__RULE = rule
        return self
    def lowercase(self, strictMode: bool = False):
        strictMode = strictMode if type(strictMode) == bool else False

        ruleValue: str = r"[A-Z]{1,}"

        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return str(value).lower() if value is not None else None
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value))) == False
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas en minuscule".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not lowercase".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__LOWERCASE__RULE = rule
        return self
    def uppercase(self, strictMode: bool = False):
        strictMode = strictMode if type(strictMode) == bool else False

        ruleValue: str = r"[A-Z]{1,}"

        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return str(value).upper() if value is not None else None
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas en majuscule".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not uppercase".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__UPPERCASE__RULE = rule
        return self
    def capitalize(self, strictMode: bool = False):
        strictMode = strictMode if type(strictMode) == bool else False

        ruleValue: str = r".{1,}"

        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return str(value).title() if value is not None else None
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas en lettre capitale".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not capitalized".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__CAPITALIZE__RULE = rule
        return self
    def ucFirst(self, strictMode: bool = False):
        strictMode = strictMode if type(strictMode) == bool else False

        ruleValue: str = r".{1,}"

        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return str(value).capitalize() if value is not None else None
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'a pas de première lettre en majuscule".format(
                            label = labelSTR,
                        ),
                        'en': "{label} does not have a capitalized first letter".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__UC_FIRST__RULE = rule
        return self
    def creditCard(self, types: list = []):
        typesPossibles = ('mastercard', 'visa', 'american-express', 'discover', 'diners-club', 'jcb')
        types = types if type(types) in (tuple, list) else []
        types = tuple(
            filter(
                lambda x: x in typesPossibles,
                types,
            )
        )
        versionRegEx = {
            'visa': re.compile(r"^(4[0-9]{12}(?:[0-9]{3}))$", re.MULTILINE),
            'mastercard': re.compile(r"^((?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12})$", re.MULTILINE),
            'american-express': re.compile(r"^(3[47][0-9]{13})$", re.MULTILINE),
            'discover': re.compile(r"^(6(?:011|5[0-9]{2})[0-9]{12})$", re.MULTILINE),
            'diners-club': re.compile(r"^(3(?:0[0-5]|[68][0-9])[0-9]{11})$", re.MULTILINE),
            'jcb': re.compile(r"^((?:2131|1800|35\d{3})\d{11})$", re.MULTILINE),
        }
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            (
                                len(types) <= 0 and (
                                    bool(re.match(versionRegEx['visa'], str(value))) or
                                    bool(re.match(versionRegEx['mastercard'], str(value))) or
                                    bool(re.match(versionRegEx['american-express'], str(value))) or
                                    bool(re.match(versionRegEx['discover'], str(value))) or
                                    bool(re.match(versionRegEx['diners-club'], str(value))) or
                                    bool(re.match(versionRegEx['jcb'], str(value)))
                                )
                            ) or (
                                len(types) > 0 and (
                                    (
                                        'visa' in types and
                                        bool(re.match(versionRegEx['visa'], str(value)))
                                    ) or (
                                        'mastercard' in types and
                                        bool(re.match(versionRegEx['mastercard'], str(value)))
                                    ) or (
                                        'american-express' in types and
                                        bool(re.match(versionRegEx['american-express'], str(value)))
                                    ) or (
                                        'discover' in types and
                                        bool(re.match(versionRegEx['discover'], str(value)))
                                    ) or (
                                        'diners-club' in types and
                                        bool(re.match(versionRegEx['diners-club'], str(value)))
                                    ) or (
                                        'jcb' in types and
                                        bool(re.match(versionRegEx['jcb'], str(value)))
                                    )
                                )
                            )
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères au format d'une carte de crédit".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is a string in the format of a credit card".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__CREDIT_CARD__RULE = rule
        return self
    def dataUri(self):
        ruleValue: str = r"^data:([\w\/\+]+);(charset=[\w-]+|base64).*,([a-zA-Z0-9+/]+={0,2})$"
        flag: re.RegexFlag = re.MULTILINE
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and 
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne d'URI de données valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a valid data URI string".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__DATAURI__RULE = rule
        return self
    def domain(self):
        ruleValue: str = "^(?!-)[A-Za-z0-9-]+([\\-\\.]{1}[a-z0-9]+)*\\.[A-Za-z]{2,6}$"
        flag: re.RegexFlag = re.MULTILINE
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and 
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un domaine valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid domain".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__DOMAIN__RULE = rule
        return self
    def url(self):
        ruleValue: str = ''.join([
            '^(https?:\\/\\/)?',
            '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|',
            '((\\d{1,3}\\.){3}\\d{1,3}))',
            '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*',
            '(\\?[;&a-z\\d%_.~+=-]*)?',
            '(\\#[-a-z\\d_]*)?$',
        ])
        flag: re.RegexFlag = re.MULTILINE
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and 
                        bool(re.match(ruleValue, str(value)))
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'une url valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid url".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__URL__RULE = rule
        return self
    def hostname(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            bool(re.match(re.compile(r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$", re.MULTILINE), str(value))) or
                            bool(re.match(re.compile(r"^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$", re.MULTILINE), str(value)))
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un nom d'hôte valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid hostname".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__HOSTNAME__RULE = rule
        return self
    def IPAddress(self, types: list = []):
        typesPossibles = ('ipv4', 'ipv6')
        types = types if type(types) in (tuple, list) else []
        types = tuple(
            filter(
                lambda x: x in typesPossibles,
                types,
            )
        )
        versionRegEx = {
            'ipv4': re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", re.MULTILINE),
            'ipv6': re.compile('|'.join([
                "(^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$)",
                "(^::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$)",
                "(^[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}$)",
                "(^[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}$)",
                "(^(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}$)",
                "(^(?:[0-9a-fA-F]{1,4}:){0,3}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:){0,2}[0-9a-fA-F]{1,4}$)",
                "(^(?:[0-9a-fA-F]{1,4}:){0,4}[0-9a-fA-F]{1,4}::(?:[0-9a-fA-F]{1,4}:)?[0-9a-fA-F]{1,4}$)",
                "(^(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}::[0-9a-fA-F]{1,4}$)",
                "(^(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}::$)",
            ]), re.MULTILINE),
        }
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            (
                                len(types) <= 0 and (
                                    bool(re.match(versionRegEx['ipv4'], str(value))) or
                                    bool(re.match(versionRegEx['ipv6'], str(value)))
                                )
                            ) or (
                                len(types) > 0 and (
                                    (
                                        'ipv4' in versionRegEx.keys() and
                                        bool(re.match(versionRegEx['ipv4'], str(value)))
                                    ) or (
                                        'ipv6' in versionRegEx.keys() and
                                        bool(re.match(versionRegEx['ipv6'], str(value)))
                                    )
                                )
                            )
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'une addresse IP valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid IP address".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__IP_ADDRESS__RULE = rule
        return self
    def email(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            bool(
                                re.match(
                                    re.compile(r"^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$", re.MULTILINE),
                                    str(value)
                                )
                            ) or
                            bool(
                                re.match(
                                    re.compile(r"""^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$""", re.MULTILINE),
                                    str(value)
                                )
                            )
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un email valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid email".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__EMAIL__RULE = rule
        return self
    def guid(self, types: list = []):
        typesPossibles = ('v1', 'v2', 'v3', 'v4', 'v5')
        types = types if type(types) in (tuple, list) else []
        types = tuple(
            filter(
                lambda x: x in typesPossibles,
                types,
            )
        )
        versionRegEx = {
            'v1': re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1][0-9a-fA-F]{3}-[89AB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$", re.MULTILINE),
            'v2': re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[2][0-9a-fA-F]{3}-[89AB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$", re.MULTILINE),
            'v3': re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[3][0-9a-fA-F]{3}-[89AB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$", re.MULTILINE),
            'v4': re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[4][0-9a-fA-F]{3}-[89AB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$", re.MULTILINE),
            'v5': re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[5][0-9a-fA-F]{3}-[89AB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$", re.MULTILINE),
        }
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                        (
                            len(types) <= 0 and (
                                bool(re.match(versionRegEx['v1'], str(value))) or
                                bool(re.match(versionRegEx['v2'], str(value))) or
                                bool(re.match(versionRegEx['v3'], str(value))) or
                                bool(re.match(versionRegEx['v4'], str(value))) or
                                bool(re.match(versionRegEx['v5'], str(value)))
                            )
                        ) or (
                            len(types) > 0 and (
                                (
                                    'v1' in types and
                                    bool(re.match(versionRegEx['v1'], str(value)))
                                ) or (
                                    'v2' in types and
                                    bool(re.match(versionRegEx['v2'], str(value)))
                                ) or (
                                    'v3' in types and
                                    bool(re.match(versionRegEx['v3'], str(value)))
                                ) or (
                                    'v4' in types and
                                    bool(re.match(versionRegEx['v4'], str(value)))
                                ) or (
                                    'v5' in types and
                                    bool(re.match(versionRegEx['v5'], str(value)))
                                )
                            )
                        )
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format GUID valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in valid GUID format".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__GUID__RULE = rule
        return self
    def hexa(self, insensitive: bool = False):
        insensitive = insensitive if type(insensitive) == bool else False
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            (
                                insensitive and
                                bool(re.match(re.compile(r"^[0-9a-fA-F]+$", re.MULTILINE), str(value)))
                            ) or 
                            (
                                not(insensitive) and
                                bool(re.match(re.compile(r"^[0-9A-F]+$", re.MULTILINE), str(value)))
                            )
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un hexa valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid hexa".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__HEXA__RULE = rule
        return self
    def binary(self):
        ruleValue: str = r"^[0-1]{1,}$"
        flag: re.RegexFlag = None
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            len(str(value)) > 0 and
                            bool(re.match(ruleValue, str(value)))
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format binaire valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in valid binary format".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__BINARY__RULE = rule
        return self
    def date(self, format = None):
        format = format if (
            type(format) == str and
            len(format) > 0
        ) else (
            dateTimeFormatInitial
        )
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and 
                        isDatetimeFormat(str(value), format = format)
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'une date valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid date".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__DATE__RULE = rule
        return self
    def identifier(self):
        ruleValue: str = r"^[a-zA-Z]{1,}\w{0,}$"
        flag: re.RegexFlag = None
        flag = flag if (
            type(flag) is re.RegexFlag and
            flag is not None
        ) else None
        ruleValue = ruleValue if (
            type(ruleValue) == str and
            len(ruleValue) > 0
        ) else ''
        if flag is not None:
            ruleValue = re.compile(ruleValue, flag)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == str and (
                            len(str(value)) > 0 and
                            bool(re.match(ruleValue, str(value)))
                        )
                    ) or
                    value is None 
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères sous le format d'un identifiant".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string in the format of an identifier".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__IDENTIFIER__RULE = rule
        return self

    def enum(self, *values: list):
        self.enumChoices(*values)
        def rule(valueInitial):
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | stringEnum - valueInitial:: ", valueInitial)
                print("[jon -> JON_sup.py] String | stringEnum - values:: ", values)
                print("[jon -> JON_sup.py] String | stringEnum - self._enum_choices:: ", self._enum_choices)
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    len([choice == value for indexChoice, choice in enumerate(self._enum_choices) if (
                        choice == value
                    )]) > 0 or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est d'un type invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | stringEnum - validation:: ", {
                    'valid': checkerValidation,
                    'data': valueValidation,
                    'error': errorValidation,
                })
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__ENUM__RULE = rule
        return self
    def enumChoices(self, *values: list):
        self._enum_choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self
    def notEnum(self, *values: list):
        self.notEnumchoices(*values)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return value
            def ruleFunct(value):
                return (
                    not(len([choice == value for indexChoice, choice in enumerate(self._not_enum_choices) if not(
                        choice == value
                    )]) > 0) or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est d'un type invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__NOT_ENUM__RULE = rule
        return self
    def notEnumchoices(self, *values: list):
        self._not_enum_choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self
    
        
    def changeFormat(self,
        newFormat: str
    ):
        if (
            type(newFormat) == str and
            len(newFormat) > 0
        ):
            self._format = newFormat

        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.stringValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | stringValidation - ruleData (For String):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | stringValidation - ruleData (For Primary):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | stringValidation - ruleDataF:: ", ruleDataF)
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def stringValidation(self, value):
        try:
            ruleDataF = None

            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] String | stringValidation - self._STRING__RULE:: ", self._STRING__RULE)
            if self._STRING__RULE is not None:
                ruleData = self._STRING__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if NODEENV == 'debug':
                    print("[jon -> JON_sup.py] String | stringValidation - ruleData:: ", ruleData)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__RULE"
                    return ruleDataF
            if self._STRING__MIN__RULE is not None:
                ruleData = self._STRING__MIN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__MIN__RULE"
                    return ruleDataF
            if self._STRING__MAX__RULE is not None:
                ruleData = self._STRING__MAX__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__MAX__RULE"
                    return ruleDataF
            if self._STRING__LESS__RULE is not None:
                ruleData = self._STRING__LESS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__LESS__RULE"
                    return ruleDataF
            if self._STRING__GREATER__RULE is not None:
                ruleData = self._STRING__GREATER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__GREATER__RULE"
                    return ruleDataF
            if self._STRING__LENGTH__RULE is not None:
                ruleData = self._STRING__LENGTH__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__LENGTH__RULE"
                    return ruleDataF
            if self._STRING__REGEXP__RULE is not None:
                ruleData = self._STRING__REGEXP__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__REGEXP__RULE"
                    return ruleDataF
            if self._STRING__ALPHANUM__RULE is not None:
                ruleData = self._STRING__ALPHANUM__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__ALPHANUM__RULE"
                    return ruleDataF
            if self._STRING__BASE64__RULE is not None:
                ruleData = self._STRING__BASE64__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__BASE64__RULE"
                    return ruleDataF
            if self._STRING__LOWERCASE__RULE is not None:
                ruleData = self._STRING__LOWERCASE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__LOWERCASE__RULE"
                    return ruleDataF
            if self._STRING__UPPERCASE__RULE is not None:
                ruleData = self._STRING__UPPERCASE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__UPPERCASE__RULE"
                    return ruleDataF
            if self._STRING__CAPITALIZE__RULE is not None:
                ruleData = self._STRING__CAPITALIZE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__CAPITALIZE__RULE"
                    return ruleDataF
            if self._STRING__UC_FIRST__RULE is not None:
                ruleData = self._STRING__UC_FIRST__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__UC_FIRST__RULE"
                    return ruleDataF
            if self._STRING__CREDIT_CARD__RULE is not None:
                ruleData = self._STRING__CREDIT_CARD__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__CREDIT_CARD__RULE"
                    return ruleDataF
            if self._STRING__DATAURI__RULE is not None:
                ruleData = self._STRING__DATAURI__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__DATAURI__RULE"
                    return ruleDataF
            if self._STRING__DOMAIN__RULE is not None:
                ruleData = self._STRING__DOMAIN__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__DOMAIN__RULE"
                    return ruleDataF
            if self._STRING__URL__RULE is not None:
                ruleData = self._STRING__URL__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__URL__RULE"
                    return ruleDataF
            if self._STRING__HOSTNAME__RULE is not None:
                ruleData = self._STRING__HOSTNAME__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__HOSTNAME__RULE"
                    return ruleDataF
            if self._STRING__IP_ADDRESS__RULE is not None:
                ruleData = self._STRING__IP_ADDRESS__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__IP_ADDRESS__RULE"
                    return ruleDataF
            if self._STRING__EMAIL__RULE is not None:
                ruleData = self._STRING__EMAIL__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__EMAIL__RULE"
                    return ruleDataF
            if self._STRING__GUID__RULE is not None:
                ruleData = self._STRING__GUID__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__GUID__RULE"
                    return ruleDataF
            if self._STRING__HEXA__RULE is not None:
                ruleData = self._STRING__HEXA__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__HEXA__RULE"
                    return ruleDataF
            if self._STRING__BINARY__RULE is not None:
                ruleData = self._STRING__BINARY__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__BINARY__RULE"
                    return ruleDataF
            if self._STRING__DATE__RULE is not None:
                ruleData = self._STRING__DATE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__DATE__RULE"
                    return ruleDataF
            if self._STRING__IDENTIFIER__RULE is not None:
                ruleData = self._STRING__IDENTIFIER__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__IDENTIFIER__RULE"
                    return ruleDataF
                
            if self._STRING__ENUM__RULE is not None:
                ruleData = self._STRING__ENUM__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__ENUM__RULE"
                    return ruleDataF
            if self._STRING__NOT_ENUM__RULE is not None:
                ruleData = self._STRING__NOT_ENUM__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__NOT_ENUM__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
        
        
class AnyType(JONDefaultSchema):
    _ANY_TYPE__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
        self.anyType()

    def anyType(self):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                valid = True
                return valid == True
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} est d'un type invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueFinal = valueInitial if valueInitial is not None else self._default
            checkerValidation = ruleFunct(valueFinal)
            valueValidation = sanitizeFunct(valueFinal) if checkerValidation else None
            self._value = valueValidation
            errorValidation = None if checkerValidation else  errorFunct(valueFinal)
            return {
                'valid': checkerValidation,
                'data': valueValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ANY_TYPE__RULE = rule
        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.anyTypeValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                initialError = ruleDataF['error']
                ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                return self._mapError['map'](
                    res=ruleDataF,
                    error=initialError,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if ruleDataF is None:
                resp = {
                    'data': None,
                    'valid': False,
                    'error': {
                        'fr': 'Aucune règle defini',
                        'en': 'No rule define',
                    }[self.getLang()],
                }
                resp = self._mapError['map'](
                    res=ruleDataF,
                    ruleName='NO_RULE__RULE',
                    label = self.get_label(),
                    lang = self.getLang(),
                )
                return resp
            if(
                ruleDataF['valid'] == True and
                self.map is not None and
                callable(self.map)
            ):
                ruleDataF['data'] = self.map(ruleDataF['data'])
            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            if NODEENV == 'debug':
                print("[jon -> JON_sup.py] AnyType | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def anyTypeValidation(self, value):
        try:
            ruleDataF = None

            if self._ANY_TYPE__RULE is not None:
                ruleData = self._ANY_TYPE__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ANY_TYPE__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                error=stack,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp