from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def dualMeshWithRouters():
    "Cria duas redes mesh conectadas por roteadores"
    
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)
    
    info('*** Adicionando controlador\n')
    net.addController('c0')
    
    info('*** Criando primeira rede mesh (Rede A - 10.0.1.0/24)\n')
    # Switches da Rede A
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    
    # Conectando switches da Rede A em mesh
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s3)
    
    # Hosts da Rede A
    h1 = net.addHost('h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.1.11/24', defaultRoute='via 10.0.1.1')
    
    # Conectando hosts aos switches da Rede A
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    
    info('*** Criando segunda rede mesh (Rede B - 10.0.2.0/24)\n')
    # Switches da Rede B
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    
    # Conectando switches da Rede B em mesh
    net.addLink(s4, s5)
    net.addLink(s4, s6)
    net.addLink(s5, s6)
    
    # Hosts da Rede B
    h3 = net.addHost('h3', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1')
    h4 = net.addHost('h4', ip='10.0.2.11/24', defaultRoute='via 10.0.2.1')
    
    # Conectando hosts aos switches da Rede B
    net.addLink(h3, s4)
    net.addLink(h4, s5)
    
    info('*** Adicionando roteadores\n')
    # Criando roteadores (usamos hosts como roteadores)
    r1 = net.addHost('r1', ip='10.0.1.1/24')
    r2 = net.addHost('r2', ip='10.0.2.1/24')
    
    # Conectando roteadores às suas redes mesh
    net.addLink(r1, s3)  # Roteador 1 conectado ao Switch 3 da Rede A
    net.addLink(r2, s6)  # Roteador 2 conectado ao Switch 6 da Rede B
    
    # Conectando os roteadores entre si (Rede 192.168.100.0/30)
    net.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth1',
                params1={'ip': '192.168.100.1/30'}, 
                params2={'ip': '192.168.100.2/30'})
    
    info('*** Iniciando a rede\n')
    net.start()
    
    info('*** Configurando roteamento estático\n')
    # Configuração do roteador 1
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1.cmd('ip route add 10.0.2.0/24 via 192.168.100.2 dev r1-eth1')
    
    # Configuração do roteador 2
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('ip route add 10.0.1.0/24 via 192.168.100.1 dev r2-eth1')
    
    info('*** Testando conectividade entre h1 (Rede A) e h3 (Rede B)\n')
    net.ping([h1, h3])
    
    info('*** Testando conectividade entre h2 (Rede A) e h4 (Rede B)\n')
    net.ping([h2, h4])
    
    info('*** Executando CLI (digite "exit" para sair)\n')
    CLI(net)
    
    info('*** Parando a rede\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    dualMeshWithRouters()