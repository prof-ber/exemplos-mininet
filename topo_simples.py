from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def meshTopo():
    "Cria uma topologia simples com 4 workstations"
    
    net = Mininet(controller=Controller)
    
    info('*** Adicionando controlador\n')
    net.addController('c0')
    
    info('*** Adicionando workstations\n')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    
    info('*** Criando os enlaces (totalmente conectado)\n')
    # Conecta cada host a todos os outros
    net.addLink(h1, h2)
    net.addLink(h1, h3)
    net.addLink(h1, h4)
    net.addLink(h2, h3)
    net.addLink(h2, h4)
    net.addLink(h3, h4)
    
    info('*** Iniciando a rede\n')
    net.start()
    
    info('*** Testando conectividade entre h1 e h2\n')
    net.ping([h1, h2])
    
    info('*** Executando CLI\n')
    CLI(net)
    
    info('*** Parando a rede\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    meshTopo()