#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:58:10 2016

@author: pascal
"""

class derivatives_position(object):
    ''' Class to model a derivatives position.
    
    Attributes
    ==========
    
    name : string
        name of the object
    quantity : float
        number of assets/derivatives making up the position
    underlying : string
        name of asset/risk factor for the derivative
    mar_env : instance of market_environment
        constant, lists, and curves relevant for valuation_class
    otype : string
        valuation class to use
    payoff_func : string
        payoff string for the derivative
        
    Methods
    =======
    get_info :
        prints information about the derivattive position
    '''
    
    def __init__(self, name, quantity, underlying, mar_env, otype, payoff_func):
       self.name = name
       self.quantity = quantity
       self.underlying = underlying
       self.mar_env = mar_env
       self.otype = otype
       self.payoff_func = payoff_func
       
    def get_info(self):
        ''' Get info of derivative position. '''
        print "Name"
        print self.name, '\n'
        print "Quantity"
        print self.quantity, '\n'
        print "UNDERLYING"
        print self.underlying, '\n'
        print "MARKET ENVIRONMENT"
        print "\n**Constants**"
        for key, value in self.mar_env.constants.items():
            print key, value
        print "\n**Lists**"
        for key, value in self.mar_env.lists.items():
            print key, value
        print "\n**Curves**"
        for key in self.mar_env.curves.items():
            print key, value
        print "\nOPTION TYPE"
        print self.otype, '\n'
        print "PAYOFF FUNCTION"
        print self.payoff_func
       