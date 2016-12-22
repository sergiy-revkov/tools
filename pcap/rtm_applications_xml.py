#!/usr/bin/python -tt


import sys
import xml.etree.ElementTree as ET
import sap_end_points
import shutil


def appxml_add_service(appxml, service):
    """ add service configuration to appxml file
    Args:
        appxml - where to add
        service - what service to add. It is a list

    Returns:
        nothing.
    
    """
    if not service[0]:
        service[0] = 'SAPGUI:'+service[1] + ':' + service[2]

    node_str = """
    <application>
      <name>""" + service[0] + """</name>
      <report>
        <service>
          <ip>""" + service[1] + """</ip>
          <port>""" + service[2] + """</port>
        </service>
      </report>
      <analyzer>
        <sapgui>
          <nonSyn>true</nonSyn>
          <slowThold>80000</slowThold>
          <slowSrvThold>0</slowSrvThold>
          <vLog>true</vLog>
          <safeThreshold>90</safeThreshold>
          <srvTimeFormula>sum</srvTimeFormula>
          <zLog>true</zLog>
        </sapgui>
      </analyzer>
    </application>
     """

    sapgui_node = ET.fromstring(node_str)
    appxml.append(sapgui_node)

def prepare_applications_xml(filepath, endpoints, interactive=None):
    tree = ET.parse(filepath)
    root = tree.getroot()

    found_services = {}
    if interactive:
        print '\n[MSG]found following services:'
        for child in root.findall('./application/report/service'):
            ip_el = child.find('ip')
            port_el = child.find('port')
            if ip_el!=None and port_el!=None :
                print '[DATA]'+ip_el.text+':'+port_el.text
                found_services[(ip_el.text, int(port_el.text))]=1


    services_2_add = []
    for ep in endpoints:
        if not ep in found_services:
            services_2_add.append(ep)

    if interactive and len(services_2_add)>0 :
        print '\n[MSG]following services is going to be added to configuration'
        for ep in services_2_add:
            print '[DATA]'+ep[0]+':'+str(ep[1])
    else:
        print '\n[MSG]nothing to add to configuration'
        return

    if interactive:
        msg = '\n[REQUEST]configuration is about to be updated. Confirm ? (y/n)'
        shall = True if raw_input("%s " % msg).lower() == 'y' else False
        if not shall:
            return

    for ep in endpoints:
        appxml_add_service(root, [None, ep[0], str(ep[1])])


    shutil.copy(filepath, filepath+'.old')
    tree.write(filepath)


def main():
    if len(sys.argv) > 2:
        appxml_path = sys.argv[1]
        res = {}
        for capture in sys.argv[2:]:
            print '[MSG]processing '+capture+' ...'
            ep_list = sap_end_points.get_sap_endpoints(capture)
            for ep in ep_list:
                res[(ep[0],ep[1])] = 1

        if len(res) == 0:
            print '[MSG]no SAP endpoints found'
            return
        else: 
            print '[MSG]found endpoints: '
            for ep in res.keys():
                print '[DATA]'+ep[0]+':'+str(ep[1])

        prepare_applications_xml(appxml_path, res.keys(), True)
    else:
        print '[ERROR]rtm_applications_xml.py /path/to/applications.xml capture_file_01.pcap capture_file_02.pcap .... '

if __name__ == '__main__':
    main()
