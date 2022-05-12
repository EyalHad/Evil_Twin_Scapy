<h1> Evil Twin Project - Attack and Defense Tools </h1><br>


## Initialize the project: 
  * Basically can be executed by Ubuntu/Linux Kali.
  - ### requirements:
    - Update package manager:
      <br> 1. ```$ sudo apt-get update```
      <br> 2. ```$ sudo apt-get upgrade```
      
    - Install python3:
      <br> 3. ```$ sudo apt-get install python3.9```
      
    - Install pip3:
      <br> 4. ```$ sudo apt install python3-pip```
      
    - Install scapy:
      <br> 5. ```$ sudo apt install python3-scapy```
      
    - Install gnome-terminal:
      <br> 6. ```$ sudo apt-get install gnome-terminal```
      
    - Install hostapd:
      <br> 7. ```$ sudo apt-get install hostapd```
      
    - Install dnsmasq:
      <br> 8. ```$ sudo apt-get install dnsmasq```  
      
    - Install iptables:
      <br> 9. ```$ sudo apt-get install iptables```
      
    - Install NodeJS:
      <br> 10. ```$ sudo apt install nodejs```

    - Install npm:
      <br> 11. ```$ sudo apt install npm```

    - Install express:
      <br> 12. ```$ npm install express```

    - Install body-parser:
      <br> 13. ```$ npm install body-parser```<br><br>
     
     
## Attack Tool:   

### Schema

* Scan the network for possible Access Points to attack
* Choose one of the AP as a victim
* Scan for possible client in the victim AP
* Choose one of the clients as a victim
* Send deauthentication packets to the choosen AP and Client 
* Create a fake AP - same details as the victim AP
* Create a Captive Portal for phising (HTML page with NodeJS). 

### Files
        

### How to run the attack code

- 1. Go to the folder ```Evil_Twin_Scapy/Tools/Attack```
- 2. Run the command ```$ sudo python3 EvilTwin.py```
- 3. Follow the instructions that appers in the terminal<br><br>


## Defence Tool
 


## Code Contributors

This project exists thanks to all the people who contribute.<br>
<!-- <a href="https://github.com/Final-Project-bb/FairPolitics/graphs/contributors">
  <img src="https://contrib.rocks/image?max=3&repo=Final-Project-bb/FairPolitics" />
</a> -->
* [Itay Sharabi](https://github.com/ItaySharabi)
* [Eyal Hadad](https://github.com/EyalHad)
* [Shai Bonfil](https://github.com/shaiBonfil)

  ## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check our [issues page](https://github.com/EyalHad/Evil_Twin_Scapy/issues).
