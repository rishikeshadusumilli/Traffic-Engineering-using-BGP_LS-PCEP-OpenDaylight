#!/usr/bin/bash/env python
# -*- coding: utf-8 -*-

#Name: Rishikesh Adusumilli

from flask import Flask, render_template, Markup, request, jsonify
from flask.helpers import send_file
import os,httplib,json,subprocess


############################ Module for cURL #######################

def post(cIP,userInput,configType):
    output=apiInt(cIP,userInput,configType,"POST")
    return output

def get(cIP,userInput,configType):
    output=apiInt(cIP,userInput,configType,"GET")
    return output

def apiInt(cIP,userInput,configType,method):
    if(configType=="addLSP"):
        path="/restconf/operations/network-topology-pcep:add-lsp"
    elif(configType=="updateLSP"):
        path="/restconf/operations/network-topology-pcep:update-lsp"
    elif(configType=="removeLSP"):
        path="/restconf/operations/network-topology-pcep:remove-lsp"
    elif(configType=="pcepTopoInfo"):
        path="/restconf/operational/network-topology:network-topology/topology/pcep-topology"
    elif(configType=="lsTopoInfo"):
        path="/restconf/operational/network-topology:network-topology/topology/example-linkstate-topology"
    elif(configType=="lsRouteInfo"):
        path="/restconf/operational/bgp-rib:bgp-rib/rib/example-bgp-rib/loc-rib/tables/bgp-linkstate:linkstate-address-family/bgp-linkstate:linkstate-subsequent-address-family/linkstate-routes"


    headers = {
            'Content-type': 'application/xml',
            'Accept': 'application/xml',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
    }
    conn = httplib.HTTPConnection(cIP, 8181)
    conn.request(method,path,userInput,headers)
    response = conn.getresponse()
    output = (response.status, response.reason, response.read())
    #print output
    conn.close()
    return output


############################ Module for Flask #######################

app = Flask(__name__)

#Function for index page
@app.route('/')
def startPage():
    bodyText=Markup("<b>SDN Topology Configuration -  User Input</b>")
    return render_template('index.html', bodyText=bodyText)

#page after action performed
@app.route('/actionStatus')
def actionStatus():
    return render_template("actionStatus.html")

#Function for traffic engineering
@app.route('/form1')
def form1():
    return render_template("form1.html")

#Function for pcep-topology information
@app.route('/form2')
def form2():
    response=get("192.168.56.102"," ","pcepTopoInfo")
    #print(response)
    return jsonify(response[2])

#Function for linkState-topology information
@app.route('/form3')
def form3():
    response=get("192.168.56.102"," ","lsTopoInfo")
    #print(response)
    return jsonify(response[2])

#Function for linkState-routes information
@app.route('/form4')
def form4():
    response=get("192.168.56.102"," ","lsRouteInfo")
    #print(response)
    return jsonify(response[2])


###############Function to record user input for traffic engineerings
@app.route('/recordUserInput1', methods=['POST'])
def recordUserInput1():
    pccNodeIP=request.form['pccNodeIP']
    tunnelName=request.form['tunnelName']
    sourceIP=request.form['sourceIP']
    destinationIP=request.form['destinationIP']
    hop1=request.form['hop1']
    hop2=request.form['hop2']
    actionLSP=request.form['actionLSP']

    if(actionLSP.lower()=="create"):
        flowTEAddData='<input xmlns="urn:opendaylight:params:xml:ns:yang:topology:pcep"> <node>pcc://'+pccNodeIP+'</node> <name>'+tunnelName+'</name> <arguments> <lsp xmlns="urn:opendaylight:params:xml:ns:yang:pcep:ietf:stateful"> <delegate>true</delegate> <administrative>true</administrative> </lsp> <endpoints-obj> <ipv4> <source-ipv4-address>'+sourceIP+'</source-ipv4-address> <destination-ipv4-address>'+destinationIP+'</destination-ipv4-address> </ipv4> </endpoints-obj> <ero> <subobject> <loose>false</loose> <ip-prefix> <ip-prefix>'+hop1+'/32</ip-prefix> </ip-prefix> </subobject> <subobject> <loose>false</loose> <ip-prefix> <ip-prefix>'+hop2+'/32</ip-prefix> </ip-prefix> </subobject> </ero> </arguments> <network-topology-ref xmlns:topo="urn:TBD:params:xml:ns:yang:network-topology">/topo:network-topology/topo:topology[topo:topology-id="pcep-topology"]</network-topology-ref> </input>'
        print(post("192.168.56.102",flowTEAddData,"addLSP"))

    elif(actionLSP.lower()=="update"):
        flowTEUpdate = '<?xml version="1.0" encoding="UTF-8"?> <input xmlns="urn:opendaylight:params:xml:ns:yang:topology:pcep"> <node>pcc://'+pccNodeIP+'</node> <name>'+tunnelName+'</name> <arguments> <lsp xmlns="urn:opendaylight:params:xml:ns:yang:pcep:ietf:stateful"> <delegate>true</delegate> <administrative>true</administrative> </lsp> <ero> <subobject> <loose>false</loose> <ip-prefix> <ip-prefix>'+hop1+'/32</ip-prefix> </ip-prefix> </subobject> <subobject> <loose>false</loose> <ip-prefix> <ip-prefix>'+hop2+'/32</ip-prefix> </ip-prefix> </subobject> </ero> </arguments> <network-topology-ref xmlns:topo="urn:TBD:params:xml:ns:yang:network-topology">/topo:network-topology/topo:topology[topo:topology-id="pcep-topology"]</network-topology-ref> </input>'
        print(post("192.168.56.102",flowTEUpdate,"updateLSP"))

    elif(actionLSP.lower()=="remove"):
        flowTERemove = '<input xmlns="urn:opendaylight:params:xml:ns:yang:topology:pcep"> <node>pcc://'+pccNodeIP+'</node> <name>'+tunnelName+'</name> <network-topology-ref xmlns:topo="urn:TBD:params:xml:ns:yang:network-topology">/topo:network-topology/topo:topology[topo:topology-id="pcep-topology"]</network-topology-ref> </input>'
        print(post("192.168.56.102",flowTERemove,"removeLSP"))

    return actionStatus()

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8888)
