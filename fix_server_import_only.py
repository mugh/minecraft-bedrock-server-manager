import sys
import re

with open('server.js', 'r') as f:
    content = f.read()

# 1. Update getCachedServerInfo to check if it's managed by this app
# We add a 'managed' flag to the server data
managed_check_logic = """  // Fetch fresh data
  const container = await getContainer(serverId);
  if (!container) return null;

  const info = await container.inspect();
  const serverPath = getServerPath(serverId);

  // Check if this container is managed by this app (resides in DATA_DIR)
  const hostDataPath = await getHostDataPath();
  const dataMount = info.Mounts?.find(m => m.Destination === '/data' || m.Destination === '/app/minecraft-data');
  const isManaged = dataMount && dataMount.Source && dataMount.Source.startsWith(hostDataPath);
  const hasServerIdLabel = info.Config.Labels && info.Config.Labels['server-id'];
"""

old_managed_start = r"  // Fetch fresh data\s*const container = await getContainer\(serverId\);\s*if \(!container\) return null;\s*const info = await container\.inspect\(\);\s*const serverPath = getServerPath\(serverId\);"
content = re.sub(old_managed_start, managed_check_logic, content)

# 2. Add 'managed' flag to serverData object
server_data_old = r"const serverData = \{[\s\S]*?webPort: PORT\s*\};"
server_data_new = """const serverData = {
    id: serverId,
    name: metadata.name || info.Name.replace('/', ''),
    containerName: metadata.containerName || info.Name.replace('/', ''),
    version: metadata.version || 'UNKNOWN',
    status: info.State.Status,
    players: playerCount,
    maxPlayers: maxPlayers,
    uptime: info.State.Running ? formatUptime(info.State.StartedAt) : '0h 0m',
    memory: formatBytes(info.HostConfig.Memory || 0),
    cpu: '0%',
    worldSize: worldSize,
    ports: ports,
    webPort: PORT,
    managed: !!(isManaged || hasServerIdLabel)
  };"""
content = re.sub(server_data_old, server_data_new, content)

with open('server.js', 'w') as f:
    f.write(content)
