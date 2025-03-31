from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def meshTopoWithSwitches():
    "Cria uma topologia mesh com switches e workstations"
    
    net = Mininet(controller=Controller, switch=OVSSwitch)
    
    info('*** Adicionando controlador\n')
    net.addController('c0')
    
    info('*** Adicionando switches em topologia mesh\n')
    # Criando 4 switches
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    
    # Conectando os switches em mesh (totalmente conectado)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s2, s3)
    net.addLink(s2, s4)
    net.addLink(s3, s4)
    
    info('*** Adicionando workstations\n')
    # Cada switch terá um host conectado
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    
    # Conectando hosts aos switches
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    
    info('*** Iniciando a rede\n')
    net.start()
    
    info('*** Testando conectividade entre h1 e h2\n')
    net.ping([h1, h2])
    
    info('*** Testando conectividade entre h1 e h4\n')
    net.ping([h1, h4])
    
    info('*** Executando CLI (digite "exit" para sair)\n')
    CLI(net)
    
    info('*** Parando a rede\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    meshTopoWithSwitches()