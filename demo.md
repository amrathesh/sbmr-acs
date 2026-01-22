

## Table of Contents

- [M3_SB_2](#m3_sb_2)
- [M3_SB_3](#m3_sb_3)
- [M3_SB_4](#m3_sb_4)
- [M3_SB_5](#m3_sb_5)
- [M3_SB_6](#m3_sb_6-m3_sb_8)
- [M3_SB_7](#m3_sb_7)
- [M3_SB_8](#m3_sb_6-m3_sb_8)
- [M3_SB_9](#m3_sb_9)
- [M4_SB_1](#m4_sb_1)


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

## M3_SB_4
PLDM over MCTP binding is used as the format of PLDM over MCTP messages.

### Objective
Verify that **PLDM messages are carried using the PLDM-over-MCTP binding**, ensuring that PLDM is not transported using proprietary or non-standard encapsulation.

### Preconditions
- **M3_SB_2** has complied (PLDM is present and exposes platform-level data models)
- **M3_SB_3** has complied (MCTP transport is implemented and active)

### Test Plan

#### Verify PLDM is layered on top of MCTP transport

**Command**
```sh
systemctl show pldmd.service | grep -E "After=|Requires=|Wants="
```

**Expected Result**
- Output shows ordering or dependency on MCTP-related units  
  (for example `mctpd.service`, `mctp.target`, or `mctp-local.target`)
- Confirms PLDM operates over the MCTP transport layer

---

## M3_SB_5
SPDM is used for the purpose of supporting security related capabilities of the devices.

### Objective
Verify that **if security-related capabilities are implemented for the side-band interface**, they are implemented using **SPDM**.

### Test Plan

####  Verify SPDM support is present

**Command**
```sh
systemctl list-units --type=service | grep -i spdm
```
or
```sh
busctl list | grep -i spdm
```

**Expected Result**
- One or more SPDM-related services are listed

---

## M3_SB_6, M3_SB_8
SPDM over MCTP binding is used as the format of SPDM over MCTP messages.

### Objective
Verify that **SPDM messages are transported using the SPDM-over-MCTP binding**.

### Preconditions
- M3_SB_5 is complied.

### Test Plan

#### Verify SPDM depends on MCTP transport

**Command**
```sh
systemctl show <spdm-service> | grep -E "After=|Requires=|Wants="
```

**Expected Result**
- Dependency on MCTP services is present

---

## M3_SB_7
Secure messages using SPDM specifications is used for the purpose of supporting secure transfer of application data over PMCI transports using SPDM.

### Objective
Verify that **secure messaging uses SPDM secure messaging semantics**.

### Preconditions
- M3_SB_5 is complied.
### Test Plan

#### Step 1: Verify secure messaging capability is present

**Command**
```sh
busctl introspect <spdm-dbus-service> <object-path>
```

**Expected Result**
- Secure messaging capability is indicated

---

## M3_SB_9
The physical and data-link layer methods for MCTP communication are minimally defined by the MCTP over SMBus/I2C binding specification.

### Objective
Verify that **MCTP communication supports SMBus/I2C or a higher-bandwidth binding**.

### Preconditions
- M3_SB_3 has complied

### Test Plan

#### Step 1: Verify MCTP physical binding

**Command**
```sh
mctp link
```

**Expected Result**
- MCTP link shows SMBus/I2C or higher-bandwidth binding

---

#### Step 2: Verify bidirectional addressing

**Command**
```sh
mctp addr
```

**Expected Result**
- Endpoint ID (EID) is assigned

## M4_SB_1
The physical and data-link layer methods for MCTP communication are defined by the MCTP over I3C binding specification.

### Objective
Verify that **MCTP communication uses I3C binding** at SBMR Level M4.

### Preconditions
- Platform claims SBMR Level M4

### Test Plan

#### Verify MCTP over I3C binding

**Command**
```sh
mctp link
```

**Expected Result**
- MCTP link indicates I3C-based transport

---


