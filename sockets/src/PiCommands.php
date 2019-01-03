<?php
namespace PiApp;
use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;

class PiCommands implements MessageComponentInterface {
    protected $clients;

    public function __construct() {
        $this->clients = new \SplObjectStorage;
    }

    public function onOpen(ConnectionInterface $conn) {
        // Store the new connection to send messages to later
        $this->clients->attach($conn);

        echo "New connection! ({$conn->resourceId})\n";
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        $numRecv = count($this->clients) - 1;
        /*
        echo sprintf('Connection %d sending message "%s" to %d other connection%s' . "\n"
            , $from->resourceId, $msg, $numRecv, $numRecv == 1 ? '' : 's');
            */
        
        $params = json_decode($msg, true);

        if($params["command"] == "lightsOn")
        {
        	shell_exec('sudo python ~/LEDStrip/turnOnLights.py');
        }
        else if($params["command"] == "lightsOff")
        {
        	shell_exec('sudo python ~/LEDStrip/turnOffLights.py');
        }
        else if($params["command"] == "setLightsColor")
        {
        	list($r, $g, $b) = sscanf($params["color"], "#%02x%02x%02x");
        	$ip = "127.0.0.1";
			$port = 12123;
			$str = "$r,$g,$b";

			$sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP); 
			socket_set_option($sock, SOL_SOCKET, SO_BROADCAST, 1);
			socket_set_option($sock, SOL_SOCKET, SO_RCVTIMEO, array("sec"=>5, "usec"=>0));
			socket_sendto($sock, $str, strlen($str), 0, $ip, $port);
        	//exec("sudo python ~/LEDStrip/setLightsColor.py $r $g $b");
        }

        /*
        foreach ($this->clients as $client) {
            if ($from !== $client) {
                // The sender is not the receiver, send to each client connected
                $client->send($msg);
            }
        }*/
    }

    public function onClose(ConnectionInterface $conn) {
        // The connection is closed, remove it, as we can no longer send it messages
        $this->clients->detach($conn);

        echo "Connection {$conn->resourceId} has disconnected\n";
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";

        $conn->close();
    }
}