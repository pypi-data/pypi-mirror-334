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
from .utils import getLang

log = logging.getLogger(__name__)

def InitialMapFunct(value: any):
    return value

def cleanField(value: str, max: int = 15, reverse: bool = False):
    reverse = reverse if type(reverse) == bool else False
    max = max if (
        type(max) == int and
        max > 0
    ) else 15
    res = str(value)
    if len(res) > max:
        res = f"...{res[-max:]}" if reverse else f"{res[:max]}..."
    return res
def defaultMapError( res, error, ruleName = None, label = None, lang = 'fr' ):
    if NODEENV == 'debug':
        print("\n>----------------------")
        print("-- JON - defaultMapError | error:: ", error)
        print("-- JON - defaultMapError | ruleName:: ", ruleName)
        print("-- JON - defaultMapError | label:: ", label)
        print("-- JON - defaultMapError | lang:: ", lang)
        print("\n")
        print("-- JON - defaultMapError | error:: ", error)
        print("-- JON - defaultMapError | res:: ", res)
        print("-------------------------<")
    return res

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



def defaultAllocationMap(initialData, data):
    initialData = data
class JONDefaultSchema():
    '''
    JONDefaultSchema est la super class 'schema' permettant la validation des données sous JON
    '''
    _label: str = None
    _lang: str = 'fr'
    _default = None
    _rules: list = []
    _value = None
    _default_error = None
    
    map = None
    preMap = None
    
    _mapError = {
        'map': defaultMapError,
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
    _PRIMARY__CUSTOM11__RULE = None
    _PRIMARY__CUSTOM12__RULE = None
    _PRIMARY__CUSTOM13__RULE = None
    _PRIMARY__CUSTOM14__RULE = None
    _PRIMARY__CUSTOM15__RULE = None
    _PRIMARY__CUSTOM16__RULE = None
    _PRIMARY__CUSTOM17__RULE = None
    _PRIMARY__CUSTOM18__RULE = None
    _PRIMARY__CUSTOM19__RULE = None
    _PRIMARY__CUSTOM20__RULE = None
    _PRIMARY__CUSTOM21__RULE = None
    _PRIMARY__CUSTOM22__RULE = None
    _PRIMARY__CUSTOM23__RULE = None
    _PRIMARY__CUSTOM24__RULE = None
    _PRIMARY__CUSTOM25__RULE = None
    _PRIMARY__CUSTOM26__RULE = None
    _PRIMARY__CUSTOM27__RULE = None
    _PRIMARY__CUSTOM28__RULE = None
    _PRIMARY__CUSTOM29__RULE = None
    _PRIMARY__CUSTOM30__RULE = None
    _PRIMARY__CUSTOM31__RULE = None
    _PRIMARY__CUSTOM32__RULE = None
    _PRIMARY__CUSTOM33__RULE = None
    _PRIMARY__CUSTOM34__RULE = None
    _PRIMARY__CUSTOM35__RULE = None
    _PRIMARY__CUSTOM36__RULE = None
    _PRIMARY__CUSTOM37__RULE = None
    _PRIMARY__CUSTOM38__RULE = None
    _PRIMARY__CUSTOM39__RULE = None
    _PRIMARY__CUSTOM40__RULE = None
    _PRIMARY__CUSTOM41__RULE = None
    _PRIMARY__CUSTOM42__RULE = None
    _PRIMARY__CUSTOM43__RULE = None
    _PRIMARY__CUSTOM44__RULE = None
    _PRIMARY__CUSTOM45__RULE = None
    _PRIMARY__CUSTOM46__RULE = None
    _PRIMARY__CUSTOM47__RULE = None
    _PRIMARY__CUSTOM48__RULE = None
    _PRIMARY__CUSTOM49__RULE = None
    _PRIMARY__CUSTOM50__RULE = None

    _errorRule = None

    def __init__(self, lang: str = 'fr'):
        self._lang = getLang(lang)

    def applyApp(self,
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
        self.addRule(ruleAction)
        def initAllRuleVars():
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
            elif self._PRIMARY__CUSTOM11__RULE is None:
                self._PRIMARY__CUSTOM11__RULE = ruleAction
            elif self._PRIMARY__CUSTOM12__RULE is None:
                self._PRIMARY__CUSTOM12__RULE = ruleAction
            elif self._PRIMARY__CUSTOM13__RULE is None:
                self._PRIMARY__CUSTOM13__RULE = ruleAction
            elif self._PRIMARY__CUSTOM14__RULE is None:
                self._PRIMARY__CUSTOM14__RULE = ruleAction
            elif self._PRIMARY__CUSTOM15__RULE is None:
                self._PRIMARY__CUSTOM15__RULE = ruleAction
            elif self._PRIMARY__CUSTOM16__RULE is None:
                self._PRIMARY__CUSTOM16__RULE = ruleAction
            elif self._PRIMARY__CUSTOM17__RULE is None:
                self._PRIMARY__CUSTOM17__RULE = ruleAction
            elif self._PRIMARY__CUSTOM18__RULE is None:
                self._PRIMARY__CUSTOM18__RULE = ruleAction
            elif self._PRIMARY__CUSTOM19__RULE is None:
                self._PRIMARY__CUSTOM19__RULE = ruleAction
            elif self._PRIMARY__CUSTOM20__RULE is None:
                self._PRIMARY__CUSTOM20__RULE = ruleAction
            elif self._PRIMARY__CUSTOM21__RULE is None:
                self._PRIMARY__CUSTOM21__RULE = ruleAction
            elif self._PRIMARY__CUSTOM22__RULE is None:
                self._PRIMARY__CUSTOM22__RULE = ruleAction
            elif self._PRIMARY__CUSTOM23__RULE is None:
                self._PRIMARY__CUSTOM23__RULE = ruleAction
            elif self._PRIMARY__CUSTOM24__RULE is None:
                self._PRIMARY__CUSTOM24__RULE = ruleAction
            elif self._PRIMARY__CUSTOM25__RULE is None:
                self._PRIMARY__CUSTOM25__RULE = ruleAction
            elif self._PRIMARY__CUSTOM26__RULE is None:
                self._PRIMARY__CUSTOM26__RULE = ruleAction
            elif self._PRIMARY__CUSTOM27__RULE is None:
                self._PRIMARY__CUSTOM27__RULE = ruleAction
            elif self._PRIMARY__CUSTOM28__RULE is None:
                self._PRIMARY__CUSTOM28__RULE = ruleAction
            elif self._PRIMARY__CUSTOM29__RULE is None:
                self._PRIMARY__CUSTOM29__RULE = ruleAction
            elif self._PRIMARY__CUSTOM30__RULE is None:
                self._PRIMARY__CUSTOM30__RULE = ruleAction
            elif self._PRIMARY__CUSTOM31__RULE is None:
                self._PRIMARY__CUSTOM31__RULE = ruleAction
            elif self._PRIMARY__CUSTOM32__RULE is None:
                self._PRIMARY__CUSTOM32__RULE = ruleAction
            elif self._PRIMARY__CUSTOM33__RULE is None:
                self._PRIMARY__CUSTOM33__RULE = ruleAction
            elif self._PRIMARY__CUSTOM34__RULE is None:
                self._PRIMARY__CUSTOM34__RULE = ruleAction
            elif self._PRIMARY__CUSTOM35__RULE is None:
                self._PRIMARY__CUSTOM35__RULE = ruleAction
            elif self._PRIMARY__CUSTOM36__RULE is None:
                self._PRIMARY__CUSTOM36__RULE = ruleAction
            elif self._PRIMARY__CUSTOM37__RULE is None:
                self._PRIMARY__CUSTOM37__RULE = ruleAction
            elif self._PRIMARY__CUSTOM38__RULE is None:
                self._PRIMARY__CUSTOM38__RULE = ruleAction
            elif self._PRIMARY__CUSTOM39__RULE is None:
                self._PRIMARY__CUSTOM39__RULE = ruleAction
            elif self._PRIMARY__CUSTOM40__RULE is None:
                self._PRIMARY__CUSTOM40__RULE = ruleAction
            elif self._PRIMARY__CUSTOM41__RULE is None:
                self._PRIMARY__CUSTOM41__RULE = ruleAction
            elif self._PRIMARY__CUSTOM42__RULE is None:
                self._PRIMARY__CUSTOM42__RULE = ruleAction
            elif self._PRIMARY__CUSTOM43__RULE is None:
                self._PRIMARY__CUSTOM43__RULE = ruleAction
            elif self._PRIMARY__CUSTOM44__RULE is None:
                self._PRIMARY__CUSTOM44__RULE = ruleAction
            elif self._PRIMARY__CUSTOM45__RULE is None:
                self._PRIMARY__CUSTOM45__RULE = ruleAction
            elif self._PRIMARY__CUSTOM46__RULE is None:
                self._PRIMARY__CUSTOM46__RULE = ruleAction
            elif self._PRIMARY__CUSTOM47__RULE is None:
                self._PRIMARY__CUSTOM47__RULE = ruleAction
            elif self._PRIMARY__CUSTOM48__RULE is None:
                self._PRIMARY__CUSTOM48__RULE = ruleAction
            elif self._PRIMARY__CUSTOM49__RULE is None:
                self._PRIMARY__CUSTOM49__RULE = ruleAction
            elif self._PRIMARY__CUSTOM50__RULE is None:
                self._PRIMARY__CUSTOM50__RULE = ruleAction
        initAllRuleVars()
        return self
    def required(self, isRequired: bool = True):
        isRequired = isRequired if type(isRequired) == bool else True
        def rule(valueInitial):
            def sanitizeFunct(value: any) -> str:
                if(ruleFunct(value)):
                    return value
            def ruleFunct(value):
                return value is not None
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
    def enum(self, *choices: any):
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
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} correspond à aucun choix défini".format(
                            label = labelSTR,
                        ),
                        'en': "{label} correspond to any defined choice".format(
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
        self._PRIMARY__ENUM__RULE = rule
        return self
    def enumNot(self, *choices: any):
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
                    labelSTR = json.dumps(f"{self.get_label()}")
                    err = Exception({
                        'fr': "{label} ne correspond à aucun choix défini".format(
                            label = labelSTR,
                        ),
                        'en': "{label} does not correspond to any defined choice".format(
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
        self._PRIMARY__ENUM_NOT__RULE = rule
        return self
    
    def get_default(self,):
        '''
        Ce getter retourne la valeur par default du un schema JON

            Returns:
                any: La reponse de la fonction
        '''
        return self._default
    def set_default(self, default: any):
        '''
        Ce setter modifie la valeur par default du un schema JON

            Parameters:
                default (any): valeur par defaut
        '''
        self._default = default
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
        Ce getter retourne le label du schema JON

            Returns:
                str: La reponse de la fonction
        '''
        if NODEENV == 'debug':
            print("[jon -> JON_default.py] JONDefaultSchema | get_label - self._label:: ", self._label)
        labelF = self._label if (
            type(self._label) == str and
            len(self._label) > 0
        ) else {
            'fr': 'l\'element',
            'en': 'the element'
        }[self._lang]
        if NODEENV == 'debug':
            print("[jon -> JON_default.py] JONDefaultSchema | get_label - labelF:: ", labelF)
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
    def defaultError(self, error: any):
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
    def default(self, value: any):
        '''
        Cette fonction definit la valeur par defaut qui sera utilisée par le schema JON

            Parameters:
                value (any): valeur par defaut
        '''
        self.set_default(value)
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
    
    def validate(self, value):
        try:
            if(self.preMap is not None and callable(self.preMap)):
                value = self.preMap(value)
            ruleDataF = None

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
                print("[jon -> JON_default.py] JONDefaultSchema | validate - stack:: ", stack)
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
    def isValid(self, value):
        return self.validate(value)['valid']
    def error(self, value):
        return self.validate(value)['error']
    def sanitize(self, value):
        return self.validate(value)['data']
    
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
            if self._PRIMARY__CUSTOM11__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM11__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM11__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM12__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM12__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM12__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM13__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM13__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM13__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM14__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM14__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM14__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM15__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM15__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM15__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM16__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM16__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM16__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM17__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM17__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM17__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM18__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM18__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM18__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM19__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM19__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM19__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM20__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM20__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM20__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM21__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM21__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM21__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM22__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM22__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM22__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM23__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM23__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM23__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM24__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM24__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM24__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM25__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM25__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM25__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM26__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM26__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM26__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM27__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM27__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM27__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM28__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM28__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM28__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM29__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM29__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM29__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM30__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM30__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM30__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM31__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM31__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM31__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM32__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM32__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM32__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM33__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM33__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM33__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM34__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM34__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM34__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM35__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM35__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM35__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM36__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM36__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM36__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM37__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM37__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM37__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM38__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM38__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM38__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM39__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM39__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM39__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM40__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM40__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM40__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM41__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM41__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM41__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM42__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM42__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM42__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM43__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM43__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM43__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM44__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM44__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM44__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM45__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM45__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM45__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM46__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM46__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM46__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM47__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM47__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM47__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM48__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM48__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM48__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM49__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM49__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM49__RULE"
                    return ruleDataF
            if self._PRIMARY__CUSTOM50__RULE is not None:
                ruleData = self._PRIMARY__CUSTOM50__RULE(ruleDataF['data'] if ruleDataF is not None else value)
                if ruleData is not None:
                    ruleDataF = ruleData
                if ruleDataF is not None and not(ruleDataF['valid']):
                    ruleDataF['error'] = self._default_error if self._default_error is not None else ruleDataF['error']
                    self._errorRule = "CUSTOM50__RULE"
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
        ) else defaultMapError
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
        ) else defaultMapError
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
