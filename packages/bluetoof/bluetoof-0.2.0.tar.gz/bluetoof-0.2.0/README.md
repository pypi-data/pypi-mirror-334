# Bluetoof
Bibliothèque python pour interagir avec des appareils bluetooth via RFCOMM.

# Installation
```
pip install bluetoof
```

# Utilisation 
```
from bluetoof import Bluetoof

bt = Bluetoof()
devices = bt.list_devices()
print(devices)

```

