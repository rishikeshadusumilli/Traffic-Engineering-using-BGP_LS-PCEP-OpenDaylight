# Traffic Engineering TE using BGP-LS, PCEP, and OpenDaylight

This project displays the functionality of BGP-LS to gain a complete view of the network and the SDN controller’s ability to perform MPLS Traffic Engineering (TE) with the help of PCEP and BGP-LS protocols.

Setup:

1.	Connect Cisco IOS-XR devices as per the required topology and use OSPF area 0 for their interconnection.
2.	Connect one IOS-XR device to OpenDaylight using BGP.
3.  Use 41-bgp-example.xml in OpenDaylight folder to change the BGP port to 179.
  3.1.  OpenDaylight configuration: change the BGP peer IP to IP of IOS-XR neighbor.
  3.2.  OpenDaylight configuration: change the BGP RIB IP to IP of ODL and BGP AS same as IOS-XR router AS because it is iBGP.
4.  Check OpenDaylight DLUX at http://<controller-ip>:<controller port> for BGP link-state information.
5.  Go to Yang UI -> network-topology rev.2013-07-12->network-topology-> Send
 
link-state information transmitted to OpenDaylight using BGP-LS can be seen using the topology representation within OpenDaylight DLUX Yang UI.
  
Implement MPLS Traffic Engineering (TE) using Postman and Python - Flask:

1.	Configure MPLS configuration in IOS-XR to implement Traffic Engineering (TE)
2.  The MPLS configuration should be done only on the MPLS tunnel head device and the RSVP commands for bandwidth allocation should be performed on all the IOS-XR devices.
3.	Configure LSP tunnel using Python and Flask on OpenDaylight IOS-XR neighbor
4.  The traceroute shows the MPLS tunnel used when pinging from XRV-1 to XRV-2 loopback IP address. The tunnel-te1 is also displayed as the preferred path to reach loopback of XRV-2.
5.  LSP path can be modified or removed using POST update-lsp commands from the Flask GUI.





