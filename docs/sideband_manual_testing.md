# SBMR Side band Manual Testing 
This document provides manual test guidance for validating SBMR side-band interface requirements on server Baseboard Management Controllers (BMCs) running OpenBMC firmware.

The tests described herein use standard OpenBMC utilities (for example, systemctl, busctl, mctp, pldmtool) to verify that the server management stack is configured and layered in
accordance with DMTF PMCI architecture and the rules stated in the Arm SBMR side-band interface section. These checks focus on architectural correctness, protocol selection,
and interface exposure, rather than exhaustive protocol compliance.

This document is intended as guidance for partners and implementers to:
- Perform initial self-assessment of SBMR side-band compliance,
- Support compliance declaration during early enablement phases,
- Validate correct usage of PMCI-defined protocols (PLDM and MCTP) on OpenBMC-based systems.

At this stage, the document does not replace a full conformance test suite. It is expected that, over time, more robust and automated validation infrastructure will be developed,
including testing via PMCI-defined PTTI ([PMCI Test Tools Interface](https://www.dmtf.org/sites/default/files/standards/documents/DSP0280_1.0.0.pdf)) or equivalent mechanisms.

For non-OpenBMC implementations, this document serves as a reference example. Such systems are expected to identify and use functionally equivalent utilities or
interfaces to validate the same architectural properties, protocol layering, and side-band behaviors described here.

# Test Sections
- [PLDM Tests (M3_SB_2, M3_SB_4)](#pldm-tests-m3_sb_2-m3_sb_4)
- [MCTP Tests (M3_SB_3, M3_SB_9, M4_SB_1)](#mctp-tests-m3_sb_3-m3_sb_9-m4_sb_1)


## PLDM Tests (M3_SB_2, M3_SB_4)

### M3_SB_2
PLDM is used for the purpose of supporting platform-level data models and platform functions.

#### Objective 
Verify that **PLDM is actively used on the BMC** to support **platform-level data models and platform functions** for the side-band interface.

#### Test Plan

##### Step 1: Verify PLDM service is running

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



##### Step 2: Verify PLDM D-Bus service is registered

**Command**
```sh
busctl list | grep -i pldm
```

**Expected Result**
- A PLDM D-Bus service is present, for example:
  ```
  xyz.openbmc_project.PLDM
  ```

##### Step 3: Verify PLDM exposes a platform object model

**Command**
```sh
busctl tree xyz.openbmc_project.PLDM
```

**Expected Result**
- The object tree is **non-empty**
- One or more PLDM-related object paths are listed
- Object paths represent **platform-level entities** (termini, devices, or platform objects)

##### Step 4: Verify PLDM objects expose platform-level interfaces

Select any object path returned in Step 3 and run:

**Command**
```sh
busctl introspect xyz.openbmc_project.PLDM <object-path>
```

**Expected Result**
- One or more interfaces related to **platform management** are present
- Interfaces expose properties or methods corresponding to platform-level data models  
  (for example inventory, platform descriptors, parameters, or events)

#### Finding PLDM command arguments

Use the steps below to derive common arguments used in the PLDM commands.

##### Determine `-m <eid>` (MCTP Endpoint ID)

**Command**
```sh
mctp addr
```

**Example Result**
```
eid 8 net 1 dev mctpserial0
```

**Command**
```sh
mctp route
```

**Example Result**
```
eid min 18 max 18 net 1 dev mctpserial0
```

**Notes**
- Use the endpoint EID that corresponds to your target device (for example `18` in the route output).

##### Determine sensor/effecter IDs for `-i <id>`

**Command**
```sh
pldmtool platform GetPDR -m <eid> -d 0
```

**Example Result**
```
{
    "recordHandle": 1,
    "PDRType": "Numeric Sensor PDR",
    "sensorID": 2
}
```

**Command**
```sh
pldmtool platform GetPDR -m <eid> -d <nextRecordHandle>
```

**Example Result**
```
{
    "recordHandle": 3,
    "PDRType": "State Sensor PDR",
    "sensorID": 3
}
```

**Notes**
- Keep following `nextRecordHandle` until you find the PDRs you need.
- Use `sensorID` for sensor commands and `effecterID` for effecter commands (when present).
- If a Sensor Auxiliary Names PDR is present, it can provide human-readable names for sensor IDs.

##### Determine `-r <rearm>` (rearm behavior for sensor reads)

**Command**
```sh
pldmtool platform GetSensorReading --help
```

**Command**
```sh
pldmtool platform GetStateSensorReadings --help
```

**Notes**
- Use these help outputs to confirm the meaning and valid range for `-r`.
- When you do not need to re-arm event state, use `-r 0` as a safe default.

#### Testing PLDM commands 
PLDM tool commands from SBMR Section D.4 and Section C.2. 

##### Table 15: PLDM Platform Commands

**Command**
```sh
pldmtool base GetTID -m 18
```

**Example Result**
```
{
    "Response": 1
}
```

**Command**
```sh
pldmtool base SetTID -m 18 -t 1
```

**Example Result**
```
{
    "completionCode": 0
}
```

**Command**
```sh
pldmtool platform GetSensorReading -m 18 -i 2 -r 0
```

**Example Result**
```
{
    "sensorDataSize": "uint32",
    "sensorOperationalState": "Sensor Enabled",
    "presentReading": 28
}
```

**Command**
```sh
pldmtool platform GetStateSensorReadings -m 18 -i 3 -r 0
```

**Example Result**
```
{
    "compositeSensorCount": 1,
    "sensorOpState[0]": "Sensor Enabled",
    "presentState[0]": "Sensor Normal"
}
```

**Command**
```sh
pldmtool platform GetStateEffecterStates -m 18 -i 1
```

**Example Result**
```
{
    "compositeEffecterCount": 1,
    "effecterOpState[0])": "Effecter Enabled No Update Pending",
    "presentState[0]": 0
}
```

**Command**
```sh
pldmtool platform SetStateEffecterStates -m 18 -i 1 -c 1 -d 0 1
```

**Example Result**
```
{
    "Response": "SUCCESS"
}
```

##### Table 16: PLDM FRU Commands

**Command**
```sh
pldmtool fru GetFruRecordTableMetadata -m 18
```

**Example Result**
```
{
    "FRUDATAMajorVersion": 1,
    "FRUTableLength": 54,
    "Total number of records in table": 1
}
```

**Command**
```sh
pldmtool fru GetFruRecordTable -m 18
```

**Example Result**
```
[
    [
        {
            "FRU Record Type": "General(1)"
        }
    ]
]
```

##### Table 18: PLDM PDR Commands

**Command**
```sh
pldmtool platform GetPDR -m 18 -d 0
```

**Example Result**
```
{
    "recordHandle": 1,
    "PDRType": "Numeric Sensor PDR",
    "sensorID": 2
}
```

### M3_SB_4
PLDM over MCTP binding is used as the format of PLDM over MCTP messages.

#### Objective
Verify that **PLDM messages are carried using the PLDM-over-MCTP binding**, ensuring that PLDM is not transported using proprietary or non-standard encapsulation.

#### Preconditions
- **M3_SB_2** has complied (PLDM is present and exposes platform-level data models)
- **M3_SB_3** has complied (MCTP transport is implemented and active)

#### Test Plan

##### Verify PLDM is layered on top of MCTP transport

**Command**
```sh
systemctl show pldmd.service | grep -E "After=|Requires=|Wants="
```

**Expected Result**
- Output shows ordering or dependency on MCTP-related units  
  (for example `mctpd.service`, `mctp.target`, or `mctp-local.target`)
- Confirms PLDM operates over the MCTP transport layer

---

## MCTP Tests (M3_SB_3, M3_SB_9, M4_SB_1)

### M3_SB_3
MCTP is used as a transport protocol format that is independent of the underlying physical bus properties, as well as the data-link layer messaging used on the bus.

#### Objective
Verify that **MCTP is implemented and used as a transport protocol**, providing a **bus-independent abstraction** for side-band communication on the BMC.

#### Test Plan

##### Step 1: Verify MCTP services are present

**Command**
```sh
systemctl list-units --type=service | grep -i mctp
```

**Expected Result**
- One or more MCTP-related services are listed  
  (for example `mctpd.service`, `mctp-*.service`)
- Indicates MCTP is implemented as a distinct transport component



##### Step 2: Verify MCTP transport stack is active

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



##### Step 3: Discover MCTP D-Bus service and object model

**Command**
```sh
busctl list | grep -i mctp
```

**Expected Result**
- An MCTP D-Bus service is listed (for example `au.com.codeconstruct.MCTP1`)

**Command**
```sh
busctl tree <mctp-dbus-service>
```

**Expected Result**
- The object tree includes `.../interfaces/...` and `.../networks/<id>/endpoints/...`
- One or more endpoint object paths are present



##### Step 4: Verify MCTP exposes transport-level abstraction

**Command**
```sh
mctp link
```

**Expected Result**
- One or more MCTP links are listed
- Links are identified independently of the underlying physical bus  
  (e.g. serial, I2C, I3C, PCIe not exposed as raw interfaces)



##### Step 5: Verify MCTP endpoint addressing is present

**Command**
```sh
mctp addr
```

**Expected Result**
- One or more Endpoint IDs (EIDs) are listed
- Endpoint addressing is independent of physical bus addressing



##### Step 6: Verify MCTP routing abstraction exists

**Command**
```sh
mctp route
```

**Expected Result**
- One or more routes are listed
- Routes are expressed in terms of MCTP endpoints and links, not physical bus addresses



##### Step 7: Inspect endpoint details and names via D-Bus

**Command**
```sh
busctl tree <mctp-dbus-service> <mctp-root>/networks
```

**Expected Result**
- Endpoint object paths are listed under `.../networks/<id>/endpoints/`
- Endpoint object names are often the EID (for example `.../endpoints/8`)
- Use the root returned by `busctl tree <mctp-dbus-service>` (for example `/au/com/codeconstruct/mctp1`)

**Command**
```sh
busctl introspect <mctp-dbus-service> <endpoint-object-path>
```

**Expected Result**
- An MCTP endpoint interface is present (for example `au.com.codeconstruct.MCTP.Endpoint1`)
- Properties and methods for the endpoint are listed; use them to identify the endpoint name/identity if exposed
- The endpoint object path or properties can be correlated with `mctp addr`/`mctp route` EIDs

**Command (optional)**
```sh
busctl get-property <mctp-dbus-service> <endpoint-object-path> <endpoint-interface> <property-name>
```

**Expected Result**
- Returns the selected property value (for example an endpoint name, UUID, or supported message types if exposed)

**Command**
```sh
busctl introspect <mctp-dbus-service> <mctp-root>/interfaces/<interface-name>
```

**Expected Result**
- Interface details are listed (for example `au.com.codeconstruct.MCTP.Interface1`)
- Interface metadata can be correlated with `mctp link` output

##### Example walk-through
This example is included only to make the commands easier to follow; expect service names, object paths, and outputs to vary by system configuration.

**Command**
```sh
busctl list | grep -i mctp
```

**Expected Result**
```
au.com.codeconstruct.MCTP1   294 mctpd  root  :1.4  mctpd.service
```

**Command**
```sh
busctl tree au.com.codeconstruct.MCTP1
```

**Expected Result**
```
/au/com/codeconstruct/mctp1
|- /au/com/codeconstruct/mctp1/interfaces
|  |- /au/com/codeconstruct/mctp1/interfaces/lo
|  `- /au/com/codeconstruct/mctp1/interfaces/mctpserial0
`- /au/com/codeconstruct/mctp1/networks/1/endpoints/8
`- /au/com/codeconstruct/mctp1/networks/1/endpoints/18
```

**Command**
```sh
mctp link
```

**Expected Result**
```
dev mctpserial0 index 6 address none net 1 mtu 68 up
```

**Command**
```sh
mctp addr
```

**Expected Result**
```
eid 8 net 1 dev mctpserial0
```

**Command**
```sh
mctp route
```

**Expected Result**
```
eid min 18 max 18 net 1 dev mctpserial0
```

**Command**
```sh
busctl introspect au.com.codeconstruct.MCTP1 /au/com/codeconstruct/mctp1/networks/1/endpoints/18
```

**Expected Result**
```
au.com.codeconstruct.MCTP.Endpoint1 interface - - -
```

**Command**
```sh
busctl introspect au.com.codeconstruct.MCTP1 /au/com/codeconstruct/mctp1/interfaces/mctpserial0
```

**Expected Result**
```
au.com.codeconstruct.MCTP.Interface1 interface - - -
```


**Command (optional)**
```sh
busctl call au.com.codeconstruct.MCTP1 /au/com/codeconstruct/mctp1/interfaces/mctpserial0 \
  au.com.codeconstruct.MCTP.BusOwner1 SetupEndpoint ay 0
```

**Expected Result**
- Returns endpoint details when setup succeeds; may fail if the endpoint does not respond

---

### M3_SB_9
The physical and data-link layer methods for MCTP communication are minimally defined by the MCTP over SMBus/I2C binding specification.

#### Objective
Verify that **MCTP communication supports SMBus/I2C or a higher-bandwidth binding**.

#### Preconditions
- M3_SB_3 has complied

#### Test Plan

##### Step 1: Verify MCTP physical binding

**Command**
```sh
mctp link
```

**Expected Result**
- MCTP link shows SMBus/I2C or higher-bandwidth binding

---

##### Step 2: Verify bidirectional addressing

**Command**
```sh
mctp addr
```

**Expected Result**
- Endpoint ID (EID) is assigned

### M4_SB_1
The physical and data-link layer methods for MCTP communication are defined by the MCTP over I3C binding specification.

#### Objective
Verify that **MCTP communication uses I3C binding** at SBMR Level M4.

#### Preconditions
- Platform claims SBMR Level M4

#### Test Plan

##### Verify MCTP over I3C binding

**Command**
```sh
mctp link
```

**Expected Result**
- MCTP link indicates I3C-based transport


--------------

*Copyright (c) 2026, Arm Limited and Contributors. All rights reserved.*
