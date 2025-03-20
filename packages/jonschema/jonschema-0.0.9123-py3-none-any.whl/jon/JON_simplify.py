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
from .JON_default import cleanField
from .utils import getLang


log = logging.getLogger(__name__)

def InitialMapFunct(value: any):
    return value

def ConvertStringToInitialType(self, strValue: str):
    if isObject(strValue) == True :
        return json.load(strValue)
    elif isDate(value = strValue, dateFormat = dateTimeFormatInitial) == True:
        return getDate(value = strValue, dateFormat = dateTimeFormatInitial)
    elif isNumber(value = strValue) :
        if strValue.isdigit():
            return int(strValue)
        else:
            return float(strValue)
    elif isBoolean(value = strValue) :
        return float(strValue)
    return strValue
def isObject(
    value: str,
):
    res = False
    try:
        if type(value) == dict :
            res = True
        else:
            json.load(value)
            res = True
    except Exception as err:
        res = False
    return res
def isDatetimeFormat(
    value: str,
    format: str,
):
    res = False
    try:
        datetime.datetime.strptime(value, format)
        res = True
    except Exception as err:
        res = False
    return res
def getDate(
    value: any,
    dateFormat: str = dateTimeFormatInitial,
    timezone = None,
    typeValue = None,
):
    res = None
    typesPossible = ('datetime', 'date', 'time')
    typeValue = typeValue if typeValue in typesPossible else None
    timezone = timezone if timezone is not None else None
    dateFormat = dateFormat if (
        type(dateFormat) == str and
        len(dateFormat) > 0
    ) else None

    if(
        type(value) == str and
        len(value) > 0 and
        dateFormat is not None and
        isDatetimeFormat(value, format = dateFormat)
    ):
        res = datetime.datetime.strptime(value, dateFormat)
        if(timezone is not None):
            res = res.astimezone(timezone)
        if(typeValue == 'date'):
            res = res.date()
        if(typeValue == 'time'):
            res = res.time()
    if(
        type(value) is datetime.datetime or
        type(value) is datetime.date or
        type(value) is datetime.time
    ):
        res = value
        if(
            type(value) is datetime.datetime and
            timezone is not None
        ):
            res = res.astimezone(timezone)

    return res
def isDate(
    value: any,
    typeValue: str = None,
    dateFormat: str = dateTimeFormatInitial,
) -> bool:
    dateFormat = dateFormat if (
        type(dateFormat) == str and
        len(dateFormat) > 0
    ) else None
    types: tuple = ('datetime', 'date', 'time', 'null', 'string')
    typeValue = typeValue if typeValue in types else None
    
    res = (
        (
            isDatetimeFormat(value, format = dateFormat) or
            value is None
        ) if (
            typeValue == "string" and
            type(value) == str and
            len(value) > 0 and
            dateFormat is not None
        ) else (
            (
                type(value) is datetime.datetime and (
                    typeValue in (None, 'datetime')
                )
            ) or
            (
                type(value) is datetime.time and (
                    typeValue in (None, 'time')
                )
            ) or
            (
                type(value) is datetime.date and (
                    typeValue in (None, 'date')
                )
            ) or (
                type(value) == str and
                len(value) > 0 and
                isDatetimeFormat(value, format = dateFormat) and (
                    typeValue in (None, 'string')
                )
            ) or
            (
                type(value) is None and (
                    typeValue in (None, 'null')
                )
            )
        )
    )
    return res
def isString(
    value: any,
    typeValue: str = None,
) -> bool:
    types: tuple = ('datetime', 'date', 'time', 'null', 'other')
    typeValue = typeValue if typeValue in types else None
    res = (
        (
            value is None or (
                type(value) in (str, int, float, bool, list, tuple, dict) and (
                    typeValue is None or
                    typeValue == 'other'
                )
            )
        ) or 
        (
            value is None or (
                type(value) is datetime.datetime and (
                    typeValue is None or
                    typeValue == 'datetime'
                )
            )
        ) or
        (
            value is None or (
                type(value) is datetime.time and (
                    typeValue is None or
                    typeValue == 'time'
                )
            )
        ) or
        (
            value is None or (
                type(value) is datetime.date and (
                    typeValue is None or
                    typeValue == 'date'
                )
            )
        ) or
        (
            value is None or (
                type(value) is None and (
                    typeValue is None or
                    typeValue == 'null'
                )
            )
        )
    )
    return res
def isNumber(value: any) -> bool:
    res = True
    try:
        if(value is not None):
            float(value)
    except:
        res = False
    return res
def isBoolean(
    value: any,
    valuesPossibles: list,
    strict: bool = False
) -> bool:
    res = (
        type(value) == bool or
        (
            (
                value in valuesPossibles or
                (
                    type(value) == str and
                    value.lower() in valuesPossibles
                )
            )
        ) or
        (value is None and strict == False)
    )
    return res
def convertToBoolean(
    value: any,
) -> bool:
    # value = deepcopy(value)
    defaultVal = deepcopy(value)
    valuesPossibles: list = ('true', 't', '1', 'false', 'f', '0')
    res = defaultVal
    if type(value) == bool :
        res = value
    elif value is not None and str(value).lower() in valuesPossibles:
        res = True if str(value).lower() in ('true', 't', '1') else False
    return res

def simplifiedDefaultMapError( res, ruleName: str = None, label = None, lang = 'fr' ):
    if NODEENV == 'debug':
        print("\n>----------------------")
        print("[jon -> JON_simplify.py] defaultMapError | label:: ", label)
        print("[jon -> JON_simplify.py] defaultMapError | lang:: ", lang)
        print("[jon -> JON_simplify.py] defaultMapError | ruleName:: ", ruleName)
        print("\n")
        print("[jon -> JON_simplify.py] defaultMapError | res:: ", res)
        print("-------------------------<")
    return res




def defaultAllocationMap(initialData, data):
    initialData = data
class SimplifiedJON:
    _label: str = None
    _lang: str = 'fr'
    _default = None
    _rules: list = []
    _value = None
    _default_error = None
    
    map = None
    preMap = None
    
    _mapError = {
        'map': simplifiedDefaultMapError,
    }
    _errMsgs = None
    
    _PRIMARY__REQUIRED__RULE = None
    _PRIMARY__ENUM__RULE = None
    _PRIMARY__ENUM_NOT__RULE = None
    _PRIMARY__CUSTOM01__RULE = None
    _PRIMARY__CUSTOM02__RULE = None
    _PRIMARY__CUSTOM03__RULE = None
    _PRIMARY__CUSTOM04__RULE = None
    _PRIMARY__CUSTOM05__RULE = None
    _PRIMARY__CUSTOM06__RULE = None
    _PRIMARY__CUSTOM07__RULE = None
    _PRIMARY__CUSTOM08__RULE = None
    _PRIMARY__CUSTOM09__RULE = None
    _PRIMARY__CUSTOM10__RULE = None

    _SEQUENCE01__RULE = None
    _SEQUENCE02__RULE = None
    _SEQUENCE03__RULE = None
    _SEQUENCE04__RULE = None
    _SEQUENCE05__RULE = None
    _SEQUENCE06__RULE = None
    _SEQUENCE07__RULE = None
    _SEQUENCE08__RULE = None
    _SEQUENCE09__RULE = None
    _SEQUENCE10__RULE = None
    _SEQUENCE11__RULE = None
    _SEQUENCE12__RULE = None
    _SEQUENCE13__RULE = None
    _SEQUENCE14__RULE = None
    _SEQUENCE15__RULE = None
    _SEQUENCE16__RULE = None
    _SEQUENCE17__RULE = None
    _SEQUENCE18__RULE = None
    _SEQUENCE19__RULE = None
    _SEQUENCE20__RULE = None

    _errorRule = None

    def __init__(self, lang: str = 'fr'):
        self._lang = getLang(lang)

    def anyType(self, reallocation = None, default = None):
        isRequired = isRequired if type(isRequired) == bool else True
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                valid = True
                return valid == True
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est d'un type invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        if isRequired:
            self._PRIMARY__REQUIRED__RULE = rule
        else:
            self._PRIMARY__REQUIRED__RULE = None
        return self

    def customRule(self, reallocation = None, default = None,
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        '''
        Cette fonction permet de definir une regle personnalisée

            Parameters:
                value (any): la valeur à verifier
                rule (any): la fonction de validation de la regle
                sanitize (any): la fonction nettoyage apres validation positive
                exception ('dict|str'): l'exception de la regle

            Returns:
                self: La classe de validation
        '''
        def ruleAction(valueInitial):
            def sanitizeFunct(value: any) -> any:
                if ruleFunct(value):
                    return ( sanitize(value) if callable(rule) else value )
            def ruleFunct(value):
                return ( rule(value) if callable(rule) else False )
            def errorFunct(value):
                if not(ruleFunct(value)):
                    if(
                        type(exception) is Exception or
                        isinstance(type(exception), Exception) or
                        issubclass(type(exception), Exception)
                    ):
                        return exception
                    elif(
                        type(exception) == str and
                        len(exception) > 0
                    ):
                        return Exception(exception)
                    elif(
                        type(exception) == dict and
                        self.get_lang() in tuple(exception.keys())
                    ):
                        return Exception(exception[self.get_lang()])
                    return Exception({
                        'fr': 'Erreur inconnue',
                        'en': 'Unknown error',
                    }[self.get_lang()])
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(ruleAction)
        if self._PRIMARY__CUSTOM01__RULE is None:
            self._PRIMARY__CUSTOM01__RULE = ruleAction
        elif self._PRIMARY__CUSTOM02__RULE is None:
            self._PRIMARY__CUSTOM02__RULE = ruleAction
        elif self._PRIMARY__CUSTOM03__RULE is None:
            self._PRIMARY__CUSTOM03__RULE = ruleAction
        elif self._PRIMARY__CUSTOM04__RULE is None:
            self._PRIMARY__CUSTOM04__RULE = ruleAction
        elif self._PRIMARY__CUSTOM05__RULE is None:
            self._PRIMARY__CUSTOM05__RULE = ruleAction
        elif self._PRIMARY__CUSTOM06__RULE is None:
            self._PRIMARY__CUSTOM06__RULE = ruleAction
        elif self._PRIMARY__CUSTOM07__RULE is None:
            self._PRIMARY__CUSTOM07__RULE = ruleAction
        elif self._PRIMARY__CUSTOM08__RULE is None:
            self._PRIMARY__CUSTOM08__RULE = ruleAction
        elif self._PRIMARY__CUSTOM09__RULE is None:
            self._PRIMARY__CUSTOM09__RULE = ruleAction
        elif self._PRIMARY__CUSTOM10__RULE is None:
            self._PRIMARY__CUSTOM10__RULE = ruleAction
        return self
    def required(self, reallocation = None, default = None, isRequired: bool = True):
        isRequired = isRequired if type(isRequired) == bool else True
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedJON | required - reallocation:: ", reallocation)
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return value is not None
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est requis".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is required".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedJON | required - rule - valueInitial:: ", valueInitial)
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                        'defaultVal': default,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                        'defaultVal': default,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedJON | required - rule - valueForValidation:: ", valueForValidation)
            checkerValidation = ruleFunct(valueForValidation)
            valueValidation = sanitizeFunct(valueForValidation) if checkerValidation == True else None
            self._value = valueValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidation)
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
    def enum(self, reallocation = None, default = None, *choices: any):
        choices = choices if type(choices) in (list, tuple) else None
        choiceIsNone = choices is None
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    value is None or (
                        value in choices
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} correspond à aucun choix défini".format(
                            label = labelSTR,
                        ),
                        'en': "{label} correspond to any defined choice".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._PRIMARY__ENUM__RULE = rule
        return self
    def enumNot(self, reallocation = None, default = None, *choices: any):
        choices = choices if type(choices) in (list, tuple) else None
        choiceIsNone = choices is None
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return (
                    value is None or not(
                        value in choices
                    )
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} ne correspond à aucun choix défini".format(
                            label = labelSTR,
                        ),
                        'en': "{label} does not correspond to any defined choice".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._PRIMARY__ENUM_NOT__RULE = rule
        return self
    
    def sequence(self, schema, reallocation = None, default = None):
        def getCheckerSchema():
            return (
                type(schema) is SimplifiedChosenTypes or
                isinstance(type(schema), SimplifiedChosenTypes) or
                type(schema) is SimplifiedNumber or
                isinstance(type(schema), SimplifiedNumber) or
                type(schema) is SimplifiedString or
                isinstance(type(schema), SimplifiedString) or
                type(schema) is SimplifiedBoolean or
                isinstance(type(schema), SimplifiedBoolean) or
                type(schema) is SimplifiedEnum or
                isinstance(type(schema), SimplifiedEnum) or
                type(schema) is SimplifiedNotEnum or
                isinstance(type(schema), SimplifiedNotEnum) or
                type(schema) is SimplifiedObject or
                isinstance(type(schema), SimplifiedObject) or
                type(schema) is SimplifiedArray or
                isinstance(type(schema), SimplifiedArray) or
                type(schema) is SimplifiedSchema or
                isinstance(type(schema), SimplifiedSchema)
            )
        labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
        checkerSchema: bool = getCheckerSchema()
        if checkerSchema :
            schema = schema.label(labelSTR)
        def rule(valueInitial):
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - valueInitial:: ", valueInitial)
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - reallocation:: ", reallocation)
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - default:: ", default)
            labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
            if not(checkerSchema):
                return {
                    'valid': False,
                    'value': None,
                    'error': Exception({
                        'fr': f"{labelSTR} a un schema invalide ({schema})",
                        'en': f"{labelSTR} has an invalid schema ({schema})",
                    }[self.get_lang()])
                }
            valueInitialComp = valueInitial
            valueInitialCompTarget = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        execStr = f"valueContext = value{reallocation} if value{reallocation} is not None else defaultVal"
                        exec(execStr, context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = value if value is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - valueInitialCompTarget:: ", valueInitialComp)
            schemaValidation = schema.label(labelSTR).validate(valueInitialCompTarget)
            if NODEENV == 'debug' and self._SEQUENCE05__RULE is not None:
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - self._SEQUENCE06__RULE:: ", self._SEQUENCE06__RULE)
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - reallocation:: ", reallocation)
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - valueInitialCompTarget:: ", valueInitialCompTarget)
            if NODEENV == 'debug' and self._SEQUENCE05__RULE is not None and self._SEQUENCE06__RULE is None:
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - schemaValidation:: ", schemaValidation)
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - valueInitialCompTarget:: ", valueInitialCompTarget)
                print("[jon -> JON_simplify.py] SimplifiedJON | sequence - rule - type(valueInitialCompTarget):: ", type(valueInitialCompTarget))

            def sanitizeFunct(value: any) -> str:
                return schemaValidation['data']
            def ruleFunct(value):
                return schemaValidation['valid']
            def errorFunct(value):
                return schemaValidation['error']
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        if self._SEQUENCE01__RULE is None:
            self._SEQUENCE01__RULE = rule
        elif self._SEQUENCE02__RULE is None:
            self._SEQUENCE02__RULE = rule
        elif self._SEQUENCE03__RULE is None:
            self._SEQUENCE03__RULE = rule
        elif self._SEQUENCE04__RULE is None:
            self._SEQUENCE04__RULE = rule
        elif self._SEQUENCE05__RULE is None:
            self._SEQUENCE05__RULE = rule
        elif self._SEQUENCE06__RULE is None:
            self._SEQUENCE06__RULE = rule
        elif self._SEQUENCE07__RULE is None:
            self._SEQUENCE07__RULE = rule
        elif self._SEQUENCE08__RULE is None:
            self._SEQUENCE08__RULE = rule
        elif self._SEQUENCE09__RULE is None:
            self._SEQUENCE09__RULE = rule
        elif self._SEQUENCE10__RULE is None:
            self._SEQUENCE10__RULE = rule
        elif self._SEQUENCE11__RULE is None:
            self._SEQUENCE11__RULE = rule
        elif self._SEQUENCE12__RULE is None:
            self._SEQUENCE12__RULE = rule
        elif self._SEQUENCE13__RULE is None:
            self._SEQUENCE13__RULE = rule
        elif self._SEQUENCE14__RULE is None:
            self._SEQUENCE14__RULE = rule
        elif self._SEQUENCE15__RULE is None:
            self._SEQUENCE15__RULE = rule
        elif self._SEQUENCE16__RULE is None:
            self._SEQUENCE16__RULE = rule
        elif self._SEQUENCE17__RULE is None:
            self._SEQUENCE17__RULE = rule
        elif self._SEQUENCE18__RULE is None:
            self._SEQUENCE18__RULE = rule
        elif self._SEQUENCE19__RULE is None:
            self._SEQUENCE19__RULE = rule
        elif self._SEQUENCE20__RULE is None:
            self._SEQUENCE20__RULE = rule
        return self


    def get_lang(self,):
        '''
        Ce getter retourne la langue utilisée par un schema JON

            Returns:
                str: La reponse de la fonction
        '''
        return self._lang
    def set_lang(self, lang: str):
        '''
        Ce setter modifie la langue utilisée par un schema JON

            Parameters:
                lang (str): langue
        '''
        self._lang = getLang(lang)
    def get_label(self,):
        '''
        Ce setter retourne le label du schema JON

            Returns:
                str: La reponse de la fonction
        '''
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedJON | get_label - self._label:: ", self._label)
        labelF = self._label if (
            type(self._label) == str and
            len(self._label) > 0
        ) else {
            'fr': 'l\'element',
            'en': 'the element'
        }[self._lang]
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedJON | get_label - labelF:: ", labelF)
        return cleanField(labelF, max = 30, reverse = True)
    def set_label(self, label: any):
        '''
        Ce setter permet de modifier le label d'un schema JON

            Parameters:
                label (any): nouveau label
        '''
        self._label = label if (
            type(label) in [str] and
            len(label) > 0
        ) else None
    def get_error(self,):
        '''
        Ce getter retourne l'erreur par default du schema JON

            Returns:
                str: La reponse de la fonction
        '''
        if NODEENV == 'debug':
            print("[jon -> JON_default.py] JONDefaultSchema | get_error - self._default_error:: ", self._default_error)
        return self._default_error
    def set_error(self, error: any):
        '''
        Ce setter permet de modifier l'erreur par default du schema JON

            Parameters:
                error (any): nouvelle exception
        '''
        if(
            type(error) is Exception or
            isinstance(type(error), Exception) or
            issubclass(type(error), Exception)
        ):
            self._default_error = error
        elif(
            type(error) == str and
            len(error) > 0
        ):
            self._default_error = Exception(error)
        elif(
            type(error) == dict and
            self.get_lang() in tuple(error.keys())
        ):
            self._default_error = Exception(error[self.get_lang()])

    def error(self, error: any):
        '''
        Cette fonction definit une exception par default qui sera utilisée par le schema JON

            Parameters:
                error (any): nouvelle exception
        '''
        self.set_error(error)
        return self

    def lang(self, value: str):
        '''
        Cette fonction definit la langue qui sera utilisée par le schema JON

            Parameters:
                value (str): id de la langue ('fr' ou 'en')
        '''
        self.set_lang(value)
        return self
    def label(self, value: any):
        '''
        Cette fonction definit le label du schema JON

            Parameters:
                value (str): nouveau label
        '''
        self.set_label(value)
        return self
        
    def getLang(self,):
        '''
        Ce getter retourne la langue utilisée par un schema JON

            Returns:
                str: La reponse de la fonction
        '''
        return self._lang
    def setLang(self, lang: str):
        '''
        Ce setter modifie la langue utilisée par un schema JON

            Parameters:
                lang (str): langue
        '''
        self._lang = getLang(lang)

    def addRule(self, rule):
        self._rules.append(rule)
    def checkIfIsCorrectRule(self, ruleValue, ruleClass):
        checker = (
            type(ruleValue) == dict and
            len(tuple(ruleValue.keys())) <= 3 and
            'data' in tuple(ruleValue.keys()) and
            'valid' in tuple(ruleValue.keys()) and
            type(ruleValue['valid']) == bool and
            'valid' in tuple(ruleValue.keys()) and
            type(ruleValue['valid']) == bool and
            type(ruleValue['error']) is Exception or
            isinstance(type(ruleValue['error']), Exception) or
            issubclass(type(ruleValue['error']), Exception)
        )
        if not(checker):
            raise Exception({
                'fr': f"la regle {ruleClass} produit un resultat ({cleanField(ruleValue)})",
                'en': f"the {ruleClass} rule produces a result ({cleanField(ruleValue)})",
            }[self.getLang()])
        return checker
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedJON | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def isValid(self, ):
        return self.validate()['valid']
    def error(self, ):
        return self.validate()['error']
    def sanitize(self, ):
        return self.validate()['data']
    
    def primaryValidation(self, value):
        try:
            ruleDataF = None
            
            if self._PRIMARY__REQUIRED__RULE is not None:
                ruleData = self._PRIMARY__REQUIRED__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "REQUIRED__RULE"
                    return ruleDataF
            if self._PRIMARY__ENUM__RULE is not None:
                ruleData = self._PRIMARY__ENUM__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ENUM__RULE"
                    return ruleDataF
            if self._PRIMARY__ENUM_NOT__RULE is not None:
                ruleData = self._PRIMARY__ENUM_NOT__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "ENUM_NOT__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM01__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM01__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM01__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM02__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM02__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM02__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM03__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM03__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM03__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM04__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM04__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM04__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM05__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM05__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM05__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM06__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM06__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM06__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM07__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM07__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM07__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM08__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM08__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM08__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM09__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM09__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM09__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM10__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM10__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM10__RULE"
                    return ruleDataF
                    
            if self._SEQUENCE01__RULE is not None:
                ruleData = self._SEQUENCE01__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE01__RULE"
                    return ruleDataF
            if self._SEQUENCE02__RULE is not None:
                ruleData = self._SEQUENCE02__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE02__RULE"
                    return ruleDataF
            if self._SEQUENCE03__RULE is not None:
                ruleData = self._SEQUENCE03__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE03__RULE"
                    return ruleDataF
            if self._SEQUENCE04__RULE is not None:
                ruleData = self._SEQUENCE04__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE04__RULE"
                    return ruleDataF
            if self._SEQUENCE05__RULE is not None:
                ruleData = self._SEQUENCE05__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE05__RULE"
                    return ruleDataF
            if self._SEQUENCE06__RULE is not None:
                ruleData = self._SEQUENCE06__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE06__RULE"
                    return ruleDataF
            if self._SEQUENCE07__RULE is not None:
                ruleData = self._SEQUENCE07__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE07__RULE"
                    return ruleDataF
            if self._SEQUENCE08__RULE is not None:
                ruleData = self._SEQUENCE08__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE08__RULE"
                    return ruleDataF
            if self._SEQUENCE09__RULE is not None:
                ruleData = self._SEQUENCE09__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE09__RULE"
                    return ruleDataF
            if self._SEQUENCE10__RULE is not None:
                ruleData = self._SEQUENCE10__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE10__RULE"
                    return ruleDataF
            if self._SEQUENCE11__RULE is not None:
                valueRuleData = (ruleDataF['data'] if ruleDataF is not None else value)
                ruleData = self._SEQUENCE11__RULE(valueRuleData)
                if NODEENV == 'debug':
                    print("[jon -> JON_simplify.py] SimplifiedJON | primaryValidation - ruleData:: ", ruleData)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE11__RULE"
                    return ruleDataF
            if self._SEQUENCE12__RULE is not None:
                ruleData = self._SEQUENCE12__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE12__RULE"
                    return ruleDataF
            if self._SEQUENCE13__RULE is not None:
                ruleData = self._SEQUENCE13__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE13__RULE"
                    return ruleDataF
            if self._SEQUENCE14__RULE is not None:
                ruleData = self._SEQUENCE14__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE14__RULE"
                    return ruleDataF
            if self._SEQUENCE15__RULE is not None:
                ruleData = self._SEQUENCE15__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE15__RULE"
                    return ruleDataF
            if self._SEQUENCE16__RULE is not None:
                ruleData = self._SEQUENCE16__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE16__RULE"
                    return ruleDataF
            if self._SEQUENCE17__RULE is not None:
                ruleData = self._SEQUENCE17__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE17__RULE"
                    return ruleDataF
            if self._SEQUENCE18__RULE is not None:
                ruleData = self._SEQUENCE18__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE18__RULE"
                    return ruleDataF
            if self._SEQUENCE19__RULE is not None:
                ruleData = self._SEQUENCE19__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE19__RULE"
                    return ruleDataF
            if self._SEQUENCE20__RULE is not None:
                ruleData = self._SEQUENCE20__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "SEQUENCE20__RULE"
                    return ruleDataF

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
        
    def getMapError(self, ):
        self._mapError = self._mapError if (
            type(self._mapError) == dict
        ) else {}
        return self._mapError['map'] if (
            'map' in tuple(self._mapError.keys())
        ) else simplifiedDefaultMapError
    def initMapError(self,
        mapError: any                 
    ):
        import inspect
        self._mapError = self._mapError if (
            type(self._mapError) == dict
        ) else {}
        self._mapError['map'] = mapError if (
            callable(mapError) and 
            len((inspect.getfullargspec(mapError)).args) <= 3
        ) else simplifiedDefaultMapError
        return self
    def applyPreMapping(self, map = InitialMapFunct):
        '''
        Cette fonction permet d'appliquer un mapping personnalisé avant les etapes de validations

            Parameters:
                map (any): fonction de mapping

            Returns:
                self: La classe de validation
        '''
        self.preMap = map
        return self
    def applyMapping(self, map = InitialMapFunct):
        '''
        Cette fonction permet d'appliquer un mapping personnalisé après une validation positive

            Parameters:
                map (any): fonction de mapping

            Returns:
                self: La classe de validation
        '''
        self.map = map
        return self


class SimplifiedArray(SimplifiedJON):
    _maxValue: str = None
    _minValue: str = None
    _lessValue: str = None
    _greaterValue: str = None
    _lengthValue: str = None
    _types: list = []
    
    _ARRAY__RULE = None
    _ARRAY__MIN__RULE = None
    _ARRAY__MAX__RULE = None
    _ARRAY__LESS__RULE = None
    _ARRAY__GREATER__RULE = None
    _ARRAY__LENGTH__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def array(self, typeArray = None, reallocation = None, default = None):
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - type(typeArray):: ", type(typeArray))
            print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - typeArray OLD:: ", typeArray)
        typeArray = typeArray if (
            typeArray is None or (
                type(typeArray) is SimplifiedNumber or
                isinstance(type(typeArray), SimplifiedNumber) or
                type(typeArray) is SimplifiedString or
                isinstance(type(typeArray), SimplifiedString) or
                type(typeArray) is SimplifiedBoolean or
                isinstance(type(typeArray), SimplifiedBoolean) or
                type(typeArray) is SimplifiedDate or
                isinstance(type(typeArray), SimplifiedDate) or
                type(typeArray) is SimplifiedEnum or
                isinstance(type(typeArray), SimplifiedEnum) or
                type(typeArray) is SimplifiedNotEnum or
                isinstance(type(typeArray), SimplifiedNotEnum) or
                type(typeArray) is SimplifiedObject or
                isinstance(type(typeArray), SimplifiedObject) or
                type(typeArray) is SimplifiedArray or
                isinstance(type(typeArray), SimplifiedArray) or
                type(typeArray) is SimplifiedChosenTypes or
                isinstance(type(typeArray), SimplifiedChosenTypes) or
                type(typeArray) is SimplifiedSchema or
                isinstance(type(typeArray), SimplifiedSchema)
            )
        ) else '--'
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - typeArray:: ", typeArray)
        def rule(valueInitial):
            typeArrayCmps = None
            valueInitialComp = valueInitial
            resVFVT = valueInitial
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - reallocation:: ", reallocation)
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - valueInitial:: ", valueInitial)
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        execStr = f"valueContext = value{reallocation} if value{reallocation} is not None else defaultVal"
                        exec(execStr, context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = value if value is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
            if typeArray == '--':
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
            elif typeArray is not None and type(valueInitialCompTarget) in (list, tuple):
                def actionTypeArray(indexVal, val):
                    schemaTypeArray = typeArray.label(f"{self.get_label()}{reallocation if reallocation is not None else ''}[{indexVal}]")
                    validation = schemaTypeArray.validate(val)
                    validation['error_rule'] = schemaTypeArray._errorRule
                    if NODEENV == 'debug':
                        print(f"[jon -> JON_simplify.py] SimplifiedArray | array - rule - actionTypeArray - schemaTypeArray (indexVal: {indexVal}):: ", schemaTypeArray)
                        print(f"[jon -> JON_simplify.py] SimplifiedArray | array - rule - actionTypeArray - val (indexVal: {indexVal}):: ", val)
                        print(f"[jon -> JON_simplify.py] SimplifiedArray | array - rule - actionTypeArray - validation (indexVal: {indexVal}):: ", validation)
                    return validation
                typeArrayCmps = [actionTypeArray(indexVal, val) for indexVal, val in enumerate(valueInitialCompTarget)]
                if NODEENV == 'debug':
                    print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - typeArrayCmps:: ", typeArrayCmps)
            def compWithType(value):
                try:
                    if (
                        typeArray is not None and
                        type(value) in (list, tuple)
                    ):
                        invalidTypeArrayCmps = [val for indexVal, val in enumerate(typeArrayCmps) if not(val['valid'])]
                        if len(invalidTypeArrayCmps) > 0:
                            elmtITAC = invalidTypeArrayCmps[0]
                            self._errorRule = elmtITAC['error_rule']
                            return elmtITAC
                        else:
                            return {
                                'valid': True,
                                'data': [val['data'] for indexVal, val in enumerate(typeArrayCmps)],
                                'error': None,
                            }
                    return {
                        'data': value,
                        'valid': True,
                        'error': None,
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
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - valueInitialCompTarget:: ", valueInitialCompTarget)
            compWithTypeValue = compWithType(valueInitialCompTarget)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - compWithTypeValue:: ", compWithTypeValue)
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - self._errorRule:: ", self._errorRule)
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    if (
                        typeArray is not None and
                        type(value) in (list, tuple)
                    ):
                        return compWithTypeValue['data']
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) in (list, tuple) and (
                            typeArray is None or (
                                typeArray is not None and
                                compWithTypeValue['valid']
                            )
                        )
                    ) or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    if (
                        typeArray is not None and
                        type(value) in (list, tuple)
                    ):
                        return compWithTypeValue['error']
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - valueInitial:: ", valueInitial)
                print("[jon -> JON_simplify.py] SimplifiedArray | array - rule - reallocation:: ", reallocation)
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__RULE = rule
        return self

    def arrayMin(self, minValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__MIN__RULE = rule
        return self
    def arrayMax(self, maxValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__MAX__RULE = rule
        return self
    def arrayLess(self, lessValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__LESS__RULE = rule
        return self
    def arrayGreater(self, greaterValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ARRAY__GREATER__RULE = rule
        return self
    def arrayLength(self, lengthValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
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
                print("[jon -> JON_simplify.py] ArrayString | arrayValidation - ruleData (For Array):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] ArrayString | arrayValidation - ruleData (For Primary):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] ArrayString | arrayValidation - ruleDataF:: ", ruleDataF)
            
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
                print("[jon -> JON_simplify.py] SimplifiedArray | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
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
                        print("[jon -> JON_simplify.py] SimplifiedArray | arrayValidation - ruleData:: ", ruleData)
                        print("[jon -> JON_simplify.py] SimplifiedArray | arrayValidation - self._errorRule:: ", self._errorRule)
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

            return ruleDataF
        except Exception as err:
            stack = traceback.format_exc()
            log.error(stack)
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
class SimplifiedObject(SimplifiedJON):
    _struct: dict = {}
    _primaryStruct: bool = False
    _maxValue: str = None
    _minValue: str = None
    _lessValue: str = None
    _greaterValue: str = None
    _lengthValue: str = None

    _types: list = []
    
    _oldValueForStruct = None
    
    _OBJECT__RULE = None
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

    def object(self, typeObject = None, reallocation = None, default = None):
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedObject | array - rule - type(typeObject):: ", type(typeObject))
            print("[jon -> JON_simplify.py] SimplifiedObject | array - rule - typeObject OLD:: ", typeObject)
        typeObject = typeObject if (
            typeObject is None or (
                type(typeObject) is SimplifiedNumber or
                isinstance(type(typeObject), SimplifiedNumber) or
                type(typeObject) is SimplifiedString or
                isinstance(type(typeObject), SimplifiedString) or
                type(typeObject) is SimplifiedBoolean or
                isinstance(type(typeObject), SimplifiedBoolean) or
                type(typeObject) is SimplifiedDate or
                isinstance(type(typeObject), SimplifiedDate) or
                type(typeObject) is SimplifiedEnum or
                isinstance(type(typeObject), SimplifiedEnum) or
                type(typeObject) is SimplifiedNotEnum or
                isinstance(type(typeObject), SimplifiedNotEnum) or
                type(typeObject) is SimplifiedObject or
                isinstance(type(typeObject), SimplifiedObject) or
                type(typeObject) is SimplifiedArray or
                isinstance(type(typeObject), SimplifiedArray) or
                type(typeObject) is SimplifiedChosenTypes or
                isinstance(type(typeObject), SimplifiedChosenTypes) or
                type(typeObject) is SimplifiedSchema or
                isinstance(type(typeObject), SimplifiedSchema)
            )
        ) else '--'
        if NODEENV == 'debug':
            print("[jon -> JON_simplify.py] SimplifiedObject | array - rule - typeObject:: ", typeObject)
        def rule(valueInitial):
            typeObjectCmps = None
            valueInitialComp = valueInitial
            valueInitialCompTarget = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        execStr = f"valueContext = value{reallocation} if value{reallocation} is not None else defaultVal"
                        exec(execStr, context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = value if value is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedObject | object - rule - valueInitial:: ", valueInitial)
                print("[jon -> JON_simplify.py] SimplifiedObject | object - rule - typeObject:: ", typeObject)
            labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
            if typeObject == '--':
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
            elif typeObject is not None and type(valueInitialCompTarget) == dict:
                def actionTypeKey(key, val):
                    schemaTypeArray = typeObject.label(f"{self.get_label()}{reallocation if reallocation is not None else ''}[{key}]")
                    validation = schemaTypeArray.validate(val)
                    validation['error_rule'] = schemaTypeArray._errorRule
                    return validation
                typeObjectCmps = {keyVal: actionTypeKey(keyVal, val) for keyVal, val in valueInitialCompTarget.items()}
                if NODEENV == 'debug':
                    print("[jon -> JON_simplify.py] SimplifiedObject | object - rule - typeObjectCmps:: ", typeObjectCmps)
            def compWithType(value):
                try:
                    if (
                        typeObject is not None and
                        type(value) == dict
                    ):
                        invalidTypeObjectCmps = [val for keyVal, val in typeObjectCmps.items() if not(val['valid'])]
                        if len(invalidTypeObjectCmps) > 0:
                            elmtITAC = invalidTypeObjectCmps[0]
                            self._errorRule = elmtITAC['error_rule']
                            return elmtITAC
                        else:
                            return {
                                'valid': True,
                                'data': {keyVal: val['data'] for keyVal, val in typeObjectCmps.items()},
                                'error': None,
                            }
                    return {
                        'data': value,
                        'valid': True,
                        'error': None,
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
                print("[jon -> JON_simplify.py] SimplifiedObject | object - rule - valueInitialCompTarget:: ", valueInitialCompTarget)
            compWithTypeValue = compWithType(valueInitialCompTarget)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedObject | object - rule - compWithTypeValue:: ", compWithTypeValue)
                print("[jon -> JON_simplify.py] SimplifiedArray | object - rule - self._errorRule:: ", self._errorRule)
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    if (
                        typeObject is not None and
                        type(value) == dict
                    ):
                        return compWithTypeValue['data']
                    return value
            def ruleFunct(value):
                return (
                    (
                        type(value) == dict and (
                            typeObject is None or (
                                typeObject is not None and
                                compWithTypeValue['valid']
                            )
                        )
                    ) or
                    value is None
                )
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    if (
                        typeObject is not None and
                        type(value) in dict
                    ):
                        return compWithTypeValue['error']
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas un objet".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not an object".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__RULE = rule
        return self

    def objectContainsKeys(self, keys = [], strict = False, reallocation = None, default = None):
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__CONTAINS_KEYS__RULE = rule
        return self
    def objectNoContainsKeys(self, keys = [], strict = False, reallocation = None, default = None):
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__NO_CONTAINS_KEYS__RULE = rule
        return self

    def objectRegExpContainsKeys(self, ruleValue: str, flag: re.RegexFlag = None, strict: bool = False, reallocation = None, default = None):
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
                                    SimplifiedString(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) > 0
                            ) or 
                            (
                                strict == True and
                                len([keyValue for keyValue, value in value.items() if (
                                    SimplifiedString(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) >= len(tuple(value.keys()))
                            )
                        )
                    )
                )
            def errorFunct(value):
                invalidKeys = [keyValue for keyValue, value in value.items() if not(
                    SimplifiedString(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__REGEXP_CONTAINS_KEYS__RULE = rule
        return self
    def objectRegExpNoContainsKeys(self, ruleValue: str, flag: re.RegexFlag = None, strict: bool = False, reallocation = None, default = None):
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
                                    SimplifiedString(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) > 0
                            ) or 
                            (
                                strict == True and
                                len([keyValue for keyValue, value in value.items() if not(
                                    SimplifiedString(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
                                )]) >= len(tuple(value.keys()))
                            )
                        )
                    )
                )
            def errorFunct(value):
                invalidKeys = [keyValue for keyValue, value in value.items() if (
                    SimplifiedString(self.lang).stringRegexp(keyValue, ruleValue=ruleValue, flag=flag).isValid()
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__REGEXP_NO_CONTAINS_KEYS__RULE = rule
        return self
    
    def objectMin(self, minValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__MIN__RULE = rule
        return self
    def objectMax(self, maxValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__MAX__RULE = rule
        return self
    def objectLess(self, lessValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__LESS__RULE = rule
        return self
    def objectGreater(self, greaterValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._OBJECT__GREATER__RULE = rule
        return self
    def objectLength(self, lengthValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
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
                print("[jon -> JON_simplify.py] ObjectString | objectValidation - ruleData (For String):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] ObjectString | objectValidation - ruleData (For Primary):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] ObjectString | objectValidation - ruleDataF:: ", ruleDataF)
            
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
                print("[jon -> JON_simplify.py] SimplifiedObject | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
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
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }

class SimplifiedChosenTypes(SimplifiedJON):
    _types = []
    _invalid_types = []

    _CHOSEN_TYPE__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def chosenTypes(self, *types: list, reallocation = None, default = None):
        self.chosenTypesChoices(*types)
        def rule(valueInitial):
            if len(self._invalid_types) > 0:
                labelSTR = json.dumps(self.get_label())
                return {
                    'valid': False,
                    'value': None,
                    'error': Exception({
                        'fr': f"{labelSTR} possède un ou plusieurs types incorrectes ({','.join(self._invalid_types)})",
                        'en': f"{labelSTR} has one or more incorrect types ({','.join(self._invalid_types)})",
                    }[self.get_lang()])
                }
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - self._types:: ", self._types)
            if NODEENV == 'debug':
                print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - valueInitial:: ", valueInitial)
                print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - reallocation:: ", reallocation)
            valueInitialComp = valueInitial
            valueInitialCompTarget = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        execStr = f"valueContext = value{reallocation} if value{reallocation} is not None else defaultVal"
                        exec(execStr, context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = value if value is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueInitialComp,
                        'defaultVal': default,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueInitialCompTarget = valueContextF
                    valueInitialComp = context['valueF']
                    self._value = valueInitialComp
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            self._types = [typeCT.label(f"{self.get_label()}{reallocation if reallocation is not None else ''}") for indexCT, typeCT in enumerate(self._types)]
            def comparatorCT():
                resultCT = {
                    'invalid': None,
                    'valid': None,
                }
                for indexCT, typeCT in enumerate(self._types):
                    validationCT = typeCT.validate(valueInitialCompTarget)
                    if validationCT['valid'] == True:
                        resultCT['valid'] = validationCT
                        resultCT['invalid'] = None
                        break
                    resultCT['valid'] = None
                    resultCT['invalid'] = validationCT
                return resultCT

            initialCheckerDatas = [typeCT.validate(valueInitialCompTarget) for indexCT, typeCT in enumerate(self._types)]
            checkerDatas = comparatorCT()
            initialCheckerValidData = checkerDatas['valid']
            initialCheckerInvalidData = checkerDatas['invalid']

            if NODEENV == 'debug':
                print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - valueInitialCompTarget:: ", valueInitialCompTarget)
                print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - checkerDatas:: ", checkerDatas)
                print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - initialCheckerDatas:: ", initialCheckerDatas)
            def sanitizeFunct(value: any) -> str:
                if ruleFunct(value):
                    return initialCheckerValidData['data'] if value is not None else None
            def ruleFunct(value):
                return (
                    initialCheckerValidData is not None or
                    value is None
                )
            def errorFunct(value):
                checkerErrorFunct = not(ruleFunct(value))
                if NODEENV == 'debug':
                    print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - errorFunct - ruleFunct(value):: ", ruleFunct(value))
                    print(f"[jon -> JON_simplify.py] SimplifiedChosenTypes | chosenTypes - errorFunct - value:: ", value)
                if(not(ruleFunct(value))):
                    return initialCheckerInvalidData['error']
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._CHOSEN_TYPE__RULE = rule
        return self
    def chosenTypesChoices(self, *types: list):
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
                        type(typeCT) is SimplifiedChosenTypes or
                        isinstance(type(typeCT), SimplifiedChosenTypes) or
                        type(typeCT) is SimplifiedNumber or
                        isinstance(type(typeCT), SimplifiedNumber) or
                        type(typeCT) is SimplifiedString or
                        isinstance(type(typeCT), SimplifiedString) or
                        type(typeCT) is SimplifiedBoolean or
                        isinstance(type(typeCT), SimplifiedBoolean) or
                        type(typeCT) is SimplifiedDate or
                        isinstance(type(typeCT), SimplifiedDate) or
                        type(typeCT) is SimplifiedEnum or
                        isinstance(type(typeCT), SimplifiedEnum) or
                        type(typeCT) is SimplifiedNotEnum or
                        isinstance(type(typeCT), SimplifiedNotEnum) or
                        type(typeCT) is SimplifiedObject or
                        isinstance(type(typeCT), SimplifiedObject) or
                        type(typeCT) is SimplifiedArray or
                        isinstance(type(typeCT), SimplifiedArray) or
                        type(typeCT) is SimplifiedSchema or
                        isinstance(type(typeCT), SimplifiedSchema)
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
                    datasTA.append(typeCT)
            return datasTA
        self._types = []
        checker2 = checker2Action()
        if not(type(checker2) in (list, tuple)):
            return self
        self._types = checker2
        if NODEENV == 'debug':
            print(f"[jon -> JON_sup.py] ChosenType | chosenTypesChoices - self._types:: ", self._types)

        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.chosenTypesValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedChosenTypes | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
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
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }

class SimplifiedEnum(SimplifiedJON):
    _choices: any = []

    _ENUM__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def enum(self, *values: list, reallocation = None, default = None):
        self.enumChoices(*values)
        def rule(valueInitial):
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedEnum | enum - rule - reallocation:: ", reallocation)
                print("[jon -> JON_simplify.py] SimplifiedEnum | enum - rule - default:: ", default)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedEnum | enum - self._choices:: ", self._choices)
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._ENUM__RULE = rule
        return self
    def enumChoices(self, *values: list):
        self._choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.enumValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedEnum | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
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
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
class SimplifiedNotEnum(SimplifiedJON):
    _choices: any = []

    _NOT_ENUM__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def notEnum(self, *values: list, reallocation = None, default = None):
        self.notEnumChoices(*values)
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NOT_ENUM__RULE = rule
        return self
    def notEnumChoices(self, *values: list):
        self._choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.notEnumValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedNotEnum | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
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
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
    
class SimplifiedDate(SimplifiedJON):
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

    def date(self, reallocation = None, default = None):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(value is not None):
                    if(self._format is None):
                        self.stringChangeFormat(dateTimeFormatInitial)
                            
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une date".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a date".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._BOOLEAN__RULE = rule
        return self
    def dateMin(self, minValue: any, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__MIN__RULE = rule
        return self
    def dateMax(self, maxValue: any, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__MAX__RULE = rule
        return self
    def dateLess(self, lessValue: any, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__LESS__RULE = rule
        return self
    def dateGreater(self, greatedValue: any, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__GREATER__RULE = rule
        return self
    def dateEqualTo(self, equalValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__EQUAL_TO__RULE = rule
        return self
    def dateToDate(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est d'un type \"Date\" invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid \"Date\" type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__TO_DATE__RULE = rule
        return self
    def dateToTime(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est d'un type \"Date\" invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid \"Date\" type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._DATE__TO_TIME__RULE = rule
        return self
    
    def dateChangeFormat(self,
        newFormat: str
    ):
        if (
            type(newFormat) == str and
            len(newFormat) > 0
        ):
            self._format = newFormat

        return self
    def dateChangeTimezone(self,
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
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedDate | validate - stack:: ", stack)
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
    
class SimplifiedBoolean(SimplifiedJON):
    _trueValues: list = ['true', 't', '1', 1, True]
    _falseValues: list = ['false', 'f', '0', 0, False]

    _BOOLEAN__RULE = None

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)

    def boolean(self, reallocation = None, default = None):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                return convertToBoolean(value)
            def ruleFunct(value):
                return isBoolean(value, (self._trueValues + self._falseValues), False)
            def errorFunct(value):
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas un booléen".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a Boolean".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._BOOLEAN__RULE = rule
        return self
    def required(self, reallocation = None, default = None, isRequired: bool = True):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est requis".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is required".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        if isRequired:
            self._PRIMARY__REQUIRED__RULE = rule
        else:
            self._PRIMARY__REQUIRED__RULE = None
        return self
    
    def booleanTrueValues(self, valueInitial: list, reallocation = None, default = None):
        values = valueInitial if type(valueInitial) in (list, tuple) else []
        if(len(values) > 0):
            self._trueValues = values
        return self
    def booleanFalseValues(self, valueInitial: list, reallocation = None, default = None):
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
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedBoolean | validate - stack:: ", stack)
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }


class SimplifiedNumber(SimplifiedJON):
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

    def number(self, reallocation = None, default = None):
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
                    print(f"[jon -> JON_simplify.py] SimplifiedNumber | number - errorFunct - value:: '{value}'")
                    print("""[jon -> JON_simplify.py] SimplifiedNumber | number - errorFunct - type(value):: """, type(value))
                    print("""[jon -> JON_simplify.py] SimplifiedNumber | number - errorFunct - ruleFunct(value):: """, ruleFunct(value))
                    print("""[jon -> JON_simplify.py] SimplifiedNumber | number - errorFunct - isNumber(value):: """, isNumber(value))
                if(not(ruleFunct(value) == True)):
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas un nombre".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__RULE = rule
        return self
    def numberMin(self, minValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__MIN__RULE = rule
        return self
    def numberMax(self, maxValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__MAX__RULE = rule
        return self
    def numberLess(self, lessValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__LESS__RULE = rule
        return self
    def numberGreater(self, greaterValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__GREATER__RULE = rule
        return self
    def numberNegative(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        "fr": "{label} doit être un nombre negatif".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a negative number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__NEGATIVE__RULE = rule
        return self
    def numberPositive(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        "fr": "{label} doit être un nombre positif".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a positive number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__POSITIVE__RULE = rule
        return self
    def numberSigned(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        "fr": "{label} doit être soit un nombre négatif soit un nombre positif".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be either a negative number or a positive number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__SIGNED__RULE = rule
        return self
    def numberInteger(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        "fr": "{label} doit être un nombre entier valide".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a valid integer number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__INTEGER__RULE = rule
        return self
    def numberDecimal(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        "fr": "{label} doit être un nombre décimal valide".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be a valid decimal number".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__DECIMAL__RULE = rule
        return self
    def numberMultiple(self, nber: float, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._NUMBER__MULTIPLE__RULE = rule
        return self
    def numberTCPPort(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        "fr": "{label} doit être au format d'un port TCP".format(
                            label = labelSTR,
                        ),
                        "en": "{label} must be in the format of a TCP port".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
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
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
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
                print("[jon -> JON_simplify.py] SimplifiedNumber | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
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
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }

class SimplifiedString(SimplifiedJON):
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

    def string(self, reallocation = None, default = None):
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value) == True):
                    if(value is not None):
                        if(self._format is None):
                            if (
                                isString(value, typeValue = "datetime")
                            ):
                                self.stringChangeFormat(dateTimeFormatInitial)
                            elif (
                                isString(value, typeValue = "date")
                            ):
                                self.stringChangeFormat(self._dateFormat)
                            elif (
                                isString(value, typeValue = "time")
                            ):
                                self.stringChangeFormat(self._timeFormat)

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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__RULE = rule
        return self
    def stringMin(self, minValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__MIN__RULE = rule
        return self
    def stringMax(self, maxValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__MAX__RULE = rule
        return self
    def stringLess(self, lessValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__LESS__RULE = rule
        return self
    def stringGreater(self, greaterValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__GREATER__RULE = rule
        return self
    def stringLength(self, lengthValue: int, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
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
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__LENGTH__RULE = rule
        return self
    def stringRegexp(self, ruleValue: str, flag: re.RegexFlag = None, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} ne respecte pas la rêgle appliquée".format(
                            label = labelSTR,
                        ),
                        'en': "{label} does not respect the ruleFunct applied".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__REGEXP__RULE = rule
        return self
    def stringAlphanum(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères alphanumeriques".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string of alphanumeric characters".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__ALPHANUM__RULE = rule
        return self
    def stringBase64(self, reallocation = None, default = None, paddingRequired: bool = True, urlSafe: bool = True):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères de type base64".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a base64 string".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__BASE64__RULE = rule
        return self
    def stringLowercase(self, reallocation = None, default = None, strictMode: bool = False):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas en minuscule".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not lowercase".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__LOWERCASE__RULE = rule
        return self
    def stringUppercase(self, reallocation = None, default = None, strictMode: bool = False):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas en majuscule".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not uppercase".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__UPPERCASE__RULE = rule
        return self
    def stringCapitalize(self, reallocation = None, default = None, strictMode: bool = False):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas en lettre capitale".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not capitalized".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__CAPITALIZE__RULE = rule
        return self
    def stringUcFirst(self, reallocation = None, default = None, strictMode: bool = False):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'a pas de première lettre en majuscule".format(
                            label = labelSTR,
                        ),
                        'en': "{label} does not have a capitalized first letter".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__UC_FIRST__RULE = rule
        return self
    def stringCreditCard(self, reallocation = None, default = None, types: list = []):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères au format d'une carte de crédit".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is a character string in the format of a credit card".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__CREDIT_CARD__RULE = rule
        return self
    def stringDataUri(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne d'URI de données valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a valid data URI string".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__DATAURI__RULE = rule
        return self
    def stringDomain(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un domaine valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid domain".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__DOMAIN__RULE = rule
        return self
    def stringUrl(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'une url valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string is in the format of a valid url".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__URL__RULE = rule
        return self
    def stringHostname(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un nom d'hôte valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in the format of a valid hostname".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__HOSTNAME__RULE = rule
        return self
    def stringIPAddress(self, reallocation = None, default = None, types: list = []):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'une addresse IP valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string is in the format of a valid IP address".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__IP_ADDRESS__RULE = rule
        return self
    def stringEmail(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un email valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string is in the format of a valid email".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__EMAIL__RULE = rule
        return self
    def stringGuid(self, reallocation = None, default = None, types: list = []):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format GUID valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string is in valid GUID format".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__GUID__RULE = rule
        return self
    def stringHexa(self, reallocation = None, default = None, insensitive: bool = False):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'un hexa valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string is in the format of a valid hexa".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__HEXA__RULE = rule
        return self
    def stringBinary(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format binaire valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a string is in valid binary format".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__BINARY__RULE = rule
        return self
    def stringDate(self, reallocation = None, default = None, format = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères est au format d'une date valide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string is in the format of a valid date".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__DATE__RULE = rule
        return self
    def stringIdentifier(self, reallocation = None, default = None):
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} n'est pas une chaîne de caractères sous le format d'un identifiant".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is not a character string in the format of an identifier".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__IDENTIFIER__RULE = rule
        return self

    def stringEnum(self, *values: list, reallocation = None, default = None):
        self.stringEnumChoices(*values)
        def rule(valueInitial):
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedString | stringEnum - self._enum_choices:: ", self._enum_choices)
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est d'un type invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__ENUM__RULE = rule
        return self
    def stringEnumChoices(self, *values: list):
        self._enum_choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self
    def stringNotEnum(self, *values: list, reallocation = None, default = None):
        self.stringNotEnumChoices(*values)
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
                    labelSTR = json.dumps(f"{self.get_label()}{reallocation if reallocation is not None else ''}")
                    err = Exception({
                        'fr': "{label} est d'un type invalide".format(
                            label = labelSTR,
                        ),
                        'en': "{label} is of an invalid type".format(
                            label = labelSTR,
                        ),
                    }[self.get_lang()])
                    return err
            valueForValidationTarget = valueInitial
            valueForValidation = valueInitial
            try:
                if(type(reallocation) == str and len(reallocation) > 0):
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'value': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial{reallocation} if valueInitial{reallocation} is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF{reallocation} = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
                else:
                    valueContextF = None
                    try:
                        self._value = valueInitial
                        context = {
                            'valueInitial': valueInitial,
                            'defaultVal': default,
                        }
                        exec(f"valueContext = valueInitial if valueInitial is not None else defaultVal", context)
                        valueContextF = context['valueContext']
                    except Exception as err:
                        valueContextF = default
                    context = {
                        'value': valueContextF,
                        'valueF': valueForValidation,
                    }
                    execStr = f"valueF = value"
                    exec(execStr, context)
                    valueForValidationTarget = valueContextF
                    valueForValidation = context['valueF']
                    self._value = valueForValidation
            except Exception as err:
                stack = traceback.format_exc()
                valueErr = cleanField(f"{valueInitial}", max=20)
                attrErr = cleanField(f"{reallocation}", max=20)
                valueTarget = cleanField(f"{valueInitial}{reallocation}", max=50, reverse = True)
                self._errorRule = 'REALLOCATION__RULE'
                return {
                    'valid': False,
                    'data': None,
                    'error': Exception({
                        'fr': f"Erreur lors de la réallocation, valeur  introuvable: \"{valueTarget}\"",
                        'en': f"Error during reallocation, value not found: \"{valueTarget}\"",
                    }[self.getLang()]),
                }
            checkerValidation = ruleFunct(valueForValidationTarget)
            valueForValidationTarget = sanitizeFunct(valueForValidationTarget) if checkerValidation == True else None
            context = {
                'valueInput': valueForValidationTarget,
                'valueF': valueForValidation,
            }
            execStr = f"valueF{reallocation if type(reallocation) == str else ''} = valueInput"
            exec(execStr, context)
            valueForValidation = context['valueF'] if checkerValidation == True else None
            self._value = valueForValidation
            errorValidation = None if checkerValidation == True else  errorFunct(valueForValidationTarget)
            return {
                'valid': checkerValidation,
                'data': valueForValidation,
                'error': errorValidation,
            }
        self.addRule(rule)
        self._STRING__NOT_ENUM__RULE = rule
        return self
    def stringNotEnumChoices(self, *values: list):
        self._not_enum_choices = copy.deepcopy(values) if (
            type(values) in (list, tuple) and
            len(values) > 0
        ) else None

        return self
    
        
    def stringChangeFormat(self,
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
                print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - ruleData (For String):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - ruleData (For Primary):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - ruleDataF:: ", ruleDataF)
            
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
                print("[jon -> JON_simplify.py] SimplifiedString | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp
    def stringValidation(self, value):
        try:
            ruleDataF = None

            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - self._STRING__RULE:: ", self._STRING__RULE)
            if self._STRING__RULE is not None:
                ruleData = self._STRING__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if NODEENV == 'debug':
                    print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - ruleData:: ", ruleData)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "STRING__RULE"
                    return ruleDataF
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - ruleDataF:: ", ruleDataF)
                if ruleDataF is not None:
                    print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - value:: ", value)
                    print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - type(value):: ", type(value))
                    print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - ruleDataF['data']:: ", ruleDataF['data'])
                    print("[jon -> JON_simplify.py] SimplifiedString | stringValidation - type(ruleDataF['data']):: ", type(ruleDataF['data']))
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
            return {
                'data': None,
                'valid': False,
                'error': str(stack),
            }


class SimplifiedSchema(
    SimplifiedNumber,
    SimplifiedString,
    SimplifiedBoolean,
    SimplifiedDate,
    SimplifiedEnum,
    SimplifiedNotEnum,
    SimplifiedObject,
    SimplifiedArray,
    SimplifiedChosenTypes,
):

    def __init__(self, lang: str = 'fr'):
        super().__init__(lang)
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None
            
            ruleData = self.chosenTypesValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | chosenTypesValidation - ruleData (For Chosen Types):: ", ruleData)
                print("[jon -> JON_simplify.py] SimplifiedSchema | chosenTypesValidation - self._errorRule (For Chosen Types):: ", self._errorRule)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.arrayValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | arrayValidation - ruleData (For Array):: ", ruleData)
                print("[jon -> JON_simplify.py] SimplifiedSchema | arrayValidation - self._errorRule (For Array):: ", self._errorRule)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.objectValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | objectValidation - ruleData (For Object):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.notEnumValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | notEnumValidation - ruleData (For Not Enum):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.enumValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | enumValidation - ruleData (For Enum):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.booleanValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | booleanValidation - ruleData (For Boolean):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.numberValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | numberValidation - ruleData (For Number):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            ruleData = self.stringValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | stringValidation - ruleData (For String):: ", ruleData)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )

            ruleData = self.primaryValidation(ruleDataF['data'] if ruleDataF is not None else value)
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | primaryValidation - ruleData (For Primary):: ", ruleData)
                print("[jon -> JON_simplify.py] SimplifiedSchema | primaryValidation - self._errorRule (For Primary):: ", self._errorRule)
            if ruleData is not None:
                ruleDataF = ruleData
            if ruleDataF is not None and not(ruleDataF['valid']):
                if NODEENV == 'debug':
                    print("[jon -> JON_simplify.py] SimplifiedSchema | primaryValidation - self.getMapError:: ", self.getMapError)
                return self._mapError['map'](
                    res=ruleDataF,
                    ruleName=self._errorRule,
                    label = self.get_label(),
                    lang = self.getLang(),
                )
            
            if NODEENV == 'debug':
                print("[jon -> JON_simplify.py] SimplifiedSchema | stringValidation - self._errorRule:: ", self._errorRule)
                print("[jon -> JON_simplify.py] SimplifiedSchema | stringValidation - ruleDataF:: ", ruleDataF)
            
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
                print("[jon -> JON_simplify.py] SimplifiedSchema | validate - stack:: ", stack)
            resp = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            resp = self._mapError['map'](
                res=resp,
                ruleName='UNKNOWN__RULE',
                label = self.get_label(),
                lang = self.getLang(),
            )
            return resp

    