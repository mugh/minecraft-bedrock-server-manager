
## Minecraft Bedrock Server Manager

Full-stack application to manage multiple Minecraft Bedrock servers using itzg/docker-minecraft-bedrock-server.

## Nethernet Support

The application now support nethernet fully. Everytime server created, will expose TCP and UDP (for raknet) on specified port (like 19132) beside that also expose 16 block UDP port for nethernet.

Old server which previously using raknet can be migrated to support nethernet by clicking import button and input container name, migrate will be executed instead of importing.

## How it works

The aplication will deploy a minecraft bedrock server using docker itzg/docker-minecraft-bedrock-server latest image, assign port, persistent volume. The aplication then act as UI to manage this container.

### Features
- ✅ Real-time WebSocket Updates
- ✅ Nethernet Compatible
- ✅ Multiple server management
- ✅ Imprt current itzg container server
- ✅ Select server version (Latest, Latest Preview or custom)
- ✅ Start/Stop/Restart containers
- ✅ Server renaming
- ✅ Console command
- ✅ Allocate container memory/ram
- ✅ Advanced File Manager
  - Upload multiple files
  - Download files
  - Delete files/folders
  - Rename files/folders
  - Edit files inline (text editor)
  - Create new folders
  - Navigate folder structure
  - Context menu (right-click)
  - Zip/Unzip files and folders
  - Keyboard shortcuts
- ✅ Addon Management
  - Upload .mcaddon, .mcpack, .mcworld, .mctemplate files
  - Enable/disable addon
  - Automatic manifest parsing
  - View installed worlds
  - Switch between worlds
  - Delete worlds
- ✅ Backup & restore worlds
- ✅ Server configuration editor
- ✅ Player management (kick, ban, op, deop)
- ✅ Dynamic port allocation
- ✅ Web-based UI
- ✅ Password-protected login
- ✅ Session-based authentication
- ✅ Mobile responsive design


### Addon Management Updates

**Combined Addon List System**
- Addons are now displayed as a unified list instead of separate behavior and resource pack tabs
- Each addon shows type indicators: `BP` (Behavior Pack), `RP` (Resource Pack), or `BP + RP` (both types)
- Enable/disable and delete operations work on both pack types simultaneously


### WebSocket Real-time Features
This application uses WebSocket for real-time updates, providing instant UI synchronization across multiple browser tabs without manual refresh.

- **Automatic Fallback**: If WebSocket connection fails, the app automatically falls back to HTTP polling (30-second intervals)
- **Cross-tab Sync**: Changes made in one browser tab instantly appear in all other open tabs

- **Network Requirements**: WebSocket uses the same port as the HTTP server (default: 3001)
- **Firewall**: Ensure port 3001 is open for both HTTP and WebSocket connections

---

### Linux Installation

#### Prerequisites
- Docker installed
- Node.js 18+

Download the source  code

#### 1. **Install Dependencies**
```bash
# Install backend dependencies (includes WebSocket support)
npm install


```

#### 2. **Configure Environment**
Create a `.env` file in the root directory:
```bash
# Server Configuration
PORT=3001
DATA_DIR=/opt/minecraft-servers #change this to your data directory

# Authentication
LOGIN_PASSWORD=your_secure_password_here
MAX_LOGIN_ATTEMPTS=5
LOGIN_LOCKOUT_MINUTES=5
```

#### 3. **Create Data Directory**
```bash
# Create directory for server data
sudo mkdir -p /opt/minecraft-servers #change this to your data directory
sudo chown $USER:$USER /opt/minecraft-servers #change this to your data directory
```

#### 4. **WebSocket Setup**
```bash
# Run WebSocket setup 
npm run setup
```

#### 5. **Start the Application**
```bash
# Start the app (run on PM2)
npm start
```
**Access the application at: `http://localhost:3001`**


---

### Docker Deployment

#### Prerequisites
- Docker installed
- Docker Compose installed

#### Docker Desktop Configuration
1. Open Docker Desktop
2. Go to Settings → General
3. Enable "Expose daemon on tcp://localhost:2375 without TLS"
4. Restart Docker Desktop


Image : https://hub.docker.com/r/mugh/bdsmanagerforitzg

docker image now have 2 tag, amd64 and arm64.
arm64 version is untested.

#### Docker Compose Example
---
```bash
services:
  server-manager:
    image: mugh/bdsmanagerforitzg:latest-amd64
    ports:
      - "3001:3001"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - minecraft-data:/app/minecraft-data
    environment:
      - PORT=3001
      - LOGIN_PASSWORD=minecraft123
      - MAX_LOGIN_ATTEMPTS=5
      - LOGIN_LOCKOUT_MINUTES=5
      #- DOCKER_HOST=tcp://host.docker.internal:2375 #for system with restricted direct mounting to /var/run/docker.sock (windows or NAS)
    networks:
      - minecraft-network

volumes:
  minecraft-data:

networks:
  minecraft-network:
    driver: bridge
```

#### Access the application
   The application will be available at `http://localhost:3001`
   Default login password: `minecraft123` (change in environtment variables)

#### Environment Variables
You can customize the deployment by editing the `docker-compose.yml` file:
- `LOGIN_PASSWORD`: Set your desired password
- `PORT`: Change the port if needed (default: 3001)
- `MAX_LOGIN_ATTEMPTS`: Maximum failed login attempt
- `LOGIN_LOCKOUT_MINUTES`: duration of lockout in case or reaching MAX_LOGIN_ATTEMPTS

#### Volumes
- `minecraft-data`: Persistent storage for Minecraft server data
- `/var/run/docker.sock`: Allows the app to manage Docker containers

---

## [SUPPORT ME](https://sociabuzz.com/mughniy/donate)

## Tips for .mctemplate
most of .mctemplate will not work correctly if directly uploded and set as active world. A workaround is by creating world using the template from minecraft windows, export it as .mcworld then upload it via UI. Although not 100% guaranteed work, but worth to try if direct upload of .mctemplate did not work

---

## Expose Home Server To Public IP Using VPS and Wireguard
If you like me, using homeserver which dont have public IP, you can rent cheapest VPS service which usually come with public IP as proxy and use wireguard.

Below guide is for Ubuntu/Debian systems, whether on a VPS or a home server.

#### Install and generate keys (on both the VPS and the home server).
 
    sudo -i
    apt update && apt install -y wireguard
    umask 077
    wg genkey | tee /etc/wireguard/privatekey | wg pubkey >/etc/wireguard/publickey
    echo "PRIVATE: $(cat /etc/wireguard/privatekey)"
    echo "PUBLIC: $(cat /etc/wireguard/publickey)"


Make a note of the keys for each machine. The private key is for use only on that specific machine—do not share it. The public keys should be exchanged between the VPS and the home server.

#### Specifically for the VPS, check the name of your internet interface:

    ip route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="dev") print $(i+1)}'

The result will typically be `eth0` or `ens3`. If it is something other than `eth0`, make sure to update it in the VPS configuration provided below. 


#### Config on VPS

This setting can be fetch via aplication by clicking wireguard button.
Create /etc/wireguard/wg0.conf file:

    [Interface]
    Address = 10.8.0.1/24
    ListenPort = 51820
    PrivateKey = <VPS_PRIVATE_KEY>
    PostUp = sysctl -w net.ipv4.ip_forward=1
    PostUp = iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 19132:19136 -j DNAT --to-destination 10.8.0.2
    PostUp = iptables -t nat -A PREROUTING -i eth0 -p udp --dport 19132:19136 -j DNAT --to-destination 10.8.0.2
    PostUp = iptables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:20079 -j DNAT --to-destination 10.8.0.2
    PostUp = iptables -t nat -A POSTROUTING -o wg0 -j MASQUERADE
    PostUp = iptables -I FORWARD -i eth0 -o wg0 -j ACCEPT
    PostUp = iptables -I FORWARD -i wg0 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
    PostDown = iptables -t nat -D PREROUTING -i eth0 -p tcp --dport 19132:19136 -j DNAT --to-destination 10.8.0.2
    PostDown = iptables -t nat -D PREROUTING -i eth0 -p udp --dport 19132:19136 -j DNAT --to-destination 10.8.0.2
    PostDown = iptables -t nat -D PREROUTING -i eth0 -p udp --dport 20000:20079 -j DNAT --to-destination 10.8.0.2
    PostDown = iptables -t nat -D POSTROUTING -o wg0 -j MASQUERADE
    PostDown = iptables -D FORWARD -i eth0 -o wg0 -j ACCEPT
    PostDown = iptables -D FORWARD -i wg0 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT
    
    [Peer]
    PublicKey = <HOME_PUBLIC_KEY>
    AllowedIPs = 10.8.0.2/32

#### Configuration at home

Create the file /etc/wireguard/wg0.conf:

    [Interface]
    Address = 10.8.0.2/24
    PrivateKey = <HOME_PRIVATE_KEY>
    
    [Peer]
    PublicKey = <VPS_PUBLIC_KEY>
    Endpoint = <VPS_PUBLIC_IP>:51820
    AllowedIPs = 10.8.0.1/32
    PersistentKeepalive = 25

PersistentKeepalive keeps the connection alive even if the home network is behind NAT.

#### Firewall

On the VPS, open the necessary ports. If you are using ufw:

    ufw allow 51820/udp
    ufw allow 19132:19136/tcp
    ufw allow 19132:19136/udp
    ufw allow 20000:20079/udp

If your VPS is from a cloud provider that uses its own security groups or firewall, ensure you also open these same ports in the provider's control panel. This step is frequently overlooked. At home, if you are using `ufw`, allow traffic from the tunnel:

    ufw allow in on wg0

#### Start the service (VPS first, then the home machine)

    systemctl enable --now wg-quick@wg0
    wg show

In the `wg show` output, look for the "latest handshake" line. If it appears, the tunnel is active. Then, test with a ping:

    ping -c 3 10.8.0.2    # from the VPS
    ping -c 3 10.8.0.1    # from the home machine

If there is no handshake
Verify that the public keys have not been swapped or copied incorrectly (e.g., accidental extra spaces).
Ensure the "Endpoint" on the home machine uses the correct VPS IP address, and that UDP port 51820 is open on both the VPS and the provider's firewall panel.
On the VPS, check `journalctl -u wg-quick@wg0` for errors. A common issue is an incorrect interface name (e.g., `eth0`), which causes `iptables` commands to fail.
Verify that IP forwarding is enabled: `sysctl net.ipv4.ip_forward` should return `1`.


## Screenshot
![enter image description here](https://github.com/mugh/minecraftbedrockservermanager/blob/main/Screenshot/sc1.png?raw=true)
![enter image description here](https://github.com/mugh/minecraftbedrockservermanager/blob/main/Screenshot/sc2.png?raw=true)
![enter image description here](https://github.com/mugh/minecraftbedrockservermanager/blob/main/Screenshot/sc3.png?raw=true)
![enter image description here](https://github.com/mugh/minecraftbedrockservermanager/blob/main/Screenshot/sc4.png?raw=true)








