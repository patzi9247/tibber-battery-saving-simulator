# Tibber Battery Saving Simulator
Uses a Tibber-Token to acces the energy consumption of your house and lets you calculate the cost savings when you install a battery and charge it when prices are low. 

Simulation settings:
- capacity of the battery
- price threshold when to charge the battery
- discharge power of the battery
- charge power of the battery
## How to run
- create a .env file in the projects root dir like:
```
TIBBER_TOKEN="your_token"
```

- run this command once

```
pip install -r requierements.txt
```

- change the simulation settings in the main.py, line 142 - 149
- start the tool
```
python main.py
```

## ToDo
- Dockerize the tool
- use Dash with WebUI to instant change simulation settings