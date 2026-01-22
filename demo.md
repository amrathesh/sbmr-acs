

## M3_SB_2
PLDM is used for the purpose of supporting platform-level data models and platform functions.

### Objective 
Verify that **PLDM is actively used on the BMC** to support **platform-level data models and platform functions** for the side-band interface.

### Test Plan

#### Step 1: Verify PLDM service is running

**Command**
```sh
systemctl status pldmd.service
```

**Expected Result**
- `pldmd.service` exists
- Service state shows:
  ```
  Active: active (running)
  ```
- Service type is `dbus`



#### Step 2: Verify PLDM D-Bus service is registered

**Command**
```sh
busctl list | grep -i pldm
```

**Expected Result**
- A PLDM D-Bus service is present, for example:
  ```
  xyz.openbmc_project.PLDM
  ```

#### Step 3: Verify PLDM exposes a platform object model

**Command**
```sh
busctl tree xyz.openbmc_project.PLDM
```

**Expected Result**
- The object tree is **non-empty**
- One or more PLDM-related object paths are listed
- Object paths represent **platform-level entities** (termini, devices, or platform objects)

#### Step 4: Verify PLDM objects expose platform-level interfaces

Select any object path returned in Step 3 and run:

**Command**
```sh
busctl introspect xyz.openbmc_project.PLDM <object-path>
```

**Expected Result**
- One or more interfaces related to **platform management** are present
- Interfaces expose properties or methods corresponding to platform-level data models  
  (for example inventory, platform descriptors, parameters, or events)



## M3_SB_3
MCTP is used as a transport protocol format that is independent of the underlying physical bus properties, as well as the data-link layer messaging used on the bus.

### Objective
Verify that **MCTP is implemented and used as a transport protocol**, providing a **bus-independent abstraction** for side-band communication on the BMC.

### Test Plan

#### Step 1: Verify MCTP services are present

**Command**
```sh
systemctl list-units --type=service | grep -i mctp
```

**Expected Result**
- One or more MCTP-related services are listed  
  (for example `mctpd.service`, `mctp-*.service`)
- Indicates MCTP is implemented as a distinct transport component



#### Step 2: Verify MCTP transport stack is active

**Command**
```sh
systemctl status mctpd.service
```

**Expected Result**
- `mctpd.service` exists
- Service state shows:
  ```
  Active: active (running)
  ```
- Confirms MCTP transport daemon is operational



#### Step 3: Verify MCTP exposes transport-level abstraction

**Command**
```sh
mctp link
```

**Expected Result**
- One or more MCTP links are listed
- Links are identified independently of the underlying physical bus  
  (e.g. serial, I2C, I3C, PCIe not exposed as raw interfaces)



#### Step 4: Verify MCTP endpoint addressing is present

**Command**
```sh
mctp addr
```

**Expected Result**
- One or more Endpoint IDs (EIDs) are listed
- Endpoint addressing is independent of physical bus addressing



#### Step 5: Verify MCTP routing abstraction exists

**Command**
```sh
mctp route
```

**Expected Result**
- One or more routes are listed
- Routes are expressed in terms of MCTP endpoints and links, not physical bus addresses

---
